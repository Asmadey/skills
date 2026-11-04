#!/usr/bin/env python3
"""Генерация картинок через kie.ai: создать задачу → дождаться → скачать → привести к размеру.

API (проверено по docs.kie.ai, 02.11.2026):
    POST /api/v1/jobs/createTask      {"model", "callBackUrl"?, "input": {...}}  → {"data": {"taskId"}}
    GET  /api/v1/jobs/recordInfo?taskId=…                                       → data.state / data.resultJson
    GET  /api/v1/chat/credit                                                    → {"data": 100.5}
    POST /api/v1/common/download-url  {"url"}                                   → временная ссылка на 20 минут

Состояния задачи: waiting | queuing | generating | success | fail.
Ошибки приходят с HTTP 200 и кодом в теле: 401 — ключ, 402 — нет кредитов, 422 — задача не ваша/нет такой.

Ключ: KIE_API_KEY в окружении или первая строка ~/.hermes/keys/kie.txt (chmod 600).

Примеры:
    python3 kie_image.py --credits
    python3 kie_image.py -p "prompt" --aspect 3:2 --size 1200x800 -o public/assets/ozvuchka/hero.webp
    python3 kie_image.py -p "prompt" --status task_abc123
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any

BASE = "https://api.kie.ai"
KEY_FILE = os.path.expanduser("~/.hermes/keys/kie.txt")
DEFAULT_MODEL = "google/nano-banana"
TERMINAL = {"success", "fail"}


def api_key() -> str:
    key = os.environ.get("KIE_API_KEY", "").strip()
    if key:
        return key
    try:
        with open(KEY_FILE, encoding="utf-8") as f:
            key = f.read().strip().splitlines()[0].strip()
    except OSError:
        raise SystemExit(
            f"Нет ключа kie.ai: положи его в {KEY_FILE} (chmod 600) или в KIE_API_KEY. "
            "Ключ берётся на https://kie.ai/api-key"
        )
    if not key:
        raise SystemExit(f"Файл {KEY_FILE} пустой")
    return key


def request(method: str, path: str, payload: dict | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        BASE + path, data=data, method=method,
        headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{path}: HTTP {e.code} {e.read().decode()[:200]}")
    # kie.ai отдаёт ошибки с HTTP 200 и кодом в теле: проверяем code, а не только статус
    if body.get("code") not in (200, None):
        raise SystemExit(f"{path}: code {body.get('code')} — {body.get('msg')}")
    return body.get("data") or {}


def credits() -> float:
    return float(request("GET", "/api/v1/chat/credit") or 0)


def create(prompt: str, model: str, aspect: str, output_format: str = "png") -> str:
    payload = {"model": model, "input": {"prompt": prompt, "aspect_ratio": aspect,
                                        "output_format": output_format}}
    data = request("POST", "/api/v1/jobs/createTask", payload)
    task_id = data.get("taskId")
    if not task_id:
        raise SystemExit(f"createTask не вернул taskId: {data}")
    return task_id


def wait(task_id: str, timeout: int = 300, quiet: bool = False) -> dict[str, Any]:
    """Опрос с бэкоффом 3 → 10 с."""
    started, delay, last = time.time(), 3.0, ""
    while True:
        data = request("GET", f"/api/v1/jobs/recordInfo?taskId={task_id}")
        state = str(data.get("state", ""))
        if state != last and not quiet:
            print(f"  {task_id}: {state} {data.get('progress', '')}", flush=True)
            last = state
        if state in TERMINAL:
            return data
        if time.time() - started > timeout:
            raise SystemExit(f"задача {task_id} не завершилась за {timeout} с (state={state})")
        time.sleep(delay)
        delay = min(delay * 1.4, 10.0)


def result_urls(data: dict[str, Any]) -> list[str]:
    raw = data.get("resultJson") or "{}"
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return []
    return raw.get("resultUrls") or []


def download(url: str, out: str, size: str | None = None) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                    timeout=120) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"скачивание {url}: HTTP {e.code}")
    tmp = out + ".src"
    with open(tmp, "wb") as f:
        f.write(body)

    if size:
        from PIL import Image
        w, h = (int(x) for x in size.lower().split("x"))
        img = Image.open(tmp).convert("RGB")
        # cover-кадрирование: заполняем кадр без искажения пропорций
        scale = max(w / img.width, h / img.height)
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
        left, top = (img.width - w) // 2, (img.height - h) // 2
        img = img.crop((left, top, left + w, top + h))
        img.save(out, "WEBP", quality=90, method=6)
        os.remove(tmp)
        return f"{out} ({w}×{h})"

    os.replace(tmp, out)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="kie.ai: генерация картинки и ожидание результата")
    ap.add_argument("-p", "--prompt")
    ap.add_argument("-m", "--model", default=DEFAULT_MODEL,
                    help="google/nano-banana (по умолчанию), google/nanobanana2, "
                         "google/nano-banana-pro, google/nano-banana-2-lite")
    ap.add_argument("-a", "--aspect", default="1:1",
                    help="1:1 | 3:2 | 4:3 | 16:9 | 9:16 | 2:3 | 3:4 | 4:5 | 5:4 | 21:9 | auto")
    ap.add_argument("-o", "--out", default="out.png")
    ap.add_argument("-s", "--size", help="привести к размеру, например 1200x800 (cover-кадрирование)")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--credits", action="store_true", help="показать баланс и выйти")
    ap.add_argument("--status", help="проверить задачу по taskId")
    args = ap.parse_args()

    if args.credits:
        print(f"кредитов: {credits():.1f}")
        return 0

    if args.status:
        data = wait(args.status, timeout=args.timeout, quiet=True)
        print(json.dumps({"state": data.get("state"), "urls": result_urls(data),
                          "fail": data.get("failMsg") or data.get("failCode") or None},
                         ensure_ascii=False))
        return 0

    if not args.prompt:
        ap.error("нужен --prompt (или --credits / --status)")

    print(f"модель {args.model}, {args.aspect}, кредитов до: {credits():.1f}")
    task_id = create(args.prompt, args.model, args.aspect)
    print(f"задача {task_id}")
    data = wait(task_id, timeout=args.timeout)
    if data.get("state") != "success":
        print(f"ОШИБКА: {data.get('failCode')} {data.get('failMsg')}", file=sys.stderr)
        return 1
    urls = result_urls(data)
    if not urls:
        print("ОШИБКА: задача success, но resultUrls пуст", file=sys.stderr)
        return 1
    path = download(urls[0], args.out, args.size)
    print(f"готово: {path} | потрачено {data.get('creditsConsumed')} кредитов | "
          f"кредитов после: {credits():.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

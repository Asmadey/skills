#!/usr/bin/env python3
"""LLM adjudication layer for AEO/GEO claims (Ollama Cloud, deepseek-v4.1-flash).

Input : ~/.hermes/data/aeo-claims/claims.jsonl + blocks.json
Output: ~/.hermes/data/aeo-claims/adjudicated.jsonl (verdict_llm, block, tactic, why)
        ~/.hermes/data/aeo-claims/worklist.md (что править в доктрине)

Usage: python3 aeo_claims_adjudicate.py [--limit N] [--batch 8]
"""
import json, os, re, sys, time, urllib.request, urllib.error
from collections import Counter, defaultdict

DATA = os.path.expanduser("~/.hermes/data/aeo-claims")
CLAIMS = os.path.join(DATA, "claims.jsonl")
BLOCKS = os.path.join(DATA, "blocks.json")
OUT = os.path.join(DATA, "adjudicated.jsonl")
WORK = os.path.join(DATA, "worklist.md")

API = "https://ollama.com/api/chat"
MODEL = "deepseek-v4.1-flash:1017"
KEYS = []
KEY_IDX = [0]


def load_keys():
    """Ollama rotates free-plan keys; a 402 means the key is out of quota, not a code bug."""
    if KEYS:
        return KEYS
    env = os.path.expanduser("~/.hermes/.env")
    for name in ("OLLAMA_API_KEY", "OLLAMA_CLOUD_KEY_2", "OLLAMA_CLOUD_KEY_1"):
        if os.environ.get(name):
            KEYS.append(os.environ[name])
    if os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            m = re.match(r"^(OLLAMA_API_KEY|OLLAMA_CLOUD_KEY_2|OLLAMA_CLOUD_KEY_1)=(.+)$", line.strip())
            if m:
                k = m.group(2).strip().strip('"').strip("'")
                if k not in KEYS:
                    KEYS.append(k)
    if not KEYS:
        raise SystemExit("no ollama key")
    return KEYS


def chat(messages, temperature=0.1):
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False,
                       "format": "json", "options": {"temperature": temperature}}).encode()
    keys = load_keys()
    last = None
    for attempt in range(len(keys)):
        k = keys[KEY_IDX[0] % len(keys)]
        req = urllib.request.Request(API, data=body, headers={
            "Authorization": f"Bearer {k}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())["message"]["content"]
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (401, 402, 403):
                KEY_IDX[0] += 1
                continue
            raise
    raise last


SYSTEM = """Ты — аудитор SEO-доктрины. На вход: атом-утверждение из статьи (английский) и каталог
блоков доктрины (русский, id | заголовок), плюс candidate_blocks с текстом.

Порядок работы для каждого атома:
1. Прочитай ВСЕ candidate_blocks атома. Если тот же факт/число/механизм там уже есть -> DUPLICATE,
   в поле block верни id этого блока.
2. Если блок про ту же тему, но атом добавляет число, кейс или механику -> REFINES + id блока.
3. Если атом противоречит числу или утверждению блока -> CONTRADICTS + id блока.
4. NEW только если ни в candidate_blocks, ни в каталоге нет ничего про это. Для NEW block=null.

Запрещено ставить NEW, если в candidate_blocks есть блок с тем же числом или той же механикой.
why — до 15 слов по-русски, что именно нового или в чём расхождение (не пересказ атома).
tactic=true только если из атома следует конкретное действие для сайта.

Примеры:
- атом "200 characters after H1", блок 1.3 "первые 200 символов = grounding-бюджет" -> DUPLICATE, block=1.3
- атом "1,062 pages, 0% JS discovered by GPTBot", блок 1.2 "41-дневный эксперимент, 1062 pages, 0% JS" -> DUPLICATE, block=1.2
- атом "Amazon — топ-источник AI Mode по Semrush 2026", блок 21.4 "топ-10 источников AI Mode, Semrush июнь 2026" -> REFINES, block=21.4, why="добавлен Amazon как источник"

Отвечай строго JSON: {"results":[{"id":"...","verdict":"DUPLICATE|REFINES|CONTRADICTS|NEW","block":"<id или null>",
"tactic":true|false,"why":"..."}]}. Ровно по одному объекту на каждый входной id."""


def catalog(blocks):
    return "\n".join(f"{b['id']} | {b['title']}" for b in blocks)


LAT_RE = re.compile(r"[A-Za-z][A-Za-z0-9\-\.]{3,}")


def candidates(claim, blocks):
    """Deterministic shortlist: numeric verdict blocks + Latin-token overlap + entity hits."""
    out, seen = [], set()
    for bid in (claim.get("vs_block") or []):
        b = next((x for x in blocks if x["id"] == bid), None)
        if b and b["id"] not in seen:
            out.append(b)
            seen.add(b["id"])
    toks = {t.lower() for t in LAT_RE.findall(claim["quote"])}
    scored = []
    for b in blocks:
        if b["id"] in seen:
            continue
        blob = (b["title"] + " " + b["statement"]).lower()
        hits = sum(1 for t in toks if t in blob)
        if claim.get("entity", "general") != "general" and claim["entity"].lower() in blob:
            hits += 3
        if hits:
            scored.append((hits, b))
    scored.sort(key=lambda x: -x[0])
    for _, b in scored[:4]:
        if b["id"] not in seen:
            out.append(b)
            seen.add(b["id"])
    return out[:5]


def main():
    limit = None
    batch = 8
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--limit":
            limit = int(args[i + 1])
        if a == "--batch":
            batch = int(args[i + 1])

    claims = [json.loads(l) for l in open(CLAIMS, encoding="utf-8")]
    blocks = json.load(open(BLOCKS, encoding="utf-8"))
    done = {}
    if os.path.exists(OUT):
        for l in open(OUT, encoding="utf-8"):
            r = json.loads(l)
            done[r["id"]] = r
    todo = [c for c in claims if c["id"] not in done]
    if limit:
        todo = todo[:limit]
    print(f"claims={len(claims)} already={len(done)} todo={len(todo)}")

    cat = catalog(blocks)
    for start in range(0, len(todo), batch):
        chunk = todo[start:start + batch]
        payload = []
        for c in chunk:
            cand = candidates(c, blocks)
            payload.append({
                "id": c["id"], "quote": c["quote"][:420],
                "numbers": c["numbers"][:8], "entity": c["entity"],
                "candidate_blocks": [{"id": b["id"], "title": b["title"],
                                      "statement": b["statement"][:420]} for b in cand],
            })
        user = ("КАТАЛОГ БЛОКОВ ДОКТРИНЫ (id | заголовок):\n" + cat +
                "\n\nАТОМЫ:\n" + json.dumps(payload, ensure_ascii=False))
        try:
            raw = chat([{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}])
            res = json.loads(raw).get("results", [])
        except Exception as e:
            print("ERR batch", start, repr(e)[:200])
            time.sleep(5)
            continue
        by_id = {r.get("id"): r for r in res if isinstance(r, dict)}
        with open(OUT, "a", encoding="utf-8") as f:
            for c in chunk:
                r = by_id.get(c["id"]) or {}
                rec = {**c,
                       "verdict_llm": (r.get("verdict") or "PARSE_FAIL").upper(),
                       "block_llm": r.get("block"),
                       "tactic": bool(r.get("tactic")),
                       "why": (r.get("why") or "")[:200]}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        done_before = start
        print(f"  {start+len(chunk)}/{len(todo)} ok", flush=True)

    if not os.path.exists(OUT):
        raise SystemExit("nothing adjudicated - API refused every key")
    rows = [json.loads(l) for l in open(OUT, encoding="utf-8")]
    by_v = Counter(r["verdict_llm"] for r in rows)
    print("verdicts_llm:", dict(by_v))

    order = {"CONTRADICTS": 0, "REFINES": 1, "NEW": 2, "DUPLICATE": 3, "PARSE_FAIL": 4}
    rows.sort(key=lambda r: (order.get(r["verdict_llm"], 9), -r.get("score", 0)))
    L = ["# AEO/GEO worklist (LLM adjudication)", "",
         f"Атомов: {len(rows)} | вердикты: {dict(by_v)}", ""]
    for v in ("CONTRADICTS", "REFINES", "NEW"):
        sub = [r for r in rows if r["verdict_llm"] == v]
        L += [f"## {v} ({len(sub)})"]
        for r in sub[:40]:
            flag = "действие" if r["tactic"] else "факт"
            L.append(f"- [{flag}] блок {r.get('block_llm') or '—'} | {r['entity']} | {r['why']}")
            L.append(f"  > {r['quote'][:300]}")
            L.append(f"  {r['article_url']}")
        L.append("")
    open(WORK, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", WORK)


if __name__ == "__main__":
    main()

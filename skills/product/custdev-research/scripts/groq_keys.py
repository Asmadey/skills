#!/usr/bin/env python3
"""
groq_keys.py — Multi-key rotation for the Groq API (per-model day/minute budgets).

WHY
---
Groq free-tier limits are per ACCOUNT and per MODEL:
  * openai/gpt-oss-120b  -> 8 000 tokens/min  (TPM), 200 000 tokens/day (TPD), 1 000 req/day
  * whisper-large-v3     -> audio-seconds/min  and  audio-seconds/day
When one key burns its daily budget the whole pipeline used to die (429 / TPD) halfway
through a meeting. Now the ring simply moves to the next key and remembers the
exhausted one on disk, so a re-run later the same day starts on a healthy key.

KEY SOURCES (merged, de-duplicated, order = priority order)
-----------------------------------------------------------
  1. env  GROQ_API_KEYS / GROQ_KEYS   "gsk_a,gsk_b"  (comma / space / newline separated)
  2. .env entries named  groq, groq2, groq_2, GROQ_KEY_3, GROQ_API_KEY_4 ...
  3. <repo>/groq_keys.txt             one key per line, '#' comments allowed
  4. ~/.groq_keys                     same format (shared across checkouts)

USAGE
-----
    from groq_keys import KEYRING

    resp = KEYRING.chat(model="openai/gpt-oss-120b", messages=[...], temperature=0.0)
    tr   = KEYRING.transcribe(file=(name, bytes), model="whisper-large-v3", language="ru")

Both are drop-in replacements for client.chat.completions.create / client.audio.transcriptions.create,
with automatic key rotation on 429 and per-(key, model) budget tracking.

CLI
---
    python3 skills/product/custdev-research/scripts/groq_keys.py status   # keys loaded + remaining budget state
    python3 skills/product/custdev-research/scripts/groq_keys.py check    # live 1-token probe per key, records real limits
    python3 skills/product/custdev-research/scripts/groq_keys.py reset    # forget exhausted state (e.g. next day)

NOTE: rotating accounts to dodge rate limits is against Groq's ToS ("circumvent rate
limits"). This module is a resilience layer for keys YOU legitimately own (own account,
team accounts, org/project keys, paid Dev-tier keys). Use it at your own risk.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

_SHARED_DIR = Path(__file__).resolve().parent


def _resolve_base_dir() -> Path:
    """Корень проекта пользователя: env CUSTDEV_BASE_DIR → поиск вверх от CWD по Meets/ или .git.

    Считается от текущей папки, а не от расположения модуля: скилл может лежать внутри
    проекта (skills/product/custdev-research/scripts) или как отдельно установленный пакет.
    """
    env = os.getenv("CUSTDEV_BASE_DIR")
    if env:
        return Path(env).expanduser().resolve()
    here = Path.cwd().resolve()
    for cand in (here, *here.parents):
        if (cand / "Meets").is_dir() or (cand / ".git").is_dir():
            return cand
    return here


REPO_ROOT = _resolve_base_dir()
CACHE_DIR = REPO_ROOT / ".cache"
STATE_PATH = CACHE_DIR / "groq_keys_state.json"

SHORT_WAIT_CAP = 90.0      # seconds we are willing to sleep through a per-minute limit
LONG_WAIT_CAP = 300.0      # absolute max single sleep before giving up on the run
DAILY_KEYWORDS = ("per day", "tokens per day", "tpd", "requests per day", "rpd",
                  "audio seconds per day", "seconds per day", "as d", "asd")
MINUTE_KEYWORDS = ("per minute", "tokens per minute", "tpm", "requests per minute",
                   "rpm", "audio seconds per minute", "per hour", "tph", "per second")


# --------------------------------------------------------------------------- errors

class AllKeysExhausted(RuntimeError):
    """No key in the ring can serve this model right now."""

    def __init__(self, model: str, retry_in: float | None = None, detail: str = ""):
        self.model = model
        self.retry_in = retry_in
        human = _human(retry_in) if retry_in else "unknown"
        super().__init__(f"all Groq keys exhausted for {model} (nearest reset in {human}){detail}")


# --------------------------------------------------------------------------- helpers

def _human(seconds: float | None) -> str:
    if seconds is None:
        return "?"
    s = max(0, int(seconds))
    if s >= 86400:
        return f"{s // 86400}d{(s % 86400) // 3600}h"
    if s >= 3600:
        return f"{s // 3600}h{(s % 3600) // 60:02d}m"
    if s >= 60:
        return f"{s // 60}m{s % 60:02d}s"
    return f"{s}s"


def _utc_day() -> str:
    return time.strftime("%Y-%m-%d", time.gmtime())


USAGE_LOG = CACHE_DIR / "groq_usage.jsonl"


def _mask(key: str) -> str:
    return f"…{key[-4:]}" if len(key) > 8 else "…"


def _key_id(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def _clean(raw: str) -> str:
    return raw.strip().strip('"\'').strip()


def _status_code(err: Exception) -> int | None:
    for attr in ("status_code",):
        code = getattr(err, attr, None)
        if isinstance(code, int):
            return code
    resp = getattr(err, "response", None)
    code = getattr(resp, "status_code", None)
    return code if isinstance(code, int) else None


def _error_message(err: Exception) -> str:
    body = getattr(err, "body", None)
    if isinstance(body, dict):
        msg = (body.get("error") or {}).get("message")
        if msg:
            return str(msg)
    resp = getattr(err, "response", None)
    text = getattr(resp, "text", None)
    if text:
        try:
            parsed = json.loads(text)
            msg = (parsed.get("error") or {}).get("message")
            if msg:
                return str(msg)
        except Exception:
            pass
        return text[:400]
    return str(err)


def _retry_after(err: Exception) -> float | None:
    """Seconds to wait, parsed from the retry-after header or the error message."""
    resp = getattr(err, "response", None)
    headers = getattr(resp, "headers", None) or {}
    for name in ("retry-after", "Retry-After", "x-ratelimit-reset-tokens", "x-ratelimit-reset-requests"):
        try:
            raw = headers.get(name)
        except Exception:
            raw = None
        if not raw:
            continue
        raw = str(raw)
        m = re.fullmatch(r"([\d.]+)(ms|s)?", raw)
        if m:
            val = float(m.group(1))
            return val / 1000.0 if m.group(2) == "ms" else val
        parsed = _parse_duration(raw)
        if parsed:
            return parsed

    msg = _error_message(err)
    m = re.search(r"try again in ([0-9hms.]+)", msg, re.I)
    if m:
        return _parse_duration(m.group(1))
    m = re.search(r"reset(?:s)? in ([0-9hms.]+)", msg, re.I)
    if m:
        return _parse_duration(m.group(1))
    return None


def _parse_duration(raw: str) -> float | None:
    """'12m24.335999s' / '1h0m28.8s' / '547ms' / '4.2s' -> seconds."""
    raw = raw.strip()
    if not raw:
        return None
    m = re.fullmatch(r"([\d.]+)ms", raw)
    if m:
        return float(m.group(1)) / 1000.0
    total, found = 0.0, False
    for value, unit in re.findall(r"([\d.]+)\s*([dhms])", raw):
        found = True
        total += float(value) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[unit]
    if found:
        return total
    m = re.fullmatch(r"[\d.]+", raw)
    return float(raw) if m else None


def classify(err: Exception) -> tuple[str, float | None, str]:
    """-> ('daily'|'minute'|'too_large'|'invalid'|'transient'|'fatal', wait_seconds, message)"""
    code = _status_code(err)
    msg = _error_message(err)
    low = msg.lower()
    wait = _retry_after(err)

    if code in (401, 403):
        return "invalid", None, msg
    if "request too large" in low or "too large for model" in low:
        # Not a key problem: the REQUEST exceeds this model's TPM. Caller must shrink it.
        return "too_large", None, msg
    if code == 429:
        if any(k in low for k in DAILY_KEYWORDS):
            return "daily", wait, msg
        return "minute", wait, msg
    if code in (413, 422):
        return "fatal", None, msg            # payload too large — rotating will not help
    if code is None:
        name = type(err).__name__.lower()
        if any(k in name for k in ("connection", "timeout", "protocol")):
            return "transient", wait, msg
        if any(k in low for k in ("timed out", "connection", "temporarily")):
            return "transient", wait, msg
        return "fatal", None, msg
    if 500 <= code < 600:
        return "transient", wait, msg
    return "fatal", None, msg


# --------------------------------------------------------------------------- state

@dataclass
class _KeyModel:
    day_until: float = 0.0          # когда снимется дневной лимит (epoch)
    min_until: float = 0.0          # когда снимется минутный лимит (epoch)
    day: str = ""                   # UTC-дата учёта, для сброса счётчиков
    tokens_used: int = 0            # израсходовано токенов за этот UTC-день
    audio_used: float = 0.0         # израсходовано секунд аудио за этот UTC-день
    calls: int = 0
    daily_limit: int = 0            # выучено из 429-сообщения ("Limit 200000")
    daily_limit_kind: str = ""      # "tokens" | "audio_seconds"


@dataclass
class _Key:
    value: str
    mask: str = ""
    invalid: bool = False
    note: str = ""
    limits: dict = field(default_factory=dict)
    models: dict[str, _KeyModel] = field(default_factory=dict)

    def __post_init__(self):
        if not self.mask:
            self.mask = _mask(self.value)

    def slot(self, model: str) -> _KeyModel:
        slot = self.models.setdefault(model, _KeyModel())
        today = _utc_day()
        if slot.day != today:                 # новый UTC-день — счётчики с нуля
            slot.day, slot.tokens_used, slot.audio_used, slot.calls = today, 0, 0.0, 0
        return slot

    def ready_at(self, model: str) -> float:
        if self.invalid:
            return float("inf")
        slot = self.slot(model)
        return max(slot.min_until, slot.day_until)

    def day_reset_at(self, model: str) -> float | None:
        until = self.slot(model).day_until
        return until if until > time.time() else None


class KeyRing:
    def __init__(self, keys: list[str] | None = None, state_path: Path | str | None = None,
                 verbose: bool = True, spread: bool = True):
        self.state_path = Path(state_path) if state_path else STATE_PATH
        self.verbose = verbose
        self.spread = spread
        self._lock = threading.Lock()
        self._rr = 0
        self._clients: dict[str, object] = {}
        self.keys: list[_Key] = []
        for value in (keys if keys is not None else load_keys()):
            self._add(value)
        self._load_state()
        if self.verbose:
            self._banner()

    # ---- construction / loading ----

    def _add(self, raw: str) -> None:
        value = _clean(raw)
        if not value or any(k.value == value for k in self.keys):
            return
        self.keys.append(_Key(value=value))

    def _banner(self) -> None:
        if not self.keys:
            print("⚠️  Groq key ring is empty — set GROQ_API_KEYS or `groq` in .env")
            return
        masks = ", ".join(k.mask for k in self.keys)
        print(f"🔑 Groq key ring: {len(self.keys)} key(s) [{masks}]")

    def _load_state(self) -> None:
        if not self.state_path.exists():
            return
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            stored = data.get("keys") or {}
        except Exception:
            return
        for key in self.keys:
            node = stored.get(_key_id(key.value))
            if not node:
                continue
            key.invalid = bool(node.get("invalid"))
            key.note = node.get("note") or ""
            key.limits = node.get("limits") or {}
            for model, slot in (node.get("models") or {}).items():
                key.models[model] = _KeyModel(
                    day_until=float(slot.get("day_until") or 0),
                    min_until=float(slot.get("min_until") or 0),
                    day=slot.get("day") or "",
                    tokens_used=int(slot.get("tokens_used") or 0),
                    audio_used=float(slot.get("audio_used") or 0),
                    calls=int(slot.get("calls") or 0),
                    daily_limit=int(slot.get("daily_limit") or 0),
                    daily_limit_kind=slot.get("daily_limit_kind") or "",
                )

    def save_state(self) -> None:
        payload: dict = {"version": 1, "saved_at": time.time(), "keys": {}}
        for key in self.keys:
            payload["keys"][_key_id(key.value)] = {
                "mask": key.mask,
                "invalid": key.invalid,
                "note": key.note,
                "limits": key.limits,
                "models": {
                    model: {
                        "day_until": slot.day_until,
                        "min_until": slot.min_until,
                        "day": slot.day,
                        "tokens_used": slot.tokens_used,
                        "audio_used": slot.audio_used,
                        "calls": slot.calls,
                        "daily_limit": slot.daily_limit,
                        "daily_limit_kind": slot.daily_limit_kind,
                    }
                    for model, slot in key.models.items()
                },
            }
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as err:            # never break a pipeline over telemetry
            if self.verbose:
                print(f"⚠️  could not save key state: {err}")

    # ---- client / selection ----

    def client_for(self, key: _Key):
        if key.value not in self._clients:
            from groq import Groq        # imported lazily so `status` works without the SDK
            self._clients[key.value] = Groq(api_key=key.value)
        return self._clients[key.value]

    def client(self):
        """Backward-compatible client bound to the next usable key (for code that
        still calls client.chat.completions.create directly)."""
        key = self._pick_any()
        if key is None:
            raise AllKeysExhausted("<any>")
        return self.client_for(key)

    def _ordered(self) -> list[_Key]:
        if not self.keys:
            return []
        with self._lock:
            start = self._rr % len(self.keys)
            if self.spread:
                self._rr = (self._rr + 1) % len(self.keys)
        return self.keys[start:] + self.keys[:start]

    def _pick(self, model: str) -> tuple[_Key | None, float | None]:
        """-> (usable_key, None) or (None, seconds_until_some_key_is_ready)"""
        now = time.time()
        earliest = float("inf")
        live = False
        for key in self._ordered():
            if key.invalid:
                continue
            live = True
            ready = key.ready_at(model)
            if ready <= now:
                return key, None
            earliest = min(earliest, ready)
        if not live:
            return None, None                 # every key is invalid -> unrecoverable
        return None, max(0.0, earliest - now)

    def _pick_any(self) -> _Key | None:
        now = time.time()
        for key in self._ordered():
            if not key.invalid and all(k.ready_at(m) <= now for m in (key.models or {"": _KeyModel()})):
                return key
        for key in self._ordered():
            if not key.invalid:
                return key
        return None

    # ---- budget ledger ----

    def remaining(self, key: _Key, model: str) -> tuple[float, float] | None:
        """-> (used, limit) для дневного лимита этой модели, или None если лимит неизвестен."""
        slot = key.slot(model)
        limit = slot.daily_limit
        if not limit:
            return None
        used = slot.audio_used if slot.daily_limit_kind == "audio_seconds" else slot.tokens_used
        return used, limit

    def can_afford(self, key: _Key, model: str, est_tokens: int = 0, est_audio_seconds: float = 0.0) -> bool:
        """Хватит ли дневного бюджета на ещё один запрос (консервативно, по локальному учёту)."""
        rem = self.remaining(key, model)
        if rem is None:
            return True                        # лимит ещё не выучен — не блокируем
        used, limit = rem
        need = est_audio_seconds if est_tokens == 0 and est_audio_seconds else est_tokens
        return used + need <= limit

    def record(self, key: _Key, model: str, prompt_tokens: int = 0, completion_tokens: int = 0,
               audio_seconds: float = 0.0) -> None:
        slot = key.slot(model)
        slot.calls += 1
        slot.tokens_used += max(0, int(prompt_tokens)) + max(0, int(completion_tokens))
        slot.audio_used += max(0.0, float(audio_seconds))
        if audio_seconds and not slot.daily_limit_kind:
            slot.daily_limit_kind = "audio_seconds"
        elif prompt_tokens and not slot.daily_limit_kind:
            slot.daily_limit_kind = "tokens"
        try:
            line = json.dumps({
                "ts": round(time.time(), 3),
                "utc_day": _utc_day(),
                "key": key.mask,
                "model": model,
                "tokens_in": int(prompt_tokens),
                "tokens_out": int(completion_tokens),
                "audio_sec": round(float(audio_seconds), 2),
            }, ensure_ascii=False)
            USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(USAGE_LOG, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except Exception:
            pass

    def _learn_limits(self, key: _Key, model: str, msg: str) -> None:
        """Достаёт из текста 429 реальные лимиты: 'Limit 200000, Used 198589'."""
        m = re.search(r"Limit (\d+), Used (\d+)", msg)
        if not m:
            return
        limit, used = int(m.group(1)), int(m.group(2))
        slot = key.slot(model)
        slot.daily_limit = limit
        if "audio second" in msg.lower():
            slot.daily_limit_kind = "audio_seconds"
            slot.audio_used = max(slot.audio_used, float(used))
        else:
            slot.daily_limit_kind = "tokens"
            slot.tokens_used = max(slot.tokens_used, used)
        print(f"   📊 выучен дневной лимит {model}: {limit} "
              f"({'сек. аудио' if slot.daily_limit_kind == 'audio_seconds' else 'токенов'}), "
              f"израсходовано {used}")

    # ---- core call wrapper ----

    def run(self, fn, model: str, what: str = "", max_attempts: int = 0, max_wait: float = LONG_WAIT_CAP,
            est_tokens: int = 0, est_audio_seconds: float = 0.0):
        """Run fn(client) with key rotation. Retries other keys on 429, sleeps on TPM."""
        if not self.keys:
            raise AllKeysExhausted(model, detail=" — no keys configured")
        attempts = 0
        limit = max_attempts or max(4, 3 * len(self.keys))
        waited = 0.0
        last_error: Exception | None = None

        while attempts < limit:
            attempts += 1
            key, wait = self._pick(model)
            if key is None:
                if wait is None:
                    raise AllKeysExhausted(model, detail=" — every key is invalid/revoked")
                if wait > SHORT_WAIT_CAP or waited + wait > max_wait:
                    raise AllKeysExhausted(model, retry_in=wait)
                print(f"⏳ [{model}] all keys at minute limit — waiting {_human(wait)}")
                time.sleep(min(wait + 0.5, SHORT_WAIT_CAP))
                waited += wait
                continue

            if not self.can_afford(key, model, est_tokens, est_audio_seconds):
                used, limit = self.remaining(key, model)
                slot = key.slot(model)
                # Помечаем как «дневной отказ» (а не минутный) — иначе движок будет
                # крутить короткие ожидания вместо перехода на другой ключ.
                if slot.day_until <= time.time():
                    slot.day_until = time.time() + 3600
                print(f"🔁 [{model}] key {key.mask}: дневной бюджет не влезает "
                      f"({used:.0f}/{limit} израсходовано) → следующий ключ")
                self.save_state()
                continue

            try:
                resp = fn(self.client_for(key))
                usage = getattr(resp, "usage", None)
                duration = 0.0
                if est_audio_seconds:
                    duration = float(getattr(resp, "duration", 0) or est_audio_seconds)
                self.record(
                    key, model,
                    prompt_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                    completion_tokens=getattr(usage, "completion_tokens", 0) or 0,
                    audio_seconds=duration,
                )
                self.save_state()
                return resp
            except Exception as err:
                verdict, wait, msg = classify(err)
                last_error = err
                brief = msg.split("Need more tokens")[0].split("—")[0].strip()[:110]

                if verdict == "daily":
                    self._learn_limits(key, model, msg)
                    hold = float(wait or 3600.0) + 5.0
                    key.slot(model).day_until = time.time() + hold
                    self.save_state()
                    print(f"🔁 [{model}] key {key.mask} out of daily budget "
                          f"({_human(hold)} left) → next key")
                    continue

                if verdict == "minute":
                    hold = float(wait or 60.0) + 1.0
                    key.slot(model).min_until = time.time() + hold
                    self.save_state()
                    others = any(k is not key and not k.invalid and k.ready_at(model) <= time.time()
                                 for k in self.keys)
                    if others:
                        print(f"🔁 [{model}] key {key.mask} hit per-minute limit → next key")
                        continue
                    print(f"⏳ [{model}] rate limited on all keys — waiting {_human(hold)}")
                    time.sleep(min(hold, SHORT_WAIT_CAP))
                    waited += hold
                    continue

                if verdict == "invalid":
                    key.invalid = True
                    key.note = brief
                    self.save_state()
                    print(f"⛔ key {key.mask} rejected (401/403) — disabled for future runs")
                    continue

                if verdict == "too_large":
                    raise                    # caller shrinks the request and retries

                if verdict == "transient":
                    backoff = min(2.0 ** (attempts - 1), 20.0)
                    print(f"⚠️  [{model}] transient error on key {key.mask} ({brief}) — retry in {backoff:.0f}s")
                    time.sleep(backoff)
                    continue

                raise                            # fatal: bad payload, nothing to rotate

        raise AllKeysExhausted(model, detail=f" — gave up after {attempts} attempts"
                                             + (f": {_error_message(last_error)[:120]}" if last_error else ""))

    # ---- drop-in wrappers ----

    def chat(self, est_tokens: int = 0, **kwargs):
        model = kwargs.get("model", "unknown")
        return self.run(lambda client: client.chat.completions.create(**kwargs), model=model,
                        what="chat", est_tokens=est_tokens)

    def transcribe(self, est_audio_seconds: float = 0.0, **kwargs):
        model = kwargs.get("model", "whisper-large-v3")
        return self.run(lambda client: client.audio.transcriptions.create(**kwargs), model=model,
                        what="asr", est_audio_seconds=est_audio_seconds)

    # ---- reporting ----

    def status_rows(self) -> list[tuple[str, str, str, str]]:
        rows, now = [], time.time()
        for idx, key in enumerate(self.keys, 1):
            if key.invalid:
                rows.append((f"#{idx} {key.mask}", "INVALID", key.note or "401/403", "-"))
                continue
            models = key.models or {}
            if not models:
                rows.append((f"#{idx} {key.mask}", "ok", "no calls recorded yet", "-"))
                continue
            for model, slot in models.items():
                state, reset = "ok", "-"
                if slot.day_until > now:
                    state, reset = "DAILY EXHAUSTED", _human(slot.day_until - now)
                elif slot.min_until > now:
                    state, reset = "minute cooldown", _human(slot.min_until - now)
                if slot.daily_limit_kind == "audio_seconds":
                    spent = f"аудио {slot.audio_used:.0f}"
                else:
                    spent = f"{slot.tokens_used} ток."
                if slot.daily_limit:
                    spent += f"/{slot.daily_limit} ({100 * (slot.audio_used if slot.daily_limit_kind == 'audio_seconds' else slot.tokens_used) / slot.daily_limit:.0f}%)"
                rows.append((f"#{idx} {key.mask}", state, model, f"{spent}; calls {slot.calls}; reset {reset}"))
        return rows

    def preflight(self, models=("openai/gpt-oss-120b", "whisper-large-v3"),
                  est_tokens: int = 0, est_audio_seconds: float = 0.0) -> None:
        """Печатает состояние бюджета ДО запуска пайплайна и вердикт «влезает / нет».

        Вызывать в начале пайплайна: пользователь сразу видит, есть ли запас,
        вместо того чтобы узнать об этом из 429 на середине встречи.
        """
        print("💰 Бюджет Groq (по локальному учёту за текущие UTC-сутки):")
        if not self.keys:
            print("   ⚠️  ключей нет — добавь GROQ_API_KEYS или groq_keys.txt")
            return
        for idx, key in enumerate(self.keys, 1):
            if key.invalid:
                print(f"   #{idx} {key.mask}: ⛔ отключён ({key.note or '401'})")
                continue
            shown = False
            for model in models:
                slot = key.slot(model)
                if not (slot.calls or slot.daily_limit):
                    continue
                shown = True
                used = slot.audio_used if slot.daily_limit_kind == "audio_seconds" else slot.tokens_used
                unit = "сек. аудио" if slot.daily_limit_kind == "audio_seconds" else "токенов"
                if slot.daily_limit:
                    pct = 100 * used / slot.daily_limit
                    left = slot.daily_limit - used
                    extra = ""
                    if est_tokens and slot.daily_limit_kind != "audio_seconds":
                        extra = f" | на эту работу нужно ≈{est_tokens}, остаток {left:.0f} → " + \
                                ("влезает" if est_tokens <= left else "НЕ влезает")
                    elif est_audio_seconds:
                        extra = f" | на эту работу нужно ≈{est_audio_seconds:.0f} сек → " + \
                                ("влезает" if est_audio_seconds <= left else "НЕ влезает")
                    print(f"   #{idx} {key.mask} [{model}]: {used:.0f}/{slot.daily_limit} {unit} "
                          f"({pct:.0f}%), сброс через {_human(max(0.0, slot.day_until - time.time())) if slot.day_until > time.time() else '-'}{extra}")
                else:
                    print(f"   #{idx} {key.mask} [{model}]: {used:.0f} {unit}, {slot.calls} вызовов (лимит ещё не выучен)")
            if not shown:
                print(f"   #{idx} {key.mask}: расходов ещё не было")

    def daily_report(self) -> str:
        """Короткая строка «сколько сожжено за сегодня» для печати в начале пайплайна."""
        parts = []
        for idx, key in enumerate(self.keys, 1):
            if key.invalid:
                continue
            for model, slot in key.models.items():
                if slot.calls:
                    limit = f"/{slot.daily_limit}" if slot.daily_limit else ""
                    unit = "сек.аудио" if slot.daily_limit_kind == "audio_seconds" else "ток."
                    used = slot.audio_used if slot.daily_limit_kind == "audio_seconds" else slot.tokens_used
                    parts.append(f"{key.mask} {model}: {used:.0f}{limit} {unit} ({slot.calls} вызовов)")
        return "; ".join(parts) if parts else "за сегодня расходов ещё не было"

    def live_check(self) -> None:
        """One tiny call per key to record real per-request limits from the headers."""
        for key in self.keys:
            if key.invalid:
                print(f"  {key.mask}: skipped (invalid)")
                continue
            try:
                raw = self.client_for(key).with_raw_response.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": "ping"}],
                    max_completion_tokens=1,
                )
                headers = {k.lower(): v for k, v in raw.headers.items()}
                key.limits["openai/gpt-oss-120b"] = {
                    "rpd": headers.get("x-ratelimit-limit-requests"),
                    "tpm": headers.get("x-ratelimit-limit-tokens"),
                    "tokens_left": headers.get("x-ratelimit-remaining-tokens"),
                }
                print(f"  {key.mask}: alive, limits {key.limits['openai/gpt-oss-120b']}")
            except Exception as err:
                verdict, wait, msg = classify(err)
                if verdict == "invalid":
                    key.invalid = True
                if verdict == "daily":
                    key.slot("openai/gpt-oss-120b").day_until = time.time() + float(wait or 3600) + 5
                print(f"  {key.mask}: {verdict} — {msg[:90]}")
        self.save_state()


# --------------------------------------------------------------------------- key discovery

_KEY_NAME_RE = re.compile(r"^(?:groq|groqkey|groq_key|groq_api_key)(?:_?(\d+))?$", re.I)


def load_keys(explicit: list[str] | None = None) -> list[str]:
    if explicit:
        return [_clean(k) for k in explicit if _clean(k)]

    found: list[str] = []

    for var in ("GROQ_API_KEYS", "GROQ_KEYS"):
        raw = os.getenv(var)
        if raw:
            found.extend(part for part in re.split(r"[,\s;]+", raw) if part)

    try:
        from dotenv import dotenv_values, find_dotenv, load_dotenv
        load_dotenv(find_dotenv(usecwd=False))
        env_path = REPO_ROOT / ".env"
        values = dotenv_values(env_path) if env_path.exists() else {}
    except Exception:
        values = {}

    named: list[tuple[int, str]] = []
    for name, value in values.items():
        if not value:
            continue
        m = _KEY_NAME_RE.match(name.strip())
        if m:
            named.append((int(m.group(1) or 1), value))
    for name in ("groq", "GROQ_API_KEY"):
        raw = os.getenv(name)
        if raw:
            named.append((1, raw))
    for _, value in sorted(named, key=lambda item: item[0]):
        found.append(value)

    for path in (REPO_ROOT / "groq_keys.txt", Path.home() / ".groq_keys"):
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.split("#", 1)[0].strip()
                if line:
                    found.append(line)

    out, seen = [], set()
    for raw in found:
        value = _clean(raw)
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


KEYRING = KeyRing()


# --------------------------------------------------------------------------- CLI

def _usage_report(days: float) -> int:
    """Суммирует лог вызовов за последние `days` суток (30 = «месяц»)."""
    if not USAGE_LOG.exists():
        print("лог пуст — вызовов ещё не было")
        return 0
    cutoff = time.time() - days * 86400
    per_model: dict[str, dict[str, float]] = {}
    per_day: dict[str, dict[str, float]] = {}
    for line in USAGE_LOG.read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if rec.get("ts", 0) < cutoff:
            continue
        model = rec.get("model", "?")
        m = per_model.setdefault(model, {"in": 0, "out": 0, "audio": 0.0, "calls": 0})
        m["in"] += rec.get("tokens_in", 0)
        m["out"] += rec.get("tokens_out", 0)
        m["audio"] += rec.get("audio_sec", 0.0)
        m["calls"] += 1
        d = per_day.setdefault(rec.get("utc_day", "?"), {"tok": 0, "audio": 0.0, "calls": 0})
        d["tok"] += rec.get("tokens_in", 0) + rec.get("tokens_out", 0)
        d["audio"] += rec.get("audio_sec", 0.0)
        d["calls"] += 1

    print(f"📊 Расход за последние {days:.0f} сут. (по локальному логу {USAGE_LOG.name}):")
    for model, m in sorted(per_model.items(), key=lambda kv: kv[1]["in"] + kv[1]["out"], reverse=True):
        audio = f", аудио {m['audio'] / 60:.1f} мин" if m["audio"] else ""
        print(f"   {model}: {m['in']} in + {m['out']} out токенов, {m['calls']} вызовов{audio}")
    print("\nПо дням:")
    for day, d in sorted(per_day.items()):
        audio = f", аудио {d['audio'] / 60:.1f} мин" if d["audio"] else ""
        print(f"   {day}: {d['tok']} токенов{audio}, {d['calls']} вызовов")
    return 0


def _main(argv: list[str]) -> int:
    cmd = (argv[1] if len(argv) > 1 else "status").lower()
    if cmd in ("usage", "month"):
        days = float(argv[2]) if len(argv) > 2 else (30.0 if cmd == "month" else 1.0)
        return _usage_report(days)
    if cmd == "reset":
        if STATE_PATH.exists():
            STATE_PATH.unlink()
        print(f"🧹 state cleared: {STATE_PATH}")
        return 0
    if not KEYRING.keys:
        print("No keys found. Add GROQ_API_KEYS=\"gsk_a,gsk_b\" to .env or create groq_keys.txt")
        return 1
    if cmd == "check":
        print(f"🔍 live probe of {len(KEYRING.keys)} key(s):")
        KEYRING.live_check()
        cmd = "status"
    if cmd == "status":
        rows = KEYRING.status_rows()
        width = [max(len(str(r[i])) for r in rows + [("key", "state", "model", "reset/limits")]) for i in range(4)]
        for row in [("key", "state", "model", "reset/limits")] + rows:
            print("  " + "  ".join(str(c).ljust(width[i]) for i, c in enumerate(row)))
        print(f"\nstate file: {STATE_PATH}")
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))

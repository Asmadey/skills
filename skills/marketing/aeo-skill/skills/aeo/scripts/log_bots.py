#!/usr/bin/env python3
"""Активность AI-ботов в логах веб-сервера (combined / common log format).

Примеры:
  python3 log_bots.py /var/log/nginx/access.log
  python3 log_bots.py access.log access.log.1 --top 20 --json
  zcat access.log.*.gz | python3 log_bots.py -
"""
import argparse
import collections
import json
import re
import sys

BOTS = {
    "GPTBot": "обучение", "OAI-SearchBot": "поиск", "ChatGPT-User": "чтение по запросу",
    "ClaudeBot": "обучение", "Claude-SearchBot": "поиск", "Claude-User": "чтение по запросу",
    "PerplexityBot": "поиск", "Perplexity-User": "чтение по запросу",
    "Googlebot": "поиск", "GoogleOther": "прочее Google", "bingbot": "поиск",
    "meta-externalagent": "Meta AI", "Amazonbot": "Amazon", "Applebot": "Apple",
    "Bytespider": "ByteDance", "CCBot": "Common Crawl", "DuckAssistBot": "DuckDuckGo AI",
}
LINE = re.compile(r'"(?P<m>[A-Z]+) (?P<path>\S+)[^"]*" (?P<st>\d{3}) (?P<size>\S+)(?: "(?P<ref>[^"]*)" "(?P<ua>[^"]*)")?')
AI_REF = re.compile(r"chatgpt\.com|chat\.openai\.com|perplexity\.ai|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|you\.com|deepseek\.com|grok\.com", re.I)
ASSET = re.compile(r"\.(?:css|js|png|jpe?g|gif|svg|webp|avif|ico|woff2?|ttf|map)(?:\?|$)", re.I)


def main():
    ap = argparse.ArgumentParser(description="AI-боты в логах сервера")
    ap.add_argument("files", nargs="+", help="файлы логов или - для stdin")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    hits = collections.Counter()
    status = collections.defaultdict(collections.Counter)
    paths = collections.defaultdict(collections.Counter)
    refs = collections.Counter()
    ref_paths = collections.Counter()
    total = 0
    for name in a.files:
        fh = sys.stdin if name == "-" else open(name, encoding="utf-8", errors="replace")
        for line in fh:
            m = LINE.search(line)
            if not m:
                continue
            total += 1
            ua, ref, path = m.group("ua") or "", m.group("ref") or "", m.group("path")
            r = AI_REF.search(ref)
            if r:
                refs[r.group(0).lower()] += 1
                ref_paths[path] += 1
            low = ua.lower()
            for bot in BOTS:
                if bot.lower() in low:
                    hits[bot] += 1
                    status[bot][m.group("st")] += 1
                    if not ASSET.search(path):
                        paths[bot][path] += 1
                    break

    out = {"lines": total, "bots": [], "ai_referrals": dict(refs), "ai_referral_pages": ref_paths.most_common(a.top), "findings": []}
    for bot, n in hits.most_common():
        errs = sum(c for s, c in status[bot].items() if s[0] in "45")
        out["bots"].append({"bot": bot, "purpose": BOTS[bot], "hits": n, "status": dict(status[bot]),
                            "error_pct": round(100 * errs / n, 1), "top_paths": paths[bot].most_common(a.top)})
    f = out["findings"]
    for b in out["bots"]:
        if b["error_pct"] >= 20:
            f.append(f"{b['bot']}: {b['error_pct']}% ответов 4xx/5xx — проверь блокировки и битые URL")
        if b["status"].get("403") or b["status"].get("429"):
            f.append(f"{b['bot']}: есть ответы 403/429 — бот блокируется или упирается в лимит")
    for need in ("OAI-SearchBot", "ChatGPT-User", "bingbot", "Googlebot"):
        if need not in hits:
            f.append(f"{need} в логах не встречается: бот не доходит до сервера, или лог покрывает слишком короткий период")
    scraped = sum(hits[b] for b in ("GPTBot", "OAI-SearchBot", "ChatGPT-User"))
    got = refs.get("chatgpt.com", 0) + refs.get("chat.openai.com", 0)
    if scraped and got:
        f.append(f"OpenAI: обращений ботов — {scraped}, переходов с реферером — {got} (соотношение {scraped // got}:1)")
    elif scraped:
        f.append(f"OpenAI: обращений ботов — {scraped}, переходов с реферером нет (чтение в режиме рассуждения рефереров не оставляет)")

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print(f"Строк разобрано: {total}\n\n{'Бот':<20}{'запросов':<10}{'ошибок %':<10}назначение")
    for b in out["bots"]:
        print(f"{b['bot']:<20}{b['hits']:<10}{b['error_pct']:<10}{b['purpose']}")
    for b in out["bots"]:
        if b["purpose"] == "чтение по запросу" and b["top_paths"]:
            print(f"\nСтраницы, которые читает {b['bot']} (их спрашивают пользователи):")
            for p, n in b["top_paths"]:
                print(f"  {n:>6}  {p}")
    if refs:
        print("\nПереходы из AI-ассистентов:")
        for k, n in refs.most_common():
            print(f"  {n:>6}  {k}")
    print("\nНаходки:")
    for x in f or ["Замечаний нет"]:
        print(f"  • {x}")


if __name__ == "__main__":
    main()

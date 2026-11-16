#!/usr/bin/env python3
"""Проверка доступа AI-ботов к сайту: robots.txt и ответы сервера.

Примеры:
  python3 check_access.py https://example.com
  python3 check_access.py https://example.com/pricing --no-fetch
  python3 check_access.py https://example.com --robots-file robots.txt --json
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
import urllib.robotparser
from urllib.parse import urlparse

# (токен в robots.txt, назначение, строка User-Agent для запроса)
BOTS = [
    ("GPTBot", "обучение OpenAI", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)"),
    ("OAI-SearchBot", "поиск ChatGPT", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"),
    ("ChatGPT-User", "запрос пользователя ChatGPT", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot"),
    ("ClaudeBot", "обучение Anthropic", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"),
    ("Claude-SearchBot", "поиск Claude", "Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +https://www.anthropic.com)"),
    ("Claude-User", "запрос пользователя Claude", "Mozilla/5.0 (compatible; Claude-User/1.0; +https://www.anthropic.com)"),
    ("PerplexityBot", "поиск Perplexity", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)"),
    ("Perplexity-User", "запрос пользователя Perplexity", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)"),
    ("Google-Extended", "обучение Gemini (только токен robots.txt)", None),
    ("Googlebot", "поиск Google, AI Overviews, AI Mode", "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
    ("Bingbot", "поиск Bing, Copilot", "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"),
    ("Applebot-Extended", "обучение Apple (только токен robots.txt)", None),
    ("Meta-ExternalAgent", "Meta AI", "meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)"),
    ("Amazonbot", "Amazon", "Mozilla/5.0 (compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot)"),
    ("CCBot", "Common Crawl (обучающие наборы)", "CCBot/2.0 (https://commoncrawl.org/faq/)"),
]
RETRIEVAL = {"OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User", "PerplexityBot",
             "Perplexity-User", "Googlebot", "Bingbot"}


def http_get(url, ua, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(5_000_000)
            return r.status, len(body), body, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, 0, b"", dict(e.headers or {})
    except Exception as e:  # сеть, TLS, таймаут
        return None, 0, b"", {"error": str(e)}


def main():
    ap = argparse.ArgumentParser(description="Доступ AI-ботов: robots.txt и ответы сервера")
    ap.add_argument("url")
    ap.add_argument("--robots-file", help="локальный robots.txt вместо загрузки")
    ap.add_argument("--no-fetch", action="store_true", help="не запрашивать страницу от имени ботов")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    u = urlparse(a.url if "://" in a.url else "https://" + a.url)
    origin = f"{u.scheme}://{u.netloc}"
    target = u.geturl()
    out = {"url": target, "robots": {}, "bots": [], "sitemaps": [], "findings": []}

    if a.robots_file:
        text, status = open(a.robots_file, encoding="utf-8", errors="replace").read(), 200
    else:
        status, _, body, _ = http_get(origin + "/robots.txt", "Mozilla/5.0 (compatible; aeo-skill)")
        text = body.decode("utf-8", "replace") if status == 200 else ""
    out["robots"]["status"] = status
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    out["sitemaps"] = [l.split(":", 1)[1].strip() for l in text.splitlines() if l.lower().startswith("sitemap:")]
    named = {l.split(":", 1)[1].strip().lower() for l in text.splitlines() if l.lower().startswith("user-agent:")}

    baseline = None
    if not a.no_fetch:
        baseline = http_get(target, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
        out["browser"] = {"status": baseline[0], "bytes": baseline[1]}

    for token, purpose, ua in BOTS:
        row = {"bot": token, "purpose": purpose,
               "robots_allowed": rp.can_fetch(token, target) if text else True,
               "named_in_robots": token.lower() in named}
        if ua and not a.no_fetch:
            st, size, _, hdr = http_get(target, ua)
            row.update(status=st, bytes=size)
            if st is None:
                row["error"] = hdr.get("error")
        out["bots"].append(row)

    f = out["findings"]
    if status in (None, 403) or (status and status >= 500):
        f.append(("Критично", f"robots.txt отвечает {status}: поисковые системы могут прекратить сканирование"))
    if status == 404:
        f.append(("Низкий", "robots.txt отсутствует: сканирование разрешено всем, но нет ссылки на sitemap"))
    for r in out["bots"]:
        if not r["robots_allowed"]:
            level = "Критично" if r["bot"] in RETRIEVAL else "Средний"
            f.append((level, f"{r['bot']} ({r['purpose']}) запрещён в robots.txt"))
        st = r.get("status")
        if st in (401, 403, 429, 503) or (st is None and "status" in r):
            level = "Критично" if r["bot"] in RETRIEVAL else "Высокий"
            f.append((level, f"{r['bot']} получает {st or 'ошибку сети'}: вероятна блокировка на уровне CDN или WAF (проверь настройки Cloudflare)"))
        if baseline and baseline[1] and r.get("bytes") is not None and st == 200 and r["bytes"] < baseline[1] * 0.5:
            f.append(("Высокий", f"{r['bot']} получает {r['bytes']} байт против {baseline[1]} у браузера: возможна подмена или заглушка"))
    if not out["sitemaps"]:
        f.append(("Средний", "В robots.txt нет строки Sitemap: карта сайта — запасной канал обнаружения страниц"))
    if not f:
        f.append(("OK", "Блокировок AI-ботов не найдено"))
    f.append(("Инфо", "Запросы идут не с IP-адресов ботов: блокировки по IP и настройки CDN этим тестом не выявляются, сверяйся с логами сервера"))

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print(f"URL: {target}\nrobots.txt: HTTP {status}\nSitemap: {', '.join(out['sitemaps']) or 'не указан'}")
    if "browser" in out:
        print(f"Браузер: HTTP {out['browser']['status']}, {out['browser']['bytes']} байт")
    print(f"\n{'Бот':<20}{'robots.txt':<12}{'HTTP':<7}{'байт':<10}назначение")
    for r in out["bots"]:
        print(f"{r['bot']:<20}{'разрешён' if r['robots_allowed'] else 'ЗАПРЕЩЁН':<12}{str(r.get('status', '-')):<7}{str(r.get('bytes', '-')):<10}{r['purpose']}")
    print("\nНаходки:")
    for level, msg in f:
        print(f"  [{level}] {msg}")


if __name__ == "__main__":
    sys.exit(main())

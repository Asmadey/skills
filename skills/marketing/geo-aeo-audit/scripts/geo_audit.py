#!/usr/bin/env python3
"""GEO/AEO-аудит сайта по критериям seo_aeo_geo_playbook_v2.

Только машинно-проверяемые пункты: то, что можно подтвердить запросом к сайту,
без домыслов и без LLM. Каждая находка несёт ссылку на технику плейбука,
поэтому отчёт читается как список задач, а не как «оценка качества».

    python3 geo_audit.py --site https://popizdim.com
    python3 geo_audit.py --site https://popizdim.com --json
    python3 geo_audit.py --site https://popizdim.com --limit 12

Выход: markdown в stdout, снимок в ~/.hermes/data/seo/geo/<host>/audit-<дата>.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
           "PerplexityBot", "Google-Extended", "Applebot", "CCBot"]
SEARCH_BOTS = ["Googlebot", "YandexBot", "bingbot"]
QUESTION_START = re.compile(
    r"^(как|что|чем|почему|зачем|когда|где|кто|сколько|какой|какая|какие|можно|стоит|нужно|"
    r"how|what|why|when|where|who|which|can|should|does|is|are)\b", re.I)
BOILERPLATE_START = re.compile(
    r"^\s*(опубликовано|обновлено|дата|время чтения|оглавление|содержание|навигация|"
    r"published|updated|table of contents|breadcrumb|читать \d|min read)", re.I)
SEVERITY_WEIGHT = {"critical": 10, "high": 5, "medium": 2, "low": 1}

ACTIONS = {
    "robots_ai": "Открыть доступ AI-ботам в robots.txt: закрытый бот это невидимость в ChatGPT/Perplexity.",
    "raw_text": "Вынести текст страницы в HTML: AI-краулеры не исполняют JS.",
    "size": "Урезать страницу до 4 МБ: большее LLM отвергает целиком.",
    "orphans": "Связать страницы HTML-ссылками, чтобы они были не дальше двух кликов от главной.",
    "h1": "Оставить ровно один h1 на страницу.",
    "internal_links": "Добавить в HTML ссылки на соседние страницы кластера.",
    "answer_first": "Поставить ответ сразу после h1, служебные блоки убрать ниже.",
    "question_h2": "Переформулировать часть h2 как вопросы: такие пассажи цитируются вдвое чаще.",
    "canonical": "Привести canonical к собственному URL.",
    "schema": "Добавить JSON-LD с типом страницы.",
    "schema_type": "Дополнить JSON-LD типом страницы (WebPage/Article).",
    "sameas": "Добавить в Organization sameAs на Wikidata, LinkedIn, GitHub.",
    "meta_description": "Заполнить meta description.",
    "date_modified": "Отдавать dateModified в JSON-LD: свежесть это сигнал доверия для AI.",
    "cluster_links": "Связать статью с соседями по кластеру двусторонними ссылками.",
    "img_alt": "Проставить атрибут alt всем изображениям.",
    "img_alt_empty": "Заполнить alt содержательным текстом: по нему AI понимает картинку.",
    "img_format": "Перевести изображения в webp/avif.",
    "table": "Добавить HTML-таблицу сравнения: она цитируется чаще любого текста.",
    "noindex": "Убрать noindex из HTML, иначе страница не попадёт в индекс.",
    "lang": "Указать lang у <html>.",
    "robots_sitemap": "Добавить директиву Sitemap в robots.txt.",
    "sitemap": "Починить sitemap: без него теряется резервный канал дискавери.",
    "http": "Починить HTTP-статус страницы.",
    "title": "Заполнить title самодостаточной фразой.",
    "title_len": "Сократить title.",
}


class PageParser(HTMLParser):
    """Достаёт из raw HTML ровно то, что видит краулер без исполнения JS."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.h1: list[str] = []
        self.h2: list[str] = []
        self.h3: list[str] = []
        self.links: list[str] = []
        self.images: list[tuple[str, str, bool]] = []
        self.jsonld: list[str] = []
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.lang = ""
        self.tables = 0
        self._text: list[str] = []
        self._after_h1: list[str] = []
        self._after_h1_on = False
        self._heading: str | None = None
        self._hbuf: list[str] = []
        self._seen_h1 = False
        self._skip = 0
        self._in_title = False
        self._in_jsonld = False
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):  # noqa: C901
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self._skip += 1
            if tag == "script" and a.get("type") == "application/ld+json":
                self._in_jsonld = True
                self._buf = []
            return
        if tag == "title":
            self._in_title = True
        elif tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "link" and "canonical" in (a.get("rel") or ""):
            self.canonical = a.get("href", "")
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name:
                self.meta[name] = a.get("content", "")
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            width = a.get("width") or ""
            self.images.append((a.get("src", ""), a.get("alt", ""), "alt" in a, str(width),
                                a.get("class") or ""))
        elif tag == "table":
            self.tables += 1
        elif tag in ("h1", "h2", "h3"):
            self._heading = tag
            self._hbuf = []
            if tag == "h1":
                self._seen_h1 = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = max(0, self._skip - 1)
            if tag == "script" and self._in_jsonld:
                self.jsonld.append("".join(self._buf))
                self._in_jsonld = False
            return
        if tag == "title":
            self._in_title = False
            return
        if tag in ("h1", "h2", "h3") and tag == self._heading:
            text = " ".join(self._hbuf).strip()
            {"h1": self.h1, "h2": self.h2, "h3": self.h3}[tag].append(text)
            self._heading = None
            self._hbuf = []
            if tag == "h1":
                self._after_h1_on = True

    def handle_data(self, data):
        if self._in_jsonld:
            self._buf.append(data)
            return
        if self._in_title:
            self.title += data
            return
        if self._skip:
            return
        text = data.strip()
        if not text:
            return
        if self._heading:
            self._hbuf.append(text)
            self._text.append(text)
            return
        self._text.append(text)
        if self._after_h1_on and len(self._after_h1) < 60:
            self._after_h1.append(text)

    @property
    def text(self) -> str:
        return " ".join(self._text)

    @property
    def after_h1(self) -> str:
        return " ".join(self._after_h1)[:400]


def fetch(url: str, ua: str = BROWSER_UA, timeout: int = 30) -> tuple[int, bytes, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "ru,en;q=0.9"},
                                 method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:2000], dict(e.headers or {})
    except Exception as e:  # noqa: BLE001
        return 0, str(e).encode(), {}


def robots_rules(text: str) -> dict[str, list[str]]:
    rules: dict[str, list[str]] = {}
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip().lower(), val.strip()
        if key == "user-agent":
            current = [val.lower()]
            rules.setdefault(val.lower(), [])
        elif key == "disallow" and current:
            for agent in current:
                rules.setdefault(agent, []).append(val)
    return rules


def blocked(rules: dict[str, list[str]], bot: str) -> bool:
    disallow = rules.get(bot.lower(), [])
    return any(rule == "/" for rule in disallow)


def sitemap_urls(site: str, limit: int) -> tuple[list[str], str]:
    status, body, _ = fetch(site.rstrip("/") + "/sitemap.xml")
    if status != 200:
        return [], f"sitemap.xml → HTTP {status}"
    xml = body.decode("utf-8", "replace")
    urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if any(u.endswith(".xml") for u in urls):  # sitemap index
        collected: list[str] = []
        for sub in urls:
            s2, b2, _ = fetch(sub)
            if s2 == 200:
                collected += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", b2.decode("utf-8", "replace"))
        urls = collected
    return urls[:limit] if limit else urls, f"{len(urls)} URL"


def schema_types(blobs: list[str]) -> list[str]:
    found: list[str] = []
    for blob in blobs:
        try:
            data = json.loads(blob)
        except Exception:  # noqa: BLE001
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                t = node.get("@type")
                if isinstance(t, str):
                    found.append(t)
                elif isinstance(t, list):
                    found += [x for x in t if isinstance(x, str)]
                stack += [v for v in node.values() if isinstance(v, (dict, list))]
            elif isinstance(node, list):
                stack += [v for v in node if isinstance(v, (dict, list))]
    return found


def audit_page(url: str) -> dict:
    status, body, headers = fetch(url)
    html = body.decode("utf-8", "replace")
    p = PageParser()
    try:
        p.feed(html)
    except Exception:  # noqa: BLE001
        pass
    internal = []
    host = urllib.parse.urlparse(url).netloc
    for href in p.links:
        if href.startswith(("http://", "https://")):
            if urllib.parse.urlparse(href).netloc == host:
                internal.append(href)
        elif href.startswith("/"):
            internal.append(href)
    def decorative(img: tuple) -> bool:
        """alt="" у иконки или превью-карточки рядом с подписью это норма."""
        if img[1].strip() or not img[2]:
            return False
        cls = img[4].lower()
        if "ico" in cls or "card-img" in cls or "icon" in cls:
            return True
        try:
            return 0 < int(float(img[3])) <= 80
        except (TypeError, ValueError):
            return False

    alt_ok = [i for i in p.images if i[1].strip()]
    alt_attr = [i for i in p.images if i[2]]
    decorative_n = len([i for i in p.images if decorative(i)])
    modern = [i for i in p.images if re.search(r"\.(webp|avif|svg)(\?|$)", i[0], re.I)]
    h2q = [h for h in p.h2 if h.strip().endswith("?") or QUESTION_START.match(h.strip())]
    text = p.text
    return {
        "url": url,
        "status": status,
        "bytes": len(body),
        "title": p.title.strip(),
        "canonical": p.canonical,
        "lang": p.lang,
        "robots_meta": p.meta.get("robots", ""),
        "h1": p.h1,
        "h2_count": len(p.h2),
        "h2_questions": h2q,
        "h3_count": len(p.h3),
        "words_raw": len(text.split()),
        "after_h1": p.after_h1[:220],
        "internal_links": len(internal),
        "internal_targets": internal,
        "images": len(p.images),
        "images_alt": len(alt_ok),
        "images_alt_attr": len(alt_attr),
        "images_decorative": decorative_n,
        "images_modern": len(modern),
        "tables": p.tables,
        "schema": sorted(set(schema_types(p.jsonld))),
        "jsonld_blocks": len(p.jsonld),
        "has_speakable": "SpeakableSpecification" in " ".join(schema_types(p.jsonld)),
        "schema_raw": " ".join(p.jsonld),
        "has_sameas": '"sameAs"' in " ".join(p.jsonld),
        "has_date_modified": '"dateModified"' in " ".join(p.jsonld),
        "description": p.meta.get("description", ""),
    }


def checks(page: dict, host: str, all_urls: list[str], site: str) -> list[dict]:
    out: list[dict] = []
    u = page["url"]

    def add(cid, sev, msg, tech):
        out.append({"id": cid, "severity": sev, "url": u, "message": msg, "technique": tech})

    if page["status"] != 200:
        add("http", "critical", f"HTTP {page['status']}", "1.5")
        return out
    if page["bytes"] > 4 * 1024 * 1024:
        add("size", "critical", f"страница {page['bytes'] // 1024} КБ > 4 МБ: LLM отвергает целиком", "1.5")
    if page["words_raw"] < 150:
        add("raw_text", "critical", f"в raw HTML {page['words_raw']} слов: контент зависит от JS", "1.1/1.12")
    if not page["title"]:
        add("title", "high", "нет <title>", "1.4")
    elif len(page["title"]) > 120:
        add("title_len", "low", f"title {len(page['title'])} символов", "1.4")
    if len(page["h1"]) != 1:
        add("h1", "high", f"заголовков h1: {len(page['h1'])}", "13.2")
    if page["canonical"] and page["canonical"].rstrip("/") != u.rstrip("/"):
        add("canonical", "high", f"canonical ведёт на {page['canonical']}", "1.11")
    if BOILERPLATE_START.match(page["after_h1"]):
        add("answer_first", "high", "после h1 сначала служебный блок, а не ответ", "1.3/2.4")
    if page["internal_links"] < 3:
        add("internal_links", "high", f"внутренних ссылок в HTML: {page['internal_links']}", "1.2/2.7")
    if page["h2_count"] >= 4 and not page["h2_questions"]:
        add("question_h2", "medium", "ни один h2 не сформулирован вопросом", "2.1/2.10")
    meaningful = page["images"] - page["images_decorative"]
    if meaningful > 0 and page["images_alt_attr"] < page["images"]:
        missing = page["images"] - page["images_alt_attr"]
        add("img_alt", "medium", f"без атрибута alt {missing} из {page['images']}", "14.2")
    elif meaningful > 0 and page["images_alt"] / meaningful < 0.5:
        add("img_alt_empty", "low",
            f"alt пустой у {meaningful - page['images_alt']} смысловых картинок из {meaningful}", "14.2")
    if page["images"] and page["images_modern"] / page["images"] < 0.8:
        add("img_format", "low", f"webp/avif у {page['images_modern']} из {page['images']}", "1.9")
    if re.search(r"лучше|сравн|\bvs\b|против", page["title"].lower()) and page["tables"] == 0:
        add("table", "medium", "сравнительная страница без HTML-таблицы", "2.6")
    if page["robots_meta"] and "noindex" in page["robots_meta"].lower():
        add("noindex", "critical", f"noindex в HTML: {page['robots_meta']}", "1.13")
    if "/blog/" in u and page["internal_targets"]:
        others = [t for t in page["internal_targets"] if "/blog/" in t and t.rstrip("/") != u.rstrip("/")]
        if not others:
            add("cluster_links", "medium", "в статье нет ссылок на другие статьи кластера", "2.7")
    page_types = {"Article", "BlogPosting", "NewsArticle", "WebPage", "CollectionPage",
                  "ContactPage", "AboutPage", "FAQPage", "Product", "Service",
                  "SoftwareApplication", "Organization", "ItemList", "ItemPage"}
    if not page["schema"]:
        add("schema", "high", "нет JSON-LD", "5.1")
    elif not (page_types & set(page["schema"])):
        add("schema_type", "medium", f"типы: {', '.join(page['schema'])} — нет типа страницы", "5.1")
    if not page["description"]:
        add("meta_description", "medium", "нет meta description", "1.4")
    if not page["lang"]:
        add("lang", "low", "у <html> нет атрибута lang", "13.2")
    if "/blog/" in u and not page["has_date_modified"]:
        add("date_modified", "medium", "в JSON-LD нет dateModified: AI не видит свежесть", "4.6")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--limit", type=int, default=0, help="проверить не больше N страниц")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out-dir", default="")
    args = ap.parse_args()

    site = args.site.rstrip("/")
    host = urllib.parse.urlparse(site).netloc
    findings: list[dict] = []
    notes: list[str] = []

    r_status, r_body, _ = fetch(site + "/robots.txt")
    r_text = r_body.decode("utf-8", "replace") if r_status == 200 else ""
    rules = robots_rules(r_text)
    for bot in AI_BOTS:
        if blocked(rules, bot):
            findings.append({"id": "robots_ai", "severity": "critical", "url": site + "/robots.txt",
                             "message": f"{bot} заблокирован в robots.txt", "technique": "1.6"})
    if "sitemap" not in r_text.lower():
        findings.append({"id": "robots_sitemap", "severity": "low", "url": site + "/robots.txt",
                         "message": "в robots.txt нет директивы Sitemap", "technique": "1.10"})

    urls, smap_note = sitemap_urls(site, args.limit)
    notes.append(f"sitemap: {smap_note}")
    if not urls:
        findings.append({"id": "sitemap", "severity": "critical", "url": site + "/sitemap.xml",
                         "message": "sitemap не найден или пуст", "technique": "1.10"})

    home = audit_page(site + "/")
    pages = [home] + [audit_page(u) for u in urls if u.rstrip("/") != site]

    # сироты: достижимы ли страницы из sitemap по raw-ссылкам с главной
    reachable = {site + "/", home["url"]}
    frontier = [site + "/"]
    for _ in range(2):
        nxt: list[str] = []
        for link in frontier:
            page = next((p for p in pages if p["url"].rstrip("/") == link.rstrip("/")), None)
            if not page:
                continue
            for target in page["internal_targets"]:
                full = urllib.parse.urljoin(site, target).split("#")[0].rstrip("/")
                if full not in reachable:
                    reachable.add(full)
                    nxt.append(full)
        frontier = nxt
    orphans = [u for u in urls if u.rstrip("/") not in reachable and u.rstrip("/") != site]
    if orphans:
        findings.append({"id": "orphans", "severity": "high", "url": site,
                         "message": f"страниц недостижимых за 2 клика от главной: {len(orphans)} "
                                    f"({', '.join(urllib.parse.urlparse(o).path for o in orphans[:5])})",
                         "technique": "1.2"})

    for page in pages:
        findings += checks(page, host, urls, site)

    if "Organization" in home["schema"] and not home["has_sameas"]:
        findings.append({"id": "sameas", "severity": "medium", "url": site + "/",
                         "message": "Organization без sameAs: AI не связывает бренд с внешними узлами",
                         "technique": "4.2"})

    # score: штраф за затронутую долю страниц по каждой проверке
    by_id: dict[str, list[dict]] = {}
    for f in findings:
        by_id.setdefault(f["id"], []).append(f)
    total_pages = max(1, len(pages))
    penalty = 0.0
    for cid, items in by_id.items():
        share = min(1.0, len(items) / total_pages) if items[0]["url"] != site else 1.0
        penalty += SEVERITY_WEIGHT[items[0]["severity"]] * share
    score = max(0, round(100 - penalty))

    report = {
        "site": site,
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "score": score,
        "pages": len(pages),
        "sitemap_urls": len(urls),
        "notes": notes,
        "findings": findings,
        "page_rows": [{k: p[k] for k in ("url", "status", "words_raw", "h2_count", "h2_questions",
                                         "internal_links", "images", "images_alt", "schema")}
                      for p in pages],
    }

    out_dir = Path(args.out_dir) if args.out_dir else Path(
        os.environ.get("GEO_AUDIT_DIR", Path.home() / ".geo-audit")) / host
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    (out_dir / f"audit-{stamp}.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
    (out_dir / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                         encoding="utf-8")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    label = {"critical": "КРИТИЧНО", "high": "ВАЖНО", "medium": "СРЕДНЕ", "low": "НИЗКО"}
    print(f"# GEO/AEO аудит {site}\n")
    print(f"Оценка: **{score}/100**. Страниц проверено: {len(pages)}. {smap_note}.\n")
    grouped: dict[str, list[dict]] = {}
    for f in sorted(findings, key=lambda x: (order[x["severity"]], x["id"])):
        grouped.setdefault(f["severity"], []).append(f)
    for sev in ("critical", "high", "medium", "low"):
        items = grouped.get(sev, [])
        if not items:
            continue
        print(f"## {label[sev]} ({len(items)})\n")
        for f in items[:12]:
            path = urllib.parse.urlparse(f["url"]).path or "/"
            print(f"- `{path}` {f['message']}  _(плейбук §{f['technique']})_")
        if len(items) > 12:
            print(f"- …и ещё {len(items) - 12}")
        print()
    if not findings:
        print("Находок нет: машинно-проверяемые пункты плейбука выполнены.\n")
    else:
        print("## Что делать (по убыванию отдачи)\n")
        for cid, items in sorted(by_id.items(),
                                 key=lambda kv: (order[kv[1][0]["severity"]], -len(kv[1]))):
            action = ACTIONS.get(cid, items[0]["message"])
            pages_hit = len({urllib.parse.urlparse(i["url"]).path or "/" for i in items})
            print(f"- **{label[items[0]['severity']]}**, страниц: {pages_hit}. {action} "
                  f"_(§{items[0]['technique']})_")
        print()
    print("## Страницы\n")
    print("| путь | HTTP | слов в HTML | h2 | из них вопросов | ссылок | alt | schema |")
    print("|---|---|---|---|---|---|---|---|")
    for p in pages:
        path = urllib.parse.urlparse(p["url"]).path or "/"
        print(f"| {path} | {p['status']} | {p['words_raw']} | {p['h2_count']} | "
              f"{len(p['h2_questions'])} | {p['internal_links']} | "
              f"{p['images_alt']}/{p['images']} | {', '.join(p['schema'][:3]) or '—'} |")
    print(f"\nСнимок: {out_dir / f'audit-{stamp}.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

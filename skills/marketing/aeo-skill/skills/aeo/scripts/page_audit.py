#!/usr/bin/env python3
"""Страница глазами AI-бота: сырой HTML без исполнения JavaScript и разбор пассажей.

Примеры:
  python3 page_audit.py https://example.com/guide
  python3 page_audit.py --file page.html --brand "Acme" --json
"""
import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "template", "svg", "iframe"}
HEAD = {"h1", "h2", "h3", "h4"}
BLOCK = {"p", "li", "td", "th", "div", "section", "article", "br", "tr", "blockquote", "dd", "dt"} | HEAD
DEPENDENT = re.compile(
    r"как (?:упоминалось|сказано|отмечалось|описано) (?:выше|ранее)|см\. выше|вышеупомянут|как мы уже|"
    r"as (?:mentioned|noted|discussed|described) (?:above|earlier|previously)|see above|aforementioned", re.I)
PRONOUN_START = re.compile(r"^(?:это|он|она|оно|они|этот|эта|эти|такой|данный|it|this|that|they|these|those)\b", re.I)
FILLER_START = re.compile(
    r"^(?:в этой (?:статье|секции|главе)|в этом разделе|давайте|сегодня мы|прежде чем|итак|"
    r"in this (?:article|section|guide|post)|let's|before we|when it comes to|in today's)", re.I)
QUESTION = re.compile(r"\?\s*$|^(?:что|как|почему|зачем|когда|где|сколько|какой|какая|какие|кто|чем|можно ли|нужно ли|"
                      r"what|how|why|when|where|which|who|can|should|is|are|does|do)\b", re.I)
NOISE_AFTER_H1 = re.compile(r"\b\d{1,2}[./]\d{1,2}[./]\d{2,4}\b|\b(?:мин(?:ут)? чтения|min read|главная\s*[/›»>]|home\s*[/›»>]|"
                            r"содержание|оглавление|table of contents|опубликовано|обновлено|published|updated|автор:|by )", re.I)


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.cur = None            # текущий заголовок
        self.buf = []
        self.blocks = []           # (тип, текст)
        self.title = ""
        self.in_title = False
        self.meta = {}
        self.canonical = None
        self.links = 0
        self.imgs = 0
        self.imgs_noalt = 0
        self.tables = 0
        self.lists = 0
        self.jsonld = []
        self.in_ld = False
        self.ld_buf = []
        self.scripts = 0
        self.landmarks = set()
        self.lang = None

    def flush(self, kind="p"):
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        if t:
            self.blocks.append((kind, t))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "script":
            self.scripts += 1
            if (a.get("type") or "").lower() == "application/ld+json":
                self.in_ld, self.ld_buf = True, []
        if tag in SKIP:
            self.skip += 1
            return
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            k = (a.get("name") or a.get("property") or "").lower()
            if k:
                self.meta[k] = a.get("content") or ""
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = a.get("href")
        elif tag == "a" and a.get("href") and not a["href"].startswith(("#", "javascript:")):
            self.links += 1
        elif tag == "img":
            self.imgs += 1
            if not (a.get("alt") or "").strip():
                self.imgs_noalt += 1
        elif tag == "table":
            self.tables += 1
        elif tag in ("ul", "ol"):
            self.lists += 1
        if tag in ("main", "article", "nav", "header", "footer", "aside") or a.get("role"):
            self.landmarks.add(a.get("role") or tag)
        if tag in BLOCK and not self.skip:
            self.flush(self.cur or "p")
            self.cur = tag if tag in HEAD else None

    def handle_endtag(self, tag):
        if tag == "script" and self.in_ld:
            self.in_ld = False
            self.jsonld.append("".join(self.ld_buf))
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "title":
            self.in_title = False
        if tag in BLOCK:
            self.flush(self.cur or "p")
            self.cur = None

    def handle_data(self, data):
        if self.in_ld:
            self.ld_buf.append(data)
        elif self.in_title:
            self.title += data
        elif not self.skip:
            self.buf.append(data)


def ld_types(raw_blocks):
    types, same_as, errors = [], [], 0

    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if t:
                types.extend(t if isinstance(t, list) else [t])
            s = o.get("sameAs")
            if s:
                same_as.extend(s if isinstance(s, list) else [s])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for raw in raw_blocks:
        try:
            walk(json.loads(raw))
        except Exception:
            errors += 1
    return sorted(set(map(str, types))), sorted(set(map(str, same_as))), errors


def words(t):
    return re.findall(r"[\w'-]+", t, re.U)


def first_sentence(t):
    return re.split(r"(?<=[.!?…])\s+", t.strip(), maxsplit=1)[0]


def analyze(html, brand=None):
    d = Doc()
    d.feed(html)
    d.flush()
    size = len(html.encode("utf-8"))
    text_blocks = [t for k, t in d.blocks if k == "p"]
    total_words = sum(len(words(t)) for t in text_blocks)
    h1 = [t for k, t in d.blocks if k == "h1"]
    types, same_as, ld_err = ld_types(d.jsonld)

    # текст сразу после первого H1
    lede, seen = "", False
    for k, t in d.blocks:
        if k == "h1" and not seen:
            seen = True
            continue
        if seen and k == "p":
            lede = (lede + " " + t).strip()
            if len(lede) >= 200:
                break
        elif seen and k in HEAD and lede:
            break
    lede200 = lede[:200]

    # секции по H2/H3
    sections, cur = [], None
    for k, t in d.blocks:
        if k in ("h2", "h3"):
            cur = {"heading": t, "level": k, "text": []}
            sections.append(cur)
        elif k == "p" and cur is not None:
            cur["text"].append(t)
    passages = []
    for s in sections:
        body = " ".join(s["text"])
        wc = len(words(body))
        if wc < 15:
            continue
        fs = first_sentence(body)
        issues = []
        if DEPENDENT.search(body):
            issues.append("ссылается на другой фрагмент страницы")
        if PRONOUN_START.match(fs):
            issues.append("первое предложение начинается с местоимения: назови сущность явно")
        if FILLER_START.match(fs):
            issues.append("вступление вместо ответа")
        if len(words(fs)) > 40:
            issues.append(f"первое предложение {len(words(fs))} слов: ответ не помещается в начало")
        if wc > 300:
            issues.append(f"{wc} слов в секции: раздели на пассажи по 80–150 слов")
        passages.append({"heading": s["heading"], "question_heading": bool(QUESTION.search(s["heading"])),
                         "words": wc, "first_sentence": fs[:220], "issues": issues})

    n = len(passages) or 1
    stats = {
        "bytes": size, "words_in_raw_html": total_words, "scripts": d.scripts, "links_in_raw_html": d.links,
        "title": d.title.strip(), "title_chars": len(d.title.strip()), "h1": h1,
        "meta_description": d.meta.get("description", ""), "meta_robots": d.meta.get("robots", ""),
        "canonical": d.canonical, "lang": d.lang, "lede_200": lede200,
        "images": d.imgs, "images_without_alt": d.imgs_noalt, "tables": d.tables, "lists": d.lists,
        "jsonld_blocks": len(d.jsonld), "jsonld_types": types, "same_as": same_as, "jsonld_errors": ld_err,
        "landmarks": sorted(d.landmarks),
        "passages": len(passages),
        "question_headings_pct": round(100 * sum(p["question_heading"] for p in passages) / n),
        "clean_passages_pct": round(100 * sum(not p["issues"] for p in passages) / n),
        "median_passage_words": sorted(p["words"] for p in passages)[len(passages) // 2] if passages else 0,
    }

    f = []
    if size > 4_000_000:
        f.append(("Критично", f"HTML {size / 1e6:.1f} МБ: страницы тяжелее ~4 МБ ChatGPT отклоняет целиком", "S002"))
    if total_words < 150 and d.scripts >= 3:
        f.append(("Критично", f"В сыром HTML {total_words} слов при {d.scripts} скриптах: контент, вероятно, рисуется JavaScript и не виден AI-ботам", "S001"))
    elif total_words < 150:
        f.append(("Высокий", f"В сыром HTML всего {total_words} слов", "S006"))
    if d.links < 5:
        f.append(("Высокий", f"В сыром HTML {d.links} ссылок: внутренние ссылки, добавленные скриптами, боты не находят", "S001"))
    if "noindex" in stats["meta_robots"].lower():
        f.append(("Критично", "meta robots содержит noindex", "S074"))
    if len(h1) != 1:
        f.append(("Средний", f"H1 на странице: {len(h1)} (нужен один)", "S077"))
    if not stats["title"]:
        f.append(("Высокий", "Нет title", "S002"))
    elif len(words(stats["title"])) < 4:
        f.append(("Средний", "Title слишком короткий, чтобы быть самодостаточным описанием страницы", "S002"))
    if not lede200:
        f.append(("Высокий", "После H1 нет текста в сыром HTML: быстрый режим ChatGPT видит только title и ~200 символов", "S002"))
    elif NOISE_AFTER_H1.search(lede200):
        f.append(("Высокий", "Первые 200 символов после H1 заняты датой, хлебными крошками или оглавлением вместо ключевой мысли", "S002"))
    elif FILLER_START.match(lede200):
        f.append(("Средний", "Текст после H1 начинается со вступления, а не с ответа", "S017"))
    if brand and brand.lower() not in (stats["title"] + " " + lede + " ".join(text_blocks[:5])).lower():
        f.append(("Средний", f"Бренд «{brand}» не назван в title и начале страницы: высок риск цитаты без упоминания", "S022"))
    if passages:
        if stats["clean_passages_pct"] < 70:
            f.append(("Высокий", f"Только {stats['clean_passages_pct']}% секций самодостаточны и начинаются с ответа (ориентир — 85%)", "S003"))
        if stats["question_headings_pct"] < 30:
            f.append(("Средний", f"Заголовков-вопросов {stats['question_headings_pct']}%: пассажи под вопросом переиспользуются вдвое чаще", "S003"))
    else:
        f.append(("Высокий", "Нет секций с H2/H3 и текстом: модели нечего извлекать по частям", "S016"))
    if d.tables == 0 and total_words > 600:
        f.append(("Низкий", "Нет HTML-таблиц: сравнения в таблицах цитируются чаще", "S004"))
    if d.imgs and d.imgs_noalt / d.imgs > 0.3:
        f.append(("Средний", f"{d.imgs_noalt} из {d.imgs} изображений без alt: alt — единственное, что остаётся от картинки в кеше ChatGPT", "S002"))
    if not d.jsonld:
        f.append(("Средний", "Нет JSON-LD в сыром HTML (гигиена сущности, не рычаг цитируемости)", "S011"))
    elif ld_err:
        f.append(("Средний", f"{ld_err} блок(ов) JSON-LD не разбираются как JSON", "S006"))
    if d.jsonld and not same_as and any(t in types for t in ("Organization", "LocalBusiness", "Corporation", "Person")):
        f.append(("Низкий", "В разметке организации нет sameAs на внешние профили", "S027"))
    if "main" not in d.landmarks:
        f.append(("Низкий", "Нет элемента <main>: агентам сложнее выделить основной контент в дереве доступности", "S077"))
    return {"stats": stats, "findings": f, "passages": passages}


def main():
    ap = argparse.ArgumentParser(description="Страница глазами AI-бота")
    ap.add_argument("url", nargs="?")
    ap.add_argument("--file")
    ap.add_argument("--brand")
    ap.add_argument("--ua", default="Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.file:
        html = open(a.file, encoding="utf-8", errors="replace").read()
    elif a.url:
        req = urllib.request.Request(a.url, headers={"User-Agent": a.ua})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                html = r.read(6_000_000).decode(r.headers.get_content_charset() or "utf-8", "replace")
        except Exception as e:
            sys.exit(f"Не удалось загрузить {a.url}: {e}\nСохрани HTML в файл и передай через --file.")
    else:
        ap.error("нужен url или --file")
    res = analyze(html, a.brand)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    s = res["stats"]
    print(f"Размер HTML: {s['bytes']} байт | слов в сыром HTML: {s['words_in_raw_html']} | ссылок: {s['links_in_raw_html']} | скриптов: {s['scripts']}")
    print(f"Title ({s['title_chars']} симв.): {s['title']}")
    print(f"H1: {' | '.join(s['h1']) or '—'}")
    print(f"Первые 200 символов после H1: {s['lede_200'] or '—'}")
    print(f"JSON-LD: {', '.join(s['jsonld_types']) or 'нет'} | sameAs: {len(s['same_as'])} | таблиц: {s['tables']} | изображений без alt: {s['images_without_alt']}/{s['images']}")
    print(f"Пассажей: {s['passages']} | медиана слов: {s['median_passage_words']} | заголовков-вопросов: {s['question_headings_pct']}% | без замечаний: {s['clean_passages_pct']}%")
    print("\nНаходки:")
    for level, msg, src in res["findings"] or [("OK", "Замечаний нет", "")]:
        print(f"  [{level}] {msg} {('[' + src + ']') if src else ''}")
    bad = [p for p in res["passages"] if p["issues"]]
    if bad:
        print("\nПассажи с замечаниями:")
        for p in bad[:15]:
            print(f"  • {p['heading'][:70]} ({p['words']} сл.): {'; '.join(p['issues'])}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Language-independent numeric signature extraction (shared by AEO claim pipeline)."""

import re

NUM_RE = re.compile(r"(\d[\d,]*\.?\d*)\s*([\-]?[A-Za-z%А-Яа-я][A-Za-zА-Яа-я\-%]{0,20})?")

UNIT_MAP = {
    "%": "pct", "percent": "pct", "процент": "pct", "процента": "pct", "процентов": "pct",
    "characters": "chars", "character": "chars", "chars": "chars", "символов": "chars",
    "символа": "chars", "символ": "chars",
    "pages": "pages", "page": "pages", "страниц": "pages", "страницы": "pages",
    "sites": "sites", "site": "sites", "сайтов": "sites", "сайта": "sites",
    "urls": "urls", "url": "urls", "ссылок": "urls",
    "mb": "mb", "kb": "kb", "gb": "gb", "ms": "ms",
    "seconds": "sec", "second": "sec", "секунд": "sec",
    "days": "days", "day": "days", "дней": "days", "дня": "days",
    "weeks": "weeks", "week": "weeks", "недель": "weeks", "недели": "weeks",
    "months": "months", "month": "months", "месяцев": "months", "месяца": "months",
    "years": "years", "year": "years", "лет": "years", "года": "years",
    "queries": "queries", "query": "queries", "запросов": "queries", "запроса": "queries",
    "words": "words", "word": "words", "слов": "words", "слова": "words",
    "tokens": "tokens", "token": "tokens", "токенов": "tokens",
    "clicks": "clicks", "click": "clicks", "кликов": "clicks",
    "impressions": "impressions", "показов": "impressions",
    "times": "times", "раз": "times",
    "citations": "citations", "citation": "citations", "цитирований": "citations",
    "referrals": "referrals", "visits": "visits", "sessions": "sessions",
    "searches": "searches", "search": "searches",
    "results": "results", "result": "results", "snippets": "snippets", "snippet": "snippets",
    "brands": "brands", "brand": "brands", "products": "products", "product": "products",
    "keywords": "keywords", "keyword": "keywords", "links": "links", "link": "links",
    "domains": "domains", "domain": "domains", "bots": "bots", "bot": "bots",
    "prompts": "prompts", "prompt": "prompts", "crawls": "crawls", "crawl": "crawls",
    "users": "users", "user": "users", "respondents": "respondents",
    "companies": "companies", "websites": "sites", "articles": "articles",
}

# units trustworthy enough for cross-lingual comparison
STRONG = {"pct", "chars", "pages", "sites", "urls", "mb", "kb", "gb", "ms", "sec",
          "days", "weeks", "months", "years", "queries", "words", "tokens", "clicks",
          "impressions", "times", "citations", "referrals", "searches", "results",
          "snippets", "brands", "products", "keywords", "links", "domains", "visits"}

STOP_UNIT_WORDS = {"and", "or", "of", "in", "to", "the", "a", "an", "is", "was", "were",
                   "и", "в", "на", "с", "для", "по"}


def sig(text, strong_only=False):
    """Return ['<value>|<unit_class>'] signatures. Weak units prefixed with '~'."""
    out = []
    for m in NUM_RE.finditer(text):
        raw = m.group(1).replace(",", "").rstrip(".")
        try:
            val = float(raw)
        except ValueError:
            continue
        w = (m.group(2) or "").lower().strip("-")
        cls = UNIT_MAP.get(w)
        if cls:
            out.append(f"{val:g}|{cls}")
        elif w and w not in STOP_UNIT_WORDS:
            if not strong_only:
                out.append(f"{val:g}|~{w}")
        elif not strong_only:
            out.append(f"{val:g}|bare")
    return out


def strong(signatures):
    return {s for s in signatures if not s.endswith("|bare") and "|~" not in s
            and s.split("|")[1] in STRONG}

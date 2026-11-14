#!/usr/bin/env python3
"""Deterministic claim extractor: SearchEngineLand corpus vs AEO/GEO playbook blocks.

No LLM. Two gates:
  1. topic scope  - claim must concern AI search (AEO/GEO) vocabulary
  2. novelty      - claim's numeric/entity signature compared with playbook blocks

Verdicts:
  DUPLICATE          article cited by block AND signature overlaps that block
  REFINES            signature overlaps an existing block (>=2 shared numbers) but article not cited
  NEW                nothing comparable in the playbook
  REVIEW_NUMERIC     same entity + same unit class as a block but different value
                     -> needs LLM adjudication before it can count as a contradiction

Output: ~/.hermes/data/aeo-claims/claims.jsonl + report.md
"""
import json, os, re, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aeo_numbers import sig as num_sig, strong as strong_sig
from collections import Counter, defaultdict

DATA = os.path.expanduser("~/.hermes/data/aeo-claims")
BLOCKS = os.path.join(DATA, "blocks.json")
SLUGS = os.path.join(DATA, "playbook_source_slugs.json")
CORPUS = "/home/hermes/searchengineland_articles_consolidated.json"
OUT_CLAIMS = os.path.join(DATA, "claims.jsonl")
OUT_REPORT = os.path.join(DATA, "report.md")

# topic scope: AI search only. Deliberately narrow - this pipeline feeds AEO/GEO skills.
SCOPE_RE = re.compile(
    r"(?i)\b(ai overviews?|ai mode|aeo\b|geo\b|generative engine|answer engine|"
    r"chatgpt|gptbot|oai-searchbot|claude|claudebot|perplexity|gemini|copilot|grok|deepseek|"
    r"llms\.txt|large language model|llm[s]?\b|ai search|ai visibility|ai citation|"
    r"ai mention|aio\b|retrieval|rag\b|grounding|ai-generated|generative search|"
    r"zero-click|brand visibility in ai)")

SYSTEMS = ["Google AI Overview", "AI Overview", "AI Mode", "ChatGPT", "GPTBot", "OAI-SearchBot",
           "ClaudeBot", "Claude", "PerplexityBot", "Perplexity", "Gemini", "Copilot", "Grok",
           "DeepSeek", "Bing", "Googlebot", "Reddit", "llms.txt", "MCP", "IndexNow", "Yelp"]

STUDY_RE = re.compile(r"(?i)\b(study|experiment|tested|test of|analysis of|survey|dataset|"
                      r"sample of|crawl(?:ed)? logs?|we (?:tracked|analyzed|measured|tested)|n\s*=\s*\d)")
FIRSTPARTY_RE = re.compile(r"(?i)\b(google (?:said|says|confirmed|announced|told|updated|documented)|"
                           r"openai (?:said|says|confirmed|announced|told)|"
                           r"microsoft (?:said|says|confirmed)|according to (?:google|openai|microsoft)|"
                           r"spokesperson|official (?:blog|docs|documentation|post)|patent)")
CASE_RE = re.compile(r"(?i)\b(case study|our (?:client|site|test)|we (?:saw|found|gained|lost)|"
                     r"(?:increase|decrease|grew|declined|rose|dropped) (?:from|by))")

def clean(text):
    t = text
    t = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", t)
    t = re.sub(r"(?i)\b(table of contents|back to top|advertisement|share this|"
               r"add searchengineland to your google news feed|post a comment|"
               r"related reading|subscribe to)\b[^\n]{0,120}", " ", t)
    t = re.sub(r"(?im)^\s*(published|updated|read time|image|photo|getty|opinion|"
               r"by [A-Z][^\n]{0,60}\s*$).*$", " ", t)
    t = re.sub(r"(?i)published:\s*[^\n]{0,60}|read time:\s*\d+\s*minutes?|"
               r"[a-z]+ \d{1,2}, \d{4} at \d{1,2}:\d{2} [ap]m", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{2,}", "\n", t)
    return t.strip()


BAD_RE = re.compile(r"(?i)(^[\-\*\|#>]|\||##|\*\*|table of contents|written by|"
                    r"read time|sign up|newsletter)")


def sentences(text):
    out = []
    for p in re.split(r"(?<=[.!?])\s+", text):
        p = " ".join(p.split())
        if not (40 <= len(p) <= 520):
            continue
        if BAD_RE.search(p):
            continue
        if len(p.split()) < 6:
            continue
        out.append(p)
    return out


def entity_of(s):
    low = s.lower()
    for name in SYSTEMS:
        if name.lower() in low:
            return name
    return "general"


def evidence_of(s):
    if FIRSTPARTY_RE.search(s):
        return "first_party"
    if STUDY_RE.search(s):
        return "study"
    if CASE_RE.search(s):
        return "case"
    return "opinion"


def is_claim(s):
    if not SCOPE_RE.search(s):
        return False
    if re.search(r"\d", s) or STUDY_RE.search(s) or FIRSTPARTY_RE.search(s) or CASE_RE.search(s):
        return True
    return bool(re.search(r"(?i)\b(should|must|need to|recommend|best practice|found that|"
                          r"said|explains|according)\b", s))


def score(s, ev, sig):
    sc = 0
    sc += 2 if sig else 0
    sc += 2 if ev == "first_party" else 0
    sc += 2 if ev == "study" else 0
    sc += 1 if ev == "case" else 0
    sc += 1 if entity_of(s) != "general" else 0
    return sc


YEAR_MIN, YEAR_MAX = 2000, 2035


def distinctive(vals):
    """Values worth comparing: >=10 and not a year."""
    out = set()
    for v in vals:
        try:
            f = float(v)
        except ValueError:
            continue
        if f >= 10 and not (YEAR_MIN <= f <= YEAR_MAX):
            out.add(v)
    return out


def url_key(u):
    return re.sub(r"^https?://(www\.)?searchengineland\.com/", "", u or "").strip("/").lower()


def main():
    blocks = json.load(open(BLOCKS, encoding="utf-8"))
    slugs = set(json.load(open(SLUGS, encoding="utf-8")))
    corpus = json.load(open(CORPUS, encoding="utf-8"))

    cover = defaultdict(set)
    for b in blocks:
        for u in b["source_urls"]:
            cover[url_key(u)].add(b["id"])
    for s in slugs:
        cover[s].add("source-list")

    block_nums = {b["id"]: strong_sig(b["numbers"]) for b in blocks}
    block_nums = {k: v for k, v in block_nums.items() if v}
    # value-only signatures (language- and unit-independent): 1062 pages vs 1062 страниц
    block_vals = {b["id"]: {n.split("|")[0] for n in b["numbers"]} for b in blocks}
    block_vals = {k: v for k, v in block_vals.items() if len(v) >= 2}

    claims, seen = [], set()
    stat = Counter()
    for art in corpus:
        key = url_key(art.get("url", ""))
        if not key:
            continue
        body = clean(art.get("content") or "")
        if len(body) < 400:
            stat["skipped_short"] += 1
            continue
        cand = []
        for s in sentences(body):
            if not is_claim(s):
                continue
            h = hashlib.sha1(re.sub(r"[^a-z0-9]", "", s.lower()).encode()).hexdigest()[:12]
            if h in seen:
                stat["dup"] += 1
                continue
            seen.add(h)
            ev, sig = evidence_of(s), num_sig(s)
            cand.append((score(s, ev, sig), s, ev, sig))
        cand.sort(key=lambda x: -x[0])
        in_cover = sorted(cover.get(key, []))
        for sc, s, ev, sig in cand[:10]:
            verdict, vs = "NEW", None
            csig = strong_sig(sig)
            cdist = distinctive({x.split("|")[0] for x in csig})
            best, best_dist, best_unit = None, 0, 0
            for bid, bv in block_vals.items():
                dist = len(cdist & distinctive({x.split("|")[0] for x in block_nums.get(bid, set())}))
                unit = len(csig & block_nums.get(bid, set()))
                if (dist, unit) > (best_dist, best_unit):
                    best, best_dist, best_unit = bid, dist, unit
            conflict = None
            ent = entity_of(s)
            if csig and ent != "general":
                units = {x.split("|")[1] for x in csig}
                for b in blocks:
                    if ent.lower() not in (b["statement"] + b["title"]).lower():
                        continue
                    bn = block_nums.get(b["id"], set())
                    if any(x.split("|")[1] in units and x not in csig for x in bn) \
                            and any(x.split("|")[1] in units for x in bn):
                        conflict = b["id"]
                        break
            if best_dist >= 2 or (best_dist >= 1 and best_unit >= 1):
                verdict, vs = ("DUPLICATE" if best and best in in_cover else "REFINES"), [best]
            elif conflict and sig:
                verdict, vs = "REVIEW_NUMERIC", [conflict]
            claims.append({
                "id": f"c{len(claims)+1:05d}", "article_url": art.get("url", ""),
                "article_title": art.get("title", ""), "date": art.get("date", ""),
                "quote": s, "numbers": sig, "evidence": ev, "entity": entity_of(s),
                "score": sc, "verdict": verdict, "vs_block": vs,
                "source_in_playbook": bool(in_cover),
            })
            stat[verdict] += 1

    with open(OUT_CLAIMS, "w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    total_articles = len(corpus)
    covered = sum(1 for a in corpus if cover.get(url_key(a.get("url", ""))))
    by_ev = Counter(c["evidence"] for c in claims)
    by_v = Counter(c["verdict"] for c in claims)
    hard = [c for c in claims if c["verdict"] in ("NEW", "REFINES", "REVIEW_NUMERIC")
            and c["evidence"] in ("first_party", "study", "case") and c["numbers"]
            and c["verdict"] != "REVIEW_NUMERIC"]

    def sect(title):
        return ["", f"## {title}"]

    L = ["# AEO/GEO claims report", "",
         f"Корпус: {total_articles} статей, уже на диске (0 кредитов Firecrawl).",
         f"Блоков плейбука: {len(blocks)}; с источником: {sum(b['flags']['has_source'] for b in blocks)};"
         f" слugs в source-list: {len(slugs)}.",
         f"Атомов: {len(claims)}; из них в скоупе AEO/GEO и после дедупа.",
         f"Вердикты: {dict(by_v)}",
         f"Доказательность: {dict(by_ev)}",
         f"«Твёрдых» новых (first_party/study/case + цифры): {len(hard)}.", ""]
    L += ["## Покрытие плейбука корпусом",
          f"- Статей корпуса, на которые ссылается плейбук: {covered} из {total_articles}"
          f" ({covered/max(total_articles,1)*100:.0f}%).",
          f"- Атомов из этих статей, совпавших с блоками по числовой сигнатуре: {by_v.get('DUPLICATE',0)}",
          f"- Атомов из этих же статей, НЕ совпавших с блоком: "
          f"{sum(1 for c in claims if c['source_in_playbook'] and c['verdict'] != 'DUPLICATE')}"]
    L += sect("Топ новых твёрдых атомов (сортировка по score)")
    for c in sorted(hard, key=lambda x: -x["score"])[:25]:
        L.append(f"- **{c['evidence']} / {c['entity']}** [{c['verdict']}] — {c['quote'][:280]}")
        L.append(f"  {c['article_url']}")
    L += sect("Требуют LLM-адjudication: та же сущность и метрика, другое число")
    conf = [c for c in claims if c["verdict"] == "REVIEW_NUMERIC"]
    for c in conf[:15]:
        L.append(f"- block {c['vs_block']} ← {c['quote'][:220]}")
        L.append(f"  {c['article_url']}")
    L += sect("Распределение по сущностям")
    for e, n in Counter(c["entity"] for c in claims).most_common():
        L.append(f"- {e}: {n}")
    open(OUT_REPORT, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print(f"articles={total_articles} covered={covered} claims={len(claims)}")
    print("verdicts:", dict(by_v))
    print("evidence:", dict(by_ev))
    print("hard:", len(hard), "| conflicts:", len(conf))
    print("stat:", dict(stat))


if __name__ == "__main__":
    main()

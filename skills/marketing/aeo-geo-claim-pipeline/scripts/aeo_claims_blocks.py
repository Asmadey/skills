#!/usr/bin/env python3
"""Parse SEO/AEO/GEO playbook v2 into machine-readable blocks.

Output: ~/.hermes/data/aeo-claims/blocks.json
Each block: id, section, title, statement, source_urls, numbers, flags.
Deterministic, no LLM.
"""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aeo_numbers import sig as num_sig

SRC = "/home/hermes/seo_aeo_geo_playbook_v2.md"
OUT_DIR = os.path.expanduser("~/.hermes/data/aeo-claims")
OUT = os.path.join(OUT_DIR, "blocks.json")



def norm_numbers(text):
    return num_sig(text)

def main():
    text = open(SRC, encoding="utf-8").read()
    lines = text.split("\n")
    blocks = []
    cur_section = ""
    cur = None
    for ln in lines:
        if ln.startswith("## "):
            cur_section = ln[3:].strip()
        elif ln.startswith("### "):
            if cur:
                blocks.append(cur)
            head = ln[4:].strip()
            m = re.match(r"^([\d\.]+?)\.?\s+(.*)$", head)
            if m:
                bid = m.group(1).rstrip(".")
                title = m.group(2)
            else:
                # sub-heading inside a numbered section (e.g. F.A.C.T.S. letters)
                secnum = re.search(r"(\d+)", cur_section)
                letter = head[:1].upper() if head[:1].isalnum() else "x"
                bid = f"{secnum.group(1) if secnum else 'x'}.{letter}"
                title = head
            cur = {"id": bid, "section": cur_section, "title": title,
                   "statement": [], "source_urls": [], "raw": ""}
        elif cur is not None:
            cur["raw"] += ln + "\n"
    if cur:
        blocks.append(cur)

    # source-list section is not doctrine — harvest its slugs, drop its blocks
    src_slugs = []
    keep = []
    for b in blocks:
        if b["section"].upper().startswith("ИСТОЧНИК"):
            src_slugs += re.findall(r"[a-z0-9][a-z0-9\-]{15,}-\d{5,6}", b["raw"])
        else:
            keep.append(b)
    blocks = keep
    src_slugs = sorted(set(src_slugs))

    for b in blocks:
        raw = b.pop("raw")
        b["source_urls"] = sorted(set(re.findall(r"\]\((https?://[^\)]+)\)", raw)))
        stmt = re.sub(r"\*Источник:[^\n]*\*", "", raw)
        stmt = re.sub(r"\n{2,}", "\n", stmt).strip()
        b["statement"] = stmt
        b["numbers"] = sorted(set(norm_numbers(stmt + " " + b["title"])))
        b["flags"] = {
            "has_source": bool(b["source_urls"]),
            "has_numbers": bool(b["numbers"]),
            "has_tactic_verb": bool(re.search(
                r"(?i)должн|нужно|следует|используйте|добавьте|уберите|проверьте|"
                r"создавайте|избегайте|тестируйте|увеличьте|сократите|включите|"
                r"не \w+", stmt)),
        }
        # tier: only structural evidence matters at this stage
        if b["flags"]["has_source"] and len(b["numbers"]) >= 2:
            b["tier"] = "B_cited_specific"
        elif b["flags"]["has_source"]:
            b["tier"] = "C_cited_vague"
        else:
            b["tier"] = "D_no_source"

    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(blocks, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    from collections import Counter
    print(f"blocks: {len(blocks)}")
    print("by section:", dict(Counter(b["section"] for b in blocks)))
    print("by tier:", dict(Counter(b["tier"] for b in blocks)))
    print("with source:", sum(b["flags"]["has_source"] for b in blocks))
    print("unique source urls:", len({u for b in blocks for u in b["source_urls"]}))
    print("no numbers at all:", sum(not b["numbers"] for b in blocks))
    json.dump(src_slugs, open(os.path.join(OUT_DIR, "playbook_source_slugs.json"), "w"),
              ensure_ascii=False, indent=1)
    print("source-list slugs:", len(src_slugs))
    print("sample ids:", [b["id"] for b in blocks[:5]], "...", [b["id"] for b in blocks[-3:]])
    dups = [b["id"] for b in blocks if not re.match(r"^[\d\.]+$", b["id"])]
    if dups:
        print("bad ids:", dups[:10])


if __name__ == "__main__":
    main()

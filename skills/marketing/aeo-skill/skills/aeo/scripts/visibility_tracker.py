#!/usr/bin/env python3
"""Журнал замеров AI-видимости: прогоны промптов, четыре исхода, доли по движкам и этапам воронки.

Примеры:
  python3 visibility_tracker.py init --brand "Acme" --file aeo-visibility.csv
  python3 visibility_tracker.py add --prompt "лучшие CRM для малого бизнеса" --engine chatgpt --stage выбор \
      --mention y --cited n --position 3 --sentiment нейтрально --rivals "HubSpot;Bitrix24" --sources "g2.com;reddit.com"
  python3 visibility_tracker.py report --file aeo-visibility.csv
"""
import argparse
import collections
import csv
import datetime
import json
import os
import sys

FIELDS = ["date", "brand", "engine", "stage", "prompt", "mention", "cited", "position", "recommended",
          "sentiment", "accurate", "rivals", "sources", "note"]
YES = {"y", "yes", "1", "да", "true", "д"}


def yn(v):
    return "y" if str(v).strip().lower() in YES else "n"


def load(path):
    if not os.path.exists(path):
        sys.exit(f"Файл {path} не найден. Сначала: visibility_tracker.py init --brand ...")
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def cmd_init(a):
    if os.path.exists(a.file):
        sys.exit(f"{a.file} уже существует")
    with open(a.file, "w", encoding="utf-8", newline="") as fh:
        csv.DictWriter(fh, FIELDS).writeheader()
    with open(a.file + ".meta.json", "w", encoding="utf-8") as fh:
        json.dump({"brand": a.brand, "created": str(datetime.date.today())}, fh, ensure_ascii=False)
    print(f"Создан журнал {a.file} для бренда «{a.brand}»")


def cmd_add(a):
    brand = a.brand
    meta = a.file + ".meta.json"
    if not brand and os.path.exists(meta):
        brand = json.load(open(meta, encoding="utf-8")).get("brand", "")
    row = {"date": a.date or str(datetime.date.today()), "brand": brand, "engine": a.engine.lower(),
           "stage": a.stage, "prompt": a.prompt.strip(), "mention": yn(a.mention), "cited": yn(a.cited),
           "position": a.position or "", "recommended": yn(a.recommended) if a.recommended else "",
           "sentiment": a.sentiment or "", "accurate": yn(a.accurate) if a.accurate else "",
           "rivals": a.rivals or "", "sources": a.sources or "", "note": a.note or ""}
    new = not os.path.exists(a.file)
    with open(a.file, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print("Записано:", row["engine"], "|", row["prompt"][:60])


def outcome(r):
    m, c = r["mention"] == "y", r["cited"] == "y"
    return "оба" if m and c else "только цитата" if c else "только упоминание" if m else "ничего"


def pct(n, d):
    return f"{100 * n / d:.0f}%" if d else "—"


def cmd_report(a):
    rows = load(a.file)
    if a.since:
        rows = [r for r in rows if r["date"] >= a.since]
    if not rows:
        sys.exit("Нет записей")
    n = len(rows)
    print(f"Прогонов: {n} | период: {min(r['date'] for r in rows)} — {max(r['date'] for r in rows)}")

    oc = collections.Counter(outcome(r) for r in rows)
    print("\nИсходы:")
    for k in ("оба", "только упоминание", "только цитата", "ничего"):
        print(f"  {k:<20}{oc[k]:>5}  {pct(oc[k], n)}")
    cited = oc["оба"] + oc["только цитата"]
    if cited:
        print(f"  Доля цитат без названия бренда: {pct(oc['только цитата'], cited)}")

    for title, key in (("По движкам", "engine"), ("По этапам воронки", "stage")):
        print(f"\n{title}:\n  {'':<22}{'прогонов':<10}{'упомин.':<10}{'цитата':<10}{'рекоменд.':<10}")
        g = collections.defaultdict(list)
        for r in rows:
            g[r[key] or "—"].append(r)
        for k, rs in sorted(g.items(), key=lambda x: -len(x[1])):
            rec = [r for r in rs if r["recommended"]]
            print(f"  {k:<22}{len(rs):<10}{pct(sum(r['mention'] == 'y' for r in rs), len(rs)):<10}"
                  f"{pct(sum(r['cited'] == 'y' for r in rs), len(rs)):<10}"
                  f"{pct(sum(r['recommended'] == 'y' for r in rec), len(rec)):<10}")

    # устойчивость: доля появлений по каждой паре промпт+движок
    pairs = collections.defaultdict(list)
    for r in rows:
        pairs[(r["prompt"], r["engine"])].append(r["mention"] == "y")
    thin = sum(1 for v in pairs.values() if len(v) < 3)
    stable = sum(1 for v in pairs.values() if len(v) >= 3 and all(v))
    never = sum(1 for v in pairs.values() if len(v) >= 3 and not any(v))
    print(f"\nПар «промпт + движок»: {len(pairs)} | всегда упомянут: {stable} | никогда: {never} | "
          f"нестабильно: {len(pairs) - stable - never - thin} | меньше 3 прогонов: {thin}")
    if thin:
        print("  ⚠ По парам с 1–2 прогонами выводов делать нельзя: разброс ответов на одинаковый промпт достигает 10–34%.")

    for title, key in (("Кого называют вместо вас или рядом", "rivals"), ("Источники ответов", "sources")):
        c = collections.Counter(x.strip().lower() for r in rows for x in r[key].split(";") if x.strip())
        if c:
            print(f"\n{title}:")
            for k, v in c.most_common(a.top):
                print(f"  {v:>4}  {k}")

    bad = [r for r in rows if r["accurate"] == "n"]
    if bad:
        print(f"\nОтветы с фактическими ошибками: {len(bad)}")
        for r in bad[:10]:
            print(f"  {r['date']} {r['engine']}: {r['prompt'][:50]} — {r['note'][:80]}")

    weeks = collections.defaultdict(list)
    for r in rows:
        y, w, _ = datetime.date.fromisoformat(r["date"]).isocalendar()
        weeks[f"{y}-W{w:02d}"].append(r["mention"] == "y")
    if len(weeks) > 1:
        print("\nДинамика упоминаний по неделям:")
        for k in sorted(weeks):
            print(f"  {k}: {pct(sum(weeks[k]), len(weeks[k]))} ({len(weeks[k])} прогонов)")


def main():
    ap = argparse.ArgumentParser(description="Журнал замеров AI-видимости")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("--brand", required=True)
    p.add_argument("--file", default="aeo-visibility.csv")
    p.set_defaults(fn=cmd_init)
    p = sub.add_parser("add")
    p.add_argument("--file", default="aeo-visibility.csv")
    p.add_argument("--brand")
    p.add_argument("--prompt", required=True)
    p.add_argument("--engine", required=True, help="chatgpt, ai-mode, ai-overview, gemini, claude, perplexity, copilot")
    p.add_argument("--stage", default="", help="этап воронки: проблема, выбор, сравнение, проверка, действие")
    p.add_argument("--mention", required=True, help="y/n: бренд назван в ответе")
    p.add_argument("--cited", required=True, help="y/n: есть ссылка на ваш URL")
    p.add_argument("--position")
    p.add_argument("--recommended", help="y/n: бренд рекомендован, а не просто перечислен")
    p.add_argument("--sentiment")
    p.add_argument("--accurate", help="y/n: факты о бренде верны")
    p.add_argument("--rivals", help="бренды через ;")
    p.add_argument("--sources", help="домены-источники через ;")
    p.add_argument("--note")
    p.add_argument("--date")
    p.set_defaults(fn=cmd_add)
    p = sub.add_parser("report")
    p.add_argument("--file", default="aeo-visibility.csv")
    p.add_argument("--since", help="ГГГГ-ММ-ДД")
    p.add_argument("--top", type=int, default=15)
    p.set_defaults(fn=cmd_report)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

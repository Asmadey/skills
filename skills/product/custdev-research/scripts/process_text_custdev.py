#!/usr/bin/env python3
"""
process_text_custdev.py — CustDev pipeline for ALREADY TRANSCRIBED meetings (plain text).

Input format (tolerant):  [HH:MM:SS] Speaker label: text
Example:                  [00:04:43] Спикер 2: Смотри, а тебе не очевидно, как сгенерировать трек?

Steps: parse -> semantic re-diarization (2 speakers) -> insights & profile
-> ONE unified follow-up -> branded DOCX -> registry row.

Usage:
python3 skills/product/custdev-research/scripts/process_text_custdev.py \
  --input "transcript.txt" \
  --interviewer "Влад JGGL" \
  --respondent "Алекс" \
  --title "Кастдев и UX-тестирование JGGL — Алекс"
"""

import os
import re
import sys
import json
import argparse
import urllib.parse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_diarizer import diarize_transcript
from custdev_analyzer import extract_insights_and_profile
from docx_generator import generate_custdev_docx

load_dotenv()

def _resolve_base_dir() -> Path:
    """Корень проекта пользователя: env CUSTDEV_BASE_DIR → поиск вверх от CWD по Meets/ или .git."""
    env = os.getenv("CUSTDEV_BASE_DIR")
    if env:
        return Path(env).expanduser().resolve()
    here = Path.cwd().resolve()
    for cand in (here, *here.parents):
        if (cand / "Meets").is_dir() or (cand / ".git").is_dir():
            return cand
    return here


BASE_DIR = _resolve_base_dir()
MEETS_DIR = BASE_DIR / "Meets"
TRANSCRIPTS_DIR = MEETS_DIR / "transcripts"
FOLLOWUPS_DIR = MEETS_DIR / "followups"
REGISTRY_PATH = Path(os.getenv("CUSTDEV_REGISTRY") or (BASE_DIR / "Meets" / "реестр_кастдевов.md"))

for d in (TRANSCRIPTS_DIR, FOLLOWUPS_DIR):
    d.mkdir(parents=True, exist_ok=True)

LINE_RE = re.compile(r"^\[(\d{1,2}):(\d{2}):(\d{2})\]\s*([^:]{1,40}?)\s*:\s*(.*)$")


def parse_timestamped_text(text: str):
    """Parses '[HH:MM:SS] Speaker: text' lines into timeline segments."""
    raw = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if not m:
            # continuation of the previous segment
            if raw:
                raw[-1]["text"] = (raw[-1]["text"] + " " + line).strip()
            continue
        h, mi, s, speaker, body = m.groups()
        raw.append({
            "start": int(h) * 3600 + int(mi) * 60 + int(s),
            "speaker": speaker.strip(),
            "text": body.strip(),
        })

    segments = []
    for i, seg in enumerate(raw):
        start = float(seg["start"])
        end = float(raw[i + 1]["start"]) if i + 1 < len(raw) else start + 6.0
        if end <= start:
            end = start + 3.0
        if not seg["text"]:
            continue
        segments.append({
            "start": start,
            "end": end,
            "text": seg["text"],
            "speaker": seg["speaker"],
            "auto_speaker": seg["speaker"],
        })
    return segments


def _rel_link(path: Path, label: str = None) -> str:
    p = Path(path).resolve()
    return f"[{label or p.name}]({urllib.parse.quote(os.path.relpath(p, BASE_DIR))})"


def record_registry(source_path, interviewer, respondent, profile, transcript_path, docx_path, followup_path):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    profile_short = (profile[:60] + "...") if len(profile) > 60 else profile
    row = (
        f"| {now_str} | {_rel_link(source_path)} (текстовая расшифровка) | {interviewer} | {respondent} | "
        f"{profile_short} | {_rel_link(transcript_path)} | {_rel_link(docx_path)} | {_rel_link(followup_path)} | Успешно ✅ |\n"
    )
    with open(REGISTRY_PATH, "a", encoding="utf-8") as f:
        f.write(row)
    print(f"📊 Registry updated: {REGISTRY_PATH}")


def run_text_pipeline(input_path, interviewer="Влад JGGL", respondent="Алекс",
                      title="JGGL: Кастдев-интервью и UX-тестирование", profile=None,
                      output_docx=None, slug=None, skip_diarize=False, source_labels=None):
    src = Path(input_path).resolve()
    segments = parse_timestamped_text(src.read_text(encoding="utf-8"))
    if not segments:
        raise ValueError(f"Не удалось распознать ни одного сегмента в {src}")

    slug = slug or respondent.lower().replace(" ", "_")
    labels = [interviewer, respondent]

    if skip_diarize and source_labels:
        mapping = dict(source_labels)
        for seg in segments:
            seg["speaker"] = mapping.get(seg["speaker"], interviewer if seg["speaker"] == "" else respondent)

    t_data = {
        "audio_file": None,
        "source_file": str(src),
        "model": "text transcript",
        "full_text": " ".join(s["text"] for s in segments),
        "timeline": segments,
        "part_label": f"Полная стенограмма — {src.name}",
    }

    print("\n" + "=" * 60)
    print(f"📄 Text transcript pipeline: {src.name}")
    print(f"   Segments: {len(segments)} | Interviewer: {interviewer} | Respondent: {respondent}")
    print("=" * 60 + "\n")

    if not skip_diarize:
        t_data = diarize_transcript(
            t_data,
            interviewer_name=interviewer,
            respondent_name=respondent,
            speakers=labels,
            speaker_hints={
                interviewer: "мужчина, ведущий исследования JGGL, модерирует, просит комментировать вслух, задает наводящие вопросы",
                respondent: "мужчина, респондент, проходит сценарии по приложению и описывает вслух, что видит и чего не понимает",
            },
        )
    else:
        t_data["interviewer"] = interviewer
        t_data["respondent"] = respondent
        t_data["speakers"] = labels

    transcript_path = TRANSCRIPTS_DIR / f"{slug}.json"
    transcript_path.write_text(json.dumps(t_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"💾 Transcript saved: {transcript_path}")

    print("🧠 Extracting insights...")
    prof, bullets = extract_insights_and_profile(t_data)
    final_profile = profile or prof or f"{respondent}, респондент кастдев-тестирования JGGL."

    seen, unique = set(), []
    for b in bullets:
        key = b.strip().lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(b.strip())

    date_str = datetime.now().strftime("%d.%m.%Y")
    title_line = title if date_str in title else f"{title} — {date_str}"
    followup_path = FOLLOWUPS_DIR / f"{slug}.txt"
    followup_path.write_text(
        f"**{title_line}**\n\n"
        f"**Профиль респондента:**\n{final_profile}\n\n"
        f"**Ключевые инсайты и продуктовые боли:**\n"
        + "\n".join(f"{i}. {b}" for i, b in enumerate(unique, 1)) + "\n",
        encoding="utf-8",
    )
    print(f"📋 Follow-up saved: {followup_path}")

    docx_path = Path(output_docx).resolve() if output_docx else MEETS_DIR / f"Стенограмма_и_Фоллоуап_{respondent}_{date_str.replace('.', '_')}.docx"
    generate_custdev_docx(
        transcripts_data_list=[t_data],
        summary_bullets=unique,
        output_docx_path=docx_path,
        title=title,
        date_str=date_str,
        interviewer=interviewer,
        interviewer_role="Ведущий исследования / Product Manager (JGGL) — модерация, навигация по сценариям, проверка продуктовых гипотез",
        respondent=respondent,
        respondent_profile=final_profile,
    )

    record_registry(src, interviewer, respondent, final_profile, transcript_path, docx_path, followup_path)

    print("\n🎉 Done.")
    print(f"📄 DOCX: {docx_path}")
    print(f"📋 Follow-up: {followup_path}")
    print(f"🧾 Transcript: {transcript_path}")
    return docx_path, followup_path, transcript_path


def main():
    ap = argparse.ArgumentParser(description="CustDev pipeline for already transcribed text")
    ap.add_argument("--input", required=True, help="Path to a timestamped transcript (.txt)")
    ap.add_argument("--interviewer", default="Влад JGGL")
    ap.add_argument("--respondent", default="Алекс")
    ap.add_argument("--title", default="JGGL: Кастдев-интервью и UX-тестирование")
    ap.add_argument("--profile", help="Verified respondent profile (overrides extraction)")
    ap.add_argument("--output-docx")
    ap.add_argument("--slug", help="Base name for transcript/follow-up files")
    ap.add_argument("--skip-diarize", action="store_true", help="Trust source speaker labels")
    ap.add_argument("--map", action="append", default=[], help='Source label mapping, e.g. --map "Спикер 1=Алекс"')
    args = ap.parse_args()

    mapping = {}
    for m in args.map:
        if "=" in m:
            k, v = m.split("=", 1)
            mapping[k.strip()] = v.strip()

    run_text_pipeline(
        input_path=args.input,
        interviewer=args.interviewer,
        respondent=args.respondent,
        title=args.title,
        profile=args.profile,
        output_docx=args.output_docx,
        slug=args.slug,
        skip_diarize=args.skip_diarize,
        source_labels=mapping,
    )


if __name__ == "__main__":
    main()

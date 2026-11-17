#!/usr/bin/env python3
"""
process_group_custdev.py — Group CustDev / UX-test pipeline (N speakers, multiple recordings of ONE meeting).

Pipeline: transcription (or reuse saved raw transcripts) -> N-speaker contextual LLM diarization
-> per-respondent profiles + attributed product bullets -> ONE unified follow-up
-> ONE branded DOCX for the whole meeting -> registry row.

Usage:
python3 skills/product/custdev-research/scripts/process_group_custdev.py \
  --files "part1.webm" "part2.webm" \
  --interviewer "Интервьюер (JGGL)" \
  --respondents "Глеб" "Камила" "Стас" \
  --hint "Глеб: 27 лет, нейродизайн" --hint "Камила: 24 года, архитектор-дизайнер" \
  --title "Групповой кастдев и UX-тестирование JGGL — 12.11.2026" \
  --raw-json raw1.json raw2.json \
  --output-docx "Meets/Стенограмма_и_Фоллоуап_Группа_12.11.docx" \
  --slug "группа_12.11"
"""

import os
import sys
import json
import argparse
import urllib.parse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from groq_keys import KEYRING  # noqa: E402  бюджет/ротация ключей

from transcribe_groq import transcribe_media
from llm_diarizer import diarize_transcript, is_diarized
from custdev_analyzer import extract_group_insights
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


def _rel_link(path: Path, label: str = None) -> str:
    p = Path(path).resolve()
    rel = os.path.relpath(p, BASE_DIR)
    return f"[{label or p.name}]({urllib.parse.quote(rel)})"


def record_registry(media_paths, interviewer, respondents, profile_short, transcript_paths, docx_path, followup_path, missing_media=None):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    missing = set(missing_media or [])
    media_links = ", ".join(
        _rel_link(p) if p.exists() else f"{p.name} (источник перемещён/удалён)" for p in media_paths
    )
    transcript_links = ", ".join(_rel_link(p) for p in transcript_paths)
    profile_short = (profile_short[:60] + "...") if len(profile_short) > 60 else profile_short
    row = (
        f"| {now_str} | {media_links} | {interviewer} | {', '.join(respondents)} | {profile_short} | "
        f"{transcript_links} | {_rel_link(docx_path)} | {_rel_link(followup_path)} | Успешно ✅ |\n"
    )
    with open(REGISTRY_PATH, "a", encoding="utf-8") as f:
        f.write(row)
    print(f"📊 Registry updated: {REGISTRY_PATH}")


def run_group_pipeline(file_paths, interviewer, respondents, speaker_hints=None, title="JGGL: Групповой кастдев",
                       output_docx=None, language="ru", raw_json_paths=None, slug=None, profile_overrides=None,
                       force=False):
    raw_paths = [Path(p) for p in (raw_json_paths or [])]
    media_paths = [Path(f) for f in file_paths]
    missing_media = []
    for idx, p in enumerate(media_paths):
        if p.exists():
            media_paths[idx] = p.resolve()
        elif idx < len(raw_paths) and raw_paths[idx].exists():
            missing_media.append(p.name)
            print(f"⚠️  Source media not found ({p.name}) — using saved transcription instead.")
        else:
            raise FileNotFoundError(f"Media file not found and no saved transcript: {p}")

    labels = [interviewer] + list(respondents)
    slug = slug or "группа_" + datetime.now().strftime("%d.%m")

    print("\n" + "=" * 60)
    print(f"🚀 Group CustDev Pipeline — {len(media_paths)} recording(s) of ONE meeting")
    print(f"   Title: {title}")
    print(f"   Speakers ({len(labels)}): {', '.join(labels)}")
    print("=" * 60 + "\n")

    # Pre-flight: показать бюджет и спрогнозировать, влезает ли работа
    KEYRING.preflight(est_tokens=4000 * len(media_paths),
                      est_audio_seconds=600 * 10 * len(media_paths))

    transcripts_data, transcript_paths = [], []
    all_bullets, profiles = [], {}

    for idx, m_path in enumerate(media_paths, 1):
        print(f"\n--- [Part {idx}/{len(media_paths)}] {m_path.name} ---")

        t_json = TRANSCRIPTS_DIR / f"{slug}_ч{idx}.json"

        # Кэш: если часть уже размечена и проанализирована — не платим за это второй раз.
        cached = None
        if not force and t_json.exists():
            try:
                prev = json.loads(t_json.read_text(encoding="utf-8"))
                if is_diarized(prev):
                    cached = prev
            except Exception:
                cached = None

        if cached is not None:
            print(f"♻️  Уже обработано ранее: {t_json.name} "
                  f"({len(cached['timeline'])} сегментов, "
                  f"{(cached.get('diarization') or {}).get('engine', 'разметка v1')}) "
                  f"— пропускаю диаризацию (--force чтобы переделать)")
            t_data = cached
        else:
            if raw_paths and idx - 1 < len(raw_paths) and raw_paths[idx - 1].exists():
                print(f"♻️  Reusing saved transcription: {raw_paths[idx - 1].name}")
                t_data = json.loads(raw_paths[idx - 1].read_text(encoding="utf-8"))
            else:
                print("🎙 Transcribing...")
                t_data = transcribe_media(str(m_path), language=language)

            t_data = diarize_transcript(
                t_data,
                interviewer_name=interviewer,
                respondent_name=respondents[0] if respondents else "Респондент",
                speakers=labels,
                speaker_hints=speaker_hints,
            )
            t_data["part_label"] = f"Часть {idx} — {m_path.name}"
            t_data["source_file"] = str(m_path)
            t_json.write_text(json.dumps(t_data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"💾 Transcript saved: {t_json}")

        transcript_paths.append(t_json)
        transcripts_data.append(t_data)

        cached_insights = t_data.get("group_insights") or {}
        if cached_insights.get("bullets") and not force:
            print(f"♻️  Инсайты уже извлекались — беру из кэша ({len(cached_insights['bullets'])} пунктов)")
            prof, bullets = cached_insights.get("profiles") or {}, cached_insights["bullets"]
        else:
            print("🧠 Extracting group insights...")
            prof, bullets = extract_group_insights(t_data)
            t_data["group_insights"] = {"profiles": prof or {}, "bullets": bullets or []}
            t_json.write_text(json.dumps(t_data, ensure_ascii=False, indent=2), encoding="utf-8")

        for name, text in (prof or {}).items():
            if name not in profiles or len(text) > len(profiles[name]):
                profiles[name] = text
        all_bullets.extend(bullets)

    # Unified de-duplicated bullet list across all parts
    seen, unique_bullets = set(), []
    for b in all_bullets:
        key = b.strip().lower()
        if key and key not in seen:
            seen.add(key)
            unique_bullets.append(b.strip())

    ordered_names = [n for n in respondents if n in profiles] + [n for n in profiles if n not in respondents]
    for name, text in (profile_overrides or {}).items():
        profiles[name] = text
        if name not in ordered_names:
            ordered_names.append(name)
    profile_block = "\n".join(f"- **{n}:** {profiles[n]}" for n in ordered_names) or "- Профили не извлечены."
    profile_short = "; ".join(f"{n} — {profiles.get(n, '')[:70]}" for n in ordered_names)

    date_str = datetime.now().strftime("%d.%m.%Y")
    title_line = title if date_str in title else f"{title} — {date_str}"
    followup_path = FOLLOWUPS_DIR / f"{slug}.txt"
    followup_content = (
        f"**{title_line}**\n\n"
        f"**Участники:** {interviewer} (ведущий); {', '.join(respondents)} (респонденты)\n\n"
        f"**Профили респондентов:**\n{profile_block}\n\n"
        f"**Ключевые инсайты и продуктовые боли (сквозные по обеим частям встречи):**\n"
        + "\n".join(f"{i}. {b}" for i, b in enumerate(unique_bullets, 1)) + "\n"
    )
    followup_path.write_text(followup_content, encoding="utf-8")
    print(f"📋 Unified follow-up saved: {followup_path}")

    docx_path = Path(output_docx).resolve() if output_docx else MEETS_DIR / f"Стенограмма_и_Фоллоуап_Группа_{date_str.replace('.', '_')}.docx"

    primary = respondents[0]
    extra = [(n, profiles[n]) for n in respondents[1:] if n in profiles]
    generate_custdev_docx(
        transcripts_data_list=transcripts_data,
        summary_bullets=unique_bullets,
        output_docx_path=docx_path,
        title=title,
        date_str=date_str,
        interviewer=interviewer,
        interviewer_role="Ведущий исследования (JGGL) — фасилитация групповой сессии, навигация по сценариям, проверка продуктовых гипотез",
        respondent=primary,
        respondent_profile=profiles.get(primary, f"{primary}, участник группового тестирования JGGL."),
        extra_participants=extra,
    )

    record_registry(media_paths, interviewer, respondents, profile_short, transcript_paths, docx_path, followup_path, missing_media)

    print("\n🎉 Group CustDev pipeline completed.")
    print(f"📄 DOCX: {docx_path}")
    print(f"📋 Follow-up: {followup_path}")
    print(f"🧾 Transcripts: {[str(p) for p in transcript_paths]}")
    return docx_path, followup_path, transcript_paths


def main():
    ap = argparse.ArgumentParser(description="Group CustDev & UX-test pipeline (N speakers)")
    ap.add_argument("--files", nargs="+", required=True, help="Recordings of ONE meeting, in chronological order")
    ap.add_argument("--interviewer", default="Интервьюер (JGGL)")
    ap.add_argument("--respondents", nargs="+", required=True)
    ap.add_argument("--hint", action="append", default=[], help='Speaker hint, e.g. --hint "Глеб: 27 лет, нейродизайн"')
    ap.add_argument("--title", default="JGGL: Групповой кастдев и UX-тестирование")
    ap.add_argument("--output-docx")
    ap.add_argument("--language", default="ru")
    ap.add_argument("--raw-json", nargs="*", help="Already saved raw transcripts (skip transcription)")
    ap.add_argument("--slug", help="Base name for transcript/follow-up files")
    ap.add_argument("--profile", action="append", default=[], help='Verified profile override, e.g. --profile "Глеб: Глеб, 27 лет, нейродизайнер…"')
    ap.add_argument("--force", action="store_true", help="Переделать даже уже размеченные/проанализированные части (жжёт токены)")
    args = ap.parse_args()

    hints = {}
    for h in args.hint:
        if ":" in h:
            k, v = h.split(":", 1)
            hints[k.strip()] = v.strip()

    overrides = {}
    for p in args.profile:
        if ":" in p:
            k, v = p.split(":", 1)
            overrides[k.strip()] = v.strip()

    run_group_pipeline(
        file_paths=args.files,
        interviewer=args.interviewer,
        respondents=args.respondents,
        speaker_hints=hints,
        title=args.title,
        output_docx=args.output_docx,
        language=args.language,
        raw_json_paths=args.raw_json,
        slug=args.slug,
        profile_overrides=overrides,
        force=args.force,
    )


if __name__ == "__main__":
    main()

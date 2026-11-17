#!/usr/bin/env python3
"""
process_custdev.py — Master Pipeline Orchestrator for the custdev Skill.
Extracts audio (-vn) -> Groq Whisper -> Context Diarization -> Profile & Single Numbered UX Follow-up -> Branded DOCX.
Always produces exactly ONE unified follow-up file per CustDev interview.
"""

import os
import sys
import json
import argparse
import urllib.parse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from extract_audio_ffmpeg import split_and_extract_audio
sys.path.insert(0, str(Path(__file__).resolve().parent))
from groq_keys import KEYRING  # noqa: E402  бюджет/ротация ключей

from transcribe_groq import transcribe_media
from llm_diarizer import diarize_transcript, is_diarized
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

TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
FOLLOWUPS_DIR.mkdir(parents=True, exist_ok=True)
REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_registry():
    if not REGISTRY_PATH.exists():
        header = """# Реестр проведенных Кастдев-исследований и UX-тестирований (JGGL)

Файл автоматически обновляется навыком `custdev`.

| Дата и время | Исходные файлы | Интервьюер | Респондент | Профиль | Транскрипт (JSON) | DOCX Отчет | Фоллоу-ап (TXT) | Статус |
|---|---|---|---|---|---|---|---|---|
"""
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            f.write(header)

def record_in_registry(media_paths, interviewer, respondent, respondent_profile, transcript_paths, docx_path, followup_path):
    init_registry()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    media_links = ", ".join([
        f"[{p.name}](file://{urllib.parse.quote(str(p.resolve()))})"
        for p in media_paths
    ])

    transcript_links = ", ".join([
        f"[{p.name}](file://{urllib.parse.quote(str(p.resolve()))})"
        for p in transcript_paths
    ])

    docx_link = f"[{docx_path.name}](file://{urllib.parse.quote(str(docx_path.resolve()))})"
    followup_link = f"[{followup_path.name}](file://{urllib.parse.quote(str(followup_path.resolve()))})"
    short_profile = respondent_profile[:60] + "..." if len(respondent_profile) > 60 else respondent_profile

    row = f"| {now_str} | {media_links} | {interviewer} | {respondent} | {short_profile} | {transcript_links} | {docx_link} | {followup_link} | Успешно ✅ |\n"

    with open(REGISTRY_PATH, "a", encoding="utf-8") as f:
        f.write(row)
    print(f"📊 Registry updated: {REGISTRY_PATH}")

def run_custdev_pipeline(file_paths, interviewer="Влад JGGL", respondent="Респондент", respondent_profile=None, title="JGGL: Кастдев-интервью и UX-тестирование", output_docx=None, language="ru", force=False):
    media_paths = [Path(f).resolve() for f in file_paths]
    for p in media_paths:
        if not p.exists():
            raise FileNotFoundError(f"Media file not found: {p}")

    print(f"\n========================================================")
    print(f"🚀 Starting CustDev Pipeline for {len(media_paths)} file(s)")
    print(f"   Title: {title}")
    print(f"   Interviewer: {interviewer} | Respondent: {respondent}")
    print(f"========================================================\n")

    KEYRING.preflight(est_tokens=4000 * len(media_paths),
                      est_audio_seconds=600 * 10 * len(media_paths))

    transcripts_data = []
    all_summary_bullets = []
    transcript_paths = []
    extracted_profile = respondent_profile

    for idx, m_path in enumerate(media_paths, 1):
        stem = m_path.stem
        clean_resp = respondent.lower().replace(" ", "_")
        t_json_path = TRANSCRIPTS_DIR / f"{clean_resp}_{stem}.json"

        cached = None
        if not force and t_json_path.exists():
            try:
                prev = json.loads(t_json_path.read_text(encoding="utf-8"))
                if is_diarized(prev):
                    cached = prev
            except Exception:
                cached = None

        if cached is not None:
            print(f"\n--- [Part {idx}/{len(media_paths)}] ♻️ уже обработано: {t_json_path.name} "
                  f"({len(cached['timeline'])} сегментов) — пропускаю распознавание и диаризацию (--force чтобы переделать)")
            t_data = cached
            transcript_paths.append(t_json_path)
            transcripts_data.append(t_data)
        else:
            # Step 1: Transcribe
            print(f"\n--- [Part {idx}/{len(media_paths)}] 1. Transcription ({m_path.name}) ---")
            t_data = transcribe_media(str(m_path), language=language)

            # Step 2: Diarize
            print(f"--- [Part {idx}/{len(media_paths)}] 2. Contextual LLM Diarization ---")
            t_data = diarize_transcript(t_data, interviewer_name=interviewer, respondent_name=respondent)

            with open(t_json_path, "w", encoding="utf-8") as f:
                json.dump(t_data, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved transcript to: {t_json_path}")
            transcript_paths.append(t_json_path)
            transcripts_data.append(t_data)

        # Step 3: Extract Insights
        cached_insights = t_data.get("insights") or {}
        if cached_insights.get("bullets") and not force:
            print(f"--- [Part {idx}/{len(media_paths)}] ♻️ инсайты из кэша ({len(cached_insights['bullets'])} пунктов)")
            prof, bullets = cached_insights.get("profile"), cached_insights["bullets"]
        else:
            print(f"--- [Part {idx}/{len(media_paths)}] 3. Extracting Insights & Profile ---")
            prof, bullets = extract_insights_and_profile(t_data)
            t_data["insights"] = {"profile": prof, "bullets": bullets}
            with open(t_json_path, "w", encoding="utf-8") as f:
                json.dump(t_data, f, ensure_ascii=False, indent=2)
        if not extracted_profile and prof:
            extracted_profile = prof
        all_summary_bullets.extend(bullets)

    # Step 4: Build SINGLE unified follow-up
    print(f"\n--- 4. Building Unified Single Follow-Up ---")
    unique_bullets = []
    seen = set()
    for b in all_summary_bullets:
        cleaned = b.strip().lower()
        if cleaned not in seen:
            seen.add(cleaned)
            unique_bullets.append(b.strip())

    final_profile = extracted_profile or f"{respondent}, респондент кастдев-тестирования мобильного приложения JGGL."
    date_str = datetime.now().strftime("%d.%m.%Y")
    date_tag = datetime.now().strftime("%d.%m.%Y")

    bullets_formatted = "\n".join([f"{i}. {b}" for i, b in enumerate(unique_bullets, 1)])
    single_followup_content = f"**{title} — {date_str}**\n\n**Профиль респондента:**\n{final_profile}\n\n**Ключевые инсайты и продуктовые боли:**\n{bullets_formatted}\n"

    clean_resp = respondent.lower().replace(" ", "_")
    unified_followup_path = FOLLOWUPS_DIR / f"{clean_resp}.txt"
    with open(unified_followup_path, "w", encoding="utf-8") as f:
        f.write(single_followup_content)
    print(f"📋 Unified single follow-up saved to: {unified_followup_path}")

    # Step 5: DOCX Generation
    print(f"\n--- 5. Generating Branded DOCX Report ---")
    if not output_docx:
        clean_resp_title = respondent.replace(" ", "_")
        output_docx = MEETS_DIR / f"Стенограмма_и_Фоллоуап_{clean_resp_title}_{date_tag}.docx"
    else:
        output_docx = Path(output_docx).resolve()

    generate_custdev_docx(
        transcripts_data_list=transcripts_data,
        summary_bullets=unique_bullets,
        output_docx_path=output_docx,
        title=title,
        date_str=date_str,
        interviewer=interviewer,
        interviewer_role="Product Manager / Интервьюер (JGGL) — ведение кастдева, навигация по сценариям, проверка продуктовых гипотез",
        respondent=respondent,
        respondent_profile=final_profile
    )

    # Step 6: Update Registry
    record_in_registry(media_paths, interviewer, respondent, final_profile, transcript_paths, output_docx, unified_followup_path)

    print(f"\n🎉 CustDev Pipeline Completed Successfully!")
    print(f"📄 DOCX Report: {output_docx}")
    print(f"📋 Single Follow-up: {unified_followup_path}")
    print(f"🧾 Transcripts: {[str(p) for p in transcript_paths]}")

def main():
    parser = argparse.ArgumentParser(description="CustDev & UX Interview Master Pipeline")
    parser.add_argument("--audio", help="Single audio/video file path")
    parser.add_argument("--files", nargs="+", help="Multiple audio/video file paths for one interview")
    parser.add_argument("--interviewer", default="Влад JGGL", help="Interviewer name (default: Влад JGGL)")
    parser.add_argument("--respondent", default="Респондент", help="Respondent name")
    parser.add_argument("--profile", help="Custom respondent profile description")
    parser.add_argument("--title", default="JGGL: Кастдев-интервью и UX-тестирование", help="Meeting title")
    parser.add_argument("--output-docx", help="Optional path to output DOCX document")
    parser.add_argument("--language", default="ru", help="Audio language ISO code (default: ru)")
    parser.add_argument("--force", action="store_true",
                        help="Переделать даже уже размеченные/проанализированные файлы (жжёт токены)")

    args = parser.parse_args()

    files = args.files or ([args.audio] if args.audio else None)
    if not files:
        print("Error: Specify --audio <file> or --files <file1> <file2>...", file=sys.stderr)
        sys.exit(1)

    run_custdev_pipeline(
        file_paths=files,
        interviewer=args.interviewer,
        respondent=args.respondent,
        respondent_profile=args.profile,
        title=args.title,
        output_docx=args.output_docx,
        language=args.language,
        force=args.force,
    )

if __name__ == "__main__":
    main()

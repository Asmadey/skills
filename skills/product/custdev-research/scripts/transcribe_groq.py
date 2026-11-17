#!/usr/bin/env python3
"""
transcribe_groq.py — Speech-to-Text via Groq Whisper API with automatic fallback.
Supports whisper-large-v3 and whisper-large-v3-turbo with detailed verbose_json timeline.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent))
from groq_keys import KEYRING, AllKeysExhausted  # noqa: E402  multi-key rotation

from extract_audio_ffmpeg import split_and_extract_audio  # noqa: E402


def get_groq_client(api_key: str = None):
    """Backward-compatible accessor: a client bound to the next usable key.
    New code should call KEYRING.transcribe()/KEYRING.chat() instead so that a
    daily limit on one key silently rotates to the next one."""
    return KEYRING.client()

def transcribe_single_chunk(client, chunk_path: str, model_state: dict, language: str = "ru", time_offset: float = 0.0):
    """`client` is unused — kept so existing callers/signatures keep working."""
    with open(chunk_path, "rb") as file:
        file_bytes = file.read()

    while True:
        current_model = model_state["current_model"]
        kwargs = {
            "file": (os.path.basename(chunk_path), file_bytes),
            "model": current_model,
            "temperature": 0.0,
            "response_format": "verbose_json",
        }
        if language:
            kwargs["language"] = language

        try:
            # KEYRING rotates across all configured keys on 429 (daily or per-minute)
            transcription = KEYRING.transcribe(
                **kwargs, est_audio_seconds=model_state.get("chunk_seconds", 600)
            )
            break
        except AllKeysExhausted as e:
            # Every key is out of budget for this model — try a cheaper ASR model
            # (limits are per model, so the turbo model may still have room).
            if model_state["fallback_models"]:
                fallback = model_state["fallback_models"].pop(0)
                print(f"⚠️ Warning: {e}. Switching model to '{fallback}'...")
                model_state["current_model"] = fallback
                model_state["used_fallback"] = True
            else:
                print(f"⛔ {e}")
                raise

    result_dict = transcription.model_dump() if hasattr(transcription, "model_dump") else dict(transcription)
    segments = result_dict.get("segments", [])
    for seg in segments:
        seg["start"] += time_offset
        seg["end"] += time_offset
        # Ensure default speaker placeholder
        seg["speaker"] = "SPEAKER_UNKNOWN"

    return segments, result_dict.get("text", "")

def transcribe_media(media_path: str, groq_key: str = None, language: str = "ru", initial_model: str = "whisper-large-v3"):
    if groq_key:
        KEYRING._add(groq_key)  # explicit key goes to the front of the ring
    if not KEYRING.keys:
        raise ValueError("GROQ_API_KEYS/GROQ_API_KEY is missing. Set it in .env or groq_keys.txt")
    client = None
    chunks, temp_dir = split_and_extract_audio(media_path, chunk_duration_sec=600)

    model_state = {
        "chunk_seconds": 600,
        "current_model": initial_model,
        "fallback_models": ["whisper-large-v3-turbo"] if initial_model == "whisper-large-v3" else [],
        "used_fallback": False
    }

    all_segments = []
    full_text_parts = []

    try:
        for i, (chunk_path, offset_sec) in enumerate(chunks, 1):
            size_mb = os.path.getsize(chunk_path) / (1024 * 1024)
            print(f"🎙 Transcribing chunk {i}/{len(chunks)} ({size_mb:.1f} MB, offset: {offset_sec:.1f}s, model: {model_state['current_model']})...")
            seg, text = transcribe_single_chunk(client, chunk_path, model_state, language, offset_sec)
            all_segments.extend(seg)
            full_text_parts.append(text)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    final_model = f"{model_state['current_model']} (fallback)" if model_state["used_fallback"] else model_state["current_model"]

    return {
        "audio_file": str(Path(media_path).resolve()),
        "model": final_model,
        "full_text": " ".join(full_text_parts),
        "timeline": all_segments
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_groq.py <media_path> [output_json]")
        sys.exit(1)
    res = transcribe_media(sys.argv[1])
    out_path = sys.argv[2] if len(sys.argv) > 2 else "transcript.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"Saved transcript to {out_path}")

#!/usr/bin/env python3
"""
extract_audio_ffmpeg.py — Ultra-fast video-to-audio extraction and chunking.
Uses ffmpeg with -vn flag and speech-optimized 16kHz mono 64kbps MP3 encoding.
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

MAX_FILE_SIZE_BYTES = 24 * 1024 * 1024  # 24 MB limit for Groq Whisper API

def split_and_extract_audio(media_path: str, chunk_duration_sec: int = 600):
    """
    Extracts speech-optimized mono MP3 audio from any video/audio file and splits it into chunks.
    CRITICAL: Always uses '-vn' to completely disable video decoding, reducing extraction time
    from 25+ minutes down to 2-3 seconds.
    """
    path = Path(media_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Media file not found: {media_path}")

    file_size_mb = path.stat().st_size / (1024 * 1024)
    print(f"🎬 Processing input media: {path.name} ({file_size_mb:.1f} MB)...")

    temp_dir = tempfile.mkdtemp(prefix="custdev_audio_")
    output_pattern = os.path.join(temp_dir, "chunk_%03d.mp3")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(path),
        "-vn",                           # Disable video stream processing (HUGE speedup)
        "-f", "segment",
        "-segment_time", str(chunk_duration_sec),
        "-ar", "16000",                  # 16kHz optimal speech sample rate
        "-ac", "1",                      # Mono channel
        "-b:a", "64k",                   # 64 kbps lightweight MP3
        output_pattern
    ]

    print(f"⚡ Fast audio extraction via ffmpeg (-vn, 16kHz mono)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if res.returncode != 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"FFmpeg audio extraction failed:\n{res.stderr}")

    chunk_files = sorted([
        os.path.join(temp_dir, f)
        for f in os.listdir(temp_dir)
        if f.startswith("chunk_") and f.endswith(".mp3")
    ])

    chunks_with_offsets = []
    for i, c_path in enumerate(chunk_files):
        offset = float(i * chunk_duration_sec)
        chunks_with_offsets.append((c_path, offset))

    print(f"✅ Extracted {len(chunks_with_offsets)} speech chunk(s) to temporary directory.")
    return chunks_with_offsets, temp_dir

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_audio_ffmpeg.py <video_or_audio_path>")
        sys.exit(1)
    chunks, tmp = split_and_extract_audio(sys.argv[1])
    for p, off in chunks:
        print(f"  Chunk: {p} (offset: {off}s, size: {os.path.getsize(p)/(1024*1024):.2f} MB)")
    shutil.rmtree(tmp, ignore_errors=True)

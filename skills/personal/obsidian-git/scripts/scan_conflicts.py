#!/usr/bin/env python3
"""Сканирует хранилище Obsidian на наличие неразрешенных маркеров конфликтов Git."""

import sys
import re
from pathlib import Path

CONFLICT_START = re.compile(r"^<{7}\s+(.*)")
CONFLICT_MID = re.compile(r"^={7}")
CONFLICT_END = re.compile(r"^>{7}\s+(.*)")

def scan_file(file_path: Path):
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    lines = content.splitlines()
    conflicts = []
    in_conflict = False
    start_line = 0

    for idx, line in enumerate(lines, start=1):
        if CONFLICT_START.match(line):
            in_conflict = True
            start_line = idx
        elif CONFLICT_END.match(line) and in_conflict:
            conflicts.append((start_line, idx))
            in_conflict = False

    return conflicts

def main():
    target_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    print(f"🔍 Сканирование хранилища на конфликты Git: {target_dir}")

    total_conflicts = 0
    conflicted_files = []

    for file_path in target_dir.rglob("*.md"):
        # Пропускаем служебные папки
        if ".git" in file_path.parts or ".trash" in file_path.parts:
            continue

        conflicts = scan_file(file_path)
        if conflicts:
            total_conflicts += len(conflicts)
            conflicted_files.append((file_path, conflicts))

    if not conflicted_files:
        print("✅ Маркеров конфликтов не обнаружено. Хранилище чисто.")
        return 0

    print(f"\n⚠️ Обнаружено конфликтов: {total_conflicts} в {len(conflicted_files)} файлах:")
    for fpath, ranges in conflicted_files:
        rel = fpath.relative_to(target_dir)
        lines_str = ", ".join([f"L{s}-L{e}" for s, e in ranges])
        print(f"  - 📄 {rel} (строки: {lines_str})")

    print("\n💡 Для разрешения откройте указанные файлы и удалите маркеры <<<<<<<, =======, >>>>>>>.")
    return 1

if __name__ == "__main__":
    sys.exit(main())

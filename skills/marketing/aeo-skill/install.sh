#!/usr/bin/env bash
# Установка навыка в Claude Code: копирует навыки и агентов в ~/.claude
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}"
mkdir -p "$DEST/skills" "$DEST/agents"
for d in "$SRC"/skills/*/; do
  name="$(basename "$d")"
  if [ -e "$DEST/skills/$name" ]; then
    mv "$DEST/skills/$name" "$DEST/skills/$name.bak.$(date +%Y%m%d%H%M%S)"
    echo "Прежняя версия $name сохранена рядом с пометкой .bak"
  fi
  cp -R "$d" "$DEST/skills/$name"
done
cp "$SRC"/agents/*.md "$DEST/agents/"
chmod +x "$DEST"/skills/aeo/scripts/*.py
command -v python3 >/dev/null || echo "Внимание: python3 не найден, скрипты работать не будут"
echo "Готово. Навыки: $(ls "$SRC/skills" | tr '\n' ' ')"
echo "Перезапусти Claude Code и набери: /aeo"

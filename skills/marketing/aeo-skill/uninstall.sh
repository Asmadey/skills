#!/usr/bin/env bash
# Удаление навыка: переносит файлы в ~/.claude/aeo-skill-removed, ничего не стирает
set -euo pipefail
DEST="${CLAUDE_HOME:-$HOME/.claude}"
TRASH="$DEST/aeo-skill-removed.$(date +%Y%m%d%H%M%S)"
mkdir -p "$TRASH/skills" "$TRASH/agents"
for n in aeo aeo-audit aeo-technical aeo-content aeo-entity aeo-offpage aeo-visibility aeo-measure aeo-local aeo-ecommerce aeo-refresh aeo-plan; do
  [ -e "$DEST/skills/$n" ] && mv "$DEST/skills/$n" "$TRASH/skills/"
done
for n in aeo-technical aeo-content aeo-entity aeo-offpage; do
  [ -e "$DEST/agents/$n.md" ] && mv "$DEST/agents/$n.md" "$TRASH/agents/"
done
echo "Навык отключён. Файлы перенесены в $TRASH — папку можно удалить вручную."

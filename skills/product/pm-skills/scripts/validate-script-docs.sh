#!/usr/bin/env bash
# validate-script-docs.sh
# Ensures every .sh/.ps1 script pair in scripts/ has a companion .md file.
# Convention: scripts/foo.sh + scripts/foo.ps1 → scripts/foo.md
set -euo pipefail

SCRIPTS_DIR="scripts"
MISSING=0
CHECKED=0

# Build list of unique script base names (strip .sh and .ps1 extensions)
BASES=()
for f in "$SCRIPTS_DIR"/*.sh "$SCRIPTS_DIR"/*.ps1; do
  [[ -f "$f" ]] || continue
  base=$(basename "$f")
  base="${base%.sh}"
  base="${base%.ps1}"
  # Skip README and this script's own name collision check
  [[ "$base" == "README_SCRIPTS" ]] && continue
  BASES+=("$base")
done

# Deduplicate
UNIQUE_BASES=($(printf '%s\n' "${BASES[@]}" | sort -u))

for base in "${UNIQUE_BASES[@]}"; do
  CHECKED=$((CHECKED + 1))
  DOC_FILE="$SCRIPTS_DIR/$base.md"
  if [[ ! -f "$DOC_FILE" ]]; then
    echo "FAIL: Missing companion doc: $DOC_FILE"
    # Show which script files exist for this base
    [[ -f "$SCRIPTS_DIR/$base.sh" ]] && echo "       Has: $base.sh"
    [[ -f "$SCRIPTS_DIR/$base.ps1" ]] && echo "       Has: $base.ps1"
    MISSING=$((MISSING + 1))
  fi
done

# Also check that README_SCRIPTS.md exists
if [[ ! -f "$SCRIPTS_DIR/README_SCRIPTS.md" ]]; then
  echo "FAIL: Missing $SCRIPTS_DIR/README_SCRIPTS.md"
  MISSING=$((MISSING + 1))
fi

if [[ $MISSING -eq 0 ]]; then
  echo "PASS: All $CHECKED script pairs have companion .md files"
  exit 0
else
  echo ""
  echo "FAIL: $MISSING script pair(s) missing companion .md documentation"
  echo "  Convention: scripts/foo.sh + scripts/foo.ps1 → scripts/foo.md"
  exit 1
fi

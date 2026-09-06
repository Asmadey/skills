#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <path-to-skill-or-git-url> [output-json]"
  exit 1
fi

REPORT_FILE="${2:-/tmp/skillspector-report.json}"
TEMP_DIR=""

cleanup() {
  if [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]]; then
    rm -rf "$TEMP_DIR"
  fi
}
trap cleanup EXIT

# If git URL, clone to isolated temp dir
if [[ "$TARGET" =~ ^https?:// ]] || [[ "$TARGET" =~ ^git@ ]]; then
  TEMP_DIR=$(mktemp -d /tmp/skill-audit-XXXXXX)
  echo "Cloning $TARGET into isolated temporary directory $TEMP_DIR..."
  git clone --depth 1 "$TARGET" "$TEMP_DIR" > /dev/null 2>&1
  SCAN_PATH="$TEMP_DIR"
else
  SCAN_PATH="$TARGET"
fi

echo "🔍 Running NVIDIA SkillSpector scan on: $SCAN_PATH"

SKILLSPECTOR_BIN=$(which skillspector 2>/dev/null || echo "$HOME/.local/bin/skillspector")

if [[ ! -x "$SKILLSPECTOR_BIN" ]]; then
  echo "❌ Error: skillspector executable not found. Install with: uv tool install /tmp/SkillSpector"
  exit 1
fi

"$SKILLSPECTOR_BIN" scan "$SCAN_PATH" --no-llm --format json --output "$REPORT_FILE" || true

if [[ -f "$REPORT_FILE" ]]; then
  echo "✅ Scan completed. Report saved to: $REPORT_FILE"
  # Quick summary extraction using Python
  python3 -c "
import json, sys

try:
    with open('$REPORT_FILE') as f:
        data = json.load(f)
    print('=' * 60)
    print('🛡️  SKILLSPECTOR AUDIT SUMMARY')
    print('=' * 60)
    print(f'Risk Score:     {data.get(\"risk_score\", \"N/A\")}/100')
    print(f'Severity:       {data.get(\"severity\", \"N/A\")}')
    print(f'Recommendation: {data.get(\"recommendation\", \"N/A\")}')
    findings = data.get(\"findings\", [])
    print(f'Findings count: {len(findings)}')
    high_crit = [f for f in findings if f.get(\"severity\") in [\"HIGH\", \"CRITICAL\"]]
    if high_crit:
        print('⚠️  CRITICAL / HIGH FINDINGS DETECTED:')
        for f in high_crit:
            print(f'  - [{f.get(\"severity\")}] {f.get(\"rule_id\")}: {f.get(\"message\")} ({f.get(\"location\", {}).get(\"file_path\", \"?\")})')
    else:
        print('✅ No CRITICAL or HIGH findings detected.')
    print('=' * 60)
except Exception as e:
    print('Could not parse summary:', e)
"
else
  echo "❌ Error: Report file was not generated."
  exit 1
fi

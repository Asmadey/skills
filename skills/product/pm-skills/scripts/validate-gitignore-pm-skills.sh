#!/usr/bin/env bash
# validate-gitignore-pm-skills.sh
# Ensures _pm-skills/ is in .gitignore so local state (update reports,
# backups) is never accidentally committed.
set -euo pipefail

if grep -q '^_pm-skills/' .gitignore 2>/dev/null || \
   grep -q '^_pm-skills$' .gitignore 2>/dev/null; then
  echo "PASS: _pm-skills/ is in .gitignore"
  exit 0
else
  echo "FAIL: _pm-skills/ is not in .gitignore"
  echo "  Add '_pm-skills/' to .gitignore to prevent committing local state"
  exit 1
fi

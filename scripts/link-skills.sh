#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

TARGET_DIRS=(
  "${HOME}/.claude/skills"
  "${HOME}/.agents/skills"
)

echo "Linking skills into local harnesses..."

for target_dir in "${TARGET_DIRS[@]}"; do
  mkdir -p "${target_dir}"
  echo "Target: ${target_dir}"

  # Link engineering and productivity skills
  for bucket in engineering productivity; do
    for skill_path in "${ROOT_DIR}/skills/${bucket}"/*; do
      if [ -d "${skill_path}" ]; then
        skill_name="$(basename "${skill_path}")"
        dest_link="${target_dir}/${skill_name}"
        if [ -L "${dest_link}" ] || [ -e "${dest_link}" ]; then
          rm -rf "${dest_link}"
        fi
        ln -s "${skill_path}" "${dest_link}"
        echo "  ✓ Linked ${skill_name} (${bucket})"
      fi
    done
  done
done

echo ""
echo "All promoted skills linked successfully!"

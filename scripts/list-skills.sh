#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "========================================================="
echo "               Asmadey's Agent Skills Library            "
echo "========================================================="

for cat_dir in "${ROOT_DIR}/public"/*; do
  if [ -d "${cat_dir}" ]; then
    cat_name="$(basename "${cat_dir}")"
    count=$(find "${cat_dir}" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
    echo ""
    cat_upper=$(echo "${cat_name}" | tr '[:lower:]' '[:upper:]')
    echo "📁 [${cat_upper}] (${count} skills)"
    echo "---------------------------------------------------------"
    for skill_dir in "${cat_dir}"/*; do
      if [ -d "${skill_dir}" ]; then
        skill_name="$(basename "${skill_dir}")"
        desc=""
        skill_file="${skill_dir}/SKILL.md"
        [ -f "${skill_file}" ] || skill_file="${skill_dir}/skill.md"
        if [ -f "${skill_file}" ]; then
          desc=$(awk '/^description:/{flag=1; next} /^[a-zA-Z0-9_-]+:/{flag=0} flag{gsub(/^[ \t>"-]+|["]+$/, ""); print; exit}' "${skill_file}" 2>/dev/null || echo "")
        fi
        [ -z "${desc}" ] && desc="Agent capability module"
        printf "  • %-32s : %s\n" "${skill_name}" "${desc:0:65}..."
      fi
    done
  fi
done

echo ""
echo "========================================================="
echo "Total public skills: $(find "${ROOT_DIR}/public" -mindepth 2 -maxdepth 2 -type d | wc -l | tr -d ' ')"
echo "Total frameworks: $(find "${ROOT_DIR}/frameworks" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
echo "========================================================="

#!/bin/bash
# Show Yandex Wordstat region tree via API
# Compatible with legacy OAuth and Yandex Cloud Search API v2.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

load_config

echo "=== Yandex Wordstat: Region Tree ==="
backend_info
echo ""
echo "Fetching region tree..."

result=$(wordstat_request "getRegionsTree" '{}')

# Check for error
if echo "$result" | grep -q '"error"'; then
    echo "Error:"
    echo "$result"
    exit 1
fi

echo ""
echo "=== Common Region IDs ==="
echo ""

# Try to extract known region IDs from tree
extract_region_id() {
    local label="$1"
    echo "$result" | grep -oB1 "\"label\":\"$label\"" | grep -o '"id":[0-9]*' | head -1 | sed 's/"id"://' || echo "?"
}

russia=$(extract_region_id "Россия")
moscow=$(extract_region_id "Москва")
spb=$(extract_region_id "Санкт-Петербург")
moscow_region=$(extract_region_id "Москва и область")

echo "Countries:"
echo "  ${russia:-225} - Россия"
echo ""
echo "Moscow Region:"
echo "  ${moscow_region:-1} - Москва и область"
echo "  ${moscow:-213} - Москва (город)"
echo "  10716 - Московская область"
echo ""
echo "Major Cities:"
echo "  ${spb:-2}   - Санкт-Петербург"
echo "  54   - Екатеринбург"
echo "  65   - Новосибирск"
echo "  43   - Казань"
echo "  35   - Краснодар"
echo "  47   - Нижний Новгород"
echo "  39   - Ростов-на-Дону"
echo "  51   - Самара"
echo "  172  - Уфа"
echo ""
echo "Use these IDs with --regions parameter in other scripts."
echo "Example: bash scripts/top_requests.sh --phrase \"test\" --regions ${moscow:-213}"

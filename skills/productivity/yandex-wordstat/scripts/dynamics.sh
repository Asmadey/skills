#!/bin/bash
# Get search volume dynamics from Yandex Wordstat
# Compatible with legacy OAuth and Yandex Cloud Search API v2.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Defaults
PHRASE=""
PERIOD="monthly"
FROM_DATE=""
TO_DATE=""
REGIONS=""
DEVICES="all"

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --phrase|-p) PHRASE="$2"; shift 2 ;;
        --period) PERIOD="$2"; shift 2 ;;
        --from-date|-f) FROM_DATE="$2"; shift 2 ;;
        --to-date|-t) TO_DATE="$2"; shift 2 ;;
        --regions|-r) REGIONS="$2"; shift 2 ;;
        --devices|-d) DEVICES="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "$PHRASE" ]]; then
    echo "Usage: dynamics.sh --phrase \"search query\" [options]"
    echo ""
    echo "Options:"
    echo "  --phrase, -p    Search phrase (required)"
    echo "  --period        Grouping: daily, weekly, monthly (default: monthly)"
    echo "  --from-date, -f Start date YYYY-MM-DD (default: 1 year ago)"
    echo "  --to-date, -t   End date YYYY-MM-DD (default: last day of current month)"
    echo "  --regions, -r   Region IDs, comma-separated (optional)"
    echo "  --devices, -d   Device filter: all, desktop, phone, tablet (default: all)"
    echo ""
    echo "Examples:"
    echo "  bash scripts/dynamics.sh --phrase \"юрист дтп\" --from-date 2025-01-01"
    echo "  bash scripts/dynamics.sh --phrase \"юрист\" --period weekly --from-date 2025-06-01"
    exit 1
fi

# Set default dates
if [[ -z "$FROM_DATE" ]]; then
    FROM_DATE=$(date -v-1y +%Y-%m-%d 2>/dev/null || date -d "1 year ago" +%Y-%m-%d 2>/dev/null || echo "2025-01-01")
fi

if [[ -z "$TO_DATE" ]]; then
    TO_DATE=$(date +%Y-%m-%d)
fi

load_config

# Escape phrase for JSON
PHRASE_ESCAPED=$(json_escape "$PHRASE")

# Build JSON params
if [[ "$WORDSTAT_BACKEND" == "cloud" ]]; then
    cloud_period=$(translate_period "$PERIOD")
    cloud_from=$(to_rfc3339 "$FROM_DATE")

    # Cloud monthly requires toDate to be the last day of the month
    if [[ "$cloud_period" == "PERIOD_MONTHLY" ]]; then
        cloud_to_date=$(last_day_of_month "$TO_DATE")
        cloud_to=$(to_rfc3339 "$cloud_to_date" "23:59:59Z")
    else
        cloud_to=$(to_rfc3339 "$TO_DATE" "23:59:59Z")
    fi

    PARAMS="{\"phrase\":\"$PHRASE_ESCAPED\",\"period\":\"$cloud_period\",\"fromDate\":\"$cloud_from\",\"toDate\":\"$cloud_to\""

    if [[ -n "$REGIONS" ]]; then
        PARAMS="$PARAMS,\"regionIds\":[$REGIONS]"
    fi

    cloud_devices=$(translate_devices "$DEVICES")
    if [[ -n "$cloud_devices" ]]; then
        PARAMS="$PARAMS,\"devices\":\"$cloud_devices\""
    fi
else
    PARAMS="{\"phrase\":\"$PHRASE_ESCAPED\",\"period\":\"$PERIOD\",\"fromDate\":\"$FROM_DATE\""

    if [[ -n "$TO_DATE" ]]; then
        PARAMS="$PARAMS,\"toDate\":\"$TO_DATE\""
    fi

    if [[ -n "$REGIONS" ]]; then
        PARAMS="$PARAMS,\"regions\":[$REGIONS]"
    fi

    if [[ "$DEVICES" != "all" ]]; then
        PARAMS="$PARAMS,\"devices\":\"$DEVICES\""
    fi
fi

PARAMS="$PARAMS}"

echo "=== Yandex Wordstat: Dynamics ==="
backend_info
echo "Phrase: $PHRASE"
echo "Period: $PERIOD"
echo "From: $FROM_DATE"
echo "To: $TO_DATE"
[[ -n "$REGIONS" ]] && echo "Regions: $REGIONS"
echo "Devices: $DEVICES"
echo ""
echo "Fetching data..."

result=$(wordstat_request "dynamics" "$PARAMS")

# Check for error
if echo "$result" | grep -q '"error"'; then
    echo "Error:"
    echo "$result"
    exit 1
fi

echo ""
echo "=== Results ==="
echo ""

echo "| Date | Count |"
echo "|------|-------|"

# Extract dynamics data
echo "$result" | grep -o '{"date":"[^"]*","count":[0-9]*' | while IFS= read -r entry; do
    dt=$(echo "$entry" | grep -o '"date":"[^"]*"' | sed 's/"date":"//' | tr -d '"' | cut -dT -f1)
    cnt=$(echo "$entry" | grep -o '"count":[0-9]*' | sed 's/"count"://')

    echo "| $dt | $(format_number "$cnt") |"
done

echo ""
echo "=== Raw JSON ==="
echo "$result" | head -c 2000
echo ""
echo "[truncated if > 2000 chars]"

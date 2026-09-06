#!/bin/bash
# Common functions for Yandex Wordstat API
# Supports both legacy OAuth (api.wordstat.yandex.net/v1) and
# Yandex Cloud Search API v2 (searchapi.api.cloud.yandex.net/v2/wordstat).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config/.env"
CACHE_DIR="$SCRIPT_DIR/../cache"
NORMALIZE_SCRIPT="$SCRIPT_DIR/ws_normalize.py"

# Legacy
LEGACY_API_URL="https://api.wordstat.yandex.net/json/v5/"
LEGACY_WS_URL="https://api.wordstat.yandex.net/v1"

# Cloud
CLOUD_API_URL="https://searchapi.api.cloud.yandex.net/v2/wordstat"

# Backend selector
WORDSTAT_BACKEND=""

# Load config
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        # shellcheck disable=SC1090
        source "$CONFIG_FILE"
    fi

    # Prefer explicit env override
    if [[ -n "$YANDEX_WORDSTAT_BACKEND" ]]; then
        WORDSTAT_BACKEND="$YANDEX_WORDSTAT_BACKEND"
    elif [[ -n "$YANDEX_WORDSTAT_API_KEY" ]]; then
        WORDSTAT_BACKEND="cloud"
    elif [[ -n "$YANDEX_WORDSTAT_TOKEN" ]]; then
        WORDSTAT_BACKEND="legacy"
    fi

    if [[ -z "$WORDSTAT_BACKEND" ]]; then
        echo "Error: No Wordstat credentials found."
        echo "Set YANDEX_WORDSTAT_API_KEY (recommended) or YANDEX_WORDSTAT_TOKEN in config/.env."
        echo "See config/README.md for instructions."
        exit 1
    fi

    if [[ "$WORDSTAT_BACKEND" == "cloud" && -z "$YANDEX_WORDSTAT_API_KEY" ]]; then
        echo "Error: cloud backend selected but YANDEX_WORDSTAT_API_KEY is empty."
        exit 1
    fi

    if [[ "$WORDSTAT_BACKEND" == "legacy" && -z "$YANDEX_WORDSTAT_TOKEN" ]]; then
        echo "Error: legacy backend selected but YANDEX_WORDSTAT_TOKEN is empty."
        exit 1
    fi
}

# Normalize cloud response to legacy-like shape using Python (handles pretty-printed JSON).
# Usage: normalize_response "method" "json"
normalize_response() {
    local method="$1"
    local json="$2"

    printf '%s\n' "$json" | python3 "$NORMALIZE_SCRIPT" "$method"
}

# Make a request to the appropriate Wordstat backend.
# Usage: wordstat_request "method" "params_json"
# Methods: topRequests, dynamics, regions, getRegionsTree
wordstat_request() {
    local method="$1"
    local params="$2"

    if [[ "$WORDSTAT_BACKEND" == "cloud" ]]; then
        _cloud_request "$method" "$params"
    else
        _legacy_request "$method" "$params"
    fi
}

_cloud_request() {
    local method="$1"
    local params="$2"

    local ws_url="$CLOUD_API_URL/$method"

    local response
    response=$(curl -s -X POST "$ws_url" \
        -H "Authorization: Api-Key $YANDEX_WORDSTAT_API_KEY" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "$params")

    # Normalize so downstream scripts see legacy-like JSON
    normalize_response "$method" "$response"
}

_legacy_request() {
    local method="$1"
    local params="$2"

    local ws_url="$LEGACY_WS_URL/$method"

    curl -k -s -X POST "$ws_url" \
        -H "Authorization: Bearer $YANDEX_WORDSTAT_TOKEN" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "$params"
}

# Translate legacy --devices values to cloud if needed
translate_devices() {
    local devices="$1"
    if [[ "$WORDSTAT_BACKEND" == "cloud" ]]; then
        case "$devices" in
            desktop) echo "DEVICE_DESKTOP" ;;
            phone)   echo "DEVICE_PHONE" ;;
            tablet)  echo "DEVICE_TABLET" ;;
            *)       echo "" ;;
        esac
    else
        echo "$devices"
    fi
}

# Translate legacy period values to cloud
translate_period() {
    local period="$1"
    if [[ "$WORDSTAT_BACKEND" == "cloud" ]]; then
        case "$period" in
            daily)   echo "PERIOD_DAILY" ;;
            weekly)  echo "PERIOD_WEEKLY" ;;
            monthly) echo "PERIOD_MONTHLY" ;;
            *)       echo "PERIOD_MONTHLY" ;;
        esac
    else
        echo "$period"
    fi
}

# Convert YYYY-MM-DD to RFC3339 (cloud requires full timestamp)
to_rfc3339() {
    local date_str="$1"
    local time_str="${2:-00:00:00Z}"
    echo "${date_str}T${time_str}"
}

# Last day of month for given YYYY-MM-DD
last_day_of_month() {
    local date_str="$1"
    local y m
    y=$(echo "$date_str" | cut -d- -f1)
    m=$(echo "$date_str" | cut -d- -f2)
    local next_month first_day last_day
    if [[ "$m" -eq 12 ]]; then
        next_month=$((y + 1))-01-01
    else
        next_month=$y-$(printf "%02d" $((m + 1)))-01
    fi
    first_day=$(date -j -f "%Y-%m-%d" "$next_month" +%s 2>/dev/null || date -d "$next_month" +%s 2>/dev/null)
    last_day=$((first_day - 86400))
    date -j -r "$last_day" "+%Y-%m-%d" 2>/dev/null || date -d "@$last_day" "+%Y-%m-%d" 2>/dev/null
}

# Extract JSON value using grep/sed (no jq dependency)
# Usage: json_value "$json" "key"
json_value() {
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\"$key\":[^,}]*" | head -1 | sed 's/.*://' | tr -d '"[:space:]'
}

# Extract JSON string value (handles strings with quotes)
json_string() {
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\"$key\":\"[^\"]*\"" | head -1 | sed 's/.*://' | tr -d '"'
}

# Extract JSON array
json_array() {
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\"$key\":\[[^]]*\]" | head -1 | sed 's/.*:\[/[/' | sed 's/\]/]/' | head -1
}

# Escape string for JSON
json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

# Format number with thousands separator (macOS compatible)
format_number() {
    local num="$1"
    printf "%'d" "$num" 2>/dev/null || echo "$num"
}

# Echo backend in use for diagnostics
backend_info() {
    echo "Backend: $WORDSTAT_BACKEND"
    if [[ "$WORDSTAT_BACKEND" == "cloud" ]]; then
        echo "API: $CLOUD_API_URL"
    else
        echo "API: $LEGACY_WS_URL"
    fi
}

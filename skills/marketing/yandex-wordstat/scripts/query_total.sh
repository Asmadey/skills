#!/bin/sh
# Get totalCount from Yandex Wordstat API for an OR-query.
# Works with both legacy OAuth and Yandex Cloud Search API v2.
#
# Usage:
#   bash scripts/query_total.sh --phrase "(купить|заказать) телефон ретро" [--regions "213"]
#
# Output: JSON {"total_count": N, "query": "..."} or {"error": "...", "query": "..."}

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
load_config

# Parse arguments
PHRASE=""
REGIONS=""

while [ $# -gt 0 ]; do
    case $1 in
        --phrase|-p) PHRASE="$2"; shift 2 ;;
        --regions|-r) REGIONS="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$PHRASE" ]; then
    echo "Usage: query_total.sh --phrase \"(a|b) query\" [--regions \"213\"]"
    echo ""
    echo "Options:"
    echo "  --phrase, -p   Search phrase with operators and minus-words (required)"
    echo "  --regions, -r  Region IDs, comma-separated (optional)"
    echo ""
    echo "Output: JSON with total_count"
    exit 1
fi

# Use topRequests with numPhrases=1 to get totalCount quickly
PHRASE_ESCAPED=$(json_escape "$PHRASE")
PARAMS="{\"phrase\":\"$PHRASE_ESCAPED\",\"numPhrases\":1"

if [ -n "$REGIONS" ]; then
    PARAMS="$PARAMS,\"regionIds\":[$REGIONS]"
fi

PARAMS="$PARAMS}"

response=$(wordstat_request "topRequests" "$PARAMS")

if echo "$response" | grep -q '"error"'; then
    echo "{\"error\": $(echo "$response" | tr -d '\n\r'), \"query\": \"$PHRASE\"}"
    exit 1
fi

total_count=$(echo "$response" | grep -o '"totalCount":[0-9]*' | head -1 | sed 's/"totalCount"://')

if [ -z "$total_count" ]; then
    echo "{\"error\": \"totalCount not found\", \"query\": \"$PHRASE\"}"
    exit 1
fi

echo "{\"total_count\": $total_count, \"query\": \"$PHRASE\"}"

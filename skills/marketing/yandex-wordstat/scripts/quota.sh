#!/bin/bash
# Check Yandex Wordstat API connection
# Compatible with legacy OAuth and Yandex Cloud Search API v2.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

load_config

echo "Checking Wordstat API connection..."
echo ""

backend_info
echo ""

# Test with a small topRequests query
response=$(wordstat_request "topRequests" '{"phrase":"тест","numPhrases":1}')

if echo "$response" | grep -q '"topRequests"'; then
    echo "Wordstat API: OK"
    echo ""

    top_count=$(echo "$response" | grep -o '"topRequests":\[' | wc -l | tr -d ' ')
    echo "Test query returned topRequests data"
else
    echo "Wordstat API: Error"
    echo "$response"
    exit 1
fi

echo ""
echo "=== API Limits ==="
echo "- Rate limit: 10 requests/second"
echo "- Daily quota: 1000 requests"
echo ""
echo "=== Available endpoints ==="
echo "- /v2/wordstat/topRequests (cloud) / /v1/topRequests (legacy)"
echo "- /v2/wordstat/dynamics   (cloud) / /v1/dynamics   (legacy)"
echo "- /v2/wordstat/regions    (cloud) / /v1/regions    (legacy)"
echo ""
echo "API is accessible."

#!/bin/sh
# Get or refresh IAM token for Yandex Cloud via OAuth token
# Zero external dependencies: python3 stdlib + curl

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

load_config

OAUTH_TOKEN=$(cfg_get "auth.yandex_passport_oauth_token")
if [ -z "$OAUTH_TOKEN" ]; then
    echo "Error: auth.yandex_passport_oauth_token not set in config.json" >&2
    exit 1
fi

echo "Generating new IAM token via OAuth..." >&2

IAM_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "{\"yandexPassportOauthToken\": \"$OAUTH_TOKEN\"}" \
    https://iam.api.cloud.yandex.net/iam/v1/tokens)

if [ -z "$IAM_RESPONSE" ]; then
    echo "Error: Empty response from IAM API" >&2
    exit 1
fi

# Extract token and expiry
IAM_RESULT=$(echo "$IAM_RESPONSE" | python3 -c "
import json, sys
from datetime import datetime

d = json.load(sys.stdin)
token = d.get('iamToken', '')
expires_at_str = d.get('expiresAt', '')

if not token:
    print('ERROR: No iamToken in response', file=sys.stderr)
    print(json.dumps(d), file=sys.stderr)
    sys.exit(1)

# Parse RFC3339 expiresAt to unix timestamp
if expires_at_str:
    ts = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00')).timestamp()
    expires_at = int(ts)
else:
    import time
    expires_at = int(time.time()) + 43200

print(f'{token}|{expires_at}')
")

IAM_TOKEN=$(echo "$IAM_RESULT" | cut -d'|' -f1)
EXPIRES_AT=$(echo "$IAM_RESULT" | cut -d'|' -f2)

if [ -z "$IAM_TOKEN" ]; then
    echo "Error: Failed to extract IAM token" >&2
    exit 1
fi

# Save to cache (atomic via common.sh function if available, or manual)
# Note: save_iam_token is defined in common.sh
save_iam_token "$IAM_TOKEN" "$EXPIRES_AT"

echo "IAM token generated via OAuth and cached successfully."

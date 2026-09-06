#!/usr/bin/env python3
# Normalize Yandex Cloud Search API v2 Wordstat responses to legacy-like shape.
# Used by common.sh so existing shell scripts can stay unchanged.

import sys, json, re

method = sys.argv[1]
s = sys.stdin.read()

# Convert string counts/ids to numbers
s = re.sub(r'"count"\s*:\s*"([0-9]+)"', r'"count": \1', s)
s = re.sub(r'"totalCount"\s*:\s*"([0-9]+)"', r'"totalCount": \1', s)
# Cloud regions returns "region" as a numeric string; normalize after renaming.

# Cloud topRequests returns "results"; legacy uses "topRequests"
if method == 'topRequests' and '"results"' in s:
    s = s.replace('"results"', '"topRequests"', 1)

# Cloud regions returns "region" (string); legacy uses "regionId" (number)
if method == 'regions':
    s = s.replace('"region"', '"regionId"')
    s = re.sub(r'"regionId"\s*:\s*"([0-9]+)"', r'"regionId": \1', s)

# Compact output for downstream grep/sed parsing, preserve non-ASCII chars
print(json.dumps(json.loads(s), separators=(',', ':'), ensure_ascii=False))

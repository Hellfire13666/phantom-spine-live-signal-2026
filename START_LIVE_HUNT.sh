#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
printf '%s\n' '[PHANTOM SPINE] Starting genuine public HTTPS DNS lookup for example.com.'
printf '%s\n' '[NOTICE] This sends the public domain example.com to Google and Cloudflare DNS-over-HTTPS endpoints.'
exec bash "$HERE/START_PHANTOM_SPINE_LIVE.sh" hunt example.com --engine native --providers dns --timeout 5

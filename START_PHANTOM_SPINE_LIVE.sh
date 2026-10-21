#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
if [ "$#" -eq 0 ]; then
  set -- start
fi
exec python3 -B "$HERE/phantom_spine_live_v0_2_0.py" "$@"

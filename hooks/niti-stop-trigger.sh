#!/usr/bin/env bash
# Cursor `stop` hook: record event + optional NITI followup_message when thresholds hit.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../scripts/niti/stop_trigger.py" ]]; then
  PY="$SCRIPT_DIR/../scripts/niti/stop_trigger.py"
elif [[ -f "${HOME}/.cursor/scripts/niti/stop_trigger.py" ]]; then
  PY="${HOME}/.cursor/scripts/niti/stop_trigger.py"
else
  echo '{}'
  exit 0
fi

python3 "$PY" || echo '{}'
exit 0

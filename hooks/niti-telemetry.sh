#!/usr/bin/env bash
# Record redacted Cursor hook events for NITI. Fail-open. No secrets/source bodies.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Prefer kit scripts when running from repo; fall back to ~/.cursor
if [[ -f "$SCRIPT_DIR/../scripts/niti/record_event.py" ]]; then
  REC="$SCRIPT_DIR/../scripts/niti/record_event.py"
elif [[ -f "${HOME}/.cursor/scripts/niti/record_event.py" ]]; then
  REC="${HOME}/.cursor/scripts/niti/record_event.py"
else
  # fail open
  echo '{}'
  exit 0
fi

python3 "$REC" || echo '{}'
exit 0

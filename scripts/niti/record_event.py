#!/usr/bin/env python3
"""Append a redacted Cursor hook event to NITI events.jsonl. Reads JSON from stdin."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import append_jsonl, ensure_layout, new_id, niti_home, redact_hook_payload  # noqa: E402


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        # fail open for hooks
        print("{}")
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print("{}")
        return 0
    home = ensure_layout(niti_home())
    event = redact_hook_payload(payload if isinstance(payload, dict) else {})
    event["event_id"] = event.get("event_id") or new_id("evt")
    append_jsonl(home / "logs" / "events.jsonl", event)
    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

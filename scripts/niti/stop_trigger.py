#!/usr/bin/env python3
"""
Cursor `stop` hook helper for NITI.

Reads hook stdin JSON, optionally records a provisional signal, and may emit
followup_message when a pending NITI trigger exists.

Does NOT claim cron/scheduling. Only runs when Cursor fires `stop`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import (  # noqa: E402
    append_jsonl,
    ensure_layout,
    niti_home,
    redact_hook_payload,
    should_invoke,
)

FOLLOWUPS = {
    "lightweight": (
        "NITI trigger: lightweight review. "
        "Run the niti agent on recent telemetry under $KESH_NITI_HOME or ~/.cursor/niti. "
        "Use: python3 scripts/niti/analyze_prep.py --mode lightweight "
        "then produce a human-readable system health report. "
        "Do not modify product application code. "
        "After analysis run: python3 scripts/niti/consume_trigger.py --mode lightweight"
    ),
    "deep": (
        "NITI trigger: deep audit (20 meaningful tasks). "
        "Run niti with --mode deep via analyze_prep.py. "
        "Include recommendation backlog review and agent usefulness vs frequency. "
        "Do not auto-edit agents or rules. "
        "After analysis: python3 scripts/niti/consume_trigger.py --mode deep"
    ),
    "post_incident": (
        "NITI trigger: post-incident analysis. "
        "Inspect recent FAILED/BLOCKED executions and tool failures in NITI logs. "
        "Produce failure-pattern report. Do not auto-mutate the kit. "
        "After analysis: python3 scripts/niti/consume_trigger.py --mode post_incident"
    ),
}


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print("{}")
        return 0

    home = ensure_layout(niti_home())
    event = redact_hook_payload(payload if isinstance(payload, dict) else {})
    event["hook_event_name"] = event.get("hook_event_name") or "stop"
    append_jsonl(home / "logs" / "events.jsonl", event)

    # Only nudge on completed agent loops — not aborted mid-flight spam
    status = (payload.get("status") or "").lower()
    loop_count = int(payload.get("loop_count") or 0)

    decision = should_invoke(home)
    out: dict = {}

    if (
        decision.get("invoke")
        and decision.get("mode") in FOLLOWUPS
        and status in {"completed", "error"}
        and loop_count == 0
    ):
        # loop_count==0: first stop in this auto-followup chain — avoid NITI→NITI loops
        out["followup_message"] = FOLLOWUPS[decision["mode"]]

    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a machine-readable context bundle for the NITI agent (not the human report)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import (  # noqa: E402
    compute_agent_stats,
    detect_repeated_failures,
    detect_unnecessary_invocations,
    ensure_layout,
    load_jsonl,
    niti_home,
    read_json,
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--mode",
        default="lightweight",
        choices=["lightweight", "deep", "post_incident", "before_after", "on_demand"],
    )
    p.add_argument("--limit", type=int, default=0, help="Override execution window size")
    p.add_argument("--before-tag", help="kit_change_tag for before window")
    p.add_argument("--after-tag", help="kit_change_tag for after window")
    args = p.parse_args()

    home = ensure_layout(niti_home())
    executions = load_jsonl(home / "logs" / "executions.jsonl")
    events = load_jsonl(home / "logs" / "events.jsonl")
    recommendations = load_jsonl(home / "recommendations.jsonl")
    state = read_json(home / "state.json", {})

    default_limits = {
        "lightweight": 20,
        "deep": 100,
        "post_incident": 30,
        "before_after": 50,
        "on_demand": 50,
    }
    limit = args.limit or default_limits[args.mode]
    window = executions[-limit:]

    analyzed = set(state.get("analyzed_execution_ids") or [])
    unanalyzed = [e for e in window if e.get("execution_id") not in analyzed]

    stats = compute_agent_stats(window)
    repeated = []
    for agent in stats:
        hit = detect_repeated_failures(window, agent, min_count=3)
        if hit:
            repeated.append(hit)

    unavailable = []
    if any(not e.get("token_usage_available") for e in window):
        unavailable.append("token_usage")
    if any(not e.get("cost_available") for e in window):
        unavailable.append("cost_usd")
    if any((e.get("test_results") or {}).get("unknown") for e in window):
        unavailable.append("test_results_detail")
    if any((e.get("review_findings") or {}).get("unknown") for e in window):
        unavailable.append("review_findings_detail")
    if any(e.get("success") is None for e in window):
        unavailable.append("success_boolean_for_some_rows")

    bundle = {
        "mode": args.mode,
        "niti_home": str(home),
        "state": state,
        "execution_count_in_window": len(window),
        "unanalyzed_count": len(unanalyzed),
        "executions": window,
        "recent_events_count": len(events[-200:]),
        "recent_tool_failures": [
            e
            for e in events[-200:]
            if e.get("hook_event_name") == "postToolUseFailure"
            or e.get("failure_type")
        ],
        "agent_stats": stats,
        "repeated_failures": repeated,
        "unnecessary_invocation_flags": detect_unnecessary_invocations(window),
        "recommendations_open": [
            r
            for r in recommendations
            if (r.get("status") or "").upper() in {"PROPOSED", "APPROVED", "IMPLEMENTED", "EVALUATED"}
        ],
        "evidence_limitations": sorted(set(unavailable)),
        "notes": [
            "Missing fields must not be treated as success.",
            "Billing tokens/cost are unavailable from Cursor Agent Chat hooks.",
            "Human report must be natural language; this JSON is the sidecar.",
        ],
    }

    if args.mode == "before_after" and args.before_tag and args.after_tag:
        before = [e for e in executions if e.get("kit_change_tag") == args.before_tag]
        after = [e for e in executions if e.get("kit_change_tag") == args.after_tag]
        from lib import before_after_compare

        bundle["before_after"] = before_after_compare(before, after)
        bundle["before_tag"] = args.before_tag
        bundle["after_tag"] = args.after_tag

    print(json.dumps(bundle, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

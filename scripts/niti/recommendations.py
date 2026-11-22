#!/usr/bin/env python3
"""Track NITI recommendations through PROPOSED → … → ACCEPTED|REVERTED."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import append_jsonl, ensure_layout, load_jsonl, new_id, niti_home, utc_now  # noqa: E402

ALLOWED = [
    "PROPOSED",
    "APPROVED",
    "IMPLEMENTED",
    "EVALUATED",
    "ACCEPTED",
    "REVERTED",
]
TRANSITIONS = {
    "PROPOSED": {"APPROVED", "REVERTED"},
    "APPROVED": {"IMPLEMENTED", "REVERTED"},
    "IMPLEMENTED": {"EVALUATED", "REVERTED"},
    "EVALUATED": {"ACCEPTED", "REVERTED"},
    "ACCEPTED": set(),
    "REVERTED": set(),
}


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add")
    add.add_argument("--file", help="JSON file with recommendation body")
    add.add_argument("--json", help="Inline JSON")

    adv = sub.add_parser("advance")
    adv.add_argument("--id", required=True)
    adv.add_argument("--status", required=True, choices=ALLOWED)
    adv.add_argument("--note", default="")

    sub.add_parser("list")

    args = p.parse_args()
    home = ensure_layout(niti_home())
    path = home / "recommendations.jsonl"

    if args.cmd == "add":
        raw = Path(args.file).read_text(encoding="utf-8") if args.file else args.json
        if not raw:
            print(json.dumps({"status": "error", "error": "need --file or --json"}))
            return 1
        body = json.loads(raw)
        required = [
            "observed_problem",
            "evidence",
            "root_cause_or_hypothesis",
            "proposed_change",
            "expected_benefit",
            "risks_and_tradeoffs",
            "success_metric",
        ]
        missing = [k for k in required if not body.get(k)]
        if missing:
            print(json.dumps({"status": "error", "error": f"missing fields: {missing}"}))
            return 1
        rec = {
            "recommendation_id": body.get("recommendation_id") or new_id("rec"),
            "status": "PROPOSED",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "history": [{"status": "PROPOSED", "at": utc_now(), "note": "created"}],
            **{k: body[k] for k in required},
            "priority": body.get("priority") or "MEDIUM",
        }
        append_jsonl(path, rec)
        print(json.dumps({"status": "added", "recommendation": rec}, indent=2))
        return 0

    rows = load_jsonl(path)

    if args.cmd == "list":
        print(json.dumps(rows, indent=2))
        return 0

    if args.cmd == "advance":
        target = None
        for r in rows:
            if r.get("recommendation_id") == args.id:
                target = r
                break
        if not target:
            print(json.dumps({"status": "error", "error": "not found"}))
            return 1
        cur = (target.get("status") or "PROPOSED").upper()
        nxt = args.status.upper()
        if nxt not in TRANSITIONS.get(cur, set()):
            print(
                json.dumps(
                    {
                        "status": "error",
                        "error": f"illegal transition {cur} → {nxt}",
                        "allowed": sorted(TRANSITIONS.get(cur, set())),
                    }
                )
            )
            return 1
        # rewrite file with updated row (simple rewrite — local small store)
        target["status"] = nxt
        target["updated_at"] = utc_now()
        hist = list(target.get("history") or [])
        hist.append({"status": nxt, "at": utc_now(), "note": args.note})
        target["history"] = hist
        with path.open("w", encoding="utf-8") as f:
            for r in rows:
                if r.get("recommendation_id") == args.id:
                    f.write(json.dumps(target, sort_keys=True) + "\n")
                else:
                    f.write(json.dumps(r, sort_keys=True) + "\n")
        print(json.dumps({"status": "advanced", "recommendation": target}, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

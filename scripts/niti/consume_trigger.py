#!/usr/bin/env python3
"""Mark a NITI trigger consumed and optionally record analyzed execution ids."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ensure_layout, mark_trigger_consumed, niti_home  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--mode",
        required=True,
        choices=["lightweight", "deep", "post_incident", "before_after", "on_demand"],
    )
    p.add_argument(
        "--analyzed-ids",
        default="",
        help="Comma-separated execution_ids included in this analysis",
    )
    args = p.parse_args()
    ids = [x.strip() for x in args.analyzed_ids.split(",") if x.strip()]
    home = ensure_layout(niti_home())
    mark_trigger_consumed(home, args.mode, ids or None)
    print(json.dumps({"status": "consumed", "mode": args.mode, "analyzed_ids": ids}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

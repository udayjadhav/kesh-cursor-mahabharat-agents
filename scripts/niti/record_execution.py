#!/usr/bin/env python3
"""Record a meaningful Kesh execution into NITI telemetry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ensure_layout, niti_home, record_execution  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="Record a NITI execution record")
    p.add_argument("--file", "-f", help="JSON file (default: stdin)")
    p.add_argument("--json", "-j", help="Inline JSON string")
    args = p.parse_args()

    if args.file:
        raw = Path(args.file).read_text(encoding="utf-8")
    elif args.json:
        raw = args.json
    else:
        raw = sys.stdin.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "error": f"invalid json: {e}"}))
        return 1

    home = ensure_layout(niti_home())
    result = record_execution(home, data)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

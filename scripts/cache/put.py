#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ensure_cache, put_entry  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f")
    p.add_argument("--json", "-j")
    args = p.parse_args()
    raw = Path(args.file).read_text(encoding="utf-8") if args.file else args.json or sys.stdin.read()
    entry = json.loads(raw)
    home = ensure_cache()
    result = put_entry(home, entry)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())

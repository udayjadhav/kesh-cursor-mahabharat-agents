#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ensure_cache, invalidate  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fingerprint")
    p.add_argument("--all", action="store_true")
    args = p.parse_args()
    home = ensure_cache()
    result = invalidate(home, args.fingerprint, all_entries=args.all)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") in {"invalidated", "cleared_all"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ensure_cache, get_entry  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fingerprint", required=True)
    args = p.parse_args()
    home = ensure_cache()
    print(json.dumps(get_entry(home, args.fingerprint), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

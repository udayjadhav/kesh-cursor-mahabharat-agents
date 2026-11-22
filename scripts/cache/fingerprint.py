#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import fingerprint  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--topic", required=True)
    p.add_argument("--input-type", required=True)
    p.add_argument("--entities", default="", help="Comma-separated")
    p.add_argument("--code-revision", default="n/a")
    args = p.parse_args()
    ents = [x.strip() for x in args.entities.split(",") if x.strip()]
    fp = fingerprint(args.topic, args.input_type, ents, args.code_revision)
    print(json.dumps({"fingerprint": fp}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

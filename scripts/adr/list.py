#!/usr/bin/env python3
"""List ADRs with status/title for retrieval before major design work."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="docs/architecture/decisions")
    args = p.parse_args()
    d = Path(args.dir)
    rows = []
    if d.exists():
        for path in sorted(d.glob("ADR-*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            title = text.splitlines()[0].lstrip("# ").strip() if text else path.name
            status = "unknown"
            m = re.search(r"^## Status\s*\n+\s*(\S+)", text, re.M)
            if m:
                status = m.group(1)
            rows.append({"path": str(path), "title": title, "status": status})
    print(json.dumps({"adrs": rows, "note": "Re-validate ADRs against current repo revision"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Create a numbered ADR stub under docs/architecture/decisions/ (or --dir)."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

TEMPLATE = """# ADR-{num}: {title}

## Status
Proposed

## Date
{today}

## Context
What is going on?

## Problem
What decision is needed?

## Options considered
1. …
2. …
3. Option 0 — reuse-only (if data/schema involved)

## Decision
What we choose.

## Rationale
Why.

## Consequences
Operational and technical effects.

## Risks
What could go wrong?

## Alternatives rejected
…

## Related modules
…

## Review conditions
Re-validate when: repo fingerprint / key contracts change.
"""


def next_num(dir_path: Path) -> int:
    nums = []
    for p in dir_path.glob("ADR-*.md"):
        m = re.match(r"ADR-(\d+)", p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--dir", default="docs/architecture/decisions")
    args = p.parse_args()
    d = Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    n = next_num(d)
    slug = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")[:60]
    path = d / f"ADR-{n:04d}-{slug}.md"
    path.write_text(
        TEMPLATE.format(num=f"{n:04d}", title=args.title, today=date.today().isoformat()),
        encoding="utf-8",
    )
    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

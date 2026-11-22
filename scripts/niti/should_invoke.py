#!/usr/bin/env python3
"""Print whether NITI should run and at what depth."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ensure_layout, niti_home, should_invoke  # noqa: E402


def main() -> int:
    home = ensure_layout(niti_home())
    print(json.dumps(should_invoke(home), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

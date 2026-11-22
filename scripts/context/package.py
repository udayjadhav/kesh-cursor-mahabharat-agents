#!/usr/bin/env python3
"""Build a per-agent context package and report size (token proxy = chars/4)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_package(raw: dict) -> dict:
    pkg = {
        "agent": raw.get("agent") or "unknown",
        "execution_mode": raw.get("execution_mode") or "STANDARD",
        "task_class": raw.get("task_class") or "UNKNOWN",
        "requirements": raw.get("requirements") or "",
        "constraints": raw.get("constraints") or [],
        "source_refs": raw.get("source_refs") or [],
        "standards_refs": raw.get("standards_refs") or [],
        "verified_findings": raw.get("verified_findings") or [],
        "expected_output": raw.get("expected_output") or "",
        "dependencies": raw.get("dependencies") or [],
        "open_questions": raw.get("open_questions") or [],
        "cache_refs": raw.get("cache_refs") or [],
        "max_context_chars_hint": int(raw.get("max_context_chars_hint") or 12000),
    }
    # Optional inline excerpts — keep small
    excerpts = raw.get("excerpts") or {}
    if excerpts:
        trimmed = {}
        for k, v in excerpts.items():
            s = str(v)
            if len(s) > 4000:
                trimmed[k] = s[:4000] + "\n…[truncated]"
            else:
                trimmed[k] = s
        pkg["excerpts"] = trimmed

    serialized = json.dumps(pkg, sort_keys=True)
    chars = len(serialized)
    pkg["_meta"] = {
        "context_chars": chars,
        "token_proxy_estimate": chars // 4,
        "token_proxy_note": "char/4 heuristic — not billing tokens",
        "over_hint": chars > pkg["max_context_chars_hint"],
    }
    return pkg


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f")
    p.add_argument("--json", "-j")
    p.add_argument("--check-only", action="store_true")
    args = p.parse_args()
    if args.file:
        raw = json.loads(Path(args.file).read_text(encoding="utf-8"))
    elif args.json:
        raw = json.loads(args.json)
    else:
        raw = json.loads(sys.stdin.read())
    pkg = build_package(raw)
    if args.check_only:
        print(json.dumps(pkg["_meta"], indent=2))
    else:
        print(json.dumps(pkg, indent=2, sort_keys=True))
    return 1 if pkg["_meta"]["over_hint"] and args.check_only else 0


if __name__ == "__main__":
    raise SystemExit(main())

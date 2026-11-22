#!/usr/bin/env python3
"""
Deterministic before/after *structure* benchmark for token optimization.

Measures: execution_mode, standards count, context package size, suggested agent template size.
Does NOT invent billing tokens or live LLM quality scores.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "modes"))
sys.path.insert(0, str(ROOT / "scripts" / "standards"))
sys.path.insert(0, str(ROOT / "scripts" / "context"))

from select_mode import AGENT_TEMPLATES, select_mode  # noqa: E402
from select_standards import select as select_standards  # noqa: E402
from package import build_package  # noqa: E402


def agent_count_for_mode(mode: str) -> int:
    t = AGENT_TEMPLATES[mode]
    names = set()
    for k, v in t.items():
        if isinstance(v, list):
            names.update(v)
    return len(names)


def run_scenario(sc: dict) -> dict:
    mode_out = select_mode(sc["task_class"], sc.get("signals") or [])
    mode = mode_out["execution_mode"]
    std = select_standards(
        sc.get("paths") or [],
        sc.get("signals") or [],
        sc.get("engines") or [],
        code_change=True,
    )
    pkg = build_package(
        {
            "agent": "parth",
            "execution_mode": mode,
            "task_class": sc["task_class"],
            "requirements": sc["name"],
            "source_refs": sc.get("paths") or [],
            "standards_refs": std["standards_refs"],
            "expected_output": "implementation + verification",
            "max_context_chars_hint": 12000,
        }
    )
    expected = sc.get("expected_mode")
    return {
        "id": sc["id"],
        "name": sc["name"],
        "task_class": sc["task_class"],
        "execution_mode": mode,
        "expected_mode": expected,
        "mode_ok": mode == expected,
        "standards_count": len(std["standards_refs"]),
        "standards_refs": std["standards_refs"],
        "context_chars": pkg["_meta"]["context_chars"],
        "token_proxy_estimate": pkg["_meta"]["token_proxy_estimate"],
        "template_agent_mentions": agent_count_for_mode(mode),
        "billing_tokens": None,
        "billing_tokens_available": False,
        "live_quality": None,
        "note": "Fill live_quality / billing_tokens only from real runs",
    }


def main() -> int:
    scenarios = json.loads(
        (Path(__file__).parent / "scenarios.json").read_text(encoding="utf-8")
    )["scenarios"]
    rows = [run_scenario(s) for s in scenarios]
    summary = {
        "scenario_count": len(rows),
        "mode_pass": sum(1 for r in rows if r["mode_ok"]),
        "avg_standards": round(sum(r["standards_count"] for r in rows) / len(rows), 2),
        "avg_context_chars": round(sum(r["context_chars"] for r in rows) / len(rows), 2),
        "avg_token_proxy": round(
            sum(r["token_proxy_estimate"] for r in rows) / len(rows), 2
        ),
        "all_mode_ok": all(r["mode_ok"] for r in rows),
    }
    out = {"summary": summary, "results": rows}
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if summary["all_mode_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

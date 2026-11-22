#!/usr/bin/env python3
"""Select execution_mode from task_class + risk signals. Never auto-downgrades for cost."""

from __future__ import annotations

import argparse
import json
import sys

MODES = ("FAST", "STANDARD", "CRITICAL", "INCIDENT_ARCHITECTURE")

DEFAULT_CLASS = {
    "EXPLANATION": "FAST",
    "INVESTIGATION": "FAST",
    "DEBUGGING": "STANDARD",
    "PATCH": "STANDARD",
    "BUG_FIX": "STANDARD",
    "FEATURE": "STANDARD",
    "REFACTOR": "STANDARD",
    "CODE_REVIEW": "STANDARD",
    "DATABASE_CHANGE": "CRITICAL",
    "SECURITY_CHANGE": "CRITICAL",
    "ARCHITECTURE": "INCIDENT_ARCHITECTURE",
    "PRODUCTION_INCIDENT": "INCIDENT_ARCHITECTURE",
}

# Signals that force at least CRITICAL (or INCIDENT if already higher intent)
CRITICAL_SIGNALS = {
    "security",
    "auth",
    "secrets",
    "pii",
    "phi",
    "schema",
    "migration",
    "database",
    "distributed",
    "consistency",
    "multi-tenant",
    "payment",
    "api",
    "contract",
    "breaking-change",
    "workflow",
    "saga",
    "ai",
    "llm",
    "healthcare",
}

INCIDENT_SIGNALS = {
    "production",
    "prod",
    "incident",
    "outage",
    "data-loss",
    "breach",
}


def rank(mode: str) -> int:
    return MODES.index(mode)


def escalate(current: str, target: str) -> str:
    return target if rank(target) > rank(current) else current


def select_mode(task_class: str, signals: list[str], force_mode: str | None = None) -> dict:
    tc = (task_class or "FEATURE").upper().replace(" ", "_")
    mode = DEFAULT_CLASS.get(tc, "STANDARD")
    sigs = [s.strip().lower() for s in signals if s.strip()]
    reasons = [f"default for {tc}"]

    if force_mode:
        fm = force_mode.upper().replace("-", "_")
        if fm not in MODES:
            return {"error": f"invalid force_mode {force_mode}", "allowed": list(MODES)}
        # Force may escalate; refuse silent downgrade below default when risks present
        mode = escalate(mode, fm)
        reasons.append(f"force_mode={fm}")

    for s in sigs:
        if s in INCIDENT_SIGNALS or s.startswith("incident"):
            mode = escalate(mode, "INCIDENT_ARCHITECTURE")
            reasons.append(f"signal:{s}→INCIDENT_ARCHITECTURE")
        elif s in CRITICAL_SIGNALS:
            mode = escalate(mode, "CRITICAL")
            reasons.append(f"signal:{s}→CRITICAL")

    return {
        "task_class": tc,
        "execution_mode": mode,
        "signals": sigs,
        "reasons": reasons,
        "policy": "escalate-only; never downgrade solely to save tokens",
    }


# Suggested agent sets by mode (minimum sufficient — not mandatory full roster)
AGENT_TEMPLATES = {
    "FAST": {
        "required": ["kesh"],
        "often": ["sanjaya"],
        "avoid_unless_needed": [
            "vidura",
            "vyasa",
            "vishwakarma",
            "sarthi",
            "parth",
            "krishna",
            "money-lens",
            "decision-engine",
            "niti",
        ],
    },
    "STANDARD": {
        "required_on_code_change": ["parth", "swachalit", "bhishma"],
        "review_specialized": ["lakshman", "draupadi"],
        "understand_as_needed": ["vidura", "sanjaya", "sarthi"],
    },
    "CRITICAL": {
        "required_on_code_change": ["parth", "swachalit", "bhishma"],
        "often": ["sanjaya", "vishwakarma", "lakshman"],
        "specialists_by_signal": {
            "api": ["api-architect"],
            "contract": ["api-architect"],
            "ai": ["ai-product-engineer"],
            "llm": ["ai-product-engineer"],
            "healthcare": ["healthcare-domain"],
        },
        "gates_as_warranted": ["krishna", "decision-engine", "kripacharya"],
        "skills": "scripts/skills/select_skills.py",
    },
    "INCIDENT_ARCHITECTURE": {
        "required": ["sanjaya", "kesh"],
        "full_applicable": True,
        "note": "Invoke all specialists whose inputs exist; evidence-first; human approval for consequential acts",
    },
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--task-class", required=True)
    p.add_argument(
        "--signals",
        default="",
        help="Comma-separated risk signals (security,schema,production,...)",
    )
    p.add_argument("--force-mode", default=None)
    p.add_argument("--with-agents", action="store_true")
    args = p.parse_args()
    signals = [x for x in args.signals.split(",") if x.strip()]
    out = select_mode(args.task_class, signals, args.force_mode)
    if args.with_agents and "execution_mode" in out:
        out["agent_template"] = AGENT_TEMPLATES[out["execution_mode"]]
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if "error" not in out else 1


if __name__ == "__main__":
    raise SystemExit(main())

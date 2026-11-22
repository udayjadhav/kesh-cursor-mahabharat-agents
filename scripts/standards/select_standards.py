#!/usr/bin/env python3
"""Progressive standards selection from file paths / tech inventory. No irrelevant packs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Core for any code change
CORE_CODE = [
    "rules/kesh-code-quality.mdc",
    "rules/standards/testing.mdc",
]

RULES = [
    {
        "id": "java-quarkus",
        "paths": [r"\.java$", r"\.kt$", r"pom\.xml$", r"build\.gradle", r"application\.(yml|yaml|properties)$"],
        "modules": ["rules/standards/java-quarkus.mdc"],
    },
    {
        "id": "python",
        "paths": [r"\.py$", r"pyproject\.toml$", r"requirements.*\.txt$"],
        "modules": ["rules/standards/python.mdc"],
    },
    {
        "id": "react-typescript",
        "paths": [r"\.tsx?$", r"\.jsx?$", r"package\.json$"],
        "modules": ["rules/standards/react-typescript.mdc"],
    },
    {
        "id": "database",
        "paths": [
            r"migration",
            r"\.sql$",
            r"flyway",
            r"liquibase",
            r"schema",
            r"alembic",
        ],
        "modules": [
            "rules/standards/database/database-design.mdc",
            "rules/standards/database/database-migrations.mdc",
        ],
        "engines": {
            "postgres": "rules/standards/database/engines/postgresql.mdc",
            "postgresql": "rules/standards/database/engines/postgresql.mdc",
            "mysql": "rules/standards/database/engines/mysql.mdc",
            "mongodb": "rules/standards/database/engines/mongodb.mdc",
            "redis": "rules/standards/database/engines/redis.mdc",
            "elasticsearch": "rules/standards/database/engines/elasticsearch.mdc",
            "cockroach": "rules/standards/database/engines/cockroachdb.mdc",
            "spanner": "rules/standards/database/engines/google-spanner.mdc",
            "bigquery": "rules/standards/database/engines/bigquery.mdc",
        },
    },
    {
        "id": "security",
        "paths": [r"auth", r"oauth", r"security", r"crypto", r"secret"],
        "modules": ["rules/standards/security.mdc"],
        "on_signals": ["security", "auth", "secrets"],
    },
    {
        "id": "distributed",
        "paths": [r"kafka", r"saga", r"outbox", r"event", r"queue"],
        "modules": [
            "rules/standards/distributed-systems.mdc",
            "rules/standards/microservices.mdc",
        ],
        "on_signals": ["distributed", "consistency"],
    },
    {
        "id": "architecture",
        "paths": [r"ARCHITECTURE", r"/adr/", r"/docs/architecture"],
        "modules": ["rules/standards/software-architecture.mdc"],
        "on_signals": ["architecture"],
    },
]


def select(
    paths: list[str],
    signals: list[str] | None = None,
    engines: list[str] | None = None,
    code_change: bool = True,
) -> dict:
    signals = [s.lower() for s in (signals or [])]
    engines = [e.lower() for e in (engines or [])]
    selected: list[str] = []
    matched_rules: list[str] = []

    if code_change:
        selected.extend(CORE_CODE)

    blob = "\n".join(paths)

    for rule in RULES:
        hit = False
        for pat in rule["paths"]:
            if re.search(pat, blob, re.I):
                hit = True
                break
        for sig in rule.get("on_signals") or []:
            if sig in signals:
                hit = True
        if not hit:
            continue
        matched_rules.append(rule["id"])
        for m in rule["modules"]:
            if m not in selected:
                selected.append(m)
        if rule["id"] == "database":
            for eng in engines:
                mod = rule.get("engines", {}).get(eng)
                if mod and mod not in selected:
                    selected.append(mod)

    # Verify files exist in kit
    existing = [m for m in selected if (ROOT / m).exists()]
    missing = [m for m in selected if m not in existing]

    return {
        "paths": paths,
        "signals": signals,
        "engines": engines,
        "matched_rule_ids": matched_rules,
        "standards_refs": existing,
        "missing_in_kit": missing,
        "policy": "progressive — do not load unrelated language packs",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--paths", default="", help="Comma-separated file paths")
    p.add_argument("--signals", default="")
    p.add_argument("--engines", default="", help="postgres,mysql,...")
    p.add_argument("--no-code", action="store_true", help="Skip core code standards")
    args = p.parse_args()
    paths = [x.strip() for x in args.paths.split(",") if x.strip()]
    signals = [x.strip() for x in args.signals.split(",") if x.strip()]
    engines = [x.strip() for x in args.engines.split(",") if x.strip()]
    out = select(paths, signals, engines, code_change=not args.no_code)
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

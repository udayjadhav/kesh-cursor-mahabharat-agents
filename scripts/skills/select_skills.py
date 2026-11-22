#!/usr/bin/env python3
"""Progressive skill selection from paths + risk signals. Does not load every skill."""

from __future__ import annotations

import argparse
import json
import re

RULES = [
    {"id": "java-quarkus", "path": "skills/java-quarkus/SKILL.md", "paths": [r"\.java$", r"pom\.xml$", r"quarkus"], "signals": ["java", "quarkus"]},
    {"id": "api-engineering", "path": "skills/api-engineering/SKILL.md", "paths": [r"openapi", r"\.proto$", r"/api/", r"graphql"], "signals": ["api", "openapi", "grpc", "graphql", "contract"]},
    {"id": "frontend-architecture", "path": "skills/frontend-architecture/SKILL.md", "paths": [r"\.tsx?$", r"\.jsx?$"], "signals": ["frontend", "react", "ui"]},
    {"id": "data-engineering", "path": "skills/data-engineering/SKILL.md", "paths": [r"migration", r"\.sql$", r"spanner", r"bigquery", r"kafka"], "signals": ["database", "schema", "kafka", "spanner", "bigquery"]},
    {"id": "workflow-architecture", "path": "skills/workflow-architecture/SKILL.md", "paths": [r"saga", r"outbox", r"workflow", r"job"], "signals": ["workflow", "saga", "outbox", "async"]},
    {"id": "ai-engineering", "path": "skills/ai-engineering/SKILL.md", "paths": [r"prompt", r"llm", r"openai", r"anthropic"], "signals": ["ai", "llm", "prompt", "eval"]},
    {"id": "reliability-performance", "path": "skills/reliability-performance/SKILL.md", "paths": [r"otel", r"slo", r"sentry"], "signals": ["performance", "slo", "latency", "reliability"]},
    {"id": "security-compliance", "path": "skills/security-compliance/SKILL.md", "paths": [r"auth", r"rbac", r"security"], "signals": ["security", "auth", "rbac", "pii", "phi", "multi-tenant"]},
    {"id": "staff-engineering", "path": "skills/staff-engineering/SKILL.md", "paths": [r"/adr/", r"design-doc", r"RFC"], "signals": ["adr", "design-doc", "architecture-review", "tech-debt"]},
    {"id": "production-engineering", "path": "skills/production-engineering/SKILL.md", "paths": [r"Dockerfile", r"k8s", r"\.github/workflows", r"helm"], "signals": ["deploy", "kubernetes", "ci"]},
    {"id": "healthcare-provider", "path": "optional/healthcare/skills/healthcare-provider/SKILL.md", "paths": [r"fhir", r"npi", r"provider"], "signals": ["healthcare", "provider", "npi", "fhir", "hl7"], "optional": True},
]


def select(paths: list[str], signals: list[str], include_optional: bool = False) -> dict:
    blob = "\n".join(paths)
    sigs = [s.lower() for s in signals]
    out = []
    for rule in RULES:
        if rule.get("optional") and not include_optional:
            continue
        hit = any(re.search(p, blob, re.I) for p in rule["paths"]) or any(
            s in sigs for s in rule["signals"]
        )
        if hit:
            out.append({"id": rule["id"], "path": rule["path"], "optional": bool(rule.get("optional"))})
    return {"skills": out, "policy": "progressive — do not load all skills"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--paths", default="")
    p.add_argument("--signals", default="")
    p.add_argument("--include-optional", action="store_true")
    args = p.parse_args()
    paths = [x.strip() for x in args.paths.split(",") if x.strip()]
    signals = [x.strip() for x in args.signals.split(",") if x.strip()]
    print(json.dumps(select(paths, signals, args.include_optional), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

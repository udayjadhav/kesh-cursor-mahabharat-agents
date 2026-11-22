#!/usr/bin/env python3
"""
Repository intelligence profile from filesystem evidence.
Never invent frameworks from job descriptions — only what is present.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fingerprint_paths(root: Path, rels: list[str]) -> str:
    h = hashlib.sha256()
    for rel in sorted(rels):
        p = root / rel
        h.update(rel.encode())
        if p.is_file():
            try:
                h.update(p.read_bytes()[:65536])
            except OSError:
                pass
    return h.hexdigest()[:16]


def detect(root: Path) -> dict:
    files = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    # Cap walk noise
    files = [f for f in files if ".git" not in f.split("/") and "node_modules" not in f.split("/")][:5000]

    langs = []
    if any(f.endswith(".java") for f in files):
        langs.append("java")
    if any(f.endswith(".py") for f in files):
        langs.append("python")
    if any(f.endswith(x) for f in files for x in (".ts", ".tsx", ".js", ".jsx")):
        langs.append("typescript/javascript")
    if any(f.endswith(".go") for f in files):
        langs.append("go")

    frameworks = []
    blob = "\n".join(files).lower()
    markers = {
        "quarkus": [r"quarkus", r"application\.properties"],
        "spring": [r"spring-boot", r"springframework"],
        "react": [r"package\.json"],  # refined below
        "next": [r"next\.config"],
        "kafka": [r"kafka"],
        "spanner": [r"spanner"],
        "bigquery": [r"bigquery"],
        "postgres": [r"postgres", r"postgresql"],
    }
    for name, pats in markers.items():
        if any(re.search(p, blob) for p in pats):
            frameworks.append(name)

    # React: package.json dependencies if present
    pkg = root / "package.json"
    react = False
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "react" in deps:
                react = True
                if "react" not in frameworks:
                    frameworks.append("react")
        except (json.JSONDecodeError, OSError):
            pass

    build = []
    for cand in ("pom.xml", "build.gradle", "build.gradle.kts", "package.json", "pyproject.toml", "go.mod"):
        if (root / cand).exists() or any(f.endswith(cand) or f == cand for f in files):
            build.append(cand)

    tests = []
    if any("src/test" in f or f.endswith("_test.go") or "pytest" in f or ".test." in f for f in files):
        tests.append("test_sources_present")
    ci = [f for f in files if ".github/workflows" in f or f.startswith(".gitlab-ci")]

    key_files = [f for f in files if f in {
        "pom.xml", "package.json", "pyproject.toml", "Dockerfile", "docker-compose.yml",
        "openapi.yaml", "openapi.yml", "README.md",
    } or f.endswith("openapi.yaml") or "/migrations/" in f or "/migration/" in f][:40]

    fp = fingerprint_paths(root, key_files or files[:20])

    return {
        "repo_root": str(root.resolve()),
        "generated_at": utc_now(),
        "content_fingerprint": fp,
        "languages": langs,
        "frameworks_detected": sorted(set(frameworks)),
        "build_manifests": sorted(set(build)),
        "react_dependency": react,
        "test_signals": tests,
        "ci_workflows": ci[:20],
        "key_files": key_files,
        "confidence": "high" if langs or build else "low",
        "invalidation": "Re-run when key manifests or migration/OpenAPI files change",
        "source": "filesystem_evidence_only",
        "notes": [
            "Does not assume job-description tech is present",
            "Deep architecture still requires Sanjaya/xray",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".", help="Repository root to profile")
    p.add_argument("--cache-put", action="store_true", help="Also write via scripts/cache if available")
    args = p.parse_args()
    root = Path(args.root).resolve()
    profile = detect(root)
    print(json.dumps(profile, indent=2, sort_keys=True))
    if args.cache_put:
        try:
            import sys

            sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cache"))
            from lib import ensure_cache, fingerprint, put_entry

            home = ensure_cache()
            fp = fingerprint(
                f"repo-profile:{profile['repo_root']}",
                "REPO_PROFILE",
                profile.get("key_files") or [],
                profile["content_fingerprint"],
            )
            put_entry(
                home,
                {
                    "fingerprint": fp,
                    "topic": f"repo-profile:{profile['repo_root']}",
                    "input_type": "REPO_PROFILE",
                    "entities": profile.get("key_files") or [],
                    "code_revision_hint": profile["content_fingerprint"],
                    "ttl_hours": 24,
                    "content_class": "repo_profile",
                    "agent_summaries": {"sanjaya": json.dumps(profile)[:4000]},
                    "synthesis": f"langs={profile['languages']} frameworks={profile['frameworks_detected']}",
                },
            )
        except Exception as e:
            profile_err = {"cache_put_error": str(e)}
            print(json.dumps(profile_err), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Discover deterministic quality tools in a target repo. Never invent PASS."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def exists(root: Path, *parts: str) -> bool:
    return (root.joinpath(*parts)).exists()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    args = p.parse_args()
    root = Path(args.root).resolve()

    tools = []

    def add(name: str, present: bool, how: str):
        tools.append(
            {
                "name": name,
                "present": present,
                "suggested_command": how if present else None,
                "status": "AVAILABLE" if present else "MISSING",
            }
        )

    add("maven", exists(root, "pom.xml"), "mvn -q test")
    add("gradle", exists(root, "build.gradle") or exists(root, "build.gradle.kts"), "./gradlew test")
    add("npm", exists(root, "package.json"), "npm test")
    add("pytest", exists(root, "pyproject.toml") or exists(root, "pytest.ini"), "pytest")
    add("ruff", shutil.which("ruff") is not None and (exists(root, "pyproject.toml") or exists(root, "ruff.toml")), "ruff check .")
    add("eslint", exists(root, "eslint.config.js") or exists(root, ".eslintrc.js") or exists(root, ".eslintrc.cjs"), "npx eslint .")
    add("tsc", exists(root, "tsconfig.json"), "npx tsc --noEmit")
    add("docker", exists(root, "Dockerfile"), "docker build .")
    add(
        "github_actions",
        (root / ".github" / "workflows").is_dir(),
        "inspect .github/workflows",
    )
    add(
        "openapi_file",
        any(root.rglob("openapi*.y*ml")),
        "validate OpenAPI with project tool if configured",
    )

    print(
        json.dumps(
            {
                "repo_root": str(root),
                "tools": tools,
                "policy": "A tool not executed must be reported NOT RUN; MISSING is explicit",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Regression tests for execution modes, standards selection, context packages, cache."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "modes"))
sys.path.insert(0, str(ROOT / "scripts" / "standards"))
sys.path.insert(0, str(ROOT / "scripts" / "context"))
sys.path.insert(0, str(ROOT / "scripts" / "cache"))

from select_mode import select_mode  # noqa: E402
from select_standards import select as select_standards  # noqa: E402
from package import build_package  # noqa: E402
from lib import fingerprint, get_entry, invalidate, put_entry, ensure_cache  # noqa: E402


class TokenOptimizationTests(unittest.TestCase):
    def test_mode_defaults_and_escalation(self):
        self.assertEqual(select_mode("EXPLANATION", [])["execution_mode"], "FAST")
        self.assertEqual(select_mode("FEATURE", [])["execution_mode"], "STANDARD")
        self.assertEqual(
            select_mode("FEATURE", ["security"])["execution_mode"], "CRITICAL"
        )
        self.assertEqual(
            select_mode("BUG_FIX", ["production", "incident"])["execution_mode"],
            "INCIDENT_ARCHITECTURE",
        )

    def test_never_downgrade_for_force_below_risk(self):
        # force FAST but security signal still escalates to CRITICAL
        out = select_mode("FEATURE", ["security"], force_mode="FAST")
        self.assertEqual(out["execution_mode"], "CRITICAL")

    def test_standards_progressive(self):
        java = select_standards(["src/Foo.java"], [], [], True)
        self.assertTrue(any("java-quarkus" in s for s in java["standards_refs"]))
        self.assertFalse(any("python" in s for s in java["standards_refs"]))
        py = select_standards(["app.py"], [], [], True)
        self.assertTrue(any("python" in s for s in py["standards_refs"]))
        db = select_standards(
            ["db/migration/V1.sql"], ["schema"], ["postgresql"], True
        )
        self.assertTrue(any("database-design" in s for s in db["standards_refs"]))
        self.assertTrue(any("postgresql" in s for s in db["standards_refs"]))

    def test_context_package_meta(self):
        pkg = build_package(
            {
                "agent": "bhishma",
                "requirements": "review auth change",
                "source_refs": ["a.java"],
                "standards_refs": ["rules/standards/security.mdc"],
            }
        )
        self.assertIn("_meta", pkg)
        self.assertGreater(pkg["_meta"]["context_chars"], 0)
        self.assertFalse(pkg["_meta"].get("billing_tokens_available", False))

    def test_cache_hit_stale_and_dedup_cap(self):
        with tempfile.TemporaryDirectory() as td:
            os.environ["KESH_CACHE_HOME"] = td
            # re-import path uses env via cache_home
            home = ensure_cache(Path(td))
            fp = fingerprint("auth flow", "EXPLANATION", ["a.java"], "abc")
            put_entry(
                home,
                {
                    "fingerprint": fp,
                    "topic": "auth flow",
                    "input_type": "EXPLANATION",
                    "entities": ["a.java"],
                    "ttl_hours": 24,
                    "agent_summaries": {"sanjaya": "summary"},
                    "synthesis": "ok",
                },
            )
            hit = get_entry(home, fp)
            self.assertEqual(hit["result"], "HIT")
            stale_fp = fingerprint("old topic", "EXPLANATION", ["b.java"], "def")
            put_entry(
                home,
                {
                    "fingerprint": stale_fp,
                    "topic": "old topic",
                    "input_type": "EXPLANATION",
                    "ttl_hours": 1,
                    "created_at": "2000-01-01T00:00:00Z",
                    "agent_summaries": {"sanjaya": "old"},
                },
            )
            stale = get_entry(home, stale_fp)
            self.assertEqual(stale["result"], "STALE")
            invalidate(home, fp)
            miss = get_entry(home, fp)
            self.assertEqual(miss["result"], "MISS")

    def test_benchmark_harness_all_modes(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "benchmarks/token-optimization/harness.py")],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertTrue(data["summary"]["all_mode_ok"])
        self.assertEqual(data["summary"]["scenario_count"], 12)

    def test_always_apply_reduced(self):
        # Demoted rules should not be alwaysApply true
        for rel in (
            "rules/kesh-explanation-framework.mdc",
            "rules/global-local-sync.mdc",
            "rules/dev-spec-authorship-voice.mdc",
            "rules/kesh-external-output-voice.mdc",
            "rules/kesh-execution-modes.mdc",
            "rules/kesh-context-packaging.mdc",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("alwaysApply: false", text)
        guard = (ROOT / "rules/kesh-quality-guardrails.mdc").read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", guard)


if __name__ == "__main__":
    unittest.main()

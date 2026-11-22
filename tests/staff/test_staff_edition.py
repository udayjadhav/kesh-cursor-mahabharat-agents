#!/usr/bin/env python3
"""Staff Engineer Edition regression tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "skills"))
sys.path.insert(0, str(ROOT / "scripts" / "modes"))

from select_skills import select as select_skills  # noqa: E402
from select_mode import select_mode  # noqa: E402


class StaffEditionTests(unittest.TestCase):
    def test_core_agents_exist_healthcare_not_core(self):
        self.assertTrue((ROOT / "agents/api-architect.md").exists())
        self.assertTrue((ROOT / "agents/ai-product-engineer.md").exists())
        self.assertFalse((ROOT / "agents/healthcare-domain.md").exists())
        self.assertTrue(
            (ROOT / "optional/healthcare/agents/healthcare-domain.md").exists()
        )

    def test_skills_progressive(self):
        api = select_skills(["openapi.yaml"], ["api"])
        ids = {s["id"] for s in api["skills"]}
        self.assertIn("api-engineering", ids)
        self.assertNotIn("healthcare-provider", ids)
        hc = select_skills([], ["healthcare"], include_optional=True)
        self.assertTrue(any(s["id"] == "healthcare-provider" for s in hc["skills"]))

    def test_ai_signal_escalates(self):
        out = select_mode("FEATURE", ["ai", "llm"])
        self.assertEqual(out["execution_mode"], "CRITICAL")

    def test_repo_profile_evidence_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "pom.xml").write_text("<project></project>", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "A.java").write_text("class A {}", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/repo/profile.py"), "--root", str(root)],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(proc.stdout)
            self.assertIn("java", data["languages"])
            self.assertEqual(data["source"], "filesystem_evidence_only")

    def test_adr_new_and_list(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td) / "decisions"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/adr/new.py"),
                    "--title",
                    "Use outbox for writes",
                    "--dir",
                    str(d),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            path = Path(proc.stdout.strip())
            self.assertTrue(path.exists())
            listed = subprocess.run(
                [sys.executable, str(ROOT / "scripts/adr/list.py"), "--dir", str(d)],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(listed.stdout)
            self.assertEqual(len(data["adrs"]), 1)

    def test_discover_tools_missing_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/quality/discover_tools.py"),
                    "--root",
                    td,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(proc.stdout)
            self.assertTrue(any(t["status"] == "MISSING" for t in data["tools"]))


if __name__ == "__main__":
    unittest.main()

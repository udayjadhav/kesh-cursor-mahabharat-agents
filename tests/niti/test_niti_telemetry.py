#!/usr/bin/env python3
"""Executable validation for NITI telemetry, triggers, and recommendation loop."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "niti"
sys.path.insert(0, str(SCRIPTS))

from lib import (  # noqa: E402
    before_after_compare,
    compute_agent_stats,
    detect_repeated_failures,
    detect_unnecessary_invocations,
    ensure_layout,
    load_jsonl,
    mark_trigger_consumed,
    normalize_execution,
    read_json,
    record_execution,
    redact_hook_payload,
    should_invoke,
)


def _home(td: str) -> Path:
    home = Path(td) / "niti-home"
    ensure_layout(home)
    return home


class NitiTelemetryTests(unittest.TestCase):
    def test_01_receives_execution_telemetry(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            r = record_execution(
                home,
                {
                    "execution_id": "exec_a1",
                    "task_class": "FEATURE",
                    "delivery_status": "COMPLETE",
                    "agents_invoked": [
                        {"name": "parth", "status": "completed", "duration_ms": 1000}
                    ],
                    "token_usage_available": False,
                    "cost_available": False,
                },
            )
            self.assertEqual(r["status"], "recorded")
            rows = load_jsonl(home / "logs" / "executions.jsonl")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["execution_id"], "exec_a1")
            self.assertFalse(rows[0]["token_usage_available"])

    def test_02_five_task_trigger_persists_across_sessions(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            for i in range(4):
                record_execution(
                    home,
                    {
                        "execution_id": f"exec_l{i}",
                        "delivery_status": "COMPLETE",
                        "task_class": "PATCH",
                    },
                )
            d1 = should_invoke(home)
            self.assertFalse(d1["invoke"])
            # "new session" = re-read state from disk
            home2 = Path(td) / "niti-home"
            record_execution(
                home2,
                {
                    "execution_id": "exec_l4",
                    "delivery_status": "PARTIAL",
                    "task_class": "PATCH",
                },
            )
            d2 = should_invoke(home2)
            self.assertTrue(d2["invoke"])
            self.assertEqual(d2["mode"], "lightweight")
            self.assertEqual(d2["since_lightweight"], 5)

    def test_03_twenty_task_deep_audit(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            for i in range(20):
                record_execution(
                    home,
                    {
                        "execution_id": f"exec_d{i}",
                        "delivery_status": "COMPLETE",
                        "task_class": "FEATURE",
                    },
                )
            d = should_invoke(home)
            self.assertTrue(d["invoke"])
            self.assertEqual(d["mode"], "deep")
            self.assertEqual(d["since_deep"], 20)

    def test_04_failed_executions_captured(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            r = record_execution(
                home,
                {
                    "execution_id": "exec_fail",
                    "delivery_status": "FAILED",
                    "success": False,
                    "agents_invoked": [{"name": "parth", "status": "error"}],
                    "tool_failures": [{"tool": "Shell", "failure_type": "error"}],
                },
            )
            self.assertEqual(r["status"], "recorded")
            self.assertEqual(r["trigger"], "post_incident")
            rows = load_jsonl(home / "logs" / "executions.jsonl")
            self.assertFalse(rows[0]["success"])
            # failures do not increment meaningful completed counter
            state = read_json(home / "state.json", {})
            self.assertEqual(state["meaningful_completed_count"], 0)

    def test_05_missing_telemetry_not_success(self):
        ex = normalize_execution(
            {"execution_id": "x", "delivery_status": "UNKNOWN"}
        )
        self.assertIsNone(ex["success"])
        stats = compute_agent_stats(
            [
                {
                    "agents_invoked": [
                        {"name": "bhishma", "status": "unknown"}
                    ]
                }
            ]
        )
        self.assertIsNone(stats["bhishma"]["success_rate"])
        self.assertEqual(stats["bhishma"]["unknown_outcome"], 1)

    def test_06_duplicate_execution_not_counted_twice(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            payload = {
                "execution_id": "exec_dup",
                "delivery_status": "COMPLETE",
                "task_class": "BUG_FIX",
            }
            r1 = record_execution(home, payload)
            r2 = record_execution(home, payload)
            self.assertEqual(r1["status"], "recorded")
            self.assertEqual(r2["status"], "duplicate")
            state = read_json(home / "state.json", {})
            self.assertEqual(state["meaningful_completed_count"], 1)
            self.assertEqual(len(load_jsonl(home / "logs" / "executions.jsonl")), 1)

    def test_07_detect_repeated_agent_failures(self):
        rows = []
        for i in range(3):
            rows.append(
                {
                    "execution_id": f"e{i}",
                    "agents_invoked": [{"name": "parth", "status": "failed"}],
                }
            )
        hit = detect_repeated_failures(rows, "parth", min_count=3)
        self.assertIsNotNone(hit)
        self.assertEqual(hit["failure_count"], 3)

    def test_08_unnecessary_agent_invocations(self):
        rows = [
            {
                "execution_id": "e1",
                "task_class": "EXPLANATION",
                "agents_invoked": [
                    {"name": "sanjaya"},
                    {"name": "krishna"},
                    {"name": "vishwakarma"},
                ],
            }
        ]
        flags = detect_unnecessary_invocations(rows)
        agents = {f["agent"] for f in flags}
        self.assertIn("krishna", agents)
        self.assertIn("vishwakarma", agents)
        self.assertNotIn("sanjaya", agents)

    def test_09_recommendation_lifecycle(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            env = {**os.environ, "KESH_NITI_HOME": str(home)}
            body = {
                "observed_problem": "Parth high rework",
                "evidence": "3 FAIL loops in window",
                "root_cause_or_hypothesis": "weak checklist",
                "proposed_change": "tighten Parth self-check",
                "expected_benefit": "fewer critique loops",
                "risks_and_tradeoffs": "slightly slower first pass",
                "success_metric": "avg retries < 1 over next 10 tasks",
                "priority": "HIGH",
            }
            add = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "recommendations.py"),
                    "add",
                    "--json",
                    json.dumps(body),
                ],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            added = json.loads(add.stdout)
            rid = added["recommendation"]["recommendation_id"]
            for status in ("APPROVED", "IMPLEMENTED", "EVALUATED", "ACCEPTED"):
                subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPTS / "recommendations.py"),
                        "advance",
                        "--id",
                        rid,
                        "--status",
                        status,
                    ],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=True,
                )
            listed = subprocess.run(
                [sys.executable, str(SCRIPTS / "recommendations.py"), "list"],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            rows = json.loads(listed.stdout)
            self.assertEqual(rows[0]["status"], "ACCEPTED")

    def test_10_before_after_evaluation(self):
        before = [
            {"success": True},
            {"success": False},
            {"success": None},
        ]
        after = [
            {"success": True},
            {"success": True},
            {"success": True},
        ]
        cmp_ = before_after_compare(before, after)
        self.assertEqual(cmp_["before"]["success_unknown"], 1)
        self.assertEqual(cmp_["after"]["success_rate_known_only"], 1.0)
        self.assertEqual(cmp_["before"]["success_rate_known_only"], 0.5)

    def test_11_trivial_and_cancelled_not_counted(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            record_execution(
                home,
                {
                    "execution_id": "t1",
                    "delivery_status": "COMPLETE",
                    "trivial": True,
                },
            )
            record_execution(
                home,
                {
                    "execution_id": "c1",
                    "delivery_status": "COMPLETE",
                    "cancelled": True,
                },
            )
            state = read_json(home / "state.json", {})
            self.assertEqual(state["meaningful_completed_count"], 0)

    def test_12_redaction_drops_sensitive_fields(self):
        red = redact_hook_payload(
            {
                "hook_event_name": "afterFileEdit",
                "file_path": "/tmp/x",
                "edits": [{"old_string": "secret", "new_string": "also"}],
                "prompt": "do not store",
                "user_email": "a@b.com",
                "subagent_type": "parth",
                "status": "completed",
                "duration_ms": 12,
            }
        )
        self.assertNotIn("edits", red)
        self.assertNotIn("prompt", red)
        self.assertNotIn("user_email", red)
        self.assertEqual(red["subagent_type"], "parth")
        self.assertTrue(red["redacted"])

    def test_13_hook_event_script_and_stop_trigger(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            env = {**os.environ, "KESH_NITI_HOME": str(home)}
            # seed threshold
            for i in range(5):
                record_execution(
                    home,
                    {
                        "execution_id": f"exec_s{i}",
                        "delivery_status": "COMPLETE",
                    },
                )
            payload = json.dumps(
                {
                    "hook_event_name": "stop",
                    "status": "completed",
                    "loop_count": 0,
                    "conversation_id": "c1",
                    "text": "SHOULD_NOT_PERSIST",
                }
            )
            stop = subprocess.run(
                [sys.executable, str(SCRIPTS / "stop_trigger.py")],
                input=payload,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            out = json.loads(stop.stdout)
            self.assertIn("followup_message", out)
            self.assertIn("lightweight", out["followup_message"].lower())
            events = load_jsonl(home / "logs" / "events.jsonl")
            self.assertTrue(events)
            self.assertNotIn("text", events[-1])

    def test_14_consume_trigger_resets_counter(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            for i in range(5):
                record_execution(
                    home,
                    {"execution_id": f"exec_c{i}", "delivery_status": "COMPLETE"},
                )
            mark_trigger_consumed(home, "lightweight", ["exec_c0", "exec_c1"])
            d = should_invoke(home)
            self.assertFalse(d["invoke"])
            state = read_json(home / "state.json", {})
            self.assertEqual(state["since_lightweight"], 0)
            self.assertIn("exec_c0", state["analyzed_execution_ids"])

    def test_15_analyze_prep_cli(self):
        with tempfile.TemporaryDirectory() as td:
            home = _home(td)
            env = {**os.environ, "KESH_NITI_HOME": str(home)}
            record_execution(
                home,
                {
                    "execution_id": "exec_p1",
                    "delivery_status": "COMPLETE",
                    "agents_invoked": [{"name": "parth", "status": "completed"}],
                },
            )
            prep = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "analyze_prep.py"),
                    "--mode",
                    "lightweight",
                ],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            bundle = json.loads(prep.stdout)
            self.assertEqual(bundle["execution_count_in_window"], 1)
            self.assertIn("token_usage", bundle["evidence_limitations"])


if __name__ == "__main__":
    unittest.main()

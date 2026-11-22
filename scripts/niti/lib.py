#!/usr/bin/env python3
"""Shared helpers for Kesh NITI telemetry (local-first)."""

from __future__ import annotations

import fcntl
import json
import os
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROSTER_AGENTS = frozenset(
    {
        "kesh",
        "vidura",
        "sanjaya",
        "vyasa",
        "vishwakarma",
        "sarthi",
        "parth",
        "swachalit",
        "sutradhar",
        "bhishma",
        "lakshman",
        "draupadi",
        "krishna",
        "money-lens",
        "decision-engine",
        "kripacharya",
        "niti",
        "kesh-flows",
        "kesh-context",
        "kesh-output",
        "kesh-rules",
    }
)

MEANINGFUL_STATUSES = frozenset({"COMPLETE", "PARTIAL"})
FAILURE_STATUSES = frozenset({"FAILED", "BLOCKED"})

LIGHTWEIGHT_EVERY = 5
DEEP_EVERY = 20

# Hook payloads that must never be persisted wholesale
REDACT_KEYS = frozenset(
    {
        "text",
        "prompt",
        "content",
        "edits",
        "tool_input",
        "tool_output",
        "attachments",
        "result_json",
        "output",
        "command",  # may contain secrets; keep truncated tool name only elsewhere
    }
)


def niti_home() -> Path:
    raw = os.environ.get("KESH_NITI_HOME")
    if raw:
        return Path(raw).expanduser().resolve()
    return Path.home() / ".cursor" / "niti"


def ensure_layout(home: Path | None = None) -> Path:
    root = home or niti_home()
    (root / "logs").mkdir(parents=True, exist_ok=True)
    (root / "reports").mkdir(parents=True, exist_ok=True)
    state_path = root / "state.json"
    if not state_path.exists():
        write_json_atomic(
            state_path,
            {
                "version": 1,
                "meaningful_completed_count": 0,
                "since_lightweight": 0,
                "since_deep": 0,
                "last_lightweight_at_count": None,
                "last_deep_at_count": None,
                "pending_trigger": None,
                "analyzed_execution_ids": [],
                "analyzed_execution_ids_cap": 500,
                "updated_at": None,
            },
        )
    for name in ("events.jsonl", "executions.jsonl"):
        p = root / "logs" / name
        if not p.exists():
            p.touch()
    rec = root / "recommendations.jsonl"
    if not rec.exists():
        rec.touch()
    return root


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_id(prefix: str = "exec") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def write_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True, ensure_ascii=False)
    with path.open("a", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                out.append(
                    {
                        "parse_error": True,
                        "raw_truncated": line[:200],
                        "success": None,
                        "delivery_status": "UNKNOWN",
                    }
                )
    return out


def with_state_lock(home: Path, fn):
    ensure_layout(home)
    lock_path = home / ".state.lock"
    lock_path.touch(exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lockf:
        fcntl.flock(lockf.fileno(), fcntl.LOCK_EX)
        try:
            state_path = home / "state.json"
            state = read_json(state_path, {})
            if not state:
                state = {
                    "version": 1,
                    "meaningful_completed_count": 0,
                    "since_lightweight": 0,
                    "since_deep": 0,
                    "last_lightweight_at_count": None,
                    "last_deep_at_count": None,
                    "pending_trigger": None,
                    "analyzed_execution_ids": [],
                    "analyzed_execution_ids_cap": 500,
                    "updated_at": None,
                }
            result = fn(state)
            state["updated_at"] = utc_now()
            write_json_atomic(state_path, state)
            return result
        finally:
            fcntl.flock(lockf.fileno(), fcntl.LOCK_UN)


def redact_hook_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Keep structural fields; drop content that may hold source/secrets."""
    out: dict[str, Any] = {}
    keep = {
        "hook_event_name",
        "conversation_id",
        "generation_id",
        "session_id",
        "model",
        "model_id",
        "cursor_version",
        "workspace_roots",
        "subagent_id",
        "subagent_type",
        "subagent_model",
        "parent_conversation_id",
        "tool_call_id",
        "is_parallel_worker",
        "git_branch",
        "status",
        "task",
        "description",
        "summary",
        "duration_ms",
        "duration",
        "message_count",
        "tool_call_count",
        "loop_count",
        "modified_files",
        "agent_transcript_path",
        "tool_name",
        "tool_use_id",
        "cwd",
        "error_message",
        "failure_type",
        "is_interrupt",
        "is_background_agent",
        "composer_mode",
        "reason",
        "final_status",
        "context_tokens",
        "context_window_size",
        "context_usage_percent",
        "trigger",
        "message_count",
    }
    for k, v in payload.items():
        if k in REDACT_KEYS:
            continue
        if k == "user_email":
            continue  # avoid unnecessary PII
        if k in keep:
            if k == "error_message" and isinstance(v, str) and len(v) > 500:
                out[k] = v[:500] + "…"
            elif k == "summary" and isinstance(v, str) and len(v) > 1000:
                out[k] = v[:1000] + "…"
            elif k == "task" and isinstance(v, str) and len(v) > 500:
                out[k] = v[:500] + "…"
            elif k == "modified_files" and isinstance(v, list):
                # paths only, cap
                out[k] = [str(x) for x in v[:50]]
            else:
                out[k] = v
    out["redacted"] = True
    out["recorded_at"] = utc_now()
    return out


def execution_exists(home: Path, execution_id: str) -> bool:
    for row in load_jsonl(home / "logs" / "executions.jsonl"):
        if row.get("execution_id") == execution_id:
            return True
    return False


def normalize_execution(raw: dict[str, Any]) -> dict[str, Any]:
    eid = raw.get("execution_id") or new_id("exec")
    status = (raw.get("delivery_status") or "UNKNOWN").upper()
    meaningful = bool(raw.get("meaningful", status in MEANINGFUL_STATUSES))
    if raw.get("trivial") or raw.get("cancelled"):
        meaningful = False
    agents = raw.get("agents_invoked") or []
    if not isinstance(agents, list):
        agents = []

    token = raw.get("token_usage")
    cost = raw.get("cost_usd")
    return {
        "execution_id": eid,
        "recorded_at": raw.get("recorded_at") or utc_now(),
        "conversation_id": raw.get("conversation_id"),
        "generation_id": raw.get("generation_id"),
        "task_class": raw.get("task_class") or "UNKNOWN",
        "meaningful": meaningful,
        "trivial": bool(raw.get("trivial", False)),
        "cancelled": bool(raw.get("cancelled", False)),
        "agents_invoked": agents,
        "delivery_status": status,
        "retry_count": int(raw.get("retry_count") or 0),
        "tool_failures": raw.get("tool_failures") or [],
        "test_results": raw.get("test_results")
        or {"ran": False, "passed": None, "failed": None, "unknown": True},
        "review_findings": raw.get("review_findings")
        or {"blocking": None, "major": None, "unknown": True},
        "token_usage": token,
        "token_usage_available": bool(raw.get("token_usage_available", token is not None)),
        "cost_usd": cost,
        "cost_available": bool(raw.get("cost_available", cost is not None)),
        "duration_ms": raw.get("duration_ms"),
        "model": raw.get("model"),
        "human_correction": bool(raw.get("human_correction", False)),
        "notes": raw.get("notes") or "",
        "source": raw.get("source") or "manual",
        "kit_change_tag": raw.get("kit_change_tag"),
        "success": _infer_success(status, raw.get("success")),
        # Token optimization proxies (billing tokens usually unavailable from Agent hooks)
        "execution_mode": raw.get("execution_mode"),
        "context_chars": raw.get("context_chars"),
        "token_proxy_estimate": raw.get("token_proxy_estimate"),
        "agents_invoked_count": raw.get("agents_invoked_count")
        or (len(agents) if agents else None),
        "cache_hit": raw.get("cache_hit"),
        "review_iterations": raw.get("review_iterations"),
        "rework": bool(raw.get("rework", False)),
        "duplicate_findings_count": raw.get("duplicate_findings_count"),
        "standards_refs_count": raw.get("standards_refs_count"),
    }


def _infer_success(status: str, explicit: Any) -> bool | None:
    if explicit is True or explicit is False:
        return explicit
    if status in MEANINGFUL_STATUSES:
        return True
    if status in {"FAILED"}:
        return False
    # Missing telemetry must not become success
    return None


def record_execution(home: Path, raw: dict[str, Any]) -> dict[str, Any]:
    ensure_layout(home)
    exe = normalize_execution(raw)

    def mutate(state: dict[str, Any]) -> dict[str, Any]:
        if execution_exists(home, exe["execution_id"]):
            return {
                "status": "duplicate",
                "execution": exe,
                "state": state,
                "trigger": None,
            }
        append_jsonl(home / "logs" / "executions.jsonl", exe)
        trigger = None
        counted = False
        if (
            exe["meaningful"]
            and not exe["trivial"]
            and not exe["cancelled"]
            and exe["delivery_status"] in MEANINGFUL_STATUSES
        ):
            state["meaningful_completed_count"] = int(state.get("meaningful_completed_count") or 0) + 1
            state["since_lightweight"] = int(state.get("since_lightweight") or 0) + 1
            state["since_deep"] = int(state.get("since_deep") or 0) + 1
            counted = True
            if state["since_deep"] >= DEEP_EVERY:
                state["pending_trigger"] = "deep"
                trigger = "deep"
            elif state["since_lightweight"] >= LIGHTWEIGHT_EVERY:
                state["pending_trigger"] = "lightweight"
                trigger = "lightweight"
        if exe["delivery_status"] in FAILURE_STATUSES or exe.get("success") is False:
            if state.get("pending_trigger") not in {"deep", "lightweight"}:
                state["pending_trigger"] = "post_incident"
                trigger = trigger or "post_incident"
        return {
            "status": "recorded",
            "execution": exe,
            "counted": counted,
            "state": {
                "meaningful_completed_count": state.get("meaningful_completed_count"),
                "since_lightweight": state.get("since_lightweight"),
                "since_deep": state.get("since_deep"),
                "pending_trigger": state.get("pending_trigger"),
            },
            "trigger": trigger,
        }

    return with_state_lock(home, mutate)


def should_invoke(home: Path) -> dict[str, Any]:
    ensure_layout(home)
    state = read_json(home / "state.json", {})
    pending = state.get("pending_trigger")
    since_l = int(state.get("since_lightweight") or 0)
    since_d = int(state.get("since_deep") or 0)
    mode = None
    if pending in {"deep", "lightweight", "post_incident", "before_after", "on_demand"}:
        mode = pending
    elif since_d >= DEEP_EVERY:
        mode = "deep"
    elif since_l >= LIGHTWEIGHT_EVERY:
        mode = "lightweight"
    return {
        "invoke": mode is not None,
        "mode": mode,
        "since_lightweight": since_l,
        "since_deep": since_d,
        "meaningful_completed_count": int(state.get("meaningful_completed_count") or 0),
        "pending_trigger": pending,
    }


def mark_trigger_consumed(home: Path, mode: str, analyzed_ids: list[str] | None = None) -> None:
    def mutate(state: dict[str, Any]) -> None:
        if mode == "lightweight":
            state["since_lightweight"] = 0
            state["last_lightweight_at_count"] = state.get("meaningful_completed_count")
        elif mode == "deep":
            state["since_lightweight"] = 0
            state["since_deep"] = 0
            state["last_deep_at_count"] = state.get("meaningful_completed_count")
        if state.get("pending_trigger") == mode:
            state["pending_trigger"] = None
        if analyzed_ids:
            existing = list(state.get("analyzed_execution_ids") or [])
            for i in analyzed_ids:
                if i not in existing:
                    existing.append(i)
            cap = int(state.get("analyzed_execution_ids_cap") or 500)
            state["analyzed_execution_ids"] = existing[-cap:]

    with_state_lock(home, mutate)


def compute_agent_stats(executions: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per-agent metrics. Missing success ≠ success."""
    agents: dict[str, dict[str, Any]] = {}
    for ex in executions:
        if ex.get("parse_error"):
            continue
        for a in ex.get("agents_invoked") or []:
            name = (a.get("name") or a.get("agent_name") or "unknown").lower()
            bucket = agents.setdefault(
                name,
                {
                    "invocations": 0,
                    "completed": 0,
                    "failed": 0,
                    "unknown_outcome": 0,
                    "retries_total": 0,
                    "duration_ms_total": 0,
                    "duration_samples": 0,
                },
            )
            bucket["invocations"] += 1
            st = (a.get("status") or "").lower()
            if st in {"completed", "success", "ok"}:
                bucket["completed"] += 1
            elif st in {"error", "failed", "aborted"}:
                bucket["failed"] += 1
            else:
                bucket["unknown_outcome"] += 1
            bucket["retries_total"] += int(a.get("retries") or 0)
            if a.get("duration_ms") is not None:
                try:
                    bucket["duration_ms_total"] += int(a["duration_ms"])
                    bucket["duration_samples"] += 1
                except (TypeError, ValueError):
                    pass

    out = {}
    for name, b in agents.items():
        known = b["completed"] + b["failed"]
        success_rate = (b["completed"] / known) if known else None
        out[name] = {
            **b,
            "success_rate": success_rate,
            "avg_retries": (b["retries_total"] / b["invocations"]) if b["invocations"] else None,
            "avg_duration_ms": (
                b["duration_ms_total"] / b["duration_samples"] if b["duration_samples"] else None
            ),
            # usefulness ≠ frequency
            "invocation_frequency": b["invocations"],
        }
    return out


def detect_repeated_failures(
    executions: list[dict[str, Any]], agent: str, min_count: int = 3
) -> dict[str, Any] | None:
    fails = []
    for ex in executions:
        for a in ex.get("agents_invoked") or []:
            name = (a.get("name") or "").lower()
            if name != agent.lower():
                continue
            st = (a.get("status") or "").lower()
            if st in {"error", "failed", "aborted"}:
                fails.append(ex.get("execution_id"))
    if len(fails) >= min_count:
        return {"agent": agent, "failure_count": len(fails), "execution_ids": fails}
    return None


def detect_unnecessary_invocations(
    executions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Heuristic: agent invoked on EXPLANATION/trivial classes where roster says rare value."""
    flags = []
    heavy = {"vishwakarma", "krishna", "decision-engine", "money-lens", "vyasa"}
    for ex in executions:
        tc = (ex.get("task_class") or "").upper()
        if tc not in {"EXPLANATION"} and not ex.get("trivial"):
            continue
        for a in ex.get("agents_invoked") or []:
            name = (a.get("name") or "").lower()
            if name in heavy:
                flags.append(
                    {
                        "execution_id": ex.get("execution_id"),
                        "task_class": tc,
                        "agent": name,
                        "reason": "heavy agent on explanation/trivial task",
                    }
                )
    return flags


def before_after_compare(
    before: list[dict[str, Any]], after: list[dict[str, Any]]
) -> dict[str, Any]:
    def window_stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(rows)
        successes = sum(1 for r in rows if r.get("success") is True)
        failures = sum(1 for r in rows if r.get("success") is False)
        unknown = sum(1 for r in rows if r.get("success") is None)
        return {
            "count": n,
            "success_true": successes,
            "success_false": failures,
            "success_unknown": unknown,
            "success_rate_known_only": (
                successes / (successes + failures) if (successes + failures) else None
            ),
        }

    return {"before": window_stats(before), "after": window_stats(after)}

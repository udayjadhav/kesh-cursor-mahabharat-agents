#!/usr/bin/env python3
"""Operational knowledge cache — implements kesh-token-cache fingerprint/TTL."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def cache_home() -> Path:
    raw = os.environ.get("KESH_CACHE_HOME")
    if raw:
        return Path(raw).expanduser().resolve()
    return Path.home() / ".cursor" / "knowledge" / "cache"


def ensure_cache(home: Path | None = None) -> Path:
    root = home or cache_home()
    (root / "entries").mkdir(parents=True, exist_ok=True)
    idx = root / "index.json"
    if not idx.exists():
        write_json(idx, {"version": 1, "entries": []})
    return root


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_topic(topic: str) -> str:
    t = topic.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


def fingerprint(
    topic: str,
    input_type: str,
    entities: list[str],
    code_revision_hint: str = "n/a",
) -> str:
    ent = "|".join(sorted({e.strip() for e in entities if e.strip()}))
    raw = f"{normalize_topic(topic)}|{input_type}|{ent}|{code_revision_hint}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".cache-", suffix=".json")
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
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def parse_iso(ts: str) -> datetime | None:
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def is_fresh(created_at: str, ttl_hours: int) -> bool:
    created = parse_iso(created_at)
    if not created:
        return False
    age_h = (datetime.now(timezone.utc) - created).total_seconds() / 3600.0
    return age_h <= float(ttl_hours)


# Content classes that must not be treated as current verification evidence when stale
NEVER_STALE_AS_EVIDENCE = frozenset(
    {"test_results", "security_review", "source_dependent", "bhishma", "lakshman"}
)


def get_entry(home: Path, fp: str) -> dict[str, Any]:
    ensure_cache(home)
    idx = read_json(home / "index.json", {"entries": []})
    meta = None
    for e in idx.get("entries") or []:
        if e.get("fingerprint") == fp:
            meta = e
            break
    if not meta:
        return {"result": "MISS", "fingerprint": fp}
    path = home / meta.get("path", f"entries/{fp}.json")
    entry = read_json(path, None)
    if not entry:
        return {"result": "MISS", "fingerprint": fp, "reason": "missing_entry_file"}
    ttl = int(meta.get("ttl_hours") or entry.get("ttl_hours") or 24)
    if not is_fresh(meta.get("created_at") or entry.get("created_at") or "", ttl):
        return {
            "result": "STALE",
            "fingerprint": fp,
            "entry": entry,
            "note": "Do not treat stale tests/security/source conclusions as current evidence",
        }
    return {"result": "HIT", "fingerprint": fp, "entry": entry, "meta": meta}


def put_entry(home: Path, entry: dict[str, Any], cap: int = 50) -> dict[str, Any]:
    ensure_cache(home)
    fp = entry.get("fingerprint")
    if not fp:
        return {"status": "error", "error": "fingerprint required"}
    # Strip forbidden bulk
    summaries = entry.get("agent_summaries") or {}
    clean_sum = {}
    for k, v in summaries.items():
        s = str(v)
        if len(s) > 8000:
            s = s[:8000] + "…[truncated]"
        clean_sum[k] = s
    entry = {
        **entry,
        "agent_summaries": clean_sum,
        "created_at": entry.get("created_at") or utc_now(),
    }
    # Never store secrets markers naively — reject obvious
    blob = json.dumps(entry)
    for needle in ("BEGIN RSA PRIVATE KEY", "AWS_SECRET", "password="):
        if needle.lower() in blob.lower():
            return {"status": "error", "error": "refusing to cache possible secret material"}

    rel = f"entries/{fp}.json"
    write_json(home / rel, entry)
    idx = read_json(home / "index.json", {"version": 1, "entries": []})
    entries = [e for e in (idx.get("entries") or []) if e.get("fingerprint") != fp]
    entries.append(
        {
            "fingerprint": fp,
            "topic": entry.get("topic"),
            "input_type": entry.get("input_type"),
            "entities": entry.get("entities") or [],
            "created_at": entry["created_at"],
            "ttl_hours": int(entry.get("ttl_hours") or 24),
            "path": rel,
            "content_class": entry.get("content_class") or "general",
        }
    )
    entries = entries[-cap:]
    idx = {"version": 1, "entries": entries}
    write_json(home / "index.json", idx)
    return {"status": "ok", "fingerprint": fp, "path": rel}


def invalidate(home: Path, fp: str | None = None, all_entries: bool = False) -> dict:
    ensure_cache(home)
    idx = read_json(home / "index.json", {"version": 1, "entries": []})
    if all_entries:
        for e in idx.get("entries") or []:
            p = home / e.get("path", "")
            if p.exists():
                p.unlink()
        write_json(home / "index.json", {"version": 1, "entries": []})
        return {"status": "cleared_all"}
    if not fp:
        return {"status": "error", "error": "fingerprint or --all required"}
    kept = []
    for e in idx.get("entries") or []:
        if e.get("fingerprint") == fp:
            p = home / e.get("path", "")
            if p.exists():
                p.unlink()
        else:
            kept.append(e)
    write_json(home / "index.json", {"version": 1, "entries": kept})
    return {"status": "invalidated", "fingerprint": fp}

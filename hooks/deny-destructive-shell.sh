#!/usr/bin/env bash
# Kesh optional safety hook — beforeShellExecution
# Reads Cursor hook JSON on stdin; prints permission JSON on stdout.
# Requires python3.
set -euo pipefail

MODE="${KESH_HOOK_MODE:-ask}"
INPUT="$(cat)"

export KESH_HOOK_MODE="$MODE"
export KESH_HOOK_INPUT="$INPUT"

python3 - <<'PY'
import json, os, re, sys

mode = os.environ.get("KESH_HOOK_MODE", "ask")
raw = os.environ.get("KESH_HOOK_INPUT", "")

try:
    payload = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    payload = {}

command = payload.get("command") or payload.get("cmd") or ""
if not command and isinstance(payload.get("input"), dict):
    command = payload["input"].get("command") or ""

if mode == "off":
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

patterns = [
    r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b",
    r"\bTRUNCATE\s+TABLE\b",
    r"\bDELETE\s+FROM\b.+\bWHERE\s+1\s*=\s*1\b",
    r"\bgit\s+push\s+[^\n]*--force\b",
    r"\bgit\s+push\s+[^\n]*\s-f\b",
    r"\bgit\s+push\s+-f\b",
    r"\bgit\s+reset\s+[^\n]*--hard\b",
    r"\brm\s+-[^\s]*r[^\s]*f\b|\brm\s+-[^\s]*f[^\s]*r\b",
    r"\bkubectl\s+delete\b",
    r"\bhelm\s+uninstall\b",
    r"\bterraform\s+destroy\b",
    r"\baws\s+s3\s+rb\b",
    r"\bgsutil\s+rm\s+-r\b",
    r"\bdocker\s+system\s+prune\b",
    r"\bALTER\s+TABLE\b.+\bDROP\b",
    r"\bproduction\b.+\bdeploy\b|\bdeploy\b.+\bproduction\b|\bprod\b.+\bdeploy\b",
    r"\bflyway\s+repair\b",
    r"\bpsql\b.+\b-c\b.+\bDROP\b",
]

matched = None
for p in patterns:
    if re.search(p, command, flags=re.IGNORECASE):
        matched = p
        break

if not matched:
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

permission = "deny" if mode == "deny" else "ask"
msg = (
    "Kesh safety hook flagged a potentially destructive or production-impacting command. "
    "Review carefully. Destructive database operations, force-push, and production deploys "
    "require explicit human approval."
)
print(json.dumps({
    "permission": permission,
    "user_message": msg,
    "agent_message": f"Blocked/ask pattern matched ({matched}) for command: {command[:200]}",
}))
sys.exit(0)
PY

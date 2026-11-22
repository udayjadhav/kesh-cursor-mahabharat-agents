# NITI telemetry (kit)

Local-first execution telemetry and trigger helpers for the NITI agent.

**Runtime data directory (default):** `~/.cursor/niti/`  
**Override:** `KESH_NITI_HOME`

This folder in the kit ships **schemas, templates, and docs**. Live logs are written under the runtime home after install / first use — not into the git repo.

## Honest capabilities

| Capability | Status |
|------------|--------|
| Append redacted hook events | **D** when NITI hooks installed |
| Record meaningful executions | **D** via `scripts/niti/record_execution.py`; Kesh must call it (**B**) |
| Persist task counters across sessions | **D** (`state.json`) |
| Nudge NITI after 5 / 20 tasks | **D** via `stop` hook `followup_message` — **not** cron |
| Billing tokens / USD cost from Cursor Agent hooks | **Unavailable** — fields stay `null` + `*_available: false` |
| Auto-rewrite agents/rules | **Forbidden** — NITI proposes only |

See [docs/kesh-2.0/NITI-AUDIT.md](../docs/kesh-2.0/NITI-AUDIT.md).

## Layout (runtime)

```text
~/.cursor/niti/
  state.json
  logs/events.jsonl
  logs/executions.jsonl
  recommendations.jsonl
  reports/
```

## Quick commands

```bash
# Record a meaningful delivery (called by Kesh at end of work)
python3 scripts/niti/record_execution.py --file /path/to/execution.json

# Should NITI run?
python3 scripts/niti/should_invoke.py

# Prepare context bundle for NITI
python3 scripts/niti/analyze_prep.py --mode lightweight
```

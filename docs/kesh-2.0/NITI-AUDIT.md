# NITI Audit & Implementation Plan

**Date:** 2026-11-22  
**Branch:** `feature/niti-activation`  
**Authority:** verified against this repository + Cursor Hooks documentation (cursor.com docs → Hooks)

---

## Phase 1 — Audit findings

### Documented vs executable

| Claim | Where claimed | Verified reality | Level |
|-------|---------------|------------------|-------|
| NITI runs every 5 tasks | `agents/niti.md` frontmatter | **No counter, no scheduler, no hook** | B (prompt myth) |
| NITI receives `execution_logs` JSON | `agents/niti.md` input format | **No producer in kit**; `~/.cursor/niti/logs/executions.jsonl` is **empty (0 bytes)** | Dead contract |
| Kesh invokes NITI periodically | `agents/kesh.md` (“Periodic / on-demand”) | One-line mention only; **no workflow step** in `kesh-flows.md` / `WORKFLOW.md` | B |
| Agent performance metrics collected | Implied by NITI input | **Not in kit**; hooks only gate destructive shell | Absent |
| Sutradhar feeds NITI | — | Sutradhar tracks in-loop `execution_state` in-prompt only; **never persists** | B |
| Runtime router / cache gate trigger NITI | — | **Zero references** in those rules | Absent |
| Installer sets up NITI telemetry | `install.sh` | Installs agents/rules/skills; optional safety hooks only — **no NITI telemetry** | Absent |
| Legacy `~/.cursor/niti/` | Outside kit (Phase-1 baseline) | Exists (Apr 2026): empty JSONL + sample report referencing **Spartan** (pre-Kesh). **Not wired** | Orphan |

### Answers to audit questions

1. **How NITI is invoked today:** Only if a human/agent manually `@niti` or Kesh decides ad hoc. No automatic path.
2. **Five-task trigger implemented?** **No.**
3. **Execution logs generated?** **No** (file exists empty; no writer in kit).
4. **Agent performance metrics collected?** **No.**
5. **Does NITI receive actual execution data?** **No** — would need pasted/synthetic JSON.
6. **Access to previous execution history?** Directory exists; **no data**. Transcripts exist under Cursor project paths but NITI is not instructed to read them as primary telemetry.
7. **Can recommendations influence future workflows?** **No closed loop** — JSON output only; no recommendation store or approval workflow.
8. **Model / tier appropriate?** Currently **Tier B / `composer-2`** (execution). NITI does **evaluation and system design recommendations**, not app coding → **mis-tiered**. Target: **Tier A / `claude-4-6-sonnet`** (same band as Sarthi / Money Lens / Kripacharya). Remains **outside** mandatory delivery path.

### Hooks / telemetry platform facts (do not invent)

**Available (Agent Chat hooks):** `sessionStart`, `sessionEnd`, `subagentStart`, `subagentStop`, `stop`, `postToolUse` / `postToolUseFailure`, shell/MCP/file hooks, `preCompact` (context window counts — **not** billing tokens).

**Useful fields:** `conversation_id`, `generation_id`, `model` / `model_id`, `subagent_type`, `status`, `duration_ms` / `duration`, `loop_count`, failure messages.

**Not exposed on Agent Chat hooks:** billing token usage, USD cost. Mark `token_usage_available: false` / `cost_available: false` unless filled manually.

**Auto-continue:** `stop` and `subagentStop` may return `followup_message` (subject to `loop_limit`). This is **not** cron — only fires when an agent turn stops.

**Current kit hooks:** `beforeShellExecution` destructive gate only. No telemetry hooks.

---

## Phase 2–7 — Design summary

### Role

NITI = **independent optimization & evaluation specialist**. Never implements product features. Proposes changes; **Kesh + human approve** material kit changes. Recommendation lifecycle: `PROPOSED → APPROVED → IMPLEMENTED → EVALUATED → ACCEPTED | REVERTED`.

### Local-first telemetry (`~/.cursor/niti/`)

```
niti/
  state.json                 # counters, pending trigger, analyzed ids
  logs/events.jsonl          # redacted hook events
  logs/executions.jsonl      # meaningful execution records
  recommendations.jsonl
  reports/*.md               # human reports
```

No external DB. No source code / secrets in logs (hooks omit file contents, prompt text, edit bodies).

### Dual write path

| Path | Mechanism | Enforcement |
|------|-----------|-------------|
| Raw events | Hooks → `record_event.py` | **D** when hooks installed |
| Meaningful executions | Kesh/Sutradhar call `record_execution.py` at delivery | **B** (prompt) + **D** (script) |
| Threshold nudge | `stop` hook → `stop_trigger.py` → optional `followup_message` | **D** when hooks installed |
| On-demand / post-incident / before-after | User or Kesh invokes NITI | **B** |

**Honest limit:** Without installed hooks + Kesh recording, counters do not advance. Do **not** claim periodic scheduling.

### Triggers

| Trigger | Condition | Depth |
|---------|-----------|-------|
| Lightweight | every **5** completed meaningful (`COMPLETE`/`PARTIAL`) | last ~10–20 executions |
| Deep | every **20** completed meaningful | broader window + recommendations backlog |
| Post-incident | `FAILED` or significant workflow failure recorded | failure-focused |
| On-demand | user asks | as requested |
| Before/after | after material Kesh kit change (tagged evaluation) | compare windows |

Counters in `state.json` persist across sessions. Dedup by `execution_id`. Incomplete/cancelled/trivial not counted.

### Evaluation lenses (distinct)

- Performance (success, retries, latency)
- Usefulness / unique value
- Invocation frequency (low ≠ bad)
- Engineering value (e.g. security reviewer)

### Human reports

Natural-language system health report + separate machine JSON sidecar. Never JSON-only. State evidence limitations explicitly.

---

## Phase 8 — Validation plan

Executable tests under `tests/niti/` covering: telemetry ingest, 5/20 counters across sessions (state file), failures captured, missing ≠ success, dedup, repeated failure detection helpers, unnecessary-invocation heuristic, recommendation lifecycle, before/after metric compare. Mark capabilities complete **only** after tests pass.

---

## Implementation checklist

1. Rewrite `agents/niti.md` (Tier A sonnet, responsibilities, report format, no auto-mutate kit)
2. Add `rules/kesh-niti.mdc` + wire Kesh / flows / WORKFLOW / AGENTS / CHANGELOG / validator
3. Ship `niti/` schema + `scripts/niti/*` + hooks templates
4. Installer opt-in `INSTALL_NITI=1`
5. Tests + run them
6. Do **not** commit/push without approval

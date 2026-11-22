# Token Optimization Architecture

**Spec version:** 2.5.0  
**Companion audit:** [TOKEN-OPTIMIZATION-AUDIT.md](./TOKEN-OPTIMIZATION-AUDIT.md)

## Goal

Maximize verified engineering outcomes per token. Spend less on repetition and orchestration overhead; spend enough on reasoning, verification, and independent challenge.

## Execution modes

| Mode | Use for | Typical agents |
|------|---------|----------------|
| **FAST** | Explanations, isolated low-risk Qs | Minimal (often Sanjaya and/or Kesh); deterministic checks if code touched |
| **STANDARD** | Features, fixes, refactors, PR review | Implement → test → specialized review |
| **CRITICAL** | Security, DB, distributed, consequential prod-bound | Architecture as needed → implement → test → independent review → gates as warranted |
| **INCIDENT_ARCHITECTURE** | Prod incidents, major system change | Full applicable specialists + independent validation |

**Selection:** from `task_class` + risk signals (security, schema, prod, blast radius).  
**Escalation:** allowed when new risks appear.  
**Never downgrade** solely to save tokens.

Rule: `rules/kesh-execution-modes.mdc`  
Router: `rules/kesh-runtime-router.mdc`  
Selector: `scripts/modes/select_mode.py`

## Context packaging

Each Task/subagent gets a **context package**, not the whole chat or every rule file.

Fields: requirements, constraints, source_refs, standards_refs, verified_findings, expected_output, dependencies, open_questions, mode, task_class.

Tool: `scripts/context/package.py`  
Rule: `rules/kesh-context-packaging.mdc`

## Progressive standards

```bash
python3 scripts/standards/select_standards.py --paths 'src/Foo.java,migration.sql'
```

Core code-quality always for code changes; language/DB/security/distributed only when paths/inventory warrant.

## Deterministic verification first

Prefer project formatters, linters, compilers, typecheckers, tests, scanners, schema validators. LLM review **complements** tools — does not replace failed or skipped mandatory tests.

## Specialized review

| Agent | Primary | Blocks on |
|-------|---------|-----------|
| Bhishma | Correctness, security, data integrity, contracts | CRITICAL / HIGH |
| Lakshman | Requirements/behavior / edge cases | Requirement misses, broken behavior |
| Draupadi | User/customer impact | Advisory (unless CRITICAL user harm + Kesh elevates) |

Do not triple-report the same stylistic nit. Do not suppress real security/correctness issues.

## Operational cache

```bash
python3 scripts/cache/fingerprint.py ...
python3 scripts/cache/get.py --fingerprint ...
python3 scripts/cache/put.py --file entry.json
python3 scripts/cache/invalidate.py --fingerprint ... | --all
```

Never treat stale tests/security/source-dependent conclusions as current evidence.

## NITI

Records proxies: `context_chars`, `agents_invoked_count`, `cache_hit`, `review_iterations`, `rework`. Billing tokens remain unavailable from Agent Chat hooks unless filled manually.

## Quality guardrails

`rules/kesh-quality-guardrails.mdc` — non-negotiables that token savings cannot override.

## Benchmarks

`benchmarks/token-optimization/` — 10 fixed scenarios; harness measures mode, agent count, standards set, context package size. Live LLM quality before/after requires operator runs — kit records structure, not fabricated token bills.

## Migration

1. Pull `feature/token-optimization` (or install kit 2.5).  
2. Optional: demoted alwaysApply rules take effect after Cursor reload.  
3. Use `select_mode.py` / `package.py` / `standards/select_standards.py` / `cache/*` in deliveries.  
4. `INSTALL_NITI=1` if telemetry desired.

## Rollback

1. Revert to previous kit tag / re-install prior agents+rules.  
2. Re-enable demoted rules’ `alwaysApply: true` if needed.  
3. Cache files under `~/.cursor/knowledge/cache` are additive — delete entries to clear.  
4. No DB migrations; local files only.

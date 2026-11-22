# Rules Reference

Cursor rules live under `rules/` (nested `standards/` included). Files with `alwaysApply: true` apply broadly when installed to `~/.cursor/rules/`. Glob-scoped rules load selectively (**C**).

## Core Kesh rules (required)

| File | alwaysApply | Purpose |
|------|-------------|---------|
| `kesh-agent-spec.mdc` | yes | **Canonical contract** (evolving in 2.0 toward adaptive workflows) |
| `kesh-runtime-router.mdc` | yes | Intent → agent selection |
| `kesh-always-on.mdc` | yes | Route engineering work through Kesh by default |
| `kesh-token-cache.mdc` | yes | Step 0.5 Cache Gate |
| `kesh-knowledge-discovery.mdc` | yes | Tech detection, gap research, MDC propose/update |
| `kesh-human-communication.mdc` | yes | Staff/Principal voice; paste-ready findings; no AI filler |
| `kesh-code-quality.mdc` | yes | Code maintainability, comments, contracts, docs/ADRs (no doc spam) |
| `kesh-niti.mdc` | yes | NITI telemetry, triggers, evaluation lenses, recommend-only loop |
| `kesh-execution-modes.mdc` | no (via router/spec) | FAST / STANDARD / CRITICAL / INCIDENT_ARCHITECTURE |
| `kesh-context-packaging.mdc` | no (via router/spec) | Per-agent context packages (no full-chat dumps) |
| `kesh-quality-guardrails.mdc` | yes | Token savings never override correctness/security/tests |
| `kesh-explanation-framework.mdc` | no (selective) | Chat explanation structure |
| `kesh-external-output-voice.mdc` | no (when external paste) | Scrub agent vocabulary; channel packaging |
| `global-local-sync.mdc` | no (agents/rules edits) | Global vs local overrides |

## Quality and design rules

| File | alwaysApply | Purpose |
|------|-------------|---------|
| `reuse-before-extend.mdc` | yes | Option 0 reuse-only; field carrier inventory |
| `dev-spec-authorship-voice.mdc` | no (specs/docs globs) | Specs read as engineer-authored |
| `dev-spec-scoping-defaults.mdc` | no | L1–L6 lifecycle tasks in dev specs |

## Engineering standards (Kesh 2.0)

See [STANDARDS.md](./STANDARDS.md). Path: `rules/standards/**` — `alwaysApply: false`, glob-selective.

Includes Java/Quarkus, Python, React/TS, security, testing, architecture, microservices, distributed systems, database tree + engines, and optional Clojure pack.

## Optional / org-specific

| File | Notes |
|------|-------|
| `optional/teams.mdc` | Jira roster template — copy into rules only if needed |

## Rule precedence

1. `kesh-agent-spec.mdc` wins over agent `.md` files
2. Local `<repo>/.cursor/rules/` overrides global for that repo
3. Engine-specific DB standards override generic DB advice when they conflict
4. Repository evidence overrides generic standards when they conflict

## Key invariants

- Parth and Bhishma **must not** share the same model
- No self-approval of implementation by the implementer
- LLM review does not replace security scanners or test execution evidence
- Skip agents by applicability and task class — not to inflate coverage arbitrarily

## Editing after install

```bash
vim ~/.cursor/rules/kesh-agent-spec.mdc
vim ~/.cursor/rules/standards/java-quarkus.mdc
```

Restart Cursor or reload the window after changes.

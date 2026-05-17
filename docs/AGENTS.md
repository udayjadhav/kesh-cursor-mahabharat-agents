# Agent Reference

All agent files live in `agents/<name>.md`. Each file has YAML frontmatter:

```yaml
---
model: claude-4-7-opus   # pinned model (see Cursor subagents docs)
name: kesh
description: ...
---
```

## Tier model

| Tier | Purpose | Typical models |
|------|---------|----------------|
| **A** | Deep reasoning — planning, gates, final authority | `claude-4-7-opus`, `claude-4-6-sonnet` |
| **B** | Fast execution — code and tests | `composer-2` |
| **C** | Independent critique — must differ from executor | `claude-4-6-sonnet` |

## Complete roster

### Tier A — Strategic / planning

| Agent | File | Model | Output |
|-------|------|-------|--------|
| **Kesh** | `kesh.md` | claude-4-7-opus | SHIP / NO-SHIP / HOLD; orchestrates all |
| **Vidura** | `vidura.md` | claude-4-7-opus | Requirements, edge cases, acceptance criteria |
| **Sanjaya** | `sanjaya.md` | claude-4-6-sonnet | Repo map, architecture, risks (XRay) |
| **Vyasa** | `vyasa.md` | claude-4-6-sonnet | Org context bundle (Confluence, Jira, helpcenter, dev ref, status) |
| **Vishwakarma** | `vishwakarma.md` | claude-4-7-opus | Architecture options incl. **Option 0 — Reuse-only** |
| **Sarthi** | `sarthi.md` | claude-4-6-sonnet | Task breakdown, estimates, dependencies |
| **Krishna** | `krishna.md` | claude-4-7-opus | STRONG / WEAK / KILL; devil's advocate |
| **Money Lens** | `money-lens.md` | claude-4-6-sonnet | INVEST / DEFER / REJECT |
| **Decision Engine** | `decision-engine.md` | claude-4-7-opus | GO / CONDITIONAL / NO-GO + tradeoffs |
| **Kripacharya** | `kripacharya.md` | claude-4-6-sonnet | Production-readiness NOT-READY / READY |

### Tier B — Execution

| Agent | File | Model | Output |
|-------|------|-------|--------|
| **Parth** | `parth.md` | composer-2 | Production code only (no self-review) |
| **Swachalit** | `swachalit.md` | composer-2 | Unit/integration tests, coverage gaps |
| **Sutradhar** | `sutradhar.md` | composer-2 | Coordinates build–critique loop |
| **NITI** | `niti.md` | composer-2 | Agent performance / inefficiency analysis |

### Tier C — Critique

| Agent | File | Model | Output |
|-------|------|-------|--------|
| **Bhishma** | `bhishma.md` | claude-4-6-sonnet | PASS/FAIL code review; schema reuse check |
| **Lakshman** | `lakshman.md` | claude-4-6-sonnet | PASS/FAIL QA; edge cases |
| **Draupadi** | `draupadi.md` | claude-4-6-sonnet | Customer impact (advisory) |

## Kesh support modules

| File | Role |
|------|------|
| `kesh-flows.md` | Input types, 15-step diagram, parallel points, emergency |
| `kesh-context.md` | What each agent receives and returns |
| `kesh-output.md` | Tables, verdicts, diagrams for final response |
| `kesh-rules.md` | Index of enforcement rules |

## When to invoke which agent

| User intent | Primary agents |
|-------------|----------------|
| Understand codebase | Sanjaya (+ Vyasa if org topic) |
| Clarify vague ask | Vidura |
| Design / RFC | Vishwakarma, Sarthi |
| Implement feature | Kesh → full flow or Parth under Sutradhar |
| Review PR / diff | Bhishma, Lakshman, Draupadi |
| Is this worth building? | Krishna, Money Lens |
| Final ship decision | Kripacharya, Kesh |

## Invocation in Cursor

```
@kesh <task>           # supervisor (recommended default)
@sanjaya analyze repo
@bhishma review changes
@krishna challenge this design
```

Aliases for Kesh: `ai`, `assistant`, `system`, `boss` (see `kesh.md`).

## Adding a new agent

1. Create `agents/my-agent.md` with `name`, `model`, `description` in frontmatter.
2. Assign tier A/B/C and pick a model consistent with tier rules.
3. Update `kesh.md` orchestration list.
4. Update `rules/kesh-agent-spec.mdc` roster if the agent is mandatory in the flow.

## Model fallback

If a pinned model is unavailable (plan, Max Mode, admin block), Cursor may fall back to the parent model. Check usage reports; update frontmatter slugs per [Cursor models docs](https://cursor.com/docs/models-and-pricing).

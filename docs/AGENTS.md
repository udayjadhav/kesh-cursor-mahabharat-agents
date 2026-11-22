# Agent Reference (Kesh 2.0)

All agent files live in `agents/<name>.md` with YAML frontmatter:

```yaml
---
model: claude-4-7-opus
name: kesh
description: ...
---
```

## Tier model

| Tier | Purpose | Typical models |
|------|---------|----------------|
| **A** | Deep reasoning | `claude-4-7-opus`, `claude-4-6-sonnet` |
| **B** | Fast execution | `composer-2` |
| **C** | Independent critique (≠ Parth) | `claude-4-6-sonnet` |

## Complete roster

### Tier A

| Agent | File | Model | Output |
|-------|------|-------|--------|
| **Kesh** | `kesh.md` | claude-4-7-opus | Delivery status; consolidated report |
| **Vidura** | `vidura.md` | claude-4-7-opus | Requirements + edge cases |
| **Sanjaya** | `sanjaya.md` | claude-4-6-sonnet | Repo map (XRay) |
| **Vyasa** | `vyasa.md` | claude-4-6-sonnet | Org context or `no_context` |
| **Vishwakarma** | `vishwakarma.md` | claude-4-7-opus | Options + ADR; Option 0 |
| **Sarthi** | `sarthi.md` | claude-4-6-sonnet | Plan + estimates |
| **Krishna** | `krishna.md` | claude-4-7-opus | STRONG / WEAK / KILL |
| **Money Lens** | `money-lens.md` | claude-4-6-sonnet | Advisory trade-offs |
| **Decision Engine** | `decision-engine.md` | claude-4-7-opus | GO / CONDITIONAL / NO-GO |
| **Kripacharya** | `kripacharya.md` | claude-4-6-sonnet | READY / NOT-READY |

### Tier B

| Agent | File | Model | Output |
|-------|------|-------|--------|
| **Parth** | `parth.md` | composer-2 | Code + check evidence |
| **Swachalit** | `swachalit.md` | composer-2 | Tests + execution evidence |
| **Sutradhar** | `sutradhar.md` | composer-2 | Loop state + stop on critical fail |
| **NITI** | `niti.md` | claude-4-6-sonnet | Optimization & evaluation (out of band; telemetry-driven) |
| **API Architect** | `api-architect.md` | claude-4-6-sonnet | API/contract critique (not implementer) |
| **AI Product Engineer** | `ai-product-engineer.md` | claude-4-6-sonnet | LLM product architecture + evals |

Optional: **Healthcare Domain** — `optional/healthcare/agents/healthcare-domain.md` (`INSTALL_HEALTHCARE=1`).

### Tier C

| Agent | File | Model | Output |
|-------|------|-------|--------|
| **Bhishma** | `bhishma.md` | claude-4-6-sonnet | Issues-only review; PASS/FAIL |
| **Lakshman** | `lakshman.md` | claude-4-6-sonnet | QA PASS/FAIL |
| **Draupadi** | `draupadi.md` | claude-4-6-sonnet | Customer impact (advisory) |

## Support modules

| File | Role |
|------|------|
| `kesh-flows.md` | Adaptive classification + loops |
| `kesh-context.md` | Shared context object |
| `kesh-output.md` | Delivery report template |
| `kesh-rules.md` | Enforcement index |

## When to invoke

| Intent | Primary agents |
|--------|----------------|
| Explain / investigate | Sanjaya (± Vyasa) |
| Vague requirements | Vidura |
| Design / ADR | Vishwakarma, Krishna (+ staff-engineering skill / `scripts/adr`) |
| API contract | api-architect (± Vishwakarma) |
| LLM product | ai-product-engineer |
| Implement | Sutradhar → Parth → Swachalit → Bhishma |
| Review PR | Bhishma, Lakshman, Draupadi |
| Incident | Evidence-first path; approval for consequential acts |
| Orchestrate | `@kesh` (recommended default) |

Kesh selects a **minimum sufficient** set per `task_class` — not all agents every time.

## Model fallback

If a pinned model is unavailable, Cursor may fall back. Note fallbacks in the delivery report. See [Cursor models docs](https://cursor.com/docs/models-and-pricing).

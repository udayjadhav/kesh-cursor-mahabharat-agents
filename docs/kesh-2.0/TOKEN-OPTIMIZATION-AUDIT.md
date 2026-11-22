# Token Optimization — Current-State Inefficiency Report

**Date:** 2026-11-22  
**Branch:** `feature/token-optimization`  
**Principle:** Maximize *verified engineering outcomes per token* — not cheapest AI.

---

## Verified inefficiencies (evidence in-repo)

| ID | Inefficiency | Evidence | Impact |
|----|--------------|----------|--------|
| V1 | **13 `alwaysApply: true` rules** loaded every chat turn (pre-2.5) | `rg alwaysApply` baseline; large rules (explanation, external-voice, authorship, sync) | High fixed cost on *every* message → **2.5 demotes 4** (+ keeps short guardrails); target ≈10 always-on |
| V2 | **`agents/bhishma.md` ≈ 29KB** | `wc -c` | Large critic prompt even when review scope is narrow |
| V3 | **Token cache is prompt-only** | `optional/knowledge-cache/README.md` + no `scripts/cache/*` writers | Repeated Sanjaya/xray / architecture work across sessions |
| V4 | **Cache rule still cites “Agent Maximization”** | `kesh-token-cache.mdc` header | Stale mental model → over-invocation risk |
| V5 | **Context packaging is advisory only** | `kesh-context.md` “pass only relevant slices” — no schema/tool | Agents often receive over-broad handoffs (observed as process gap) |
| V6 | **No executable standards selector** | Standards use Cursor globs (**good**), but chat-only / Task prompts lack a selector script | Risk of naming “all standards” in plans |
| V7 | **NITI has no token/outcome metrics** | NITI 2.4 telemetry: tokens marked unavailable; no context-size proxy | Cannot optimize from data |
| V8 | **Billing tokens unavailable from Agent hooks** | Cursor Hooks docs + NITI audit | Must use proxies (context chars, agent counts) + honesty labels |

## Hypotheses (not yet measured on live tasks)

| ID | Hypothesis | How to verify |
|----|------------|---------------|
| H1 | Review trio duplicates findings on STANDARD patches | Benchmark scenario 10 — count overlapping issues |
| H2 | Opus agents used where STANDARD Sonnet/composer would suffice | Mode routing + before/after quality on scenarios 1–4 |
| H3 | Full conversation replayed into each Task | Inspect Task prompts; enforce context packages |
| H4 | Explanation tasks still pull FEATURE-sized stacks | Mode = FAST agent-count metric |

## What already works (preserve)

- Adaptive `task_class` + minimum-sufficient agents (spec 2.x) — **not** mandatory 15-step
- Standards `alwaysApply: false` + **globs** (Java/Python/React/DB/security)
- Knowledge discovery gate (SUFFICIENT → no research theater)
- Parth = composer-2 ≠ Bhishma = sonnet (independent critique)
- Money Lens advisory (no ROI hard-stop on mandatory fixes)
- NITI out-of-band (not on every delivery)

## Model assignment audit

| Agent | Current pin | Role fit | Change in this work? |
|-------|-------------|----------|----------------------|
| Kesh, Vidura, Vishwakarma, Krishna, Decision Engine | `claude-4-7-opus` | High-ambiguity / architecture / gates | **No** — needs live quality benchmark before any downgrade |
| Sanjaya, Vyasa, Sarthi, Money Lens, Kripacharya, NITI, critics | `claude-4-6-sonnet` | Analysis / critique | **No** |
| Parth, Swachalit, Sutradhar | `composer-2` | Routine implementation / tests / orchestration | **No** — already efficient lane |

**Note:** Subagent override slugs in the IDE catalog can differ from agent frontmatter pins. Do **not** swap identifiers without Max Mode/plan checks and scenario benchmarks.

## Stages that add little value when misapplied

| Stage | Wasteful when… | Keep when… |
|-------|----------------|------------|
| Full Vidura | User gave a crisp one-line fix | Ambiguous FEATURE |
| Vyasa | No org footprint | Contracts / incidents / customer claims |
| Krishna + Money Lens + Decision Engine | Tiny PATCH | ARCHITECTURE / CRITICAL / INCIDENT |
| Lakshman + Draupadi | Pure internal rename, no user surface | API/UI/behavior change |
| NITI | Every task | Threshold / incident / on-demand |

---

## Target architecture (summary)

1. **`execution_mode`:** FAST | STANDARD | CRITICAL | INCIDENT_ARCHITECTURE — risk-selected; escalate only upward  
2. **Context packages** — per-agent JSON; file refs not full dumps  
3. **Progressive standards** — `scripts/standards/select_standards.py` from paths/inventory  
4. **Deterministic verification first** — lint/test/typecheck before LLM ceremony  
5. **Specialized review** — Bhishma / Lakshman / Draupadi non-overlapping primary duties; severity blocking  
6. **Operational cache** — `scripts/cache/*` implementing existing fingerprint/TTL spec  
7. **NITI** — tokens_proxy, agents_invoked, cache hit rate, rework; propose only  
8. **Guardrails** — never trade correctness/security/tests/independent high-risk review for tokens  

Details: `docs/kesh-2.0/TOKEN-OPTIMIZATION.md`

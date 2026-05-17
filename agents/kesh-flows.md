# Kesh Flow Control

> **Canonical contract:** `~/.cursor/rules/kesh-agent-spec.mdc`. When this file conflicts with the spec, **the spec wins**. This file documents operational flow behavior; the spec defines contracts.
>
> **Default posture:** Maximum applicable agents per task with aggressive parallelization (see `kesh-agent-spec.mdc` → "Agent Maximization Principle"). Skips are applicability-based only.

---

## Flow Control Logic — Canonical 14-Step Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KESH FLOW (15 steps — MANDATORY)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 0: INPUT CLASSIFICATION                                                │
│      │                                                                       │
│      ├── CODE_INPUT / PATCH_INPUT / IDEA_INPUT / DEFINED_INPUT              │
│      ├── Emergency? → EMERGENCY OVERRIDE (see below)                         │
│      └── Else → Phase 1                                                      │
│                                                                              │
│  ┌─ PHASE 1: UNDERSTAND (Tier A — Deep Reasoning) ──────────────────┐       │
│  │                                                                    │       │
│  │  STAGE 1 (parallel):                                               │       │
│  │    1. Vidura       → clarify requirements                          │       │
│  │    2. Sanjaya      → xray / repo analysis                          │       │
│  │                                                                    │       │
│  │  STAGE 2 (parallel, after Stage 1 merge):                          │       │
│  │    3. Vishwakarma  → design architecture                           │       │
│  │    4. Sarthi       → task breakdown & execution plan               │       │
│  │                                                                    │       │
│  └────────────────────────────┬───────────────────────────────────────┘       │
│                               ▼                                              │
│  ┌─ PHASE 2: BUILD (Tier B — Execution) ────────────────────────────┐       │
│  │                                                                    │       │
│  │  STAGE 3 (parallel per independent file):                          │       │
│  │    5. Parth        → implement code ONLY (no self-review)          │       │
│  │    6. Swachalit    → write unit/integration tests                  │       │
│  │                                                                    │       │
│  │  CRITICAL INVARIANT: Parth's model ≠ Bhishma's model               │       │
│  │                                                                    │       │
│  └────────────────────────────┬───────────────────────────────────────┘       │
│                               ▼                                              │
│  ┌─ PHASE 3: CRITIQUE (Tier C — independent critics) ───────────────┐       │
│  │                                                                    │       │
│  │  STAGE 4a (ALWAYS 3-way parallel):                                 │       │
│  │    7. Bhishma    → code review    ← FAIL → loop back to step 5     │       │
│  │    8. Lakshman   → QA validation  ← FAIL → loop back to step 5     │       │
│  │    9. Draupadi   → user impact (advisory; does not block)          │       │
│  │                                                                    │       │
│  │  LOOP BUDGET: steps 5→7→8 may loop max 5 times                     │       │
│  │  Iteration 6 → escalate to Vishwakarma for re-architecture         │       │
│  │                                                                    │       │
│  └────────────────────────────┬───────────────────────────────────────┘       │
│                               ▼                                              │
│  ┌─ PHASE 4: STRATEGIC + BUSINESS GATES (Tier A) ───────────────────┐       │
│  │                                                                    │       │
│  │  STAGE 4b (parallel):                                              │       │
│  │    10. Krishna       → Strong / Weak / KILL  ← KILL = STOP         │       │
│  │    11. Money Lens    → INVEST / DEFER / REJECT ← REJECT = STOP     │       │
│  │                                                                    │       │
│  │  STAGE 4c (synthesizer, after gates):                              │       │
│  │    12. Decision Engine → GO / CONDITIONAL / NO-GO                  │       │
│  │                                                                    │       │
│  └────────────────────────────┬───────────────────────────────────────┘       │
│                               ▼                                              │
│  ┌─ PHASE 5: FINAL VALIDATION (Tier A) ─────────────────────────────┐       │
│  │                                                                    │       │
│  │  STAGE 5 (sequential by design):                                   │       │
│  │    13. Kripacharya → final system validation                       │       │
│  │    14. Kesh        → SHIP / NO-SHIP                                │       │
│  │                                                                    │       │
│  └────────────────────────────────────────────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Wall-clock compression:** 14 logical steps collapse to **5 parallel stages** when aggressive parallelization is applied.

---

## Parallel Execution Points

### Stage 1 — Understand Entry (always parallel)

```
RUN IN PARALLEL:
    - Vidura   (requirements)
    - Sanjaya  (xray / codebase)

MERGE → shared_knowledge (requirements_summary + codebase_summary)
THEN → Stage 2
```

### Stage 2 — Design (always parallel)

```
AFTER Stage 1 merge, RUN IN PARALLEL:
    - Vishwakarma (architecture design)
    - Sarthi      (task breakdown & plan)

MERGE → shared_knowledge (architecture_decisions + plan)
THEN → Stage 3 (build)
```

### Stage 3 — Build (parallel per independent file)

```
IF task has independent files:
    RUN IN PARALLEL:
        - Parth (file1) → Swachalit (file1 tests)
        - Parth (file2) → Swachalit (file2 tests)
        - Parth (file3) → Swachalit (file3 tests)

    MERGE all outputs
THEN → Stage 4 (critique)
```

### Stage 4a — Critique trio (ALWAYS 3-way parallel)

```
AFTER build completes, RUN IN PARALLEL:
    - Bhishma  (code review — issues-only)
    - Lakshman (QA validation — use cases)
    - Draupadi (user/customer impact)

MERGE results

IF Bhishma.fail OR Lakshman.fail:
    → iteration++
    → IF iteration < 5: loop back to Parth (step 5)
    → ELSE: escalate to Vishwakarma (re-architecture)
ELSE:
    → proceed to Stage 4b (gates)
```

### Stage 4b — Strategic + Business Gates (parallel)

```
AFTER critique pass, RUN IN PARALLEL:
    - Krishna    (Strong / Weak / KILL)
    - Money Lens (INVEST / DEFER / REJECT)

IF Krishna.verdict == KILL:   → STOP, explain, alternatives
IF Money Lens.verdict == REJECT: → STOP, explain
ELSE:
    → Stage 4c (synthesis)
```

### Stage 4c — Decision Engine (synthesizer)

```
INPUT: critique trio + Krishna + Money Lens outputs
CALL Decision Engine → GO / CONDITIONAL / NO-GO

IF NO-GO:
    → STOP, explain, alternatives
IF CONDITIONAL:
    → document conditions, proceed to Phase 5
ELSE (GO):
    → Phase 5 (final)
```

### Stage 5 — Final closers (sequential by design)

```
Kripacharya (final validation) → Kesh (SHIP / NO-SHIP)
```

---

## Execution Loop Detail (Phase 2 ↔ Phase 3)

**Applies whenever code is produced. Loops until Bhishma AND Lakshman pass, OR iteration cap hit.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION LOOP                                │
│   Parth + Swachalit → (Bhishma ∥ Lakshman ∥ Draupadi) → Parth   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   iteration = 0                                                  │
│                                                                  │
│   LOOP:                                                          │
│       │                                                          │
│       ▼                                                          │
│   ┌──────────────────────┐                                       │
│   │  Parth (execution)   │ ◄────────────────────────┐            │
│   │  + Swachalit (tests) │                          │            │
│   │  [parallel per file] │                          │            │
│   └──────────┬───────────┘                          │            │
│              │                                      │            │
│              ▼                                      │            │
│   ┌──────────────────────────────────┐              │            │
│   │  Bhishma ∥ Lakshman ∥ Draupadi   │              │            │
│   │  (3-way parallel critique)       │              │            │
│   └──────────┬───────────────────────┘              │            │
│              │                                      │            │
│              ▼                                      │            │
│       ┌──────────────────┐                          │            │
│       │ Bhishma.fail OR  │                          │            │
│       │ Lakshman.fail ?  │                          │            │
│       └──────┬───────────┘                          │            │
│              │                                      │            │
│         YES  │  NO                                  │            │
│              │                                      │            │
│    ┌─────────┴─────────┐                            │            │
│    │                   │                            │            │
│    ▼                   ▼                            │            │
│  iteration++      EXIT LOOP                         │            │
│    │              → Phase 4 (Gates)                 │            │
│    │                                                │            │
│    ├── iteration < 5 ───────────────────────────────┘            │
│    │                                                             │
│    └── iteration >= 5 → ESCALATE to Vishwakarma (architect)      │
│                         (architectural rework needed)            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Loop Rules:**

| Condition | Action |
|-----------|--------|
| Bhishma reports CRITICAL / HIGH issues | → Parth fixes → Loop |
| Lakshman reports use-case failures | → Parth fixes → Loop |
| Draupadi raises blocker-class user impact | → Parth/Vishwakarma reconsider (advisory otherwise) |
| Both Bhishma + Lakshman pass | → Exit loop → Phase 4 (Gates) |
| iteration >= 5 | → Escalate to Vishwakarma |

**Important:**

- For **PATCH_INPUT** (diff-only review, no build): Bhishma ∥ Lakshman ∥ Draupadi run ONCE, no loop (no Parth to loop back to)
- The critique trio **always runs 3-way in parallel** — never sequentialize

---

## Skip Logic (applicability-based ONLY)

> Skips are allowed ONLY when an agent's input does not exist or output would be empty. Cost-saving is NEVER a valid skip reason.

See `~/.cursor/rules/kesh-agent-spec.mdc` → "Skip Logic" for the authoritative table.

### Quick reference

| Input Type | May Skip (by applicability) | Still Runs |
|------------|------------------------------|------------|
| **PATCH_INPUT** (review-only, no build) | Parth, Swachalit | Vidura, Sanjaya, Vishwakarma, Sarthi, **Bhishma, Lakshman, Draupadi, Krishna, Money Lens, Decision Engine, Kripacharya, Kesh** |
| **Pure clarification Q** | Sanjaya, Vishwakarma, Parth, Swachalit, Bhishma, Lakshman | Vidura, Sarthi (if plan needed), **Krishna, Money Lens, Decision Engine, Kripacharya, Kesh** |
| **Architecture-only Q** | Parth, Swachalit, Bhishma, Lakshman | Vidura, Sanjaya, Vishwakarma, Sarthi, Draupadi, **Krishna, Money Lens, Decision Engine, Kripacharya, Kesh** |
| **Trivial config-only change** | Sanjaya, Vishwakarma, Sarthi | Vidura, Parth, Swachalit, **Bhishma, Lakshman, Draupadi, Krishna, Money Lens, Decision Engine, Kripacharya, Kesh** |
| **Any feature / refactor / bug fix / behavior change** | **NONE** | **ALL 14 agents** |

### Never-skippable set (if any decision is being made)

- Bhishma, Lakshman, Draupadi (3-way critique)
- Krishna, Money Lens, Decision Engine (Phase 4 gates)
- Kripacharya, Kesh (final closers)

### Invalid skip reasons (anti-patterns)

- ❌ "Task seems small" — run full flow; Phase 4 is cheap
- ❌ "Save tokens / speed up" — user's call, not system's
- ❌ "User didn't ask for review" — critique is structural, not optional
- ❌ "Internal refactor" — still needs critique + gates

---

## Emergency Override

**Triggers (user must explicitly say one of these — do NOT infer):**

- "Production is down"
- "Security breach"
- "Data loss"
- "Customer escalation — critical"
- "Fast mode" / "Emergency mode"

**Action:**

```
1. Skip Phase 1 (Understand) — go straight to Sanjaya + Parth in parallel
2. Run MINIMUM viable critique: Bhishma (issues-only, single pass)
3. Fix first, analyze later
4. MANDATORY post-mortem: run full 15-step flow retroactively within 24h
5. Document emergency in NITI logs
```

**Rule:** Emergency override is an EXCEPTION, not a shortcut. It is NEVER the default.

---

## Detailed Step Logic

### STEP 0: INPUT CLASSIFICATION

```
CLASSIFY input as:

IF input is "emergency/prod-down/security/fast-mode":
    → EMERGENCY OVERRIDE (see above)

IF input contains repo / code / files:
    → mark as CODE_INPUT

IF input contains patch / diff / PR (review requested, no build):
    → mark as PATCH_INPUT

IF input is vague idea / unclear:
    → mark as IDEA_INPUT

IF input has clear requirements:
    → mark as DEFINED_INPUT

STORE → context.input_type
```

---

### STEP 1: Vidura (product) — Requirements Clarification

```
CALL Vidura in PARALLEL with Sanjaya (Stage 1)

Contains:
  - Problem statement
  - User stories / use cases
  - Functional requirements
  - Non-functional requirements
  - Scope boundaries
  - Edge cases

STORE → context.requirements_summary
```

**Applicability skip:** Only if user provided fully-defined requirements AND explicitly said "no clarification needed"

---

### STEP 2: Sanjaya (xray) — Deep Repo Analysis

```
CALL Sanjaya in PARALLEL with Vidura (Stage 1)

Contains:
  - Tech stack
  - Architecture
  - Data flow
  - Dependencies
  - Red flags / risks
  - Entry points

STORE → context.codebase_summary
```

**Applicability skip:** Only if no codebase exists (greenfield without prior repo)

---

### STEP 3: Vishwakarma (architect) — System Design

```
CALL Vishwakarma in PARALLEL with Sarthi (Stage 2)
Inputs: context.requirements_summary, context.codebase_summary

Contains:
  - Architecture diagram (Mermaid)
  - Component design
  - Interfaces / APIs
  - Data models
  - Explicit tradeoffs
  - Technical decisions

STORE → context.architecture_decisions
```

---

### STEP 4: Sarthi (planning) — Task Breakdown

```
CALL Sarthi in PARALLEL with Vishwakarma (Stage 2)
Inputs: context.requirements_summary, context.codebase_summary

Contains:
  - Task breakdown (S/M/L/XL in days)
  - Dependencies
  - Critical path
  - Phases
  - Day-based estimates

STORE → context.plan
```

---

### STEP 5: Parth (execution) — Implementation

```
CALL Parth (per independent file in parallel where possible)
Inputs: context.architecture_decisions, context.plan, context.codebase_summary
        + context.critique_feedback (if iteration > 0)

Parth writes production code ONLY — NO self-review
Parth's model MUST differ from Bhishma's model (hard invariant)

STORE → context.code
```

---

### STEP 6: Swachalit (tests) — Test Automation

```
CALL Swachalit (per file in parallel, after Parth per-file completion)
Inputs: context.code, existing test patterns

Contains:
  - Unit tests for new code
  - Integration tests for new flows
  - Coverage analysis
  - Edge case coverage

STORE → context.tests
```

---

### STEP 7-8-9: CRITIQUE TRIO (always 3-way parallel)

```
RUN IN PARALLEL:
    - Bhishma  → code review (issues-only output)
    - Lakshman → QA validation (use case pass/fail)
    - Draupadi → user/customer impact

Inputs (shared):
  - context.code
  - context.tests
  - context.requirements_summary
  - context.architecture_decisions

Outputs:
  - context.bhishma_output  (PASS / FAIL + issues by severity)
  - context.lakshman_output (PASS / FAIL + failing use cases)
  - context.draupadi_output (impact assessment + migration notes)

LOOP DECISION:
  IF bhishma_output.fail OR lakshman_output.fail:
      → iteration++
      → IF iteration < 5: GO BACK TO STEP 5 (Parth)
      → ELSE: ESCALATE to Vishwakarma (step 3)
  ELSE:
      → proceed to Phase 4 (gates)
```

**Note:** Draupadi is **advisory** — never a blocker by itself. But severe user impact should inform Krishna/Money Lens decisions.

---

### STEP 10-11: STRATEGIC + BUSINESS GATES (parallel)

```
RUN IN PARALLEL:
    - Krishna    → Strong / Weak / KILL
    - Money Lens → INVEST / DEFER / REJECT

Inputs (both):
  - All prior context
  - Critique trio outputs

IF Krishna.verdict == KILL:
    → STOP. Explain why. Offer alternatives.
IF Money Lens.verdict == REJECT:
    → STOP. Explain business impact. Offer DEFER path.
ELSE:
    → proceed to Decision Engine (step 12)
```

---

### STEP 12: Decision Engine — Synthesis

```
CALL Decision Engine (synthesizer, serial)
Inputs: ALL prior context + Krishna + Money Lens

Outputs:
  - Tradeoff matrix
  - Risk scoring (Technical / Business / Customer / Timeline)
  - Final verdict: GO / CONDITIONAL / NO-GO
  - Prioritized next actions

IF NO-GO:
    → STOP
IF CONDITIONAL:
    → document conditions, proceed
ELSE (GO):
    → Phase 5
```

---

### STEP 13: Kripacharya — Final System Validation

```
CALL Kripacharya
Inputs: ALL context

Validates:
  - Completeness vs requirements
  - Integration correctness
  - Production readiness
  - Remaining risks

Outputs: final verdict (PASS / CONDITIONAL / FAIL)
```

---

### STEP 14: Kesh — SHIP / NO-SHIP

```
INPUTS:
  - Kripacharya verdict
  - Decision Engine verdict
  - Actual cost vs estimate
  - Remaining risks

DECISION:
  🚀 SHIP     → All gates green, deliver
  ⏸️ HOLD    → Minor fixes, back to Parth
  🛑 NO SHIP → Critical issues or negative business case
  ⚠️ ESCALATE → Max retries / architectural blocker
```

---

## Agent Timeouts

| Agent | Expected Time | Max Wait | On Timeout Action |
|-------|--------------|----------|-------------------|
| **Vidura** | 1-2 min | 3 min | Proceed with available info |
| **Sanjaya** | 1-3 min | 5 min | Retry once with smaller scope |
| **Vishwakarma** | 2-4 min | 6 min | Retry once, then proceed |
| **Sarthi** | 1-2 min | 3 min | Proceed with high-level plan |
| **Parth** | 2-5 min | 10 min | Retry once, then escalate |
| **Swachalit** | 1-3 min | 5 min | Proceed without tests, note gap |
| **Bhishma** | 1-3 min | 5 min | Escalate (critical agent) |
| **Lakshman** | 1-2 min | 5 min | Escalate (critical agent) |
| **Draupadi** | 1-2 min | 3 min | Proceed with note |
| **Krishna** | 1-2 min | 3 min | Escalate (critical gate) |
| **Money Lens** | 1-2 min | 3 min | Escalate (critical gate) |
| **Decision Engine** | 1-2 min | 3 min | Escalate (critical synthesizer) |
| **Kripacharya** | 1-3 min | 5 min | Escalate (critical closer) |
| **Kesh** | 1-2 min | 3 min | Escalate (final authority) |

### Timeout Handling

```
IF agent exceeds max_wait:
    1. Log timeout event
    2. Attempt retry (if retry_count < max_retries)
    3. If still timing out:
        - For non-critical agents → proceed with warning
        - For critical agents (Bhishma, Lakshman, Krishna, Money Lens,
          Decision Engine, Kripacharya, Kesh) → escalate to user
    4. Include timeout in NITI logs for analysis
```

---

## Confidence Levels

All agents should return confidence in their output:

```json
{
  "output": { ... },
  "confidence": "high|medium|low",
  "confidence_factors": [
    "Found clear patterns",
    "Limited evidence available"
  ]
}
```

### Confidence-Based Actions

| Confidence | Action |
|------------|--------|
| **high** | Proceed to next stage |
| **medium** | Proceed but flag for review in Decision Engine |
| **low** | Consider user clarification before proceeding |

---

## Cross-References

| Concern | File |
|---------|------|
| Canonical contract (source of truth) | `~/.cursor/rules/kesh-agent-spec.mdc` |
| Kesh supervisor | `~/.cursor/agents/kesh.md` |
| Execution orchestrator | `~/.cursor/agents/sutradhar.md` |
| Each agent's contract | `~/.cursor/agents/<name>.md` |
| Always-on orchestration | `~/.cursor/rules/kesh-always-on.mdc` |
| Runtime routing logic | `~/.cursor/rules/kesh-runtime-router.mdc` |

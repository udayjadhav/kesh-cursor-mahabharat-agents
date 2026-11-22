---
name: kesh-flows
description: Kesh support module for adaptive task classification, cache gate, workflow templates, emergency/incident paths, and honest parallelization.
---

# Kesh Flow Control (v2)

> **Canonical contract:** `kesh-agent-spec.mdc` v2. Spec wins.

## Adaptive flow

```
INPUT → Emergency/Incident? → Cache Gate → Classify task_class
     → Select execution_mode (escalate-only)
     → Select agents (mode + template)
     → Context packages + progressive standards
     → Knowledge gate (SUFFICIENT → load; else discover → propose MDC)
     → Deterministic verification first
     → Execute → Consolidate (mode + CACHE + verification)
```

Knowledge gate: `kesh-knowledge-discovery.mdc`. Skip research when coverage is SUFFICIENT.  
Modes: `kesh-execution-modes.mdc`. Guardrails: `kesh-quality-guardrails.mdc`.

## Task classes

See spec table: EXPLANATION, INVESTIGATION, DEBUGGING, PATCH, BUG_FIX, FEATURE, REFACTOR, ARCHITECTURE, DATABASE_CHANGE, SECURITY_CHANGE, PRODUCTION_INCIDENT, CODE_REVIEW.

## Cache Gate

Probe per `kesh-token-cache.mdc`. `FULL_HIT` / `PARTIAL_HIT` / `MISS`. Applicability reuse only.

## Parallelism

Independent agents may run concurrently **when invoked**. Do not claim parallelism without concurrent execution.

Typical parallel groups when in-workflow:

- Vidura ∥ Sanjaya ∥ Vyasa  
- Vishwakarma ∥ Sarthi  
- Bhishma ∥ Lakshman ∥ Draupadi  
- Krishna ∥ Money Lens (advisory)

## Build–critique loop

Parth → Swachalit → critique. Bhishma/Lakshman FAIL → Parth (max 5) → else Vishwakarma.  
**Stop** on critical test or security failure — do not continue for ceremony.

## Money Lens

Advisory. No REJECT-stop on mandatory remediation classes.

## Incident path

Evidence → diagnosis → mitigation proposal → human approval for consequential production/data actions → fix + regression when approved.

## NITI (out of band)

Not in the default delivery template. After meaningful COMPLETE/PARTIAL (and on failures), Kesh records execution telemetry (`scripts/niti/record_execution.py`). Thresholds (5 / 20), post-incident, on-demand, and before/after kit evals may invoke NITI. Details: `rules/kesh-niti.mdc`.

## Legacy note

The old “mandatory 15-step for every task” posture is **withdrawn**. Prefer workflow templates by class.

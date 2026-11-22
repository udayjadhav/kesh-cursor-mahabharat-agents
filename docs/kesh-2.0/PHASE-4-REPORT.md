# Kesh 2.0 — Phase 4 Report

**Branch:** `feature/kesh-2.0-rearchitecture`  
**Status:** Complete (orchestration + core agent upgrades)

## Summary

Replaced Agent Maximization / mandatory-15 posture with adaptive task classification (12 classes). Money Lens is advisory and cannot hard-stop mandatory remediation. Delivery statuses are evidence-based. Parth, Swachalit, Bhishma, Vishwakarma, Sutradhar, Kesh, and support modules updated in place.

## Files modified / rewritten

| Path | Change |
|------|--------|
| `rules/kesh-agent-spec.mdc` | v2.0.0 adaptive contract |
| `rules/kesh-runtime-router.mdc` | Classify → select |
| `rules/kesh-always-on.mdc` | Adaptive always-on |
| `rules/kesh-explanation-framework.mdc` | Depth adaptive |
| `rules/kesh-external-output-voice.mdc` | YAML frontmatter fixed |
| `agents/kesh.md` | Classifier + delivery statuses |
| `agents/kesh-flows.md` | Adaptive flows |
| `agents/kesh-context.md` | task_class + execution_state |
| `agents/kesh-output.md` | Delivery report template |
| `agents/kesh-rules.md` | v2 index |
| `agents/money-lens.md` | Contextual; exemptions |
| `agents/decision-engine.md` | No ROI NO-GO on mandatory work |
| `agents/parth.md` | 12-step evidence workflow |
| `agents/swachalit.md` | Execution evidence; no fabricate |
| `agents/sutradhar.md` | Explicit state; stop on critical fail |
| `agents/vishwakarma.md` | ADR; parallel Stage-2 inputs |
| `agents/bhishma.md` | Finding schema + confirmation |

## Files added

- This report

## Files removed

- None (roster preserved)

## Decisions

1. Money Lens advisory; hard exemptions for BUG_FIX / SECURITY_CHANGE / PRODUCTION_INCIDENT / mandatory reliability  
2. COMPLETE ≠ SHIP without verification  
3. Parallelism claims must be honest  
4. Sutradhar timeouts remain soft (B) until hooks (Phase 5)

## Tests executed

- None automated (Phase 5 validator)

## Remaining issues

- `docs/WORKFLOW.md` / `docs/AGENTS.md` / README still describe v1 in places → Phase 6  
- `install.sh` knowledge flag → Phase 6  
- Executable hooks / validate-kit → Phase 5  
- Krishna / Lakshman / Draupadi / Vidura / Sanjaya / Sarthi / Kripacharya / NITI / Vyasa only lightly affected — still compatible; optional polish later  

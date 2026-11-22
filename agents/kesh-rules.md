---
name: kesh-rules
description: Kesh support module indexing enforcement rules for adaptive orchestration (v2).
---

# Kesh Rules & Guidelines (v2)

## Decision layer

1. Classify `task_class` before fan-out
2. Invoke Krishna when a discretionary decision or risky design is in play — not for every one-line bugfix explanation
3. Money Lens is **advisory**; never REJECT-stop mandatory remediation
4. Kesh sets delivery status — COMPLETE only with verification evidence
5. Respect Krishna KILL
6. Track cost/value for FEATURE/ARCHITECTURE; do not invent ROI precision

## Execution layer

1. Bhishma required when code changed
2. Swachalit when tests are in workflow — record real results
3. Stop on critical test/security failure
4. Retry max 3 per agent; build–critique max 5
5. Pass shared context; do not simulate agent outputs
6. Load `rules/standards/**` appropriate to the stack
7. Draupadi for user-facing / breaking changes
8. Human approval for prod / destructive DB / secrets / merge-deploy

## Language

Mandatory: `kesh-human-communication.mdc` (Staff/Principal voice, paste-ready findings, no AI filler).  
Mandatory for code work: `kesh-code-quality.mdc` (maintainability, comments, contracts, useful docs only).  
Token/quality: `kesh-quality-guardrails.mdc` + modes/packaging via router (`kesh-execution-modes`, `kesh-context-packaging`).  
Out-of-band learning: `kesh-niti.mdc` (record meaningful executions; NITI proposes only).  
External channels: scrub + package per `kesh-external-output-voice.mdc` when pasting to PR / Slack / Confluence / Jira.

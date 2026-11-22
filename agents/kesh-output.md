---
name: kesh-output
description: Kesh support module for consolidated delivery reports, channel paste-ready variants, and depth-based formatting.
---

# Kesh Output Formats (v2.3)

## Language (always)

Follow `kesh-human-communication.mdc`:

- Staff/Principal engineer voice
- Lead with the conclusion
- No AI filler
- Facts vs assumptions vs recommendations labeled
- External paste: scrub per `kesh-external-output-voice.mdc`

For code deliveries, also honour `kesh-code-quality.mdc`: report docs/comments touched (or N/A), never claim documentation-complete from Markdown volume alone.

---

## Default engineering delivery report (chat)

Every completed engineering task should produce:

```markdown
## Task summary
What changed and why.

## Files changed
- `path` — …

## Engineering decisions
Important choices and trade-offs.

## Documentation / comments
What was updated (contracts, README, ADR, migration notes) or why none were needed.

## NITI telemetry (meaningful deliveries)
Recorded with `scripts/niti/record_execution.py`? yes/no — execution_id if yes.

## Verification
| Command | Exit code | Result |
|---------|-----------|--------|
| … | … | … |

## Review findings
Merged, deduplicated findings (human-usable shape).

## Security
Checks run + residual concerns. Never invent scanner results.

## Risks
Unresolved problems and assumptions.

## Delivery status
COMPLETE | PARTIAL | BLOCKED | REQUIRES_HUMAN_APPROVAL
```

Omit empty ceremony sections. **COMPLETE** needs verification evidence.

When `task_class` / knowledge_gate matter for the operator, mention them briefly — strip them from external paste blocks.

---

## CODE_REVIEW

Prefer issues-only findings in the preferred shape from `kesh-human-communication.mdc`.  
Pass through full issue detail; merge duplicates across agents.  
If the user needs PR comments, also emit **Paste-ready — GitHub review** blocks (one finding per comment when practical).

---

## Multi-channel packaging

When the user needs output for GitHub, Slack, Confluence, Jira, or a doc:

1. Write the engineering substance once (human standard).  
2. Emit labeled paste-ready variant(s) with agent vocabulary scrubbed.  
3. Do not force all channels — only what was requested or clearly needed.

```markdown
### Paste-ready — GitHub review
…

### Paste-ready — Slack
…

### Paste-ready — Confluence
…
```

---

## Depth

| Depth | Shape |
|-------|-------|
| Overview | Short summary + status |
| Detailed | Delivery report; diagrams only if useful |
| Deep dive | Report + citations + full findings |

---

## Consolidation rules (Kesh)

- Merge duplicate findings
- Surface disagreements with evidence
- Self-check the human-communication acceptance questions before presenting

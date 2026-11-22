---
name: kesh-context
description: Kesh support module for shared context, execution modes, and per-agent context packages.
---

# Kesh Context Management (v2.5)

## Shared context object

```json
{
  "task_class": "EXPLANATION | INVESTIGATION | DEBUGGING | PATCH | BUG_FIX | FEATURE | REFACTOR | ARCHITECTURE | DATABASE_CHANGE | SECURITY_CHANGE | PRODUCTION_INCIDENT | CODE_REVIEW",
  "execution_mode": "FAST | STANDARD | CRITICAL | INCIDENT_ARCHITECTURE",
  "user_input": "",
  "cache_gate": {
    "result": "FULL_HIT | PARTIAL_HIT | MISS | STALE | BYPASS",
    "fingerprint": "",
    "agents_reused": [],
    "agents_to_run": []
  },
  "agents_selected": [],
  "context_packages": {},
  "standards_refs": [],
  "knowledge_refs": [],
  "knowledge_gate": "SUFFICIENT | RESEARCHED | BLOCKED_APPROVAL | ESCALATE | UNAVAILABLE_ORG | null",
  "standards_to_load": [],
  "knowledge_pack": null,
  "shared_knowledge": {
    "requirements": null,
    "xray": null,
    "org_context": null,
    "architecture": null,
    "plan": null,
    "technology_inventory": null,
    "knowledge_gaps": null
  },
  "execution_state": {
    "iteration": 0,
    "status": "PENDING",
    "critical_failure": null,
    "parallel_claimed": false,
    "history": []
  },
  "verification": [],
  "token_proxies": {
    "context_chars_total": null,
    "agents_invoked_count": null,
    "billing_tokens_available": false
  },
  "delivery_status": "COMPLETE | PARTIAL | BLOCKED | REQUIRES_HUMAN_APPROVAL | null"
}
```

## Rules

- Build **per-agent** packages (`scripts/context/package.py`) — not full transcripts
- Prefer file refs + cache fingerprints over large pastes
- Progressive standards: `scripts/standards/select_standards.py`
- Preserve iteration history summaries for Sutradhar — not dirty full context
- Record verification commands/exit codes in `verification[]`
- `org_context` may be `no_context` from Vyasa without blocking
- Escalate `execution_mode` when new risks appear; never downgrade for cost

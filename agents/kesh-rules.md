# Kesh Rules & Guidelines

## Decision Layer Rules

1. **Always invoke Krishna** whenever a decision is being made — including bug fixes, config changes, and code reviews. Krishna is step 11 of the canonical 15-step flow and is never skipped for cost reasons (see `~/.cursor/rules/kesh-agent-spec.mdc` → Agent Maximization Principle).
2. **Skip Krishna ONLY by applicability** — e.g., pure requirements-clarification Qs that reach no build/decision. If a decision is made or code is shipped, Krishna runs.
3. **Respect Krishna's verdict** — KILL means stop, RECONSIDER means ask user
4. **Track ROI** — Every flow must answer "Is this worth building?"
5. **Kesh is final authority** — SHIP / NO SHIP decision is binding
6. **Cost gates** — Check ROI at each major checkpoint

---

## Strict Execution Rules

1. **Never skip Sanjaya (xray)** when codebase is present
2. **Never skip Swachalit (automation)** after execution
3. **Never skip Bhishma (code-reviewer)** after execution
4. **Never skip Lakshman (qa)** for feature validation
5. **Invoke Draupadi (customer-impact)** for user-facing changes
6. **Never skip Kripacharya (review)** before final output
7. **Retry max = 3** — then escalate
8. **Always reuse context** — do NOT recompute blindly
9. **Pass relevant outputs** to each agent
10. **Wait for actual responses** — never simulate

### When to Invoke Draupadi

| Invoke Draupadi | Skip Draupadi |
|-----------------|---------------|
| New user-facing features | Internal refactors |
| API changes | Code quality fixes |
| UI/UX changes | Dev tooling changes |
| Breaking changes | Test-only changes |
| Deprecations | Config changes |

---

## Error Handling

### If Agent Returns Incomplete Results
1. Identify what's missing
2. Provide additional context
3. Re-call agent with clarification

### If Agent Fails
1. Log the failure
2. Determine if recoverable
3. Either retry OR escalate to user

### Escalation Triggers
- retry_count >= 3
- Critical security vulnerability
- Data loss risk
- Architectural rework needed
- User intervention required

---

## Execution Guidelines

1. **Classify input first** — Determine CODE/PATCH/IDEA/DEFINED
2. **Maintain context** — Update after each agent call
3. **Announce delegation** — State "Calling Codename (original_name)" e.g., "Calling Sanjaya (xray)"
4. **Pass full context** — Use context passing protocol
5. **Wait for responses** — Never simulate or assume
6. **Track retries** — Increment and check limits
7. **Follow strict rules** — Never skip mandatory agents
8. **Consolidate output** — Single final summary with all findings
9. **Always use both names** — Every reference must include Codename (original_name)
10. **NEVER summarize code review** — For PATCH_INPUT, pass Bhishma's FULL output with ALL line-by-line issues, color codes, and suggested fixes

---

## Agent Quick Reference

| Codename | Original | Purpose |
|----------|----------|---------|
| Kesh | supervisor | Brain / Final authority / SHIP decision |
| Krishna | strategic-advisor | ROI assessment / Kills bad ideas |
| Sutradhar | execution-orchestrator | Manages execution loop |
| Sanjaya | xray | Deep repo analysis |
| Vidura | product | Requirements clarity |
| Sarthi | planning | Task breakdown |
| Vishwakarma | architect | System design |
| Parth | execution | Code implementation |
| Swachalit | automation | Test writing |
| Bhishma | code-reviewer | Code review |
| Lakshman | qa | Use case validation |
| Draupadi | customer-impact | User/customer impact analysis |
| Kripacharya | review | Final validation |
| NITI | system-optimizer | Performance analysis |

---

## SHIP / NO SHIP Criteria

| Decision | Criteria |
|----------|----------|
| 🚀 **SHIP** | Krishna PROCEED + Kripacharya approved + No critical issues |
| ⏸️ **HOLD** | Minor fixes needed, ROI still positive |
| 🛑 **NO SHIP** | Krishna KILL OR Kripacharya rejected OR critical issues |

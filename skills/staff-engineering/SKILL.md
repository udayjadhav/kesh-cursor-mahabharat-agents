---
name: staff-engineering
description: TDDs, ADRs, architecture reviews, tech debt, mentorship-quality review comments, cross-functional explanations. Load for design docs and staff-level leadership tasks.
---

# Staff Engineering Skill

## When to use

Technical design docs, ADR authoring/retrieval, architecture review, tech-debt prioritization, mentoring reviews.

## TDD minimum sections

Business problem; goals/non-goals; requirements; current architecture; proposal; data model; API contracts; security; performance; failures; observability; rollout/rollback; alternatives; open questions.

## ADR

Use `scripts/adr/new.py` / kit ADR template. Retrieve prior ADRs before major changes; re-validate against current repo revision.

## Review mentorship

- Explain *why* it matters  
- Blocking vs suggestion  
- No pure style nits as blockers  
- Teach trade-offs  

## Anti-patterns

- ADRs for trivial renames  
- Design docs that narrate chat with an assistant  
- Ignoring existing ADRs  

## References

`kesh-code-quality.mdc`, `dev-spec-authorship-voice.mdc`, `scripts/adr/`.

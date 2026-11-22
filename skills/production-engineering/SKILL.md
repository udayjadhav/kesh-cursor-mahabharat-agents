---
name: production-engineering
description: Docker, Kubernetes, CI/CD, feature flags, progressive rollout, incident hygiene. Load for deploy/release risk — discover repo tooling first.
---

# Production Engineering Skill

## When to use

Deployment manifests, pipelines, flags, rollout/rollback, incident readiness.

## Principles

- Discover existing CI/CD before adding tools  
- Progressive delivery + fast rollback  
- Feature flags for risky behaviour  
- Config and secrets via approved channels only  
- No silent prod mutation — REQUIRES_HUMAN_APPROVAL  

## Verification checklist

- [ ] Pipeline validates config or NOT RUN  
- [ ] Rollback documented  
- [ ] Flags/owners identified  

## References

`skills/reliability-performance/SKILL.md`.

---
name: reliability-performance
description: SLOs, error budgets, OpenTelemetry, caching, circuit breakers, k8s deploy safety, cost. Load for latency/error/deploy risk — not a separate agent.
---

# Reliability & Performance Skill

## When to use

SLO design, perf bottlenecks, dependency failure modes, observability gaps, rollout risk.

## Principles

- User-facing SLOs with error budgets  
- Trace + metrics + structured logs with correlation  
- Graceful degradation over cascading failure  
- Caches need TTLs and invalidation stories  
- Deploy: progressive rollout, rollback, feature flags  
- Cloud cost is a design input, not an afterthought  

## Anti-patterns

- Dashboards without actionable alerts  
- Retries that amplify outages  
- “We’ll add OTel later” on CRITICAL paths  

## Verification checklist

- [ ] Golden signals identified  
- [ ] Load/perf test RUN or NOT RUN  
- [ ] Rollback path stated  

## References

`knowledge/reliability-observability.md`.

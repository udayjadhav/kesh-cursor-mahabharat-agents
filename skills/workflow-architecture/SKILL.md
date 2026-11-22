---
name: workflow-architecture
description: Long-running distributed workflows — sagas, outbox, idempotency, retries, DLQ, state machines, SSE/WebSocket progress. Minutes-to-days jobs are not sync HTTP. Load for async workflow design.
---

# Workflow Architecture Skill

## When to use

Sagas, outbox, job orchestration, event-driven flows, progress APIs, duplicate-event risks.

## Principles

- Long-running work ≠ single request/response  
- Explicit state machine; illegal transitions rejected  
- Idempotent handlers; dedupe keys  
- Retries with jitter; DLQ + replay story  
- Outbox for DB↔message atomicity needs  
- Observable: correlation id, status API, timeouts  
- FE must handle in-progress / failed / resumed states  

## Anti-patterns

- Fire-and-forget without status  
- Infinite retries without DLQ  
- Assuming order without partition keys  
- Hiding multi-day jobs behind a synchronous gateway timeout  

## Verification checklist

- [ ] State diagram reviewed  
- [ ] Duplicate delivery tested or NOT RUN  
- [ ] Progress/error API specified  
- [ ] distributed-systems standards loaded on CRITICAL  

## References

`rules/standards/distributed-systems.mdc`, `microservices.mdc`.

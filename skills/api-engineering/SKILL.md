---
name: api-engineering
description: REST/GraphQL/gRPC contracts, OpenAPI, versioning, idempotency, errors, pagination, contract tests. Load for API design or review — not every task.
---

# API Engineering Skill

## When to use

API design, OpenAPI/proto changes, breaking-change analysis, consumer compatibility.

## Required context

Contract paths, consumers, auth model, idempotency needs, error taxonomy in-repo.

## Principles

- Resource modelling over RPC-shaped REST unless evidenced otherwise  
- Explicit versioning strategy; prefer additive evolution  
- Idempotency keys for unsafe retries  
- Stable error codes + problem details where project uses them  
- Pagination/filter/sort documented and tested  
- Authn/z at the contract boundary  

## Anti-patterns

- Silent breaking field renames  
- Overloading 200 for business failures  
- Undocumented nullability  
- Chatty N+1 public APIs without evidence of need  

## Verification checklist

- [ ] OpenAPI/proto validates (tool present?)  
- [ ] Compatibility / consumer tests identified or NOT RUN  
- [ ] Authz cases listed  
- [ ] api-architect consulted on CRITICAL contract changes  

## References

`rules/standards/security.mdc`, agent `api-architect`.

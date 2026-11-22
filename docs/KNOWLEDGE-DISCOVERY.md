# Knowledge Discovery & Standards Reconciliation

Kesh progressively learns the engineering ecosystem it works in — without a new agent and without MDC spam.

## Ownership

| Step | Owner |
|------|-------|
| Detect tech + coverage | Sanjaya |
| Org docs | Vyasa (or `UNAVAILABLE`) |
| External official docs + merge | Kesh + `skills/knowledge-discovery` |
| Architecture conflicts | Vishwakarma (ADR) |
| Consume standards | Parth / Bhishma / Swachalit / … |
| Write shared MDC | Human approval |

## Flow

```mermaid
flowchart TD
  T[Task] --> D[Detect technologies]
  D --> C{Coverage?}
  C -->|SUFFICIENT| L[Load relevant standards only]
  C -->|gap| R[Repo evidence]
  R --> O[Org sources if connected]
  O --> E[Official docs]
  E --> M[Merge MUST/SHOULD/MAY]
  M --> P[Propose create or update MDC]
  P --> A{Approved?}
  A -->|yes| W[Write + update manifest]
  A -->|no| X[Proceed with limitations labeled]
  L --> X2[Implement / review]
  W --> X2
```

## Authority

Org mandatory policy > org platform standards > team ADRs > repo patterns > official vendor docs > credible external > inference.

Never silent-replace org mandates. Escalate org-vs-security conflicts.

## Acceptance scenarios

See [kesh-2.0/KNOWLEDGE-DISCOVERY-ACCEPTANCE.md](./kesh-2.0/KNOWLEDGE-DISCOVERY-ACCEPTANCE.md).

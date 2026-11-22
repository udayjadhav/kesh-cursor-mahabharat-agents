# Engineering Standards (Kesh 2.0)

Modular Cursor rules under `rules/standards/`. All use `alwaysApply: false` and **globs** so they load selectively.

**Always-on companion:** [`rules/kesh-code-quality.mdc`](../rules/kesh-code-quality.mdc) — repo-first coding, comments, contracts, README/ADR guidance (no doc spam). Spec **2.3.0**.

**Enforcement level:** **B** (prompt-guided) + **C** (Cursor glob loading). Prefer repo **D/E** lint/format/CI when present.

## Core modules

| File | Focus |
|------|-------|
| `software-architecture.mdc` | SOLID/KISS, styles, ADRs |
| `security.mdc` | Authn/z, OWASP-oriented, secrets, evidence |
| `testing.mdc` | Test types, assertions, execution evidence |
| `microservices.mdc` | Boundaries, contracts, resilience patterns |
| `distributed-systems.mdc` | Consistency, failure, delivery semantics |
| `java-quarkus.mdc` | Java/Quarkus backend |
| `python.mdc` | Python backend / data |
| `react-typescript.mdc` | React + TypeScript frontend |

## Database modules (`standards/database/`)

| File | Focus |
|------|-------|
| `database-design.mdc` | Modelling, workload split, change checklist |
| `relational-databases.mdc` | OLTP relational practices |
| `nosql-databases.mdc` | Document/kv/search caveats |
| `distributed-databases.mdc` | Distributed SQL concerns |
| `analytical-databases.mdc` | Warehouse / OLAP |
| `database-migrations.mdc` | Expand/contract, approvals |
| `database-performance.mdc` | Plans, indexes, pooling |

### Engines (`standards/database/engines/`)

`postgresql`, `cockroachdb`, `google-spanner`, `bigquery`, `mysql`, `mongodb`, `redis`, `elasticsearch`

Engines are **not** interchangeable. Prefer the engine file that matches repository evidence.

## Optional language pack

| File | Focus |
|------|-------|
| `clojure-review.mdc` | Clojure style & review |
| `clojure-daily-tips.mdc` | Short Clojure layout tips |

## Org-specific (not installed by default)

See `optional/teams.mdc`.

## Template for generated standards

`rules/standards/_TEMPLATE.mdc` — use when knowledge discovery proposes a new or updated module (MUST/SHOULD/MAY, sources, last_reviewed).

## Related

- Conceptual notes + manifest: [KNOWLEDGE.md](./KNOWLEDGE.md)
- Discovery process: [KNOWLEDGE-DISCOVERY.md](./KNOWLEDGE-DISCOVERY.md)
- Install: [INSTALL.md](./INSTALL.md)

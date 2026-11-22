---
name: data-engineering
description: Spanner, BigQuery, PostgreSQL, Kafka modelling — not interchangeable. Schema evolution, indexing, transactions vs analytics, ingestion, reconciliation. Load for DATABASE_CHANGE and data-path design.
---

# Data Engineering Skill

## When to use

Schema design, migrations, query plans, ingestion, Kafka payloads, OLTP vs OLAP choice.

## Required context

Engine in use (from repo evidence), workload type, consistency needs, migration files.

## Principles

- **Engines are not interchangeable** — Spanner ≠ PostgreSQL ≠ BigQuery  
- OLTP vs analytical separation  
- Explicit transaction boundaries; avoid cross-engine dual writes without outbox  
- Indexes match query patterns; document why  
- Migrations: expand/contract, backfill, rollback limits  
- Kafka: keys, ordering, idempotent consumers, DLQ  

## Anti-patterns

- Treating BigQuery as an OLTP store  
- Unbounded full-table scans as “temporary”  
- Schema change without consumer audit  
- Assuming exactly-once without evidence  

## Verification checklist

- [ ] Engine modules loaded (`scripts/standards/select_standards.py`)  
- [ ] Migration dry-run / validate command identified or NOT RUN  
- [ ] Query pattern ↔ indexes explained  
- [ ] Option 0 / reuse checked when associating entities  

## References

`rules/standards/database/**`, `knowledge/*.md`.

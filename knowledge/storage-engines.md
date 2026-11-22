# Storage Engines

## Idea

How a database lays out bytes — affects write amplification, read latency, and compaction.

## Families (simplified)

| Family | Strength | Watch for |
|--------|----------|-----------|
| B-tree / page | Point lookups, balanced | Write amplification under random updates |
| LSM | High write ingest | Compaction / read amplification |
| Columnar | Analytical scans | Poor OLTP point updates |

## Engineering notes

- Engine choice is usually inherited — optimize queries to the engine you have.
- Compaction, vacuum, and bloat are operational realities, not edge cases.

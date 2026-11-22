# Replication

## Idea

Keep copies of data on multiple nodes for durability, availability, and/or read scale.

## Common patterns

| Pattern | Sketch | Trade-off |
|---------|--------|-----------|
| Single-leader | One writer; followers replicate | Simple writes; failover complexity |
| Multi-leader | Multiple writers | Conflict resolution required |
| Leaderless | Quorum read/write | Tunable consistency; more app logic |

## Engineering notes

- Replication lag means followers can be stale — design UX accordingly.
- Failover can lose unreplicated writes depending on durability settings.
- “Read replicas” are not free consistency; state the requirement.

## Questions to ask

- What is RPO/RTO?
- Synchronous vs asynchronous replication?
- Who handles failover — automatic or human?

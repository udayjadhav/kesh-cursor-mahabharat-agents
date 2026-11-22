# Partitioning (Sharding)

## Idea

Split a dataset across nodes so each node holds a subset of keys.

## Key choice

- Partition key must match common transaction/query locality.
- Low-cardinality keys create hot partitions.
- Monotonic keys (time, serial) can concentrate writes — mitigate deliberately.

## Resharding

Changing partition scheme is expensive. Plan for growth early only when evidence warrants; premature sharding adds operational cost.

## Questions

- What percent of transactions stay on one partition?
- How are secondary lookups handled (scatter/gather vs local index)?

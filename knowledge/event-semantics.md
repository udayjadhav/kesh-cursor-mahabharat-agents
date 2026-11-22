# Event Delivery Semantics

## Terms

| Claim | Practical meaning |
|-------|-------------------|
| At-most-once | May lose; no dupes |
| At-least-once | May dupe; no silent loss (if durable path works) |
| Exactly-once | End-to-end effect once — requires idempotent handling + coordinated offsets/transactions |

## Rules

- Assume at-least-once unless the platform proves otherwise.
- Consumers must be idempotent for at-least-once buses.
- Ordering is per partition/key — not global — unless stated.
- Dual-write (DB + bus) without outbox is a consistency bug waiting to happen.

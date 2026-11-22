# Transactions

## Idea

Group multiple reads/writes into a unit with defined atomicity and isolation.

## Isolation (practical)

Dirty reads, non-repeatable reads, phantoms — know what your engine’s default prevents.

## Distributed transactions

- Two-phase commit couples availability of all participants.
- Prefer single-partition / single-service transactions.
- Cross-service: sagas/compensations or transactional outbox — not accidental dual-write.

## Rules of thumb

- Keep transactions short.
- No remote I/O inside a DB transaction.
- Idempotency for retries that may replay side effects.

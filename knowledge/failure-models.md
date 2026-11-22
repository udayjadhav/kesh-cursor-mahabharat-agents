# Distributed Failure Models

## Idea

Design for partial failure: nodes, disks, networks, and zones fail independently.

## Assumptions to state

- Crash-stop vs Byzantine (usually crash-stop in business systems)
- Network partitions happen; timeouts are imperfect detectors
- Clocks are unreliable for correctness across nodes

## Patterns

Timeouts, retries with jitter, idempotency, circuit breakers, bulkheads, quarantine (DLQ).

## Rule

If you cannot explain behavior under partition and retry storms, the design is incomplete.

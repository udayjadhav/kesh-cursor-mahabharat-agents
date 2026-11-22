# Schema Evolution

## Idea

Change data shape while old and new readers/writers coexist.

## Safe patterns

- Add optional fields; publish consumers that ignore unknowns.
- Expand/contract for databases and APIs.
- Version events explicitly when meaning changes.

## Unsafe patterns

- Reuse a field for a new meaning
- Remove/rename without a migration window
- Assume instantaneous fleet upgrades

## Checklist

Compatibility window, backfill, verification, rollback limits.

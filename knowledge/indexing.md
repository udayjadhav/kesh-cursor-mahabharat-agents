# Indexing

## Idea

Secondary structures that trade write/storage cost for faster lookups.

## Rules

- Index for measured predicates and join/filter paths.
- Every index slows writes and uses space.
- Composite index column order must match query patterns.
- Partial / filtered indexes when supported and selective.

## Process

Evidence (`EXPLAIN`) → hypothesis → change one thing → re-measure.

## Anti-patterns

Indexing every column; duplicate overlapping indexes; unused indexes left forever.

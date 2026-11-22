# Data Modelling

## Idea

Represent domain facts so invariants hold and access patterns stay efficient.

## Guidance

- Model invariants first (what must never be false).
- Shape tables/documents around queries that dominate.
- Separate transactional truth from read projections when they conflict.
- Name ownership: which service/module may write which data.

## Evolution

Additive fields preferred; breaking changes need expand/contract and version policy.

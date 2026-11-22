# Staff Engineer Edition benchmarks

Structural mode/skill routing uses the shared harness:

```bash
python3 benchmarks/token-optimization/harness.py
```

Scenarios 11–12 cover AI eval design and multi-tenant authz (CRITICAL).

## Live comparison (operator — not fabricated)

For each of the 12 tasks, compare kit 2.5 vs 2.6 on real work:

| Metric | Before | After |
|--------|--------|-------|
| Correctness / tests | | |
| Missed risks | | |
| Rework / human corrections | | |
| Token proxy / billing if available | | |
| Duration | | |

Do not claim improvement without filling this table from real runs.

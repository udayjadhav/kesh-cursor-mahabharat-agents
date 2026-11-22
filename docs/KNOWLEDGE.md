# Engineering Knowledge Modules

Original concise notes plus `manifest.json` in `knowledge/`. Conceptual reference only.

**Enforcement:** **A/B**. Not verified knowledge of any production system.

| File | Topic |
|------|-------|
| `manifest.json` | Technology → standards index |
| `replication.md` | Leader / multi-leader / leaderless |
| `partitioning.md` | Sharding and key design |
| `consistency.md` | Strong vs eventual; read-your-writes |
| `transactions.md` | Isolation; distributed tx caution |
| `storage-engines.md` | B-tree / LSM / columnar |
| `indexing.md` | Secondary indexes |
| `failure-models.md` | Partial failure assumptions |
| `stream-vs-batch.md` | Processing models |
| `event-semantics.md` | Delivery guarantees |
| `data-modelling.md` | Invariants and ownership |
| `schema-evolution.md` | Compatible change |
| `reliability-observability.md` | SLOs, logs/metrics/traces |

Optional install: `INSTALL_KNOWLEDGE=1 ./install.sh` → `~/.cursor/knowledge/kesh/`.

Discovery & reconciliation: [KNOWLEDGE-DISCOVERY.md](./KNOWLEDGE-DISCOVERY.md).

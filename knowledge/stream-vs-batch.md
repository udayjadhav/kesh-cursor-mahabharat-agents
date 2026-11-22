# Stream vs Batch Processing

## Idea

- **Batch:** process bounded datasets on a schedule or on demand.
- **Stream:** process unbounded events continuously.

## Choose stream when

Low-latency reaction to events matters and ops cost is accepted.

## Choose batch when

Throughput, simplicity, and recomputation matter more than sub-second freshness.

## Engineering notes

- Streaming needs watermark/late-data policy for time-based logic.
- Batch jobs need idempotent outputs and clear lineage.
- Lambda/kappa-style mixes exist — complexity must pay for itself.

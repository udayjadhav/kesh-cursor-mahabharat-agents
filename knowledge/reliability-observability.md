# Reliability & Observability

## Reliability

- Define SLIs/SLOs for user-visible journeys.
- Prefer degrading gracefully over hard failure when safe.
- Backpressure beats unbounded queues.

## Observability pillars

- Logs: structured, correlated, no secrets
- Metrics: RED/USE or domain SLIs
- Traces: cross-service path for latency/errors

## Incident mindset

Symptom → evidence → hypotheses → test → fix → regression test. Correlation is not causation.

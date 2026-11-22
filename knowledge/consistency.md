# Consistency

## Idea

Agreement on what values readers observe after concurrent writes and failures.

## Practical spectrum

- Linearizability / strong consistency — reads see latest committed write (cost: latency/availability under partition).
- Causal consistency — respects cause-effect order.
- Eventual consistency — replicas converge; temporary divergence allowed.

## Engineering notes

- Pick the weakest consistency that meets the product invariant.
- “Read-your-writes” often needed for UX after a user’s own update.
- Cross-region strong consistency has real latency costs — measure.

## Anti-pattern

Claiming strong consistency without naming the mechanism (consensus, single leader, etc.).

---
name: frontend-architecture
description: React/TypeScript component boundaries, state ownership, API integration, a11y, rendering performance. No microfrontends without proven need. Load for UI architecture tasks.
---

# Frontend Architecture Skill

## When to use

Component design, hooks/shared libs, client vs server state, FE–API contract alignment, a11y/perf reviews.

## Principles

- Clear ownership of state (server cache vs UI local)  
- Composition over premature abstraction  
- Match existing design system; do not invent a parallel one  
- Accessibility is part of done  
- Contract alignment with api-architect when APIs change  

## Anti-patterns

- Microfrontends without org/tech necessity  
- Prop drilling god-components fixed by random context  
- Fetching in every leaf without cache strategy  
- Ignoring loading/error/empty states for long ops  

## Verification checklist

- [ ] `tsc` / ESLint / component tests — run or NOT RUN  
- [ ] a11y expectations stated  
- [ ] No duplicate design-system primitives  

## References

`rules/standards/react-typescript.mdc`.

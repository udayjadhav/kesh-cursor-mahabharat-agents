# X-Ray Scoring Guide

Detailed criteria for scorecard ratings with confidence calibration.

## Confidence Levels

| Level | Criteria |
|-------|----------|
| **High** | Multiple clear indicators found, reviewed 5+ relevant files |
| **Medium** | Some indicators found, reviewed 2-4 relevant files |
| **Low** | Limited evidence, inferred from patterns, reviewed <2 files |

When confidence is low, explicitly state what additional exploration would increase confidence.

---

## Code Quality (1-10)

| Score | Criteria |
|-------|----------|
| 1-3 | No clear structure, mixed concerns, inconsistent naming, no patterns |
| 4-5 | Some structure but inconsistent, partial separation of concerns |
| 6-7 | Good structure, clear modules, mostly follows patterns |
| 8-9 | Excellent structure, consistent patterns, clear boundaries |
| 10 | Exemplary - could be used as a teaching reference |

**Key indicators**:
- File/folder organization
- Function/class size (< 200 lines ideal)
- Single responsibility adherence
- Naming conventions consistency
- Code duplication level

## Scalability (1-10)

| Score | Criteria |
|-------|----------|
| 1-3 | Single instance only, blocking operations, no caching, memory leaks likely |
| 4-5 | Can scale with effort, some bottlenecks identified |
| 6-7 | Horizontally scalable, async operations, basic caching |
| 8-9 | Built for scale, stateless, distributed-ready |
| 10 | Highly distributed, auto-scaling, battle-tested patterns |

**Key indicators**:
- Stateless design
- Database query efficiency
- Caching strategy
- Async/concurrent processing
- Connection pooling

## Security (1-10)

| Score | Criteria |
|-------|----------|
| 1-3 | No auth, SQL injection possible, secrets in code, no input validation |
| 4-5 | Basic auth, some validation, secrets partially managed |
| 6-7 | Proper auth/authz, input validation, secrets externalized |
| 8-9 | Defense in depth, rate limiting, audit logging, secure defaults |
| 10 | Security-first design, pen-tested, compliance-ready |

**Key indicators**:
- Authentication mechanism
- Authorization checks
- Input validation/sanitization
- Secrets management
- HTTPS/TLS usage
- Dependency vulnerabilities

## Maintainability (1-10)

| Score | Criteria |
|-------|----------|
| 1-3 | No docs, no tests, tribal knowledge required, fear to change |
| 4-5 | Some docs, minimal tests, changes are risky |
| 6-7 | Good docs, decent test coverage, changes manageable |
| 8-9 | Comprehensive docs, high test coverage, confident refactoring |
| 10 | Self-documenting, >90% coverage, excellent DX |

**Key indicators**:
- Documentation quality
- Test coverage
- Code comments (explaining WHY, not WHAT)
- Dependency management
- Error messages clarity

---

## Common Anti-Patterns Reference

### God Class/File
- Single file > 500 lines handling multiple concerns
- Class with 20+ methods
- "Manager" or "Helper" doing everything

### Tight Coupling
- Direct instantiation instead of injection
- Hardcoded references across modules
- Shared mutable state

### Circular Dependencies
- Module A imports B, B imports A
- Often indicates poor boundary design

### Leaky Abstractions
- Internal implementation details exposed
- Database types in API responses
- ORM entities used as DTOs

### Missing Error Handling
- Bare try/catch with generic errors
- Swallowed exceptions
- No error boundaries

### Configuration Hardcoding
- URLs, credentials, feature flags in code
- Environment-specific logic without config

---

## Onboarding Time Factors

**Reduces onboarding time**:
- Clear README with setup instructions
- Architectural documentation
- Good test suite (safe experimentation)
- Consistent patterns throughout
- Type safety / IDE support

**Increases onboarding time**:
- Multiple languages/frameworks
- Complex domain logic
- Tribal knowledge dependencies
- Inconsistent patterns
- Poor/no documentation
- Flaky or missing tests

---

## Red Flags Reference

Critical issues that should be flagged as P0:

### Security Red Flags
| Issue | How to Detect |
|-------|---------------|
| Secrets in code | Grep for API_KEY, SECRET, PASSWORD, token patterns |
| Secrets in git | Check .env files tracked, search history |
| No auth middleware | Check route definitions for unprotected endpoints |
| SQL injection | Raw string concatenation in queries |
| XSS vulnerabilities | Unescaped user input in templates |
| Outdated deps with CVEs | `npm audit`, `pip-audit`, `cargo audit` |

### Stability Red Flags
| Issue | How to Detect |
|-------|---------------|
| No error handling | Missing try/catch, no error boundaries |
| No health checks | Missing /health or /ready endpoints |
| No graceful shutdown | Missing signal handlers |
| Memory leaks | Unbounded caches, missing cleanup |

---

## Priority Definitions

| Priority | SLA | Criteria |
|----------|-----|----------|
| **P0** | Before next deploy | Security vulnerability, data loss risk, system instability |
| **P1** | Within sprint | Significant tech debt, missing critical tests, performance issues |
| **P2** | Backlog | Code quality improvements, minor refactors, nice-to-haves |

### Effort vs Impact Matrix

```
         │ Low Effort │ Med Effort │ High Effort │
─────────┼────────────┼────────────┼─────────────┤
Critical │ P0 (now)   │ P0 (now)   │ P0 (plan)   │
High     │ P1 (quick) │ P1 (sprint)│ P1 (plan)   │
Medium   │ P2 (do it) │ P2 (maybe) │ P2 (skip)   │
Low      │ P2 (maybe) │ Skip       │ Skip        │
```

---

## Executive Summary Health Ratings

| Rating | Criteria |
|--------|----------|
| **Healthy** | No red flags, scores avg >7, tests present, docs adequate |
| **Needs Work** | Minor red flags OR scores avg 5-7 OR missing tests/docs |
| **Critical** | Any P0 red flag OR scores avg <5 OR production risk |

### Production Readiness Checklist

Mark as `ready_for_production: false` if ANY of these are missing:
- [ ] No critical security vulnerabilities
- [ ] Authentication on sensitive endpoints
- [ ] Error handling in place
- [ ] Basic monitoring/logging
- [ ] At least some test coverage
- [ ] Environment configuration (not hardcoded)

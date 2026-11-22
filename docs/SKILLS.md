# Skills Reference (Staff Engineer Edition)

Skills are **progressive** — load only what `scripts/skills/select_skills.py` matches.

## Core skills (public kit)

| Skill | Path | Use for |
|-------|------|---------|
| xray | `skills/xray/` | Deep repo analysis |
| knowledge-discovery | `skills/knowledge-discovery/` | Standards gap → MDC proposal |
| java-quarkus | `skills/java-quarkus/` | Java 21 / Quarkus |
| api-engineering | `skills/api-engineering/` | REST/GraphQL/gRPC contracts |
| frontend-architecture | `skills/frontend-architecture/` | React/TS architecture |
| data-engineering | `skills/data-engineering/` | Spanner/BQ/PG/Kafka (not interchangeable) |
| workflow-architecture | `skills/workflow-architecture/` | Sagas, outbox, long jobs |
| ai-engineering | `skills/ai-engineering/` | LLM production patterns |
| reliability-performance | `skills/reliability-performance/` | SLOs, OTel, resilience |
| security-compliance | `skills/security-compliance/` | Tenancy, RBAC, PHI/PII |
| staff-engineering | `skills/staff-engineering/` | TDD, ADR, tech debt, mentorship reviews |
| production-engineering | `skills/production-engineering/` | Docker/k8s/CI/CD/rollouts |

## Optional

| Skill | Path |
|-------|------|
| healthcare-provider | `optional/healthcare/skills/healthcare-provider/` (`INSTALL_HEALTHCARE=1`) |

## Agents vs skills

| Need | Mechanism |
|------|-----------|
| Independent API contract critique | Agent `api-architect` + api-engineering skill |
| Independent LLM product critique | Agent `ai-product-engineer` + ai-engineering skill |
| Data/FE/workflow/reliability design | Vishwakarma/Bhishma **load skills** — no extra agents |
| Healthcare domain | Optional agent + skill (optional healthcare pack) |

## Selector

```bash
python3 scripts/skills/select_skills.py --paths 'src/api/Foo.java,openapi.yaml' --signals 'api,security'
```

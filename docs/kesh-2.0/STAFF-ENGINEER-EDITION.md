# Kesh Staff Engineer Edition (1A + 2A)

**Decisions locked:** Skills-first specialists; optional healthcare as **optional** pack.  
**Branch:** `feature/staff-engineer-edition`  
**Preserve:** Parth = implementation, Swachalit = tests. Core kit stays company-agnostic.

## Capability matrix (role vs kit)

| Staff SE responsibility | Existing coverage | Gap | 2.6 approach |
|-------------------------|-------------------|-----|--------------|
| Ambiguous requirements | Vidura | — | Keep |
| Repo discovery | Sanjaya + xray skill | Thin profile/cache | `scripts/repo/profile.py` + cache |
| Architecture / ADR | Vishwakarma + standards | Weak ADR memory | `skills/staff-engineering` + `scripts/adr` |
| Java 21 / Quarkus | `standards/java-quarkus` | Skill packaging | `skills/java-quarkus` |
| React / TS | `standards/react-typescript` | No FE architect agent | `skills/frontend-architecture` |
| API contracts | Partial (Bhishma/Vishwakarma) | No dedicated API critique | **Agent: api-architect** + `skills/api-engineering` |
| Spanner/BQ/PG/Kafka | `standards/database/**` + knowledge | No Data Architect agent | `skills/data-engineering` (Vishwakarma/Bhishma load) |
| Distributed workflows | `distributed-systems` | No workflow specialist agent | `skills/workflow-architecture` |
| Multi-tenant / RBAC / audit | `security` | Thin | `skills/security-compliance` |
| Healthcare provider domain | None (forbidden in core) | Missing | **optional/healthcare** + healthcare-domain agent |
| AI/LLM product | None | Missing | **Agent: ai-product-engineer** + `skills/ai-engineering` |
| Perf / SLO / OTel | knowledge module | No specialist agent | `skills/reliability-performance` |
| Test / security / deploy gates | Swachalit, Bhishma, prompt | Weak tool discovery | `scripts/quality/discover_tools.py` |
| Token efficiency | 2.5 modes/cache/context | — | Preserve |
| NITI learning | 2.4 telemetry | — | Preserve + staff metrics fields |

## Overlaps avoided

| Temptation | Instead |
|------------|---------|
| Data / Frontend / Workflow / Reliability agents | Skills loaded by Vishwakarma / Bhishma / Kesh |
| Swap Parth ↔ Swachalit | Rejected — keep current contracts |
| Employer healthcare pack in core | `optional/healthcare/` + `INSTALL_HEALTHCARE=1` |
| Competing orchestrators | Kesh + Sutradhar only |

## New agents (core)

1. **api-architect** — contract design, breaking changes, OpenAPI/GraphQL/gRPC critique  
2. **ai-product-engineer** — LLM product architecture, evals, fallbacks (HTTP 200 ≠ correct)

## Optional agents

3. **healthcare-domain** (optional healthcare pack) — provider data reasoning; facts vs assumptions; no invented business rules

## Non-executable promises (honest)

- Live LLM quality before/after: operator-run benchmarks only  
- Billing tokens: still often UNKNOWN  
- Employer repo tools: discover, do not invent PASS  

## Phases

1. This matrix + routing design  
2. Agents + skills + router/install  
3. Repo profile + ADR + quality discovery  
4. Benchmarks + docs + validation  

## Deliverables checklist (Section 17)

| # | Deliverable | Location |
|---|-------------|----------|
| 1–4 | Assessment / matrix / gaps / mods | this file |
| 5 | Responsibility map | `docs/AGENTS.md`, router examples |
| 6 | Skill inventory | `docs/SKILLS.md` |
| 7 | File list | CHANGELOG 2.6.0 |
| 8 | Routing | `kesh-runtime-router.mdc`, `select_mode.py` |
| 9 | Quality gates | `scripts/quality/discover_tools.py` + existing Swachalit/Bhishma |
| 10 | Repo intelligence | `scripts/repo/profile.py` |
| 11 | ADR memory | `scripts/adr/*`, `docs/architecture/decisions/` |
| 12 | NITI | unchanged path; proxies from 2.5 |
| 13 | Benchmarks | `benchmarks/token-optimization` + `benchmarks/staff-engineer` |
| 14 | Token efficiency | preserved 2.5 controls |
| 15 | Security | local-first; optional pack; no PHI |
| 16 | Limitations | live quality/billing UNKNOWN until operator runs |
| 17 | Next steps | Install optional pack if needed; fill live benchmark table; slim Bhishma.md size later |

## Remaining limitations

- Live LLM before/after quality **not** claimed  
- Billing tokens often UNKNOWN  
- Employer repo tool PASS not invented — MISSING/NOT RUN  
- Healthcare agent absent until `INSTALL_HEALTHCARE=1`  

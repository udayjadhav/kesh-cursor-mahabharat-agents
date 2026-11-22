# Knowledge Discovery — Acceptance Scenarios A–H

**Status legend:** `PASS` = exercised in this environment; `TABLETOP` = routing/contract verified against kit text; `NOT_EXECUTED` = needs live Cursor run against a real repo.

| ID | Scenario | Expected behavior | Kit contract | Live run |
|----|----------|-------------------|--------------|----------|
| A | Known tech (Java/Quarkus) with sufficient standards | Detect → load java-quarkus (+security/testing as needed) → **no research** | Spec + skill skip gate + manifest entry | **TABLETOP** |
| B | New technology, no standard | Repo → org → official → propose consolidated MDC | Skill steps 1–8; approval before write | **NOT_EXECUTED** |
| C | Incomplete PostgreSQL standard for a workload | Research gap → **UPDATE** existing engine/design files, not duplicate | Skill UPDATE path; template | **NOT_EXECUTED** |
| D | Org Confluence API convention ≠ external blog | Preserve org-approved convention; document trade-offs | Authority precedence; Vyasa citations | **NOT_EXECUTED** (needs Confluence) |
| E | Internal older version vs official security advisory | Surface conflict; escalate; do not silent-override | Conflict + escalate rules | **TABLETOP** (policy text) |
| F | New cloud/deploy platform in repo | Discover infra/security/ops before modify/review | Detection kinds include cloud/infra | **NOT_EXECUTED** |
| G | Confluence unavailable | Report `org_sources: UNAVAILABLE`; no fake org compliance | Vyasa + skill failure handling | **TABLETOP** |
| H | Familiar stack, adequate coverage | Proceed; **no new MDC** | Skip gate | **TABLETOP** |

## Automated checks supporting this feature

```
./tests/validate-kit.test.sh
```

Must include: knowledge-discovery skill present, discovery rule present, manifest JSON valid, `_TEMPLATE.mdc` present, spec ≥ 2.1.0.

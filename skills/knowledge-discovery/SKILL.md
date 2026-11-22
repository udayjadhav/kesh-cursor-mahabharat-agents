---
name: knowledge-discovery
description: Detect technologies, assess knowledge gaps, research repo/org/official sources, reconcile conflicts into MUST/SHOULD/MAY guidance, and propose MDC standard create/update. Use when Kesh/Sanjaya finds unfamiliar or under-covered tech, incomplete standards, or conflicting guidance.
---

# Knowledge Discovery Skill

Follow this procedure whenever coverage for a task-critical technology is missing, incomplete, outdated, or inconsistent. Integrate with `rules/kesh-knowledge-discovery.mdc`.

## Step 0 — Skip gate

If all are true, **stop** (Scenario H):

- Technologies identified
- Matching standards exist and cover the workload
- Versions roughly match
- No security/infra novelty requiring fresh advisories
- Task is not introducing a new platform

Record: `knowledge_gate: SUFFICIENT` and list standards to load.

## Step 1 — Technology inventory

Produce:

```yaml
technologies:
  - name: PostgreSQL
    kind: database
    version: "15"   # or unknown
    evidence: ["docker-compose.yml", "pom.xml"]
    task_relevance: high | medium | low
```

Ignore low-relevance transitive noise unless security-critical.

## Step 2 — Coverage assessment

For each high/medium tech, check:

| Source | Path |
|--------|------|
| Manifest | `knowledge/manifest.json` |
| Standards | `rules/standards/**` |
| Knowledge notes | `knowledge/*.md` |
| Repo | ADRs, CONTRIBUTING, lint configs, existing code |

Output per tech: `SUFFICIENT | PARTIAL | MISSING | STALE | CONFLICT_SUSPECTED`  
Presence of a file ≠ sufficient — note missing sections for the workload.

## Step 3 — Repository evidence (always first)

Collect:

- Dependency manifests and versions
- Config and deployment
- Tests and CI
- README / docs / ADRs
- Recurring code patterns and shared libs

Mark patterns as `approved_signal` vs `possible_legacy` when unclear.

## Step 4 — Organization sources

If tools/MCP available: search Confluence, handbooks, internal ADRs, eng docs, platform docs.

If **not** connected:

```text
org_sources: UNAVAILABLE
limitation: Confluence/internal docs not searchable in this session
```

Do **not** invent org policy. Do **not** claim org compliance.

Prioritize org-wide mandatory standards over team prefs; note scoped team ADR exceptions.

## Step 5 — Official external sources

Only if still insufficient. Prefer:

1. Official product/language/framework docs for **detected version**
2. Official release notes / migration guides
3. Official security advisories
4. Standards bodies / recognized specs
5. Credible eng publications only if primaries lack coverage

Avoid: random blogs, Stack Overflow as authority, scraped/generated SEO content.

For security: prefer vendor advisories.

## Step 6 — Conflict resolution

For each conflict:

1. State recommendations A vs B  
2. Source, date, authority, scope  
3. Same version/workload?  
4. Impact (security, reliability, maintainability, compatibility, ops)  
5. Preferred applicable guidance  
6. Preserve org mandates  
7. If org mandate vs security advisory conflict → **escalate** (do not silent-override)

## Step 7 — Merge into MUST / SHOULD / MAY

Draft consolidated guidance answering org / repo / vendor / agreements / differences / exceptions.

Label each item:

- `verified_org_policy` | `repo_convention` | `vendor_doc` | `inferred`

Never present inferred items as company policy.

## Step 8 — Propose standard change

Decide: **UPDATE existing** vs **CREATE new** vs **NO FILE**.

Proposal package (show user before write):

```markdown
## Knowledge proposal
- Technologies:
- Gap:
- Action: UPDATE path | CREATE path | NONE
- Sources used: (repo / org / official)
- Org sources status: available | unavailable
- Conflicts:
- Assumptions:
- MUST/SHOULD/MAY summary:
- Manifest entry draft:
```

Use template `rules/standards/_TEMPLATE.mdc`.

**Do not write** into shared `rules/standards/**` or org docs without approval.

Drafts may be placed in chat or `scratch/` if the workspace allows.

## Step 9 — Manifest update

After approved write, upsert `knowledge/manifest.json`:

- technology, version_range, mdc_paths, knowledge_paths
- internal_sources, external_sources
- last_verified, confidence, limitations, task_categories

## Step 10 — Load for task

Return `standards_to_load: [...]` — only task-relevant files. Attach `knowledge_pack` to shared_knowledge for Parth/Bhishma/Vishwakarma.

## Output contract

```yaml
knowledge_gate: SUFFICIENT | RESEARCHED | BLOCKED_APPROVAL | ESCALATE | UNAVAILABLE_ORG
technologies: [...]
coverage: [...]
standards_to_load: [...]
proposal: null | {...}
conflicts: [...]
limitations: [...]
```

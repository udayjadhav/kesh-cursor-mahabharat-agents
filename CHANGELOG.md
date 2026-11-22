# Changelog

## 2.6.0 — 2026-11-22

### Staff Engineer Edition (skills-first + optional healthcare)

- Decisions: **1A** skills-first; **2A** optional healthcare pack
- Agents: `api-architect`, `ai-product-engineer` (core); `healthcare-domain` under `optional/healthcare/`
- Skills: api, data, frontend, workflow, AI, reliability, security, staff, java-quarkus, production
- Scripts: `skills/select_skills.py`, `repo/profile.py`, `adr/*`, `quality/discover_tools.py`
- ADR memory: `docs/architecture/decisions/` + list/new helpers
- Install: all `skills/*/`; `INSTALL_HEALTHCARE=1`; helper scripts copy
- Docs: `docs/kesh-2.0/STAFF-ENGINEER-EDITION.md`
- Preserved: Parth=implementation, Swachalit=tests; company-agnostic core

---

## 2.5.0 — 2026-11-22

### Token optimization (quality-preserving)

- Audit: `docs/kesh-2.0/TOKEN-OPTIMIZATION-AUDIT.md` + architecture `TOKEN-OPTIMIZATION.md`
- Risk modes: `rules/kesh-execution-modes.mdc` + `scripts/modes/select_mode.py` (escalate-only)
- Context packages: `rules/kesh-context-packaging.mdc` + `scripts/context/package.py`
- Progressive standards: `scripts/standards/select_standards.py`
- Operational cache: `scripts/cache/*` (HIT/STALE/MISS); token-cache rule updated
- Quality guardrails: `rules/kesh-quality-guardrails.mdc`
- Demoted alwaysApply → selective: explanation-framework, global-local-sync, dev-spec-authorship-voice, external-output-voice (modes/packaging rules are reference-loaded via router/spec; guardrails stay always-on)
- Specialized review lanes (Bhishma / Lakshman / Draupadi); Parth deterministic-first
- NITI proxies: context_chars, cache_hit, review_iterations, execution_mode
- Benchmarks: `benchmarks/token-optimization/` (structural; live quality not fabricated)
- Tests: `tests/token/test_token_optimization.py`

**Model pins unchanged** pending live quality benchmarks.

---

## 2.4.0 — 2026-11-22

### Added — NITI activation

- Audit: `docs/kesh-2.0/NITI-AUDIT.md` (documented vs executable)
- `rules/kesh-niti.mdc` + redesigned `agents/niti.md` (Tier A `claude-4-6-sonnet`, propose-only)
- Local telemetry: `scripts/niti/*`, `niti/` schemas, optional hooks (`niti-telemetry`, `niti-stop-trigger`)
- Triggers: 5 / 20 meaningful tasks via `state.json`, post-incident, on-demand, before/after — **no cron**
- Recommendation lifecycle CLI; human-report contract
- Tests: `tests/niti/test_niti_telemetry.py`
- Installer: `INSTALL_NITI=1`

### Honest limits

Cursor Agent Chat hooks do not expose billing tokens/cost. Missing telemetry ≠ success. NITI is outside the mandatory delivery path.

---

## 2.3.0 — 2026-11-22

### Added — Code quality & documentation

- `rules/kesh-code-quality.mdc` — mandatory repo-first coding, maintainability, comments, contracts, DB/API/test docs, README/ADR guidance without file-count inflation
- Wired into Parth / Bhishma / Swachalit / Kesh; spec **2.3.0**

### Principle

Write code that explains itself. Comment the why. Document contracts, decisions, and operations — never generate docs to increase file count.

---

## 2.2.0 — 2026-11-22

### Added — Human-quality communication

- `rules/kesh-human-communication.mdc` — mandatory Staff/Principal engineer voice for all agents
- Paste-ready channel packaging for GitHub review, Slack, Confluence/docs (with scrubbing)
- Spec **2.2.0**; Bhishma/Kesh/kesh-output aligned; external-output-voice examples expanded

### Principle

Communication quality equals engineering quality. Outputs must be usable as PR comments, Slack messages, Confluence notes, or docs without sounding like a chatbot.

---

## 2.1.0 — 2026-11-22

### Added — Knowledge discovery & reconciliation

- `rules/kesh-knowledge-discovery.mdc` — detection, authority, merge, approval
- `skills/knowledge-discovery/SKILL.md` — end-to-end procedure
- `rules/standards/_TEMPLATE.mdc` — generated standard shape (MUST/SHOULD/MAY)
- `knowledge/manifest.json` — technology → standards index
- Docs: `docs/KNOWLEDGE-DISCOVERY.md`, acceptance scenarios A–H
- Wired Sanjaya (Technology Inventory), Kesh (knowledge gate), Vyasa/Parth/Bhishma/Vishwakarma
- Spec bump to **2.1.0**; installer copies knowledge-discovery skill
- Validator checks discovery rule, skill, template, manifest paths

### Design

- **No new agent** — research reused via `knowledge_pack`
- Skip research when coverage SUFFICIENT; update-before-create; never silent-override org mandates

---

## 2.0.0 — 2026-11-22

Kesh 2.0 — adaptive engineering OS upgrade (not a greenfield rewrite).

### Breaking

- **Agent Maximization** replaced by adaptive **12 task classes** and minimum-sufficient specialist selection (`rules/kesh-agent-spec.mdc` v2.0.0).
- **Money Lens** is advisory; must not REJECT-stop `BUG_FIX`, `SECURITY_CHANGE`, `PRODUCTION_INCIDENT`, or mandatory reliability remediation.
- Delivery status: `COMPLETE` | `PARTIAL` | `BLOCKED` | `REQUIRES_HUMAN_APPROVAL` (COMPLETE requires verification evidence).
- Clojure rules moved to `rules/standards/clojure-*.mdc`.
- `teams.mdc` moved to `optional/teams.mdc` (install with `INSTALL_TEAMS=1`).

### Added

- Modular standards: Java/Quarkus, Python, React/TS, security, testing, architecture, microservices, distributed systems, database tree + 8 engines.
- `knowledge/` concept modules (optional `INSTALL_KNOWLEDGE=1`).
- Optional safety hooks (`hooks/`, `INSTALL_HOOKS=1`).
- `scripts/validate-kit.sh` + `tests/validate-kit.test.sh`.
- `optional/knowledge-cache/README.md` schema.
- Phase reports under `docs/kesh-2.0/`.

### Changed

- Parth / Swachalit / Bhishma / Vishwakarma / Sutradhar / Kesh / support modules — evidence-first workflows.
- Runtime router, always-on, explanation framework aligned to adaptive depth.
- `kesh-external-output-voice.mdc` frontmatter restored.
- Installer supports nested `rules/standards/`, knowledge, hooks, skip Clojure, teams flags.
- Docs (README, WORKFLOW, ARCHITECTURE, AGENTS, INSTALL, RULES, STANDARDS, KNOWLEDGE) updated for 2.0.

### Enforcement note

Orchestration remains largely prompt-guided (**B**) with Cursor tool support (**C**). Kit validation and optional hooks provide **D/E** where documented — do not assume prompt rules are machine-enforced.

---

## 1.2.0 — 2026-09-11

Synced from live agents/rules (flow, models, cache gate) with org-specific product content left out of this public kit.

### Repo

- Canonical GitHub name is `kesh-cursor-mahabharat-agents` (fixes the `cusror` typo).

### Agents

- All 17 roster agents copied from live `~/.cursor/agents`, then genericised for a public kit (no company-specific language, URLs, or architecture KB).
- Model pins unchanged and match `rules/kesh-agent-spec.mdc`:
  - Tier A opus: `claude-4-7-opus`
  - Tier A sonnet / Tier C: `claude-4-6-sonnet`
  - Tier B: `composer-2`
- Removed stale `GPT-5.3` / `Claude 3.7` labels from frontmatter and bodies.
- Added YAML frontmatter (`name` + `description`) to support modules: `kesh-context`, `kesh-flows`, `kesh-output`, `kesh-rules`.
- Restored **Vyasa as step 3** in `kesh.md` and `kesh-flows.md` (the published kit still used the old 14-step numbering).
- Step numbers now match the spec: Parth 6, Swachalit 7, Bhishma 8, Lakshman 9, Draupadi 10, Krishna 11, Money Lens 12, Decision Engine 13, Kripacharya 14, Kesh 15.
- Cache Gate (Step 0.5) documented in Kesh flow ASCII and README / WORKFLOW diagrams.

### Rules added to the kit (were live-only)

- `kesh-token-cache.mdc` — Cache Gate before Phase 1

### Docs

- README, WORKFLOW, AGENTS, RULES, INSTALL, ARCHITECTURE refreshed for cache gate and the renamed clone URL.
- Team roster template lived under rules (moved to `optional/teams.mdc` in 2.0.0).
- Remaining company-specific examples (query-library names, ticket fields, helpcenter sections) replaced with generic wording.

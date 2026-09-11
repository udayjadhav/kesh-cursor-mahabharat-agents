# Changelog

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
- `rules/teams.mdc` is a blank roster template (fill in your org).

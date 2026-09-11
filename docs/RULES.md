# Rules Reference

Cursor rules live in `rules/*.mdc`. Files with `alwaysApply: true` in frontmatter apply to every chat in that workspace (global when installed to `~/.cursor/rules/`).

## Core Kesh rules (required)

| File | alwaysApply | Purpose |
|------|-------------|---------|
| `kesh-agent-spec.mdc` | yes | **Canonical contract** — 15 steps, tiers, models, skip logic, loops |
| `kesh-runtime-router.mdc` | yes | Intent analyzer → agent selection (not keyword matching) |
| `kesh-always-on.mdc` | yes | Route user instructions through Kesh by default |
| `kesh-token-cache.mdc` | yes | Step 0.5 Cache Gate before Phase 1 |
| `kesh-explanation-framework.mdc` | yes | Analogies, diagrams, multi-perspective synthesis in chat |
| `kesh-external-output-voice.mdc` | yes | Scrub agent vocabulary for Confluence / Jira / PR / Slack |
| `global-local-sync.mdc` | yes | `~/.cursor` global vs `<repo>/.cursor` local overrides |

## Quality and design rules

| File | alwaysApply | Purpose |
|------|-------------|---------|
| `reuse-before-extend.mdc` | yes | Option 0 reuse-only; field carrier inventory; consumer audit |
| `dev-spec-authorship-voice.mdc` | yes | Specs read as engineer-authored (no AI meta, no section-sign glyph) |
| `dev-spec-scoping-defaults.mdc` | no | L1–L6 lifecycle tasks in dev specs |

## Optional / org-specific

| File | Notes |
|------|-------|
| `teams.mdc` | Jira team roster **template** — replace with your org or delete |
| `clojure-review.mdc` | Clojure code review conventions (`alwaysApply: false`) |
| `clojure-daily-tips.mdc` | Clojure tips (`alwaysApply: false`) |

## Rule precedence

1. `kesh-agent-spec.mdc` wins over any agent `.md` file
2. Local `<repo>/.cursor/rules/*.mdc` overrides global `~/.cursor/rules/` for that repo
3. Local `<repo>/.cursor/agents/*.md` overrides global agents for that repo

## Key invariants (from spec)

- Parth and Bhishma **must not** share the same model
- Bhishma FAIL or Lakshman FAIL → loop to Parth (max 5)
- Krishna KILL or Money Lens REJECT → stop
- Vyasa never speculates — facts need citations
- Skip agents only when inputs do not exist (not to save tokens)
- Cache Gate skips are applicability skips (output already exists), not cost skips

## Editing rules after install

```bash
# Global (all projects)
vim ~/.cursor/rules/kesh-agent-spec.mdc

# Single repo only
vim my-repo/.cursor/rules/kesh-always-on.mdc
```

After changes, restart Cursor or reload the window.

## Syncing back to this kit

When you improve rules on one machine:

```bash
cp ~/.cursor/rules/*.mdc /path/to/kesh-cursor-mahabharat-agents/rules/
git commit -am "Sync rules from workstation"
```

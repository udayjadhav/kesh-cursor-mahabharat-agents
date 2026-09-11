# Optional / org-specific files

These files are **examples**. Customise before use or exclude from install.

## `teams.mdc` (in main `rules/`)

The shipped `rules/teams.mdc` is a **blank roster template**. On a new machine:

1. Fill in your Atlassian site, cloud ID, projects, and people, or
2. Delete `~/.cursor/rules/teams.mdc` after install if unused

Template pattern:

```markdown
## Your Team Name

| Name | Email | Jira Account ID |
|------|-------|-----------------|
| ... | ... | ... |

### Default JQL
assignee in ("account-id-1", ...) AND statusCategory != Done
```

## Clojure rules

`clojure-review.mdc` and `clojure-daily-tips.mdc` apply only if you work in Clojure. Remove from `rules/` in this kit if not needed:

```bash
rm rules/clojure-*.mdc
```

## Vyasa external sources

Vyasa expects optional integrations:

- Atlassian Confluence + Jira (MCP or API)
- Public helpcenter / developer docs / status pages (web search)

Without configuration, Vyasa returns `no_context` and the workflow continues.

## Minimal kit (smaller install)

For a minimal portable install, copy only:

```
agents/*.md
rules/kesh-agent-spec.mdc
rules/kesh-always-on.mdc
rules/kesh-runtime-router.mdc
rules/kesh-explanation-framework.mdc
rules/kesh-token-cache.mdc
rules/global-local-sync.mdc
skills/xray/*
```

Add other rules as needed.

# Optional / org-specific files

Customise before use. These are **not** required for core Kesh.

## Optional healthcare pack

See [`healthcare/README.md`](./healthcare/README.md). Install with `INSTALL_HEALTHCARE=1 ./install.sh`.  
Keeps employer/domain naming out of the public core kit scan.

## `teams.mdc` (this directory)

Blank Jira team roster template. Copy into `~/.cursor/rules/` only if you need it:

```bash
cp optional/teams.mdc ~/.cursor/rules/teams.mdc
```

Set `alwaysApply: true` only after you fill real rosters.

## Clojure standards

Shipped under `rules/standards/clojure-*.mdc` with Clojure globs (`alwaysApply: false`). Remove if unused:

```bash
rm rules/standards/clojure-*.mdc
```

## Knowledge modules

See repo `knowledge/`. Optional install to `~/.cursor/knowledge/kesh/` (`INSTALL_KNOWLEDGE=1`).

## Vyasa external sources

Optional integrations: Atlassian (Confluence/Jira), helpcenter, developer docs, status pages. Without them Vyasa returns `no_context`.

## Minimal kit

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

Add `rules/standards/**` as needed for your stacks.

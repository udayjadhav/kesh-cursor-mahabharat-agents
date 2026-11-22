# Installation Guide (Kesh 2.6)

## Requirements

- [Cursor](https://cursor.com) with **subagents** enabled
- Models in agent frontmatter available on your plan
- macOS / Linux / Windows (WSL)
- `python3` on PATH if using the optional safety hook or kit validator

## Automated install

```bash
git clone https://github.com/udayjadhav/kesh-cursor-mahabharat-agents.git
cd kesh-cursor-mahabharat-agents
chmod +x install.sh
./install.sh
```

### Flags

| Variable | Default | Effect |
|----------|---------|--------|
| `CURSOR_DIR` | `~/.cursor` | Install root |
| `DRY_RUN` | `0` | Preview only |
| `INSTALL_KNOWLEDGE` | `0` | Copy `knowledge/` → `~/.cursor/knowledge/kesh/` |
| `INSTALL_HOOKS` | `0` | Copy hook scripts to `~/.cursor/hooks/` (still need `hooks.json`) |
| `SKIP_CLOJURE` | `0` | Remove Clojure standards after install |
| `INSTALL_TEAMS` | `0` | Copy `optional/teams.mdc` into rules |

Examples:

```bash
DRY_RUN=1 ./install.sh
INSTALL_KNOWLEDGE=1 INSTALL_HOOKS=1 ./install.sh
SKIP_CLOJURE=1 ./install.sh
```

The script:

1. Backs up existing `agents/`, `rules/`, `skills/xray/` (and optional targets) with timestamps
2. Copies agents, **nested** `rules/` (including `standards/`), and xray skill
3. Optionally installs knowledge and/or hooks

**Restart Cursor** after install.

## Upgrade from 1.x → 2.0

```bash
cd kesh-cursor-mahabharat-agents
git pull
./install.sh
```

### Breaking behavioral changes

- **Agent Maximization withdrawn** — adaptive task classes instead of “run all 15”
- **Money Lens** no longer hard-stops bug/security/incident remediation
- Delivery vocabulary prefers `COMPLETE` / `PARTIAL` / `BLOCKED` / `REQUIRES_HUMAN_APPROVAL`
- Clojure rules moved to `rules/standards/clojure-*.mdc`
- `teams.mdc` is optional (`INSTALL_TEAMS=1` or copy from `optional/`)

Backups preserve your previous `~/.cursor` copies.

## Validate kit (from repo)

```bash
./scripts/validate-kit.sh
./tests/validate-kit.test.sh
```

## Optional safety hooks

```bash
INSTALL_HOOKS=1 ./install.sh
# then enable — prefer project-level:
mkdir -p my-repo/.cursor/hooks
cp hooks/deny-destructive-shell.sh my-repo/.cursor/hooks/
cp hooks/hooks.json.example my-repo/.cursor/hooks.json
# edit command path as needed; chmod +x the script
```

See `hooks/README.md`. Global user hooks need explicit operator approval.

## Manual install

```bash
KIT=/path/to/kesh-cursor-mahabharat-agents
mkdir -p ~/.cursor/{agents,rules,skills/xray}
cp -a "$KIT/agents/." ~/.cursor/agents/
cp -a "$KIT/rules/." ~/.cursor/rules/          # includes standards/
cp -a "$KIT/skills/xray/." ~/.cursor/skills/xray/
```

## Per-repository override

```bash
mkdir -p my-repo/.cursor/agents
cp agents/bhishma.md my-repo/.cursor/agents/
```

Local overrides global for that repo.

## Post-install checklist

| Step | Action |
|------|--------|
| 1 | Restart Cursor |
| 2 | Confirm rules load (Settings → Rules) |
| 3 | `@kesh explain adaptive workflows` |
| 4 | Optionally `INSTALL_KNOWLEDGE=1` / hooks / teams |
| 5 | `SKIP_CLOJURE=1` if unused |
| 6 | Enable Max Mode if Opus agents fall back |

## Troubleshooting

### Agents missing

- `ls ~/.cursor/agents/kesh.md`
- Reload window

### Standards not applying

- Confirm `~/.cursor/rules/standards/` exists
- Modules use `alwaysApply: false` + **globs** — open a matching file type

### Wrong model

- Check frontmatter; plan/Max Mode; usage report for fallbacks

### Vyasa empty

- Needs Atlassian/web tools; otherwise `no_context` (non-blocking)

## Uninstall / restore

Restore from `~/.cursor/agents-backup-*` / `rules-backup-*` created by the installer.

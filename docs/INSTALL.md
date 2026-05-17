# Installation Guide

## Requirements

- [Cursor](https://cursor.com) with **subagents** enabled
- Models in agent frontmatter available on your plan (Opus/Sonnet/Composer — see account settings)
- macOS / Linux / Windows (WSL) — paths use `~/.cursor`

## Automated install

```bash
git clone <your-repo-url> kesh-cursor-kit
cd kesh-cursor-kit
chmod +x install.sh
./install.sh
```

Options:

```bash
# Custom Cursor directory (unusual)
CURSOR_DIR=/custom/path/.cursor ./install.sh

# Preview without writing
DRY_RUN=1 ./install.sh

./install.sh --help
```

The script:

1. Creates `~/.cursor/agents`, `rules`, `skills/xray` if missing
2. Backs up existing dirs with timestamp suffix
3. Copies all kit files into place

**Restart Cursor** after install.

## Manual install

```bash
KIT=/path/to/kesh-cursor-kit
mkdir -p ~/.cursor/{agents,rules,skills/xray}
cp -a "$KIT/agents/."   ~/.cursor/agents/
cp -a "$KIT/rules/."    ~/.cursor/rules/
cp -a "$KIT/skills/xray/." ~/.cursor/skills/xray/
```

## Upgrade existing install

```bash
cd kesh-cursor-kit
git pull
./install.sh
```

Backups are created automatically (`agents-backup-YYYYMMDD-HHMMSS`, etc.).

## Per-repository override

For one project only:

```bash
mkdir -p my-repo/.cursor/agents
cp agents/bhishma.md my-repo/.cursor/agents/
```

Local agents override global for that repo. Same for `my-repo/.cursor/rules/`.

## Post-install checklist

| Step | Action |
|------|--------|
| 1 | Restart Cursor |
| 2 | Open any project; confirm rules load (Settings → Rules) |
| 3 | Test: `@kesh explain what you can do` |
| 4 | Customize `rules/teams.mdc` or remove if not using Jira teams |
| 5 | Remove `clojure-*.mdc` if not applicable |
| 6 | Enable Max Mode if Opus agents fall back unexpectedly |

## Troubleshooting

### Agents not appearing

- Confirm files exist: `ls ~/.cursor/agents/kesh.md`
- Cursor version supports custom agents / subagents
- Reload window: Command Palette → "Developer: Reload Window"

### Wrong model used

- Check agent frontmatter `model:` field
- Verify plan includes that model
- See usage report for fallback events

### Rules not applied

- `alwaysApply: true` must be in rule frontmatter
- Project may have conflicting local rules
- User rules in Cursor settings may override — check precedence in Cursor docs

### Vyasa / org knowledge empty

- Vyasa needs MCP or tools for Confluence/Jira/web — configure separately
- With no sources, Vyasa returns `no_context` and does not block the flow

## Uninstall

```bash
rm -rf ~/.cursor/agents/kesh*.md ~/.cursor/agents/{vidura,sanjaya,...}.md
# Or restore from backup:
cp -a ~/.cursor/agents-backup-XXXXXXXX/* ~/.cursor/agents/
```

Keep a backup before bulk delete.

## Copy to another machine

```bash
# Machine A: push to GitHub
cd kesh-cursor-kit && git push

# Machine B
git clone <repo> && cd kesh-cursor-kit && ./install.sh
```

Or zip without git:

```bash
tar czf kesh-cursor-kit.tgz kesh-cursor-kit
scp kesh-cursor-kit.tgz user@otherhost:~
ssh user@otherhost 'tar xzf kesh-cursor-kit.tgz && cd kesh-cursor-kit && ./install.sh'
```

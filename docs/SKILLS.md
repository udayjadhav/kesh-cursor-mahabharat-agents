# Skills Reference

Skills extend agent capabilities with structured procedures. They install to `~/.cursor/skills/<name>/`.

## Included: XRay (`skills/xray/`)

| File | Purpose |
|------|---------|
| `SKILL.md` | When to use deep repo analysis; workflow for Sanjaya |
| `scoring-guide.md` | Scoring dimensions for architecture / quality assessment |

### When to use

- Onboarding to a new codebase
- Architecture review before a large change
- Risk and anti-pattern assessment
- "How does this system work?" questions

### Install location

```
~/.cursor/skills/xray/
├── SKILL.md
└── scoring-guide.md
```

The installer copies these automatically. Sanjaya (`agents/sanjaya.md`) references this skill.

## Adding skills

1. Create `skills/<skill-name>/SKILL.md` with frontmatter per [Cursor skills docs](https://cursor.com/docs/context/skills).
2. Add the folder to this repo.
3. Extend `install.sh` if you add paths beyond `skills/xray/`.

## Skills vs agents

| | Agent | Skill |
|---|-------|-------|
| Invocation | `@sanjaya` | Loaded when agent/task matches description |
| Location | `agents/*.md` | `skills/<name>/SKILL.md` |
| Model | Pinned in agent frontmatter | Uses invoking agent's model |

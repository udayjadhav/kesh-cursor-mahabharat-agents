# Kesh 2.0 — Phase 5 Report

**Branch:** `feature/kesh-2.0-rearchitecture`  
**Status:** Complete

## Summary

Introduced executable kit validation (**D/E** for kit integrity) and an **opt-in** destructive-shell hook pack. Documented cache schema. Did **not** install hooks into the user’s global `~/.cursor` (requires explicit approval).

## Files added

| Path | Purpose | Enforcement |
|------|---------|-------------|
| `scripts/validate-kit.sh` | Frontmatter, roster, model diversity, standards, residue checks | **D** |
| `tests/validate-kit.test.sh` | Runs validator + hook smoke tests | **E** |
| `hooks/deny-destructive-shell.sh` | beforeShellExecution gate | **D** when installed |
| `hooks/hooks.json.example` | Cursor hooks template | — |
| `hooks/README.md` | Install + limitations | **A** |
| `optional/knowledge-cache/README.md` | Cache schema for token-cache rule | **A/B** |
| This report | — | — |

## Files modified

- `rules/kesh-token-cache.mdc` — points at kit cache schema

## Tests executed

```
./tests/validate-kit.test.sh
```

Results: **5 passed, 0 failed** (validator + 4 hook cases).

## Decisions

1. Hooks are **opt-in** — not part of default `install.sh` (Phase 6 may add `INSTALL_HOOKS=1`)
2. Default hook mode is `ask`, not silent `deny`
3. Sutradhar timeouts remain **B** (documented) — not claimed as hook-enforced
4. Residue scanner excludes itself and Phase 1/2 audit docs that mention banned strings intentionally

## Remaining issues

- Full docs/README/WORKFLOW sync → Phase 6  
- Installer knowledge + hooks flags → Phase 6  
- Acceptance scenarios A–J → Phase 7  
- No commit/push yet  

# Kesh 2.0 — Phase 6 Report

**Branch:** `feature/kesh-2.0-rearchitecture`  
**Status:** Complete

## Summary

Installer upgraded for nested standards, optional knowledge/hooks/teams, and Clojure skip. Core docs and CHANGELOG aligned to adaptive 2.0 contracts.

## Files added

- `docs/kesh-2.0/PHASE-6-REPORT.md` (this file)

## Files modified

| File | Change |
|------|--------|
| `install.sh` | 2.0 flags: `INSTALL_KNOWLEDGE`, `INSTALL_HOOKS`, `SKIP_CLOJURE`, `INSTALL_TEAMS`; dynamic counts; nested rules |
| `README.md` | 2.0 positioning, adaptive diagram, A–E table |
| `docs/WORKFLOW.md` | Adaptive classes + delivery statuses |
| `docs/ARCHITECTURE.md` | Layers + enforcement |
| `docs/AGENTS.md` | Roster + adaptive invocation |
| `docs/INSTALL.md` | Flags + 1.x→2.0 upgrade notes |
| `CHANGELOG.md` | `2.0.0` section |

(Earlier phases already updated `docs/RULES.md`, `STANDARDS.md`, `KNOWLEDGE.md`.)

## Files removed

- None in this phase

## Decisions

1. Default install = agents + rules (incl. standards) + xray; knowledge/hooks/teams opt-in  
2. Hooks copy scripts only — operator must enable `hooks.json`  
3. Document breaking changes prominently in INSTALL + CHANGELOG  

## Tests executed

```
DRY_RUN=1 ./install.sh
DRY_RUN=1 INSTALL_KNOWLEDGE=1 INSTALL_HOOKS=1 SKIP_CLOJURE=1 INSTALL_TEAMS=1 ./install.sh
./tests/validate-kit.test.sh
```

Results: dry-runs OK (21 agents, 35 rules / 25 standards); validate-kit.test.sh **5 passed, 0 failed**.

## Remaining issues

- Phase 7 acceptance scenarios A–J  
- No commit/push yet  
- Live Cursor install into `~/.cursor` not performed (operator choice)  

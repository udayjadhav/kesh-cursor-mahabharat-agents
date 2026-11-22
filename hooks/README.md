# Optional Kesh hooks

**Enforcement level:** **D** when installed into a Cursor `hooks.json`.  
**Default:** Not installed by `install.sh` unless `INSTALL_HOOKS=1` and/or `INSTALL_NITI=1`.

## 1. Safety — destructive shell gate

- Event: `beforeShellExecution` → `deny-destructive-shell.sh`
- Returns `permission: ask` (or `deny` if `KESH_HOOK_MODE=deny`)
- Env: `KESH_HOOK_MODE=ask|deny|off`

## 2. NITI telemetry (opt-in)

Scripts: `niti-telemetry.sh`, `niti-stop-trigger.sh`  
Example config: `hooks.json.niti.example`

| Event | Purpose |
|-------|---------|
| `subagentStart` / `subagentStop` | Record redacted agent lifecycle |
| `postToolUseFailure` | Record tool failures |
| `sessionEnd` | Session duration / reason |
| `stop` | Record + optional `followup_message` when NITI threshold pending (`loop_limit: 1`) |

**Does not expose / invent:** billing tokens, USD cost, cron schedules.  
**Does not store:** prompt text, file contents, edit bodies, user email.

Runtime data: `~/.cursor/niti/` (`KESH_NITI_HOME`).  
Recording meaningful deliveries still requires Kesh to call `scripts/niti/record_execution.py`.

## Install (project)

```bash
mkdir -p .cursor/hooks
cp hooks/*.sh hooks/*.example hooks/README.md .cursor/hooks/ 2>/dev/null || true
cp hooks/deny-destructive-shell.sh hooks/niti-*.sh .cursor/hooks/
chmod +x .cursor/hooks/*.sh
# merge hooks.json.niti.example (or hooks.json.example) into .cursor/hooks.json
```

Paths in examples assume hooks run from the directory that contains `./hooks/…` (user global `~/.cursor`) or adjust to `.cursor/hooks/…` for project roots.

## Limitations (honest)

- Pattern-based safety gate — false negatives/positives possible
- NITI counters only advance when executions are recorded
- `followup_message` is not a scheduler — fires only on agent `stop`
- Requires `python3` on PATH

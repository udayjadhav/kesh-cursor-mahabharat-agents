# Kesh Engineering Knowledge

Concise concept notes plus a lightweight **manifest** for technology → standards mapping.

**Enforcement:** **A/B**. Reading these does **not** prove knowledge of a specific production system.

**Install:** `INSTALL_KNOWLEDGE=1 ./install.sh` → `~/.cursor/knowledge/kesh/` (includes `manifest.json`).

## Files

| Path | Role |
|------|------|
| `manifest.json` | Technology index: MDC paths, confidence, limitations, last_verified |
| `*.md` | Concept modules (replication, consistency, …) |

## Knowledge discovery

When coverage is incomplete, follow:

- `rules/kesh-knowledge-discovery.mdc`
- `skills/knowledge-discovery/SKILL.md`
- Template: `rules/standards/_TEMPLATE.mdc`

Update the manifest when a standard is approved and written. Prefer **updating** existing standards over creating duplicates.

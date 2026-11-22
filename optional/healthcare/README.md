# Optional healthcare domain pack

**Not part of the public core kit.** Install only with explicit operator approval.

```bash
INSTALL_HEALTHCARE=1 ./install.sh
```

## Contents

| Path | Purpose |
|------|---------|
| `optional/healthcare/agents/healthcare-domain.md` | Healthcare Domain Analyst agent |
| `optional/healthcare/skills/healthcare-provider/SKILL.md` | Progressive skill (NPI, licensing, provenance patterns) |
| `optional/healthcare/knowledge/README.md` | Placeholder for org-approved domain notes (no secrets) |

## Rules

- Do **not** invent employer-specific business rules  
- Distinguish confirmed facts vs assumptions needing domain-expert validation  
- Never put PHI/PII samples, credentials, or proprietary dumps in this pack  
- Core `validate-kit.sh` must still pass with this tree excluded from residue scan  

Keep employer product names inside this optional tree only.

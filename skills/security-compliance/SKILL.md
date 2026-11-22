---
name: security-compliance
description: Multi-tenancy, RBAC, audit logs, PHI/PII handling, OWASP, secrets, tenant isolation. Load for SECURITY_CHANGE and CRITICAL authz work.
---

# Security & Compliance Skill

## When to use

Authn/z changes, tenant isolation, audit trails, secret handling, PHI/PII paths.

## Principles

- Deny by default; least privilege  
- Tenant isolation tested, not assumed  
- Audit who did what when on sensitive actions  
- Secrets never in prompts, logs, or git  
- Prefer repo scanners when present  

## Anti-patterns

- Client-supplied tenant id as sole authz  
- Logging tokens or PHI  
- “Temporary” public buckets  

## Verification checklist

- [ ] Authz tests RUN or NOT RUN  
- [ ] Secret scan RUN or NOT RUN  
- [ ] Tenant isolation cases listed  

## References

`rules/standards/security.mdc`.

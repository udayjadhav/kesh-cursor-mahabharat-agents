---
name: healthcare-provider
description: Optional healthcare provider-data patterns — NPI, licensing, credentialing, enrollment, FHIR/HL7, provenance. No invented employer-specific business rules.
---

# Healthcare Provider Skill (optional pack)

## When to use

Provider identity, network data, clinical/admin interoperability patterns — only with pack installed.

## Principles

- Facts vs assumptions clearly labeled  
- Provenance and freshness matter as much as payload shape  
- Reconciliation and duplicates are first-class  
- Auditability / lineage for regulated reads  
- Never invent employer-specific eligibility or credentialing rules  

## Anti-patterns

- Treating NPI as the only identity key without evidence  
- Ignoring source system conflict  
- Putting PHI in examples  

## Verification checklist

- [ ] Domain assumptions listed for human validation  
- [ ] Lineage/audit fields considered  

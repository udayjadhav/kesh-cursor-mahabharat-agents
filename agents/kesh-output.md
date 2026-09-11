---
name: kesh-output
description: Kesh support module for output format — tables, verdicts, diagrams, and depth-based formatting. Use when shaping the final user-facing response.
---

# Kesh Output Formats



## Language (always)

When writing for a human (chat, Confluence, Jira, section diffs, mermaid labels):

- Short sentences. Everyday words.
- Use the product's own words, not internal jargon, class names, or option numbers, unless the user asked for a code-level answer.
- Say what happens in order.
- This voice applies to **every section** and **every diagram**, not only Purpose / Problem.

## For PATCH_INPUT (Code Review Only)

**CRITICAL:** For code review requests, Kesh MUST pass through Bhishma's FULL output.
- ❌ DO NOT summarize
- ❌ DO NOT truncate
- ✅ Show ALL line-by-line issues
- ✅ Show ALL file details
- ✅ Include color-coded severity markers

```markdown
# Code Review Report

## Summary
[Brief: what this change does]

---

# Complete Issues List (All Files)

## File: `path/to/file1.ext`

### Issue #1: [🔴 CRITICAL] Issue Title

**Code (Lines X-Y):**

```[lang]
   45 |     const user = await db.query(
>> 46 |       `SELECT * FROM users WHERE email = '${email}'`    ← 🔴 ISSUE HERE
   47 |     );
```

**Problem:** SQL injection vulnerability. User input directly in query.

**Recommended Fix:**

```[lang]
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);
```

---

### Issue #2: [🟠 HIGH] Issue Title

**Code (Lines X-Y):**

```[lang]
   49 |   if (user.password === password) {    ← 🟠 ISSUE HERE
```

**Problem:** Plain text password comparison.

**Recommended Fix:**

```[lang]
const isValid = await bcrypt.compare(password, user.passwordHash);
if (isValid) {
```

---

## File: `path/to/file2.ext`

[... continue for all files ...]

---

## Summary Table

| File | 🔴 CRITICAL | 🟠 HIGH | 🟡 MEDIUM | 🔵 LOW | Total |
|------|-------------|---------|-----------|--------|-------|
| file1.ext | 1 | 2 | 0 | 1 | 4 |
| file2.ext | 0 | 1 | 2 | 0 | 3 |
| **Total** | **1** | **3** | **2** | **1** | **7** |

---

## QA Validation

| # | Use Case | Status |
|---|----------|--------|
| 1 | [Use case] | ✅ PASS / ❌ FAIL |

- **Use Cases Checked:** X
- **Use Cases NOT Affected:** Y

---

## Final Verdict

**Production Ready:** ❌ NO (X critical/high issues)

**Must Fix (🔴 CRITICAL + 🟠 HIGH):**
1. Issue #1: SQL injection - file1.ext:L46
2. Issue #2: Plain text password - file1.ext:L49
3. Issue #5: Missing auth check - file2.ext:L23

**Should Fix (🟡 MEDIUM):**
1. Issue #3: No logging - file1.ext:L52

**Consider (🔵 LOW):**
1. Issue #4: Verbose code - file1.ext:L60
```

---

## Color Code Reference

| Marker | Severity | Meaning |
|--------|----------|---------|
| `🔴` | CRITICAL | Block merge. Security, data loss, crash |
| `🟠` | HIGH | Should fix. Logic bugs, missing validation |
| `🟡` | MEDIUM | Fix soon. Quality, edge cases |
| `🔵` | LOW | Nice to have. Style, suggestions |
| `>>` | Line marker | Points to exact issue line |
| `← 🔴 ISSUE HERE` | Inline marker | Highlights issue in code |

---

## For Full Build (CODE_INPUT / IDEA_INPUT)

```markdown
# Final Output

## Decision: 🚀 SHIP / ⏸️ HOLD / 🛑 NO SHIP

---

## Strategic Assessment (Krishna)
- **Verdict**: PROCEED / RECONSIDER / KILL
- **ROI Assessment**: [cost vs value]
- **Key Assumptions**: [validated/challenged]
- **Alternatives Considered**: [list]

---

## Summary
What was built / analyzed

## Key Deliverables
- Features implemented
- Code produced
- Analysis completed

## Architecture
<MERMAID DIAGRAM from Vishwakarma (architect)>

## Code Review Findings
(from Bhishma - FULL OUTPUT, not summarized)
[Include complete line-by-line review]

## Test Coverage
(from Swachalit (automation))
- Tests Written: [count]
- Coverage: [percentage if available]
- Gaps: [list]

## QA Findings
(from Lakshman (qa))
- Use Cases Checked: [count]
- Use Cases Passed: [count]
- Use Cases NOT Affected: [count]
- Issues Found: [count]
- Unresolved: [list]

## Customer Impact
(from Draupadi (customer-impact) - if user-facing change)
- **Verdict**: 🔴 BREAKING / 🟠 DEGRADED / 🟡 CHANGED / 🟢 IMPROVED / ⚪ NO IMPACT
- **Users Affected**: [count/segments]
- **Migration Required**: Yes / No
- **Communication Needed**: Yes / No
- **Key Concerns**: [list]

## Risks & Improvements
(from Kripacharya (review))
- Blockers: [list]
- Recommendations: [list]

---

## Cost & ROI Summary

| Metric | Estimate | Actual |
|--------|----------|--------|
| Engineering Days | X | Y |
| Estimated Cost | $X | $Y |
| Estimated Value | $X | - |
| ROI | X% | - |

**ROI Verdict**: Worth it / Marginal / Not worth it

---

## Execution Stats
- Retry Count: [count]
- Agents Called: [list with both names]
- Steps Completed: [list]

## Final Decision

| Check | Status |
|-------|--------|
| Krishna ROI Positive | ✅ / ❌ |
| Kripacharya Approved | ✅ / ❌ |
| Critical Issues | 0 / X |
| Tests Passing | ✅ / ❌ |

**Kesh Decision**: 🚀 SHIP / ⏸️ HOLD / 🛑 NO SHIP

**Reason**: [Why this decision]

## Next Steps
[If any follow-up needed]
```

---

## SHIP / HOLD / NO SHIP Criteria

| Decision | When |
|----------|------|
| 🚀 **SHIP** | Krishna ROI positive + Kripacharya approved + No critical issues |
| ⏸️ **HOLD** | Minor issues to fix, ROI still positive |
| 🛑 **NO SHIP** | ROI negative OR critical issues OR Kripacharya rejected |

# Kesh Context Management

## Global Context Memory

Maintain this shared context object across ALL steps:

```json
{
  "input_type": "CODE_INPUT | PATCH_INPUT | IDEA_INPUT | DEFINED_INPUT",
  "user_input": "",
  "krishna_output": {
    "verdict": "PROCEED | RECONSIDER | KILL",
    "roi_assessment": {},
    "assumptions_challenged": [],
    "simpler_alternatives": [],
    "confidence": "high | medium | low"
  },
  "xray_output": {},
  "product_output": {},
  "planning_output": {},
  "architect_output": {},
  "execution_output": {},
  "test_output": {},
  "codereview_output": {},
  "qa_output": {},
  "customer_impact_output": {},
  "review_output": {},
  "iteration_count": 0,
  "current_step": 0,
  "loop_status": "IN_PROGRESS | COMPLETED | ESCALATED",
  "cost_tracking": {
    "estimated_days": 0,
    "actual_days": 0,
    "roi_percentage": 0,
    "value_estimate": ""
  },
  "final_decision": "SHIP | HOLD | NO_SHIP | null",
  "shared_knowledge": {}
}
```

---

## Shared Knowledge Base

**Purpose:** All agents receive summarized insights from previous agents (not full context, but key information).

```json
{
  "shared_knowledge": {
    "codebase_summary": {
      "tech_stack": ["typescript", "react", "postgres"],
      "red_flags": ["No input validation in auth module"],
      "architecture": "Monolithic with service layer",
      "entry_points": ["src/index.ts", "src/server.ts"]
    },
    "requirements_summary": {
      "goal": "Add user authentication",
      "constraints": ["Must use existing DB schema"],
      "acceptance_criteria": ["Login works", "Session persists"],
      "out_of_scope": ["OAuth integration"]
    },
    "architecture_decisions": {
      "patterns": ["Repository pattern", "Middleware auth"],
      "interfaces": ["IAuthService", "IUserRepository"],
      "rationale": "Separation of concerns for testability"
    },
    "iteration_history": [
      {
        "iteration": 1,
        "issues_found": ["SQL injection in login"],
        "fixes_applied": ["Used parameterized query"]
      }
    ]
  }
}
```

**What each agent receives:**

| Agent | Receives from Shared Knowledge |
|-------|-------------------------------|
| Krishna (strategic) | user_input, xray_summary (if available) |
| Sarthi (planning) | krishna_verdict, codebase_summary, requirements_summary |
| Vishwakarma (architect) | krishna_verdict, codebase_summary, requirements_summary |
| Parth (execution) | ALL (codebase, requirements, architecture, history) |
| Swachalit (automation) | execution_output, codebase_summary |
| Bhishma (code-reviewer) | codebase_summary, architecture_decisions, test_output |
| Lakshman (qa) | requirements_summary (acceptance_criteria), test_output |
| Draupadi (customer-impact) | requirements_summary, execution_summary, change_description |
| Kripacharya (review) | ALL + customer_impact_output |
| Kesh (final decision) | ALL + krishna_output + cost_tracking + customer_impact |

**Rules:**
- ALWAYS update shared_knowledge after each agent completes
- Pass relevant portions to each agent
- Track iteration_history for learning from mistakes

---

## Context Passing Protocol

When delegating, include:

```markdown
## Context for [Codename] ([agent_name])

### Background
[What has been done so far]

### Input
[Specific input for this agent]

### Previous Agent Outputs
[Relevant context from prior agents]

### Expected Output
[What you need back]
```

### Context Flow Matrix

| From | To | Pass |
|------|-----|------|
| User | Krishna (strategic) | Request, xray_summary if available |
| Krishna (strategic) | All planning agents | ROI assessment, verdict, alternatives |
| Sanjaya (xray) | All | Tech stack, architecture, red flags, risks |
| Vidura (product) | Sarthi (planning) | Requirements, user stories, scope |
| Sarthi (planning) | Vishwakarma (architect) | Task breakdown, dependencies, complexity, cost estimate |
| Vishwakarma (architect) | Parth (execution) | Architecture diagram, interfaces, contracts |
| Parth (execution) | Swachalit (automation) | Files changed, implementation summary, test hints |
| Swachalit (automation) | Bhishma (code-reviewer) | Test files, coverage report |
| Parth (execution) | Bhishma (code-reviewer) | Files changed, implementation summary |
| Bhishma (code-reviewer) | Lakshman (qa) | Code review findings, files reviewed |
| Lakshman (qa) | Parth (execution) | Issues found, reproduction steps |
| Lakshman (qa) | Draupadi (customer-impact) | QA summary, affected features |
| Execution loop | Draupadi (customer-impact) | Change summary, affected endpoints/features |
| Draupadi (customer-impact) | Kripacharya (review) | Customer impact assessment, migration needs |
| All | Kripacharya (review) | All outputs for final validation |
| All | Kesh (final decision) | All outputs + ROI + customer impact for SHIP/NO SHIP |

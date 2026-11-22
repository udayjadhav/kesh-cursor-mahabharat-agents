---
name: ai-engineering
description: Production LLM patterns — structured outputs, tools, streaming, evals, fallbacks, prompt injection, cost/latency. HTTP 200 ≠ correctness. Load with ai-product-engineer.
---

# AI Engineering Skill

## When to use

LLM features, tool calling, streaming UX, eval harnesses, model fallbacks, prompt safety.

## Principles

- Structured outputs validated before side effects  
- Eval datasets + rubrics sized to risk  
- Fallbacks and human-in-the-loop for high-impact actions  
- Prompt-injection and data-exfiltration considered  
- Measure latency/cost; UNKNOWN if not measured  
- Local-first: do not upload proprietary data without approval  

## Anti-patterns

- Shipping on a single demo transcript  
- Unbounded tool access  
- Logging raw prompts with secrets/PHI  
- Silent model swaps without eval regression  

## Verification checklist

- [ ] Eval plan exists; results RUN or NOT RUN  
- [ ] Fallback paths specified  
- [ ] Safety review for CRITICAL AI  

## References

Agent `ai-product-engineer`.

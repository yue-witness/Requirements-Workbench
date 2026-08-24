# RequestBridge - TraceGuard Audit

**Decision state:** `abstain`

## Summary

- Exact source spans resolved: 18
- Errors: 0
- Warnings: 1
- Abstentions awaiting named approval: 2

## Findings

- **WARNING TG-EVIDENCE-MISSING**: QR-03 has no exact source-span evidence. Affected: requirements, traceability.
- **ABSTAIN TG-APPROVAL-ABSTAIN**: BR-01 is high-impact and remains abstained until a named reviewer approves it. Affected: activity, domain-model, feasibility, lifecycle-roadmap, problem-vision-scope, requirements, use-cases, wireframe.
- **ABSTAIN TG-APPROVAL-ABSTAIN**: QR-01 is high-impact and remains abstained until a named reviewer approves it. Affected: activity, data-io, feasibility, lifecycle-roadmap, requirements, use-cases.

## Interpretation boundary

TraceGuard verifies configured evidence spans, links, terminology and approval gates. It does not prove that stakeholder statements or generated requirements are semantically correct.

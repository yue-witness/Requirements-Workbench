# Requirement quality and traceability

## Requirement types

- **Functional requirements** define behaviour. Check the required input,
  transformation or action, output, trigger, and exceptional conditions.
- **Quality requirements** define how well behaviour must operate. Common areas
  include accessibility, availability, efficiency, fault tolerance,
  maintainability, performance, privacy, reliability, robustness, scalability,
  security, and usability. Replace adjectives with measurable conditions.
- **Business requirements** define objectives, expected outcomes, policies, and
  processes the organisation expects the system to support. Do not confuse the
  business outcome with the functions proposed to achieve it.
- **Constraints and obligations** capture limits such as time, resources,
  mandated technology, standards, law, and contracts. Verify each claimed
  obligation from a supplied authoritative source.

## Writing and reviewing

Each requirement should express one obligation, use a stable identifier, name
the responsible system, use a defined binding term, and remain observable and
implementation-neutral unless the implementation is itself mandated. Record a
separate rationale, priority, evidence span, acceptance criterion, confidence,
and unresolved dependencies.

Review for ambiguity, duplication, conflict, missing boundaries, vague quality
words, compound obligations, premature design, inconsistent vocabulary, and
unverifiable outcomes. Completeness means sufficient coverage for the agreed
scope, not an assertion that no unknowns remain.

Acceptance criteria translate intent into an observable agreement. Use concrete
preconditions, action or event, expected result, and relevant thresholds or
error behaviour. Do not invent thresholds merely to make a statement testable;
record a question when the stakeholder has not supplied one.

## Traceability

Trace requirements across their lifecycle rather than only inside the analysis
phase. A useful matrix can link requirement IDs to source stakeholders or exact
spans, models, design elements, implementation work, verification or acceptance
tests, status, and approvals. Links should help answer:

- Why does this requirement exist?
- Which artefacts and tasks depend on it?
- How will completion be verified?
- What changes if it is revised or removed?
- Who is authorised to approve a high-impact decision?

Keep versions of analysis artefacts and preserve rollback points before shared
canonical data changes. TraceGuard adds evidence, consistency, impact, rollback,
and approval checks; it does not make stakeholder sign-off automatic.

## SRS quality

When requirements are assembled into a software requirements specification,
check that it is correct against supplied evidence, sufficiently complete for
scope, internally consistent, unambiguous, prioritised, verifiable, modifiable,
and traceable. Include supporting rationale, glossary, models, assumptions, and
open questions where they improve interpretation.

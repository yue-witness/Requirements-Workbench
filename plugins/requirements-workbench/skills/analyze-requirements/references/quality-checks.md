# Quality checks

Apply these checks before returning any module.

## Evidence and uncertainty

- Distinguish explicit client statements from inference and design proposals.
- Do not invent regulations, performance targets, data fields, integrations, or actors.
- Record missing information as an open question.
- Flag conflicting statements instead of resolving them silently.

## Requirement quality

- Keep each requirement atomic and testable.
- Classify each requirement as functional, quality, or business, and assign a unique stable ID.
- Give each requirement a separate rationale that explains why it exists and why it matters to the intended audience.
- Phrase requirements consistently using `The [system] must/shall [behaviour] when/unless/while [condition]` when a condition is relevant, and define whether `must` and `shall` are binding.
- Use stable IDs and consistent terminology.
- Avoid subjective terms such as "fast", "easy", "appropriate", or "user-friendly" without a measurable criterion.
- Keep design choices out of requirements unless the client explicitly mandates them.
- Trace every diagram element and use case to the scenario, an assumption, or a requirement.

These rules follow general documentation principles: clear wording for the intended audience, direct active language, rationale, implementation neutrality, ambiguity and consistency review, and unique identifiers. Project-specific minimum counts belong in `project.minimum_requirements`, not in the reusable skill.

## Cross-module consistency

- Actor names must match between the context diagram and use cases.
- Activity steps must not introduce functions absent from the requirements.
- Wireframe controls must trace to a requirement or use-case step.
- Fishbone causes are hypotheses for validation, not confirmed facts.
- Any revision that changes a shared concept must identify potentially affected modules even when only one module is regenerated.

## Human validation

The output is a draft for stakeholder review. For safety-critical, security-critical, regulated, or high-impact decisions, require qualified human review and appropriate specialist analysis.

## Inclusive review

- In guided mode, define specialist terms and explain what each artefact helps the user check.
- Do not confuse lack of professional terminology with lack of domain knowledge.
- Prefer short, concrete questions that a stakeholder can answer from experience.
- Keep advanced details available in the generated files so professional users do not lose traceability or verification depth.

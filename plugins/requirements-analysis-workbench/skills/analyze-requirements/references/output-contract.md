# Output contract

The canonical `analysis.json` is the single source of truth. Keep top-level keys in this order for readability:

```json
{
  "project": {},
  "selected_modules": [],
  "sources": [],
  "traceguard": {},
  "plain_language_summary": "",
  "glossary": [],
  "stakeholders": [],
  "assumptions": [],
  "open_questions": [],
  "requirements": [],
  "fishbone": {},
  "context": {},
  "use_cases": [],
  "activity": {},
  "wireframe": {}
}
```

## Module names and files

| Module | Output file | Purpose |
|---|---|---|
| `requirements` | `requirements.md` | Atomic, traceable requirements specification |
| `fishbone` | `fishbone.mmd` | Root-cause categories and candidate causes |
| `context` | `context.mmd` | System boundary, external actors, and flows |
| `use-cases` | `use-cases.md` | Structured use-case descriptions |
| `activity` | `activity.mmd` | Main workflow, decisions, and exceptions |
| `wireframe` | `wireframe.html` | Low-fidelity interface review page |

Support files are always generated: `analysis.json`, `review-index.md`,
`traceability.csv`, `traceguard.md`, `traceguard.json`, and `manifest.json`.
Selecting modules controls the six module files, not these support files.

## Sources and exact evidence spans

Record supplied source text in `sources[]` with a stable `id`, optional `title`,
and exact `text`. A requirement may carry `evidence_spans[]`, or the same spans
may be grouped under `traceguard.evidence_spans[requirement_id]`. Each span must
contain `source_id` and an exact `quote`. Optional `start` and `end` offsets are
validated when supplied; TraceGuard resolves and records offsets when they are
omitted.

Use `traceguard.high_impact_ids` for decisions that must remain abstained until
`traceguard.approvals[]` contains the same `element_id`, a non-empty named
`reviewer`, and `decision: approved`. `traceguard.terminology[]` may define a
canonical term and aliases that should be flagged across modules.

## Project record

The project object contains a non-empty `name`. It may also contain:

- `scenario_summary`;
- `analysis_status`;
- `review_mode`: `guided`, `standard`, or `professional`;
- `minimum_requirements`: a non-negative integer when a project has a count gate;
- `binding_terms`: a short statement defining whether `must` and `shall` are binding.

Do not hard-code project, organisation, industry, or policy rules into the reusable plugin. Put project-specific constraints in this record.

## Requirement record

Each requirement record contains:

```json
{
  "id": "FR-01",
  "category": "functional",
  "priority": "must",
  "statement": "The system shall ...",
  "rationale": "Why the requirement exists and matters",
  "evidence": "Scenario statement, stakeholder, policy, or labelled assumption",
  "acceptance": "Given ... when ... then ...",
  "confidence": "explicit"
}
```

`evidence_spans` is optional for legacy bundles but required for a clean
TraceGuard result when a requirement is labelled explicit.

Activity steps should include `trace_ids` that refer to a known requirement or
use-case ID. Actionable wireframe components (`button`, `input`, `select`, and
`list`) must also include at least one known trace ID.

Allowed categories are `functional`, `quality`, and `business`. Use distinct ID prefixes such as `FR`, `QR`, and `BR` when that improves scanning, but preserve user-supplied IDs.

Allowed confidence values are `explicit`, `inferred`, and `proposed`. Requirements with `inferred` or `proposed` confidence must remain visibly labelled until stakeholders confirm them.

Requirement wording should follow `The [system] must/shall [perform behaviour] when/unless/while [condition]` when a condition is relevant. Keep statements direct, active, observable, and neutral about implementation. The output groups requirements by category and presents each requirement with its rationale, followed by priority, evidence, acceptance check, and confidence.

## Plain-language support

- `plain_language_summary` explains the problem, proposed system boundary, and main unknowns without specialist jargon.
- `glossary[]` records objects with `term` and `meaning` for domain or requirements terms that a first-time contributor may not know.
- Guided mode uses the same canonical facts and quality checks as professional mode; only the explanations differ.

## Diagram data

- Fishbone: `problem` and `categories[]`, where each category has a `name` and `causes[]`.
- Context: `system`, `actors[]`, and `flows[]` with `from`, `to`, and `label`.
- Activity: `title`, `start`, `steps[]`, and optional decision nodes. Each step has `id`, `label`, and `next`; a decision also has `condition`, `yes`, and `no`.
- Wireframe: `title`, `screens[]`, and components. Supported component kinds are `heading`, `text`, `input`, `select`, `button`, `list`, and `note`. An `input` is multiline by default; set `input_type` to `text`, `email`, `tel`, `url`, `number`, `date`, or `time` when native single-line semantics are more appropriate. Add `trace_ids[]` to connect a component to requirement or use-case IDs.

## Use-case record

Each use case contains `id`, `name`, `primary_actor`, `goal`, `stakeholders`, `preconditions`, `trigger`, `main_flow`, `alternatives`, `exceptions`, `postconditions`, `business_rules`, and `related_requirements`.

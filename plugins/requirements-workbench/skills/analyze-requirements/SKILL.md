---
name: analyze-requirements
description: Turn a software idea, problem statement, user story collection, or natural-language scenario into a selected set of clear requirements artefacts. Use for both guided first-time analysis and professional requirements modelling; do not use this skill for an isolated revision of an existing module.
---

# Analyse Requirements

Turn informal software ideas into traceable review artefacts without assuming the user knows requirements-engineering terminology.

## Choose the level of guidance

Infer the lightest suitable mode from the request, or ask once if the choice materially changes the interaction:

- `guided`: explain each module in plain language, use short questions, and include a reviewer checklist;
- `standard`: provide concise explanations and normal analyst detail;
- `professional`: preserve supplied terminology and emphasise schemas, traceability, verification, and change impact.

Never reduce output quality in guided mode. Change the explanation, not the rigour.

## Inputs

Collect or infer only what the user has actually supplied:

1. A software idea, problem statement, scenario, user stories, meeting notes, or draft requirements.
2. One or more selected modules from:
   - `requirements`
   - `fishbone`
   - `context`
   - `use-cases`
   - `activity`
   - `wireframe`
3. An optional review mode: `guided`, `standard`, or `professional`.
4. An output directory. Default to `requirements-analysis-output/` in the active workspace.

If no modules are selected, present friendly descriptions: requirements (what the software must do and why), fishbone (possible causes of the problem), context (what is inside and outside the system), use cases (how people achieve goals), activity (workflow and decisions), and wireframe (a low-fidelity screen concept). Ask the user to select one or more; do not silently generate every module.

## Analysis workflow

1. Read the supplied material and separate explicit statements, assumptions, proposals, conflicts, and open questions.
2. Identify stakeholders, goals, system boundary, external systems, business rules, data, constraints, quality attributes, ambiguities, conflicts, and open questions.
3. Write atomic requirement candidates with stable IDs. Follow `references/output-contract.md`. Each requirement contains:
   - statement;
   - category (`functional`, `quality`, or `business`);
   - rationale;
   - priority;
   - evidence or source;
   - acceptance criterion;
   - confidence (`explicit`, `inferred`, or `proposed`).
4. Phrase each requirement as `The [system] must/shall [behaviour] when/unless/while [condition]` when a condition is relevant. State whether `must` and `shall` are binding. Avoid vague words and implementation assumptions.
5. Never present an inferred or proposed detail as a confirmed stakeholder requirement.
6. Create one canonical JSON file that follows `references/output-contract.md`.
7. Resolve the plugin root (the directory containing `.codex-plugin/`) and run
   `scripts/materialize_analysis.py` from that directory to create only the
   modules selected by the user.
8. Review every generated file for consistency with the canonical JSON and report unresolved questions in language suitable for the chosen review mode.

## Commands

From the plugin root, materialise all modules listed in the analysis:

```powershell
python scripts/materialize_analysis.py assets/demo_analysis.json --out demo-output
```

Use the Python executable available in the active workspace. The script uses
only the Python standard library. In addition to the selected module files, it
creates `analysis.json`, `manifest.json`, `review-index.md`, and
`traceability.csv` as supporting review files.

## References and quality boundary

Read `references/output-contract.md` before creating canonical JSON and `references/quality-checks.md` before finalising. The workbench supports elicitation and modelling; it does not replace stakeholder validation, domain review, safety analysis, legal review, or formal verification.

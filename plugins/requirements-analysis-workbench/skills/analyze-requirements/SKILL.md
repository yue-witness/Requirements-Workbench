---
name: analyze-requirements
description: Turn a software idea, problem statement, user story collection, or natural-language scenario into a selected set of clear requirements artefacts. Use for both guided first-time analysis and professional requirements modelling; do not use this skill for an isolated revision of an existing module.
---

# Analyse Requirements

Turn informal software ideas into traceable review artefacts without assuming the user knows requirements-engineering terminology.

## Visual configuration

When the user directly invokes Requirements Analysis Workbench (an
`@`-mention, a slash command such as `/analyze-requirements`, or by naming the
workbench) and supplies a matching software idea, problem statement, scenario,
user-story collection, meeting note, or requirements draft, call
`open_workbench` before analysis by default. Do the same when the user asks for
a GUI, visual selector, mode choice, or module switches.

Opening the workbench is a hard interaction gate:

1. `open_workbench` returns `state=awaiting_user_selection`, never a default
   selection.
2. After calling it, end the current turn immediately. Do not read analysis
   references, inspect project materials, create directories, draft canonical
   JSON, run scripts, or generate any module in that turn.
3. Resume only in a later user turn after the workbench submission has called
   `save_workbench_selection` and supplied `confirmed=true`, a valid mode, and at
   least one selected module. Never infer confirmation from the values initially
   displayed in the form.

Skip the automatic GUI only when the user explicitly asks not to open it **and**
provides both a mode and at least one module. Hosts that cannot render MCP Apps
(for example terminal agents and most IDE agents) still return the blocking
`open_workbench` result; treat it as the cue to use the fallback. If a native
structured user-input tool is available (such as `AskUserQuestion` in Claude
Code), use it as the first fallback because it waits for a response.
Otherwise, present the same three modes and eleven modules in conversation and end
the turn with a direct selection question. Do not begin analysis in the fallback
path until the user replies with an explicit selection.

Treat the confirmed saved selection as the source of truth for
`project.review_mode` and `selected_modules`.

## Locate the tools

Work in whichever host loaded this skill (Codex, ChatGPT, Claude Code, Claude
Desktop, Antigravity, DeepSeek Harness, Gemini CLI, Cursor, VS Code, Windsurf, or another
Agent Skills or MCP host):

- Prefer the `materialize_analysis`, `traceguard_audit`, and
  `traceguard_impact` MCP tools when the `requirements_analysis_workbench`
  server is connected. They run the bundled scripts with the same validation,
  so you never need to locate them.
- Otherwise run the scripts from the plugin root: the directory that contains
  `scripts/materialize_analysis.py` (it also holds `mcp/` and `ui/`). For a
  skill installed on its own by `scripts/install_agent.py`, the
  `plugin-root.txt` file beside this `SKILL.md` records that directory.
- Use the Python executable available in the active workspace (`python`,
  `python3`, or `py -3`).

## Choose the level of guidance

Use the explicitly confirmed mode from the workbench or fallback question:

- `guided`: explain each module in plain language, use short questions, and include a reviewer checklist;
- `standard`: provide concise explanations and normal analyst detail;
- `professional`: preserve supplied terminology and emphasise schemas, traceability, verification, and change impact.

Never reduce output quality in guided mode. Change the explanation, not the rigour.

## Inputs

Collect or infer only what the user has actually supplied:

1. A software idea, problem statement, scenario, user stories, meeting notes, or draft requirements.
2. One or more selected modules from:
   - `problem-vision-scope`
   - `requirements`
   - `fishbone`
   - `context`
   - `domain-model`
   - `use-cases`
   - `activity`
   - `wireframe`
   - `feasibility`
   - `data-io`
   - `lifecycle-roadmap`
3. An optional review mode: `guided`, `standard`, or `professional`.
4. An output directory. Default to `requirements-analysis-output/` in the active workspace.

If no modules are confirmed, present friendly descriptions: problem, vision and
scope (why change is needed and what is included), requirements (what the
software must do and why), fishbone (possible causes), context (what is inside
and outside), domain model (important concepts and relationships), use cases
(how people achieve goals), activity (workflow and decisions), wireframe (a
low-fidelity screen concept), feasibility (whether the proposal is viable and
under what conditions), data I/O (owned data, inputs, checks, and outputs), and
lifecycle roadmap (delivery approach, trade-offs, milestones, and backlog). Ask
the user to select one or more, end the turn, and wait for the reply; do not
silently generate every module.

## Analysis workflow

1. Read the supplied material and separate explicit statements, assumptions, proposals, conflicts, and open questions.
2. Read `references/knowledge-index.md`, then load only the knowledge references routed for the supplied scenario and confirmed modules. Use them as analysis heuristics, never as evidence for a project-specific claim.
3. Identify stakeholders, goals, system boundary, external systems, business rules, data, constraints, quality attributes, ambiguities, conflicts, and open questions.
4. Write atomic requirement candidates with stable IDs. Follow `references/output-contract.md`. Each requirement contains:
   - statement;
   - category (`functional`, `quality`, or `business`);
   - rationale;
   - priority;
   - evidence or source;
   - acceptance criterion;
   - confidence (`explicit`, `inferred`, or `proposed`).
   - one or more exact source-span references when source text is available.
5. Phrase each requirement as `The [system] must/shall [behaviour] when/unless/while [condition]` when a condition is relevant. State whether `must` and `shall` are binding. Avoid vague words and implementation assumptions.
6. Never present an inferred or proposed detail as a confirmed stakeholder requirement.
7. Create one canonical JSON file that follows `references/output-contract.md`.
8. Create only the modules selected by the user with the
   `materialize_analysis` MCP tool, or by running
   `scripts/materialize_analysis.py` from the plugin root (see
   *Locate the tools*).
9. Review `traceguard.md` and `traceguard.json`. Report errors, warnings, and
   abstained high-impact items; do not treat an abstained item as accepted until
   a named reviewer is recorded.
10. Review every generated file for consistency with the canonical JSON and report unresolved questions in language suitable for the chosen review mode.

## Commands

With the MCP server connected, call `materialize_analysis` with absolute
`analysis_path` and `output_dir` values. Without it, from the plugin root,
materialise all modules listed in the analysis:

```powershell
python scripts/materialize_analysis.py assets/demo_analysis.json --out demo-output
```

The script uses only the Python standard library. In addition to the selected
module files, it creates `analysis.json`, `manifest.json`, `review-index.md`,
`traceability.csv`, `traceguard.md`, and `traceguard.json` as supporting review
files.

## References and quality boundary

After a valid selection is confirmed, use `references/knowledge-index.md` to
route domain-method guidance without loading unrelated references. Read
`references/output-contract.md` before creating canonical JSON and
`references/quality-checks.md` before finalising. The workbench supports
elicitation and modelling; it does not replace stakeholder validation, domain
review, safety analysis, legal review, or formal verification.

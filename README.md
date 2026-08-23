# Requirements Analysis Workbench

[简体中文](README.zh-CN.md) | English

Requirements Analysis Workbench is a plugin for ChatGPT and Codex that turns software ideas, problem statements, user stories, meeting notes, or draft requirements into selectable, traceable review artefacts. It combines three skills, deterministic Python tools, and an MCP Apps visual configuration panel.

It supports first-time contributors with plain-language guidance and experienced analysts with evidence, confidence, acceptance, traceability, and change-scope controls. The plugin is domain-neutral, with project-specific constraints supplied as project data.

## What it produces

Choose one or more independent modules:

- `requirements`: atomic functional, quality, and business requirements;
- `fishbone`: possible causes behind the stated problem;
- `context`: the system boundary, actors, external systems, and flows;
- `use-cases`: actor goals, main flows, alternatives, and exceptions;
- `activity`: workflow decisions, failure paths, and outcomes;
- `wireframe`: accessible low-fidelity HTML screens with trace labels.

Every run also creates a canonical `analysis.json`, a reviewer-oriented `review-index.md`, `traceability.csv`, `traceguard.md`, `traceguard.json`, and a SHA-256 `manifest.json`.

## Key behaviours

- When the plugin is directly `@`-mentioned with a matching requirements description, it opens the visual workbench by default so the user can confirm the review mode and output modules. Users can explicitly decline the GUI, and hosts without MCP Apps support fall back to the same choices in conversation.
- A visual Guided, Standard, and Professional mode selector.
- Independent checkboxes for all six output modules.
- Explicit separation of stakeholder evidence, inference, assumptions, proposals, conflicts, and open questions.
- Stable IDs and trace links across generated artefacts.
- Deterministic validation before files are materialised.
- Targeted revision of one module with byte-for-byte hash checks for non-target modules.
- TraceGuard exact source spans, actor/context checks, activity and wireframe traces, terminology checks, and machine-readable findings.
- Shared-change impact previews with propagate, local-override, and cancel choices.
- Rollback snapshots and named-approval abstention gates for configured high-impact items.
- No API key or third-party Python package is required by the deterministic materialiser or local MCP server.

For example, `project.minimum_requirements` is optional and defaults to no count gate; the reusable plugin does not impose an organisation- or industry-wide minimum.

## Install from GitHub

Use a current ChatGPT desktop/Codex installation that supports plugins. Add this repository as a marketplace source:

```powershell
codex plugin marketplace add yue-witness/Requirements-Workbench --ref v0.3.1
```

Restart the desktop app, open the Plugins Directory, select the **Requirements Analysis Workbench** source, and install or enable `requirements-analysis-workbench`. Start a new task after installation so the three bundled skills and MCP tools are loaded.

To follow the latest `main` branch instead of a tagged release, omit `--ref v0.3.1`.

## Install from the release package

Download `requirements-analysis-workbench-v0.3.1.zip` from the GitHub Release and extract it. Add the extracted marketplace root:

```powershell
codex plugin marketplace add C:\path\to\requirements-analysis-workbench-v0.3.1
```

Then restart the desktop app and install the plugin from the Plugins Directory.

## Try it

Guided analysis:

> I have a software idea but I am new to requirements analysis. Explain the available outputs, help me identify missing information, and generate requirements, context, use cases, and a wireframe.

Visual configuration:

> Open the visual requirements workbench so I can choose a mode and switch modules on or off.

Direct plugin invocation also opens the workbench by default when the request includes a matching requirements description:

> @Requirements Analysis Workbench Analyse these stakeholder notes for a booking system.

Professional analysis:

> Analyse these stakeholder notes in professional mode. Generate all six modules, preserve supplied terminology, label inference, and include acceptance checks and traceability.

Targeted revision:

> Revise only the activity module to add a rejected-request path. Do not rewrite any other module file.

TraceGuard impact preview:

> Preview the effect of changing FR-01, but do not propagate the change until I confirm.

## Run the deterministic demo

Python 3.10 or later is recommended. From the repository root:

```powershell
python plugins/requirements-analysis-workbench/scripts/materialize_analysis.py `
  plugins/requirements-analysis-workbench/assets/demo_analysis.json `
  --out demo-output

python plugins/requirements-analysis-workbench/scripts/traceguard.py audit `
  plugins/requirements-analysis-workbench/assets/demo_analysis.json `
  --out demo-output
```

The materialiser itself uses only the Python standard library and does not make network calls. Model-assisted analysis still occurs inside the host ChatGPT or Codex product.

## Validate and package

```powershell
python -m unittest discover -s plugins/requirements-analysis-workbench/tests -v
python scripts/package_release.py
```

Maintainers can additionally run the official Plugin Creator and Skill Creator validators. Those external validators require PyYAML in the Python environment used to run them.

## Repository layout

```text
.
|-- .agents/plugins/marketplace.json
|-- plugins/requirements-analysis-workbench/
|   |-- .codex-plugin/plugin.json
|   |-- .mcp.json
|   |-- mcp/server.py
|   |-- ui/workbench.html
|   |-- skills/
|   |-- scripts/
|   |-- assets/
|   |-- examples/requestbridge-demo/
|   `-- tests/
|-- scripts/package_release.py
|-- CHANGELOG.md
`-- LICENSE
```

## Limitations and privacy

Outputs are structured first drafts, not formal verification or a substitute for stakeholder, domain, security, privacy, legal, safety, or regulatory review. Review source material before submitting it to any model, minimise personal or sensitive data, and keep accountable people responsible for consequential decisions.

## License

[MIT](LICENSE)

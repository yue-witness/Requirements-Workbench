# Requirements Workbench

[简体中文](README.zh-CN.md) | English

Requirements Workbench is a skills-only plugin for ChatGPT and Codex that turns software ideas, problem statements, user stories, meeting notes, or draft requirements into selectable, traceable review artefacts.

It supports first-time contributors with plain-language guidance and experienced analysts with evidence, confidence, acceptance, traceability, and change-scope controls. The plugin is domain-neutral, with project-specific constraints supplied as project data.

## What it produces

Choose one or more independent modules:

- `requirements`: atomic functional, quality, and business requirements;
- `fishbone`: possible causes behind the stated problem;
- `context`: the system boundary, actors, external systems, and flows;
- `use-cases`: actor goals, main flows, alternatives, and exceptions;
- `activity`: workflow decisions, failure paths, and outcomes;
- `wireframe`: accessible low-fidelity HTML screens with trace labels.

Every run also creates a canonical `analysis.json`, a reviewer-oriented `review-index.md`, `traceability.csv`, and a SHA-256 `manifest.json`.

## Key behaviours

- Guided, standard, and professional review modes.
- Explicit separation of stakeholder evidence, inference, assumptions, proposals, conflicts, and open questions.
- Stable IDs and trace links across generated artefacts.
- Deterministic validation before files are materialised.
- Targeted revision of one module with byte-for-byte hash checks for non-target modules.
- Human confirmation boundary for safety-critical, regulated, or high-impact conclusions.
- No API key, MCP server, or third-party Python package is required by the deterministic materialiser.

For example, `project.minimum_requirements` is optional and defaults to no count gate; the reusable plugin does not impose an organisation- or industry-wide minimum.

## Install from GitHub

Use a current ChatGPT desktop/Codex installation that supports plugins. Add this repository as a marketplace source:

```powershell
codex plugin marketplace add yue-witness/Requirements-Workbench --ref v0.2.0
```

Restart the desktop app, open the Plugins Directory, select the **Requirements Workbench** source, and install or enable `requirements-workbench`. Start a new task after installation so the two bundled skills are loaded.

To follow the latest `main` branch instead of a tagged release, omit `--ref v0.2.0`.

## Install from the release package

Download `requirements-workbench-v0.2.0.zip` from the GitHub Release and extract it. Add the extracted marketplace root:

```powershell
codex plugin marketplace add C:\path\to\requirements-workbench-v0.2.0
```

Then restart the desktop app and install the plugin from the Plugins Directory.

## Try it

Guided analysis:

> I have a software idea but I am new to requirements analysis. Explain the available outputs, help me identify missing information, and generate requirements, context, use cases, and a wireframe.

Professional analysis:

> Analyse these stakeholder notes in professional mode. Generate all six modules, preserve supplied terminology, label inference, and include acceptance checks and traceability.

Targeted revision:

> Revise only the activity module to add a rejected-request path. Do not rewrite any other module file.

## Run the deterministic demo

Python 3.10 or later is recommended. From the repository root:

```powershell
python plugins/requirements-workbench/scripts/materialize_analysis.py `
  plugins/requirements-workbench/assets/demo_analysis.json `
  --out demo-output
```

The materialiser itself uses only the Python standard library and does not make network calls. Model-assisted analysis still occurs inside the host ChatGPT or Codex product.

## Validate and package

```powershell
python -m unittest discover -s plugins/requirements-workbench/tests -v
python scripts/package_release.py
```

Maintainers can additionally run the official Plugin Creator and Skill Creator validators. Those external validators require PyYAML in the Python environment used to run them.

## Repository layout

```text
.
|-- .agents/plugins/marketplace.json
|-- plugins/requirements-workbench/
|   |-- .codex-plugin/plugin.json
|   |-- skills/
|   |-- scripts/materialize_analysis.py
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

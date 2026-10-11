# Requirements Analysis Workbench plugin

[简体中文](README.zh-CN.md) | English

This folder is the installable `requirements-analysis-workbench` plugin. It bundles three skills and a dependency-free MCP Apps UI:

- `analyze-requirements` creates a user-selected set of requirements-analysis artefacts;
- `revise-requirements-module` changes one existing module while preserving other module files.
- `traceguard-audit` audits evidence spans, cross-artefact invariants, change impact, rollback, and approval gates.

The visual workbench distinguishes Guided, Standard, and Professional modes and provides an independent checkbox for eleven modules: `problem-vision-scope`, `requirements`, `fishbone`, `context`, `domain-model`, `use-cases`, `activity`, `wireframe`, `feasibility`, `data-io`, and `lifecycle-roadmap`. Supporting files include canonical `analysis.json`, `review-index.md`, `traceability.csv`, `traceguard.md`, `traceguard.json`, and `manifest.json`.

The analysis skill also includes a progressively loaded requirements-engineering knowledge base. After the user confirms the GUI selection, it routes only the relevant guidance for problem framing and domain models, requirement quality and traceability, stakeholder and behavioural models, or delivery planning and handoff. This method knowledge guides analysis but is never treated as evidence about the user's project.

When a user directly `@`-mentions the plugin and supplies a matching requirements description, the `analyze-requirements` skill opens this workbench before analysis by default. Opening the panel does not accept its displayed defaults: analysis remains blocked until the user presses **Apply selection** and the server confirms the saved mode and modules. An explicit request not to open the GUI is respected only when the request already includes a mode and at least one module; incompatible hosts fall back to a blocking structured or conversational selection.

## Hosts

The same folder installs into several hosts: `.codex-plugin/` for ChatGPT and Codex, `.claude-plugin/` for Claude Code, and `gemini-extension.json` for Gemini CLI. For Antigravity, Cursor, VS Code, Windsurf, Claude Desktop, or any other MCP host, run `scripts/install_agent.py --target <host>`. Besides the visual selector, the MCP server publishes the skills as prompts and exposes `get_workflow_instructions`, `read_workflow_reference`, `materialize_analysis`, `traceguard_audit`, and `traceguard_impact`, so hosts without Agent Skills support run the same workflow.

In Claude Code:

```text
/plugin install requirements-analysis-workbench --marketplace yue-witness/Requirements-Workbench
```

## Deterministic demo

From this plugin folder:

```powershell
python scripts/materialize_analysis.py assets/demo_analysis.json --out demo-output
python scripts/traceguard.py audit assets/demo_analysis.json --out demo-output
python -m unittest discover -s tests -v
```

The materialiser uses only the Python standard library. `project.minimum_requirements` is optional and defaults to no count gate, so project, organisation, industry, or policy rules are not hard-coded into the reusable plugin.

For installation, release packaging, limitations, and licensing, see the [repository README](../../README.md).

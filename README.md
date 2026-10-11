# Requirements Analysis Workbench (Useful for Deakin Students)

[简体中文](README.zh-CN.md) | English

Requirements Analysis Workbench is a plugin for ChatGPT, Codex, and Claude Code, and also runs in Google Antigravity, Gemini CLI, Cursor, VS Code, Windsurf, Claude Desktop, and any other host that supports MCP servers or Agent Skills. It turns software ideas, problem statements, user stories, meeting notes, or draft requirements into selectable, traceable review artefacts. It combines three skills, deterministic Python tools, and an MCP server with an MCP Apps visual configuration panel.

It supports first-time contributors with plain-language guidance and experienced analysts with evidence, confidence, acceptance, traceability, and change-scope controls. The plugin is domain-neutral, with project-specific constraints supplied as project data.

## What it produces

Choose one or more independent modules:

- `problem-vision-scope`: problem, desired future state, objectives, scope boundaries, and constraints;
- `requirements`: atomic functional, quality, and business requirements;
- `fishbone`: possible causes behind the stated problem;
- `context`: the system boundary, actors, external systems, and flows;
- `domain-model`: domain concepts, attributes, relationships, and multiplicities;
- `use-cases`: actor goals, main flows, alternatives, and exceptions;
- `activity`: workflow decisions, failure paths, and outcomes;
- `wireframe`: accessible low-fidelity HTML screens with trace labels;
- `feasibility`: evidence-based viability, risks, costs, benefits, and conditions;
- `data-io`: data ownership, input verification and validation, outputs, privacy, and accessibility;
- `lifecycle-roadmap`: delivery approach, trade-offs, milestones, dependencies, and backlog.

Every run also creates a canonical `analysis.json`, a reviewer-oriented `review-index.md`, `traceability.csv`, `traceguard.md`, `traceguard.json`, and a SHA-256 `manifest.json`.

## Key behaviours

- When the plugin is directly `@`-mentioned with a matching requirements description, it opens the visual workbench by default so the user can confirm the review mode and output modules. Opening the panel does not accept its displayed defaults: the workflow remains blocked until the user applies a valid selection. Users can explicitly decline the GUI only when they already provide a mode and at least one module; hosts without MCP Apps support fall back to the same blocking choices in conversation.
- A visual Guided, Standard, and Professional mode selector.
- Independent checkboxes for all eleven output modules.
- Explicit separation of stakeholder evidence, inference, assumptions, proposals, conflicts, and open questions.
- Stable IDs and trace links across generated artefacts.
- Deterministic validation before files are materialised.
- Targeted revision of one module with byte-for-byte hash checks for non-target modules.
- TraceGuard exact source spans, actor/context checks, activity and wireframe traces, terminology checks, and machine-readable findings.
- Shared-change impact previews with propagate, local-override, and cancel choices.
- Rollback snapshots and named-approval abstention gates for configured high-impact items.
- No API key or third-party Python package is required by the deterministic materialiser or local MCP server.

For example, `project.minimum_requirements` is optional and defaults to no count gate; the reusable plugin does not impose an organisation- or industry-wide minimum.

## Supported hosts

| Host | Install route | Skills | Visual panel |
|---|---|---|---|
| ChatGPT desktop / Codex | Codex plugin marketplace | Yes | Yes (MCP Apps) |
| Claude Code | Claude Code plugin marketplace | Yes | Conversational fallback (`AskUserQuestion`) |
| Google Antigravity | `install_agent.py --target antigravity` | Yes | Conversational fallback |
| Gemini CLI | `gemini extensions install` or `install_agent.py --target gemini-cli` | Yes | Conversational fallback |
| Cursor, VS Code (Copilot), Windsurf | `install_agent.py --target cursor`, `vscode`, or `windsurf` | Yes where the host reads Agent Skills | Conversational fallback |
| Claude Desktop | `install_agent.py --target claude-desktop` | As MCP prompts | Yes where MCP Apps are enabled |
| Any other MCP host | `install_agent.py --target generic --print` | As MCP prompts | Depends on the host |

Every host gets the same workflow. The MCP server publishes the three skills as MCP prompts (`analyze-requirements`, `revise-requirements-module`, `traceguard-audit`) and as `get_workflow_instructions`, and runs generation and TraceGuard through the `materialize_analysis`, `traceguard_audit`, and `traceguard_impact` tools, so hosts without Agent Skills support still follow the full process. Hosts that cannot render the visual panel ask for the mode and modules in conversation and wait for an explicit answer.

All routes need Python 3.10 or later on the machine; no third-party package or API key is required.

## Install in ChatGPT desktop or Codex

Use a current ChatGPT desktop/Codex installation that supports plugins. Add this repository as a marketplace source:

```powershell
codex plugin marketplace add yue-witness/Requirements-Workbench --ref v0.5.0
```

Restart the desktop app, open the Plugins Directory, select the **Requirements Analysis Workbench** source, and install or enable `requirements-analysis-workbench`. Start a new task after installation so the three bundled skills and MCP tools are loaded.

To follow the latest `main` branch instead of a tagged release, omit `--ref v0.5.0`.

## Install in Claude Code

Inside Claude Code:

```text
/plugin marketplace add yue-witness/Requirements-Workbench
/plugin install requirements-analysis-workbench@requirements-analysis-workbench
```

Or install in one step on Claude Code 2.1.275 or later:

```text
/plugin install requirements-analysis-workbench --marketplace yue-witness/Requirements-Workbench
```

Restart Claude Code. The skills appear as `/requirements-analysis-workbench:analyze-requirements`, `/requirements-analysis-workbench:revise-requirements-module`, and `/requirements-analysis-workbench:traceguard-audit`, and Claude also selects them automatically from matching requests. The plugin starts its MCP server with `python`; if your machine only provides `python3`, edit `plugins/requirements-analysis-workbench/.claude-plugin/plugin.json` in your copy or use the installer route below.

## Install in Antigravity, Gemini CLI, Cursor, VS Code, Windsurf, or Claude Desktop

Clone the repository (or extract the release ZIP) to a folder you will keep, then run the installer with the Python you want the host to use:

```powershell
git clone https://github.com/yue-witness/Requirements-Workbench.git
cd Requirements-Workbench
python plugins/requirements-analysis-workbench/scripts/install_agent.py --target antigravity
```

Replace `antigravity` with `gemini-cli`, `cursor`, `vscode`, `windsurf`, `claude-desktop`, `claude-code`, or `generic`. The installer:

- merges a `requirements_analysis_workbench` entry into the host's MCP configuration, keeping every other server and saving a `.bak` copy first;
- copies the three skills into the host's skills folder and records the plugin location in `plugin-root.txt` beside each `SKILL.md`;
- uses the absolute path of the Python that ran it, so GUI hosts that do not inherit your shell `PATH` still start the server.

| Target | User scope (default) | `--scope workspace` |
|---|---|---|
| `antigravity` | `~/.gemini/antigravity/mcp_config.json`, `~/.gemini/antigravity/skills/` | `.agents/skills/` (MCP stays global) |
| `gemini-cli` | `~/.gemini/settings.json`, `~/.gemini/skills/` | `.gemini/settings.json`, `.gemini/skills/` |
| `cursor` | `~/.cursor/mcp.json`, `~/.cursor/skills/` | `.cursor/mcp.json`, `.cursor/skills/` |
| `vscode` | — | `.vscode/mcp.json`, `.github/skills/` |
| `windsurf` | `~/.codeium/windsurf/mcp_config.json` | `.windsurf/skills/` |
| `claude-desktop` | `claude_desktop_config.json` in the Claude app data folder | — |
| `claude-code` | `~/.claude/skills/` and a printed `claude mcp add` command | `.mcp.json`, `.claude/skills/` |

Useful options: `--print` shows the JSON snippet without writing anything, `--dry-run` lists planned changes, `--config PATH` and `--skills-dir PATH` target any other host or a newer config location, `--no-skills` or `--no-mcp` installs one half only, and `--uninstall` removes exactly what the installer added. Restart the host afterwards.

For Gemini CLI you can alternatively install the bundled extension, which loads the MCP server and skills together:

```powershell
gemini extensions install ./plugins/requirements-analysis-workbench
```

For any other MCP-capable tool, run `install_agent.py --target generic --print` and paste the snippet into that tool's MCP settings, then point its skills or rules folder (if any) at `plugins/requirements-analysis-workbench/skills/` with `--skills-dir`.

## Install from the release package

Download `requirements-analysis-workbench-v0.5.0.zip` from the GitHub Release and extract it. For Codex, add the extracted marketplace root:

```powershell
codex plugin marketplace add C:\path\to\requirements-analysis-workbench-v0.5.0
```

Then restart the desktop app and install the plugin from the Plugins Directory. For Claude Code, run `/plugin marketplace add C:\path\to\requirements-analysis-workbench-v0.5.0`; for other hosts, run `install_agent.py` from the extracted folder as shown above.

## Try it

Guided analysis:

> I have a software idea but I am new to requirements analysis. Explain the available outputs, help me identify missing information, and generate requirements, context, use cases, and a wireframe.

Visual configuration:

> Open the visual requirements workbench so I can choose a mode and switch modules on or off.

Direct plugin invocation also opens the workbench by default when the request includes a matching requirements description:

> @Requirements Analysis Workbench Analyse these stakeholder notes for a booking system.

In Claude Code you can also type `/requirements-analysis-workbench:analyze-requirements` followed by the notes; in hosts that list MCP prompts (Gemini CLI, Claude Desktop, and others), choose the `analyze-requirements` prompt.

Professional analysis:

> Analyse these stakeholder notes in professional mode. Generate all eleven modules, preserve supplied terminology, label inference, and include acceptance checks and traceability.

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

The materialiser itself uses only the Python standard library and does not make network calls. Model-assisted analysis still occurs inside the host AI product.

## Validate and package

```powershell
python -m unittest discover -s plugins/requirements-analysis-workbench/tests -v
python scripts/package_release.py
```

Maintainers can additionally run `claude plugin validate .` and the official Plugin Creator and Skill Creator validators. Those external validators require PyYAML in the Python environment used to run them.

## Repository layout

```text
.
|-- .agents/plugins/marketplace.json      # Codex marketplace
|-- .claude-plugin/marketplace.json       # Claude Code marketplace
|-- plugins/requirements-analysis-workbench/
|   |-- .codex-plugin/plugin.json
|   |-- .claude-plugin/plugin.json
|   |-- gemini-extension.json
|   |-- .mcp.json
|   |-- mcp/server.py                     # MCP tools, prompts, and UI for every host
|   |-- ui/workbench.html
|   |-- skills/
|   |-- scripts/                          # materialiser, TraceGuard, install_agent.py
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

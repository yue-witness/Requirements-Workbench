# Changelog

All notable changes to Requirements Analysis Workbench are documented here.

## [0.5.0] - 2026-10-11

### Added

- Claude Code support: a `.claude-plugin/plugin.json` plugin manifest and a repository `.claude-plugin/marketplace.json`, with the MCP server started from `${CLAUDE_PLUGIN_ROOT}`.
- Gemini CLI support through a bundled `gemini-extension.json`.
- `scripts/install_agent.py`, which merges the MCP server into Google Antigravity, Gemini CLI, Cursor, VS Code, Windsurf, Claude Desktop, Claude Code, or any MCP host configuration and copies the skills into the host's skills folder, with backups, dry runs, and uninstall.
- MCP prompts and `workbench://skills/` resources for the three workflows, plus `get_workflow_instructions` and `read_workflow_reference` tools for hosts without Agent Skills support.
- `materialize_analysis`, `traceguard_audit`, and `traceguard_impact` MCP tools that run the bundled scripts in-process, so agents no longer need to locate the plugin folder.
- Tests for the new MCP features, the installer, and version consistency across every host manifest.

### Changed

- The skills now describe a host-neutral route: prefer the MCP tools, otherwise locate the plugin root by `scripts/materialize_analysis.py` or the installer's `plugin-root.txt`, and use a host's structured question tool (such as Claude Code's `AskUserQuestion`) when the visual panel cannot render.

## [0.4.0] - 2026-08-24

### Added

- Added independently selectable `problem-vision-scope`, `domain-model`, `feasibility`, `data-io`, and `lifecycle-roadmap` modules.
- Added deterministic validation, renderers, traceability links, targeted-revision coverage, canonical demo data, and GUI switches for all eleven modules.
- Added routed output contracts and quality checks for scope, domain concepts, feasibility evidence, data verification and validation, lifecycle trade-offs, milestones, and backlog dependencies.

## [0.3.2] - 2026-08-23

### Fixed

- Made MCP stdio explicitly UTF-8 and serialized responses as ASCII-safe JSON so the visual workbench loads under legacy Windows code pages.
- Added regression coverage for Unicode round-tripping and UI resource serialization.

### Changed

- Opening the workbench now leaves analysis blocked until the user explicitly applies a valid mode and at least one output module.
- Updated the MCP Apps bridge, intrinsic-size notification, and responsive selector layout.

## [0.3.1] - 2026-08-23

### Changed

- Direct `@` invocation with a matching requirements description now opens the visual workbench before analysis by default.
- An explicit no-GUI request bypasses the visual panel, while incompatible hosts retain the conversational fallback.

## [0.3.0] - 2026-08-23

### Added

- Native MCP Apps visual selector for Guided, Standard, and Professional modes.
- Independent checkboxes for all six requirements-analysis modules.
- TraceGuard exact source-span validation and cross-artefact invariants.
- Change-impact previews with propagate, local-override, and cancel choices.
- Canonical-analysis rollback snapshots for targeted revisions.
- Abstention gates that require named approval for configured high-impact items.
- A dedicated `traceguard-audit` skill and protocol-level GUI tests.

### Changed

- Renamed the plugin and normalized identifier to Requirements Analysis Workbench / `requirements-analysis-workbench`.
- Upgraded generated bundle manifests to schema version 0.3.

## [0.2.0] - 2026-08-23

### Added

- Guided, standard, and professional requirements-analysis modes.
- Six selectable artefact modules: requirements, fishbone, context, use cases, activity, and wireframe.
- Canonical JSON analysis, review index, traceability CSV, and SHA-256 manifest.
- Independent module revision with non-target hash preservation checks.
- Deterministic validation and an eight-test regression suite.
- Generic RequestBridge example and bilingual English/Chinese documentation.
- Repository marketplace metadata and reproducible release packaging.

### Distribution boundary

- The public plugin is domain-neutral.
- Project-specific count gates are optional data fields and are not global plugin rules.

[0.2.0]: https://github.com/yue-witness/Requirements-Workbench/releases/tag/v0.2.0
[0.3.0]: https://github.com/yue-witness/Requirements-Workbench/releases/tag/v0.3.0
[0.3.1]: https://github.com/yue-witness/Requirements-Workbench/releases/tag/v0.3.1
[0.3.2]: https://github.com/yue-witness/Requirements-Workbench/releases/tag/v0.3.2
[0.4.0]: https://github.com/yue-witness/Requirements-Workbench/releases/tag/v0.4.0

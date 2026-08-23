# Changelog

All notable changes to Requirements Analysis Workbench are documented here.

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

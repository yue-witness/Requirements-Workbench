# Requirements Analysis Workbench plugin

[简体中文](README.zh-CN.md) | English

This folder is the installable `requirements-analysis-workbench` plugin. It bundles three skills and a dependency-free MCP Apps UI:

- `analyze-requirements` creates a user-selected set of requirements-analysis artefacts;
- `revise-requirements-module` changes one existing module while preserving other module files.
- `traceguard-audit` audits evidence spans, cross-artefact invariants, change impact, rollback, and approval gates.

The visual workbench distinguishes Guided, Standard, and Professional modes and provides an independent checkbox for each supported module: `requirements`, `fishbone`, `context`, `use-cases`, `activity`, and `wireframe`. Supporting files include canonical `analysis.json`, `review-index.md`, `traceability.csv`, `traceguard.md`, `traceguard.json`, and `manifest.json`.

## Deterministic demo

From this plugin folder:

```powershell
python scripts/materialize_analysis.py assets/demo_analysis.json --out demo-output
python scripts/traceguard.py audit assets/demo_analysis.json --out demo-output
python -m unittest discover -s tests -v
```

The materialiser uses only the Python standard library. `project.minimum_requirements` is optional and defaults to no count gate, so project, organisation, industry, or policy rules are not hard-coded into the reusable plugin.

For installation, release packaging, limitations, and licensing, see the [repository README](../../README.md).

# Requirements Workbench plugin

[简体中文](README.zh-CN.md) | English

This folder is the installable `requirements-workbench` plugin. It bundles two skills:

- `analyze-requirements` creates a user-selected set of requirements-analysis artefacts;
- `revise-requirements-module` changes one existing module while preserving other module files.

The supported modules are `requirements`, `fishbone`, `context`, `use-cases`, `activity`, and `wireframe`. Supporting files include canonical `analysis.json`, `review-index.md`, `traceability.csv`, and `manifest.json`.

## Deterministic demo

From this plugin folder:

```powershell
python scripts/materialize_analysis.py assets/demo_analysis.json --out demo-output
python -m unittest discover -s tests -v
```

The materialiser uses only the Python standard library. `project.minimum_requirements` is optional and defaults to no count gate, so project, organisation, industry, or policy rules are not hard-coded into the reusable plugin.

For installation, release packaging, limitations, and licensing, see the [repository README](../../README.md).

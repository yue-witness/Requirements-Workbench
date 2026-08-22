---
name: revise-requirements-module
description: Revise one existing Requirements Workbench module while preserving other generated module files. Use when the user names an existing requirements, fishbone, context, use-cases, activity, or wireframe output and asks to change only that module.
---

# Revise One Requirements Module

Apply the smallest requested change while preserving the rest of the review bundle.

## Workflow

1. Locate the existing output directory and load its `analysis.json` and `manifest.json`.
2. Confirm the target module only when the user's wording could refer to more than one module.
3. Identify whether the change is local presentation detail or a shared fact used by other modules.
4. For a local change, update only the relevant canonical data and keep existing IDs stable.
5. For a shared fact, explain the affected modules and ask whether to keep a local override or propagate the change. Do not silently make the bundle inconsistent.
6. From the plugin root, run:

```powershell
python scripts/materialize_analysis.py analysis.json --out requirements-analysis-output --only activity
```

7. Confirm the manifest lists every non-target module under `untouched_modules_verified`.
8. Report the changed file, unresolved impacts, and any new assumption or question in plain language.

The script also refreshes support files (`analysis.json`, `manifest.json`, `review-index.md`, and `traceability.csv`). The promise of byte-for-byte preservation applies to non-target module files.

Read `../analyze-requirements/references/output-contract.md` when changing canonical data and `../analyze-requirements/references/quality-checks.md` before returning the revision.

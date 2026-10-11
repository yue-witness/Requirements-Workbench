---
name: revise-requirements-module
description: Revise one existing Requirements Workbench module while preserving other generated module files. Use when the user names an existing problem-vision-scope, requirements, fishbone, context, domain-model, use-cases, activity, wireframe, feasibility, data-io, or lifecycle-roadmap output and asks to change only that module.
---

# Revise One Requirements Module

Apply the smallest requested change while preserving the rest of the review bundle.

## Workflow

1. Locate the existing output directory and load its `analysis.json` and `manifest.json`.
2. Confirm the target module only when the user's wording could refer to more than one module.
3. Identify whether the change is local presentation detail or a shared fact used by other modules.
4. For a local change, update only the relevant canonical data and keep existing IDs stable.
5. For a shared fact, generate an impact preview before editing with the
   `traceguard_impact` MCP tool or, from the plugin root:

```powershell
python scripts/traceguard.py impact analysis.json `
  --element FR-01 `
  --change "Describe the proposed change" `
  --action propagate `
  --out impact-preview.json
```

   Present the affected modules and patch set, then require the reviewer to
   choose `propagate`, `local-override`, or `cancel`. Do not silently make the
   bundle inconsistent.
6. Regenerate only the target with the `materialize_analysis` MCP tool
   (`only` set to the module) or, from the plugin root, run:

```powershell
python scripts/materialize_analysis.py analysis.json --out requirements-analysis-output --only activity
```

7. Confirm the manifest lists every non-target module under
   `untouched_modules_verified` and records a TraceGuard rollback snapshot when
   canonical data changed.
8. Re-check `traceguard.md`; an abstained high-impact item still requires named
   approval after regeneration.
9. Report the changed file, unresolved impacts, and any new assumption or question in plain language.

The script also refreshes support files (`analysis.json`, `manifest.json`,
`review-index.md`, `traceability.csv`, `traceguard.md`, and `traceguard.json`).
The promise of byte-for-byte preservation applies to non-target module files.

The plugin root is the directory that contains
`scripts/materialize_analysis.py`; a standalone install records it in
`plugin-root.txt` beside this `SKILL.md`. Pass absolute paths to the MCP tools.

Read `../analyze-requirements/references/output-contract.md` when changing canonical data and `../analyze-requirements/references/quality-checks.md` before returning the revision.

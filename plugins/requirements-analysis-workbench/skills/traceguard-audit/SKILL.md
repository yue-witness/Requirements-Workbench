---
name: traceguard-audit
description: Audit an existing Requirements Analysis Workbench bundle for exact evidence spans, cross-artefact consistency, change impact, rollback readiness, and named approvals. Use for TraceGuard checks or impact previews; do not use for generating a new analysis from raw requirements text.
---

# TraceGuard Audit

Use deterministic checks to make unsupported or inconsistent requirements
artefacts visible without claiming semantic verification.

## Audit an existing bundle

1. Locate `analysis.json` in the existing output directory.
2. From the plugin root, run:

```powershell
python scripts/traceguard.py audit analysis.json --out requirements-analysis-output
```

3. Read both `traceguard.json` and `traceguard.md`.
4. Report exact source-span failures, actor/context mismatches, unsupported
   activity steps, untraced wireframe controls, terminology conflicts, and
   abstained approval gates separately.
5. Never describe `pass` as proof that the requirements are correct. It means
   only that the configured deterministic checks passed.

## Preview a change

Before changing a shared stable ID, run:

```powershell
python scripts/traceguard.py impact analysis.json `
  --element FR-01 `
  --change "Describe the proposed change" `
  --action propagate `
  --out impact-preview.json
```

Present the affected modules and patch set. Require the reviewer to choose
`propagate`, `local-override`, or `cancel`; do not infer permission to propagate.
After an approved revision, confirm that `manifest.json` records a rollback
snapshot and that non-target module hashes remain unchanged when applicable.

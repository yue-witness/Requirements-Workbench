# Chemical Warehouse Order Verification Test Case

This public test case was re-run with Requirements Analysis Workbench 0.4.0 against a chemical-warehouse shipment-evidence scenario. The latest confirmed configuration was:

- mode: `professional`
- modules: all eleven v0.4.0 modules: `problem-vision-scope`, `requirements`, `fishbone`, `context`, `domain-model`, `use-cases`, `activity`, `wireframe`, `feasibility`, `data-io`, and `lifecycle-roadmap`
- TraceGuard: enabled

## Contents

- `source-scenario.md` preserves the supplied scenario.
- `conversation.md` records the visible user input, Workbench confirmation, and assistant feedback used for the test.
- `canonical-analysis.json` is the canonical analysis source.
- `generated/` contains all eleven selected artefacts plus the review index, traceability matrix, manifest, and TraceGuard reports.

## Observed result

The v0.4.0 re-run generated eleven selected module files plus six support files using schema version 0.4. The bundle contains 18 atomic requirements, four use cases, nine activity steps, four low-fidelity wireframe screens, six domain entities, four feasibility dimensions, two data entities, two inputs, two outputs, four milestones, and six backlog items. TraceGuard resolved 18 exact evidence spans with zero errors, zero warnings, and one intentional abstention. The abstention applies to `BR-02`, a proposed high-impact rule that would block dispatch confirmation when required evidence is incomplete; it remains unapproved until a named warehouse reviewer records approval.

## Reproduce

From the repository root:

```powershell
python plugins/requirements-analysis-workbench/scripts/materialize_analysis.py `
  test-cases/chemical-warehouse-order-verification/canonical-analysis.json `
  --out test-cases/chemical-warehouse-order-verification/generated
```

The materializer uses only the Python standard library.

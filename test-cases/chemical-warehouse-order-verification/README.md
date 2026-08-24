# Chemical Warehouse Order Verification Test Case

This public test case was re-run with Requirements Analysis Workbench 0.4.0 against a chemical-warehouse shipment-evidence scenario. It preserves the user's previously confirmed configuration:

- mode: `professional`
- modules: `requirements`, `fishbone`, `context`, `use-cases`, `activity`, and `wireframe`
- TraceGuard: enabled

## Contents

- `source-scenario.md` preserves the supplied scenario.
- `conversation.md` records the visible user input, Workbench confirmation, and assistant feedback used for the test.
- `canonical-analysis.json` is the canonical analysis source.
- `generated/` contains all six selected artefacts plus the review index, traceability matrix, manifest, and TraceGuard reports.

## Observed result

The v0.4.0 re-run generated the six selected module files plus six support files using schema version 0.4. The bundle contains 18 atomic requirements, four use cases, nine activity steps, and four low-fidelity wireframe screens. TraceGuard resolved 18 exact evidence spans with zero errors, zero warnings, and one intentional abstention. The abstention applies to `BR-02`, a proposed high-impact rule that would block dispatch confirmation when required evidence is incomplete; it remains unapproved until a named warehouse reviewer records approval.

The v0.4.0 plugin supports five additional independently selectable modules (`problem-vision-scope`, `domain-model`, `feasibility`, `data-io`, and `lifecycle-roadmap`). They are not added to this bundle because the saved Workbench confirmation selected exactly the six modules listed above; the plugin's automated suite covers generation and targeted revision across all eleven modules.

## Reproduce

From the repository root:

```powershell
python plugins/requirements-analysis-workbench/scripts/materialize_analysis.py `
  test-cases/chemical-warehouse-order-verification/canonical-analysis.json `
  --out test-cases/chemical-warehouse-order-verification/generated
```

The materializer uses only the Python standard library.

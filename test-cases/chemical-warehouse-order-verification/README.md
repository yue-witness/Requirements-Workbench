# Chemical Warehouse Order Verification Test Case

This public test case demonstrates Requirements Analysis Workbench 0.3.x against a chemical-warehouse shipment-evidence scenario. The confirmed configuration was:

- mode: `professional`
- modules: `requirements`, `fishbone`, `context`, `use-cases`, `activity`, and `wireframe`
- TraceGuard: enabled

## Contents

- `source-scenario.md` preserves the supplied scenario.
- `conversation.md` records the visible user input, Workbench confirmation, and assistant feedback used for the test.
- `canonical-analysis.json` is the canonical analysis source.
- `generated/` contains all six selected artefacts plus the review index, traceability matrix, manifest, and TraceGuard reports.

## Observed result

The bundle contains 18 atomic requirements, four use cases, nine activity steps, and four low-fidelity wireframe screens. TraceGuard resolved 18 exact evidence spans with zero errors, zero warnings, and one intentional abstention. The abstention applies to `BR-02`, a proposed high-impact rule that would block dispatch confirmation when required evidence is incomplete; it remains unapproved until a named warehouse reviewer records approval.

## Reproduce

From the repository root:

```powershell
python plugins/requirements-analysis-workbench/scripts/materialize_analysis.py `
  test-cases/chemical-warehouse-order-verification/canonical-analysis.json `
  --out test-cases/chemical-warehouse-order-verification/generated
```

The materializer uses only the Python standard library.

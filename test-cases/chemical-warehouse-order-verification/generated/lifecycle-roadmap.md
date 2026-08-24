# Chemical Warehouse Order Verification System - Lifecycle and Roadmap

**Recommended lifecycle:** `iterative`

## Rationale

- Core evidence goals are explicit, but capture technology, permissions, retention, performance and integrations remain unresolved.
- Order capture, review and export can be piloted in bounded increments with warehouse feedback before operational commitment.

## Decision factors

| Factor | Assessment | Evidence | Confidence |
|---|---|---|---|
| Requirements certainty | The desired consolidated evidence outcome is clear, while multiple policy and technical choices remain open. | The scenario requires a unified system but offers barcode scanning or a centralized mobile application as alternatives. | explicit |
| Operational feedback | The primary operator can review whether capture and evidence retrieval reduce current manual effort. | The scenario describes one current operator workflow and calls it inefficient and time-consuming. | explicit |
| High-impact decision | Dispatch blocking and override authority require named stakeholder approval before implementation. | BR-02 is proposed because the source does not specify the required dispatch-control policy. | proposed |

## Trade-off register

| Decision | Scope | Cost | Time | Quality | Status | Approver |
|---|---|---|---|---|---|---|
| Pilot order-centred capture, review and export before adding unconfirmed external integrations. | Defers ERP, WMS, carrier and customer-service integration until evidence confirms need and feasibility. | Reduces initial integration effort but may require later interface work. | Enables earlier workflow feedback without inventing external-system contracts. | Prioritises evidence integrity and reviewability while leaving integration scalability for later validation. | proposed |  |

## Milestones

| ID | Milestone | Goal | Depends on | Related requirements |
|---|---|---|---|---|
| MS-01 | Policy and boundary review | Approve first-release capture method, roles, dispatch rule, retention and evidence boundary. |  | FR-04, FR-13, BR-02, BR-03 |
| MS-02 | Capture and review pilot | Validate product, lot and photograph capture plus consolidated pre-dispatch review with representative orders. | MS-01 | FR-01, FR-02, FR-03, FR-05, FR-06, FR-07, FR-12 |
| MS-03 | Preservation and report pilot | Validate dispatch-version preservation, retrieval and comprehensive report export for human discrepancy review. | MS-02 | FR-08, FR-09, FR-10, FR-11, FR-13, QR-01 |
| MS-04 | Operational readiness decision | Review pilot evidence, unresolved risks and named approvals before any production commitment. | MS-03 | QR-02, BR-02 |

## Backlog

| ID | Item | Type | Priority | Status | Related requirements |
|---|---|---|---|---|---|
| BL-01 | Confirm barcode and mobile capture method | research | must | open | FR-04 |
| BL-02 | Approve evidence completeness and dispatch override policy | research | must | open | BR-02, FR-12 |
| BL-03 | Prototype consolidated evidence capture and review | delivery | must | planned | FR-01, FR-02, FR-03, FR-05, FR-06, FR-07 |
| BL-04 | Define and test the approved report format | delivery | should | planned | FR-08, FR-09 |
| BL-05 | Measure retrieval, export and workload performance | delivery | should | open | FR-10, QR-02 |
| BL-06 | Confirm retention, correction and external integration requirements | research | should | open | FR-13, QR-01 |

## Risks

- Unresolved capture and barcode choices may delay or invalidate a prototype.
- Unapproved dispatch controls or unclear roles may make operational use unsafe.
- Storage, retention, offline and integration requirements may materially change cost and design.

## Open questions

- Who approves each milestone exit and the final operational-readiness decision?
- Which measurable reductions in capture and discrepancy-review effort justify progression?

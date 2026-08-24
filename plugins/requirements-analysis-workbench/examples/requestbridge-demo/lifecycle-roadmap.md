# RequestBridge - Lifecycle and Roadmap

**Recommended lifecycle:** `iterative`

## Rationale

- Important policy and integration choices remain unresolved, so feedback should refine the model before broad implementation.
- The requester and staff workflows can be reviewed in bounded increments while stable IDs preserve traceability.

## Decision factors

| Factor | Assessment | Evidence | Confidence |
|---|---|---|---|
| Requirements certainty | Core goals are clear but policy thresholds and service targets remain open. | The scenario explicitly lists unresolved urgency, retention, service target, cancellation, and notification rules. | explicit |
| Stakeholder feedback | Requester usability and staff efficiency both need early review. | The interface must serve first-time non-technical users and experienced staff. | explicit |

## Trade-off register

| Decision | Scope | Cost | Time | Quality | Status | Approver |
|---|---|---|---|---|---|---|
| Pilot request submission and staff triage before aggregate reporting. | Defers manager analytics detail. | Reduces initial integration and reporting effort. | Enables earlier workflow review. | Creates earlier accessibility and traceability evidence. | proposed |  |

## Milestones

| ID | Milestone | Goal | Depends on | Related requirements |
|---|---|---|---|---|
| MS-01 | Policy and boundary review | Approve first-release scope, role access, and owners for unresolved policies. |  | QR-01, BR-01 |
| MS-02 | Requester flow pilot | Validate identity, request capture, consent, and status with representative users. | MS-01 | FR-01, FR-02, FR-05, FR-06, FR-07, QR-02 |
| MS-03 | Staff workflow pilot | Validate clarification, routing, accountable outcomes, and appointment handling. | MS-02 | FR-09, FR-10, FR-11, FR-12, BR-01 |

## Backlog

| ID | Item | Type | Priority | Status | Related requirements |
|---|---|---|---|---|---|
| BL-01 | Confirm retention and notification policy | research | must | open | FR-13, QR-01 |
| BL-02 | Test the guided requester flow at a 480-pixel viewport | delivery | must | planned | QR-02 |
| BL-03 | Prototype accountable routing-rule changes | delivery | should | planned | FR-10, FR-14 |

## Risks

- External-service readiness may change milestone timing.
- Policy approval delays may block safe production use.

## Open questions

- Who approves each milestone exit?
- Which measurable pilot outcomes permit progression to the next increment?

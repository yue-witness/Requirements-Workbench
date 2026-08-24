# RequestBridge - Problem, Vision and Scope

## Problem statement

Community members cannot consistently express, route, and track service needs through one understandable and accountable process, so requests may be delayed, misrouted, or handled without visible status.

## Vision statement

Provide an accessible RequestBridge service in which a requester can explain a need in ordinary language and follow its progress while authorised staff make transparent, auditable service decisions.

## Affected stakeholders

- Requester
- Service Staff
- Service Manager

## Pain points

| ID | Pain point | Impact | Evidence | Confidence | Related requirements |
|---|---|---|---|---|---|
| PP-01 | Requesters may not know the organisation's categories or service terminology. | Incomplete or misclassified requests create clarification work and slower routing. | The scenario asks requesters to explain needs in everyday language and says the interface must suit first-time non-technical users. | explicit | FR-02, QR-02 |
| PP-02 | Request status, responsibility, and next steps may be difficult to see across the service process. | Requesters may repeat enquiries and staff may lose accountable hand-offs. | The scenario requires a tracking reference, status viewing, triage, assignment, and auditable significant actions. | inferred | FR-07, FR-08, FR-10 |

## Objectives and success measures

| ID | Objective | Success measure | Related requirements |
|---|---|---|---|
| OBJ-01 | Enable a requester to submit a complete and understandable service request. | A requester can reach a validated review summary and receive one tracking reference after consent. | FR-02, FR-05, FR-06, FR-07 |
| OBJ-02 | Make staff routing and high-impact outcomes accountable. | Every assignment or outcome records the responsible human decision and supporting rule or reason. | FR-10, FR-12, BR-01 |

## In scope

- Requester identity and request submission
- Clarification, triage, assignment, appointment, status, and closure
- Managed categories and routing rules
- Aggregate demand reporting

## Out of scope

- Automatic high-impact eligibility decisions
- Operation of external identity, email, SMS, or file-storage services
- Unapproved urgency, retention, service-target, cancellation, or notification policies

## Constraints

- Sensitive information is limited to authorised roles.
- Significant actions are auditable.
- Unresolved policy choices remain open rather than being invented.

## Open questions

- Which service categories belong in the first release?
- Which policy owner approves urgency, retention, cancellation, and notification rules?

# RequestBridge - Requirements Specification

> **Binding language:** Must and shall are binding in this specification. Proposed requirements remain subject to stakeholder approval.

## Functional Requirements

### FR-01

**Requirement:** The system shall identify a requester through an approved organisational account or verified email link before protected request details are displayed.

**Rationale:** A verified identity is needed to protect request information while still supporting people who do not have an organisational account.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario permits an organisational account or verified email link. | Given either approved identity method, when verification succeeds, then the requester can access only requests associated with that verified identity. | explicit |

### FR-02

**Requirement:** The system shall allow a requester to select a request type and describe the service need in everyday language.

**Rationale:** Staff need a minimum description to understand and route the request, while requesters should not need professional terminology.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario requires a request type and plain-language description. | Given an identified requester, when a draft is created, then the requester can save one request type and a free-text description. | explicit |

### FR-03

**Requirement:** The system shall allow a requester to record preferred contact channel, language needs, accessibility needs, and proposed availability when those details are relevant.

**Rationale:** These preferences help staff communicate and arrange an accessible service interaction.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario lists contact, language, accessibility, and availability information. | Given a draft request, when the requester records a preference, then the review summary displays the saved value before submission. | explicit |

### FR-04

**Requirement:** The system shall allow a requester to attach supporting information when the selected request type permits attachments.

**Rationale:** Optional supporting information may help staff understand a request without forcing every requester to upload a file.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| should | The scenario states that supporting information may be attached. | Given an attachment-enabled request type, when an allowed file is uploaded, then the draft lists its name and upload status before submission. | explicit |

### FR-05

**Requirement:** The system shall present a complete, validated review summary before a requester can submit a request.

**Rationale:** Early validation reduces avoidable clarification while the summary lets the requester correct misunderstandings.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario requires validation and a pre-submission review summary. | Given an incomplete draft, when submission is attempted, then each missing field is identified; given a complete draft, then a summary is shown before final confirmation. | explicit |

### FR-06

**Requirement:** The system shall obtain the requester's recorded consent before creating a submitted request.

**Rationale:** The organisation needs evidence that the requester agreed to the stated use of submitted information.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario requires consent before submission. | Given a complete draft, when consent has not been recorded, then final submission is unavailable; when consent is recorded, submission can proceed. | explicit |

### FR-07

**Requirement:** The system shall create a unique tracking reference and an initial status when a valid request is submitted.

**Rationale:** A stable reference lets requesters and staff discuss and trace the same request.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario requires a tracking reference and status viewing. | Given a valid confirmed submission, when processing succeeds, then exactly one request, one unique reference, and one initial status are stored and displayed. | explicit |

### FR-08

**Requirement:** The system shall display the current status and a plain-language history for each request accessible to the verified requester.

**Rationale:** Visible progress reduces uncertainty and unnecessary status enquiries.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario states that requesters can view status. | Given an accessible request, when its status page is opened, then the current status and time-ordered history are displayed without internal-only notes. | explicit |

### FR-09

**Requirement:** The system shall preserve each authorised clarification exchange against the original request.

**Rationale:** Staff need a controlled way to resolve missing or ambiguous information without losing the request history.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario states that triage staff can ask for clarification. | Given an assigned staff member, when clarification is requested and the requester replies, then both messages are linked to the request and visible to authorised participants. | explicit |

### FR-10

**Requirement:** The system shall allow authorised service staff to classify and assign a request according to approved categories and routing rules.

**Rationale:** Consistent classification and assignment help a request reach the responsible team.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario gives triage staff assignment responsibility and managers ownership of routing rules. | Given an unassigned request and active routing rules, when staff confirms a category and destination, then one current assignment and the rule or reason used are recorded. | explicit |

### FR-11

**Requirement:** The system shall allow authorised service staff to propose and confirm an appointment time when a service interaction requires an appointment.

**Rationale:** Some requests require a scheduled conversation rather than an asynchronous response.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| should | The scenario includes booking a conversation with service staff. | Given a request requiring an appointment, when requester and staff confirm an available time, then one appointment is linked to the request and shown in its history. | explicit |

### FR-12

**Requirement:** The system shall require an authorised staff member to record a reason when a request is rejected or closed.

**Rationale:** A recorded reason supports transparency, audit, and meaningful communication to the requester.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario permits rejection with a reason and closure of completed work. | Given an open request, when rejection or closure is attempted without a reason, then the status change is blocked; with a reason, the change is recorded. | explicit |

### FR-13

**Requirement:** The system shall send a status notification through each approved channel selected for the request when a configured notification event occurs.

**Rationale:** Timely notifications reduce the need for requesters to repeatedly check status while respecting organisational channel rules.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| should | The scenario states that email and SMS notifications may be enabled; exact rules are unresolved. | Given an enabled channel and configured event, when the event occurs, then one notification request is sent and its delivery result is recorded. | inferred |

### FR-14

**Requirement:** The system shall allow an authorised service manager to maintain request categories and routing rules with effective dates.

**Rationale:** Managers need controlled configuration so service changes do not require hidden or ad hoc routing decisions.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario assigns categories and routing rules to service managers. | Given an authorised manager, when a valid rule version is activated, then new triage decisions use it and existing audit history retains the previous version. | explicit |

### FR-15

**Requirement:** The system shall provide authorised service managers with aggregate request counts by approved category, status, and time period.

**Rationale:** Aggregated demand information supports service planning without exposing individual request details.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| should | The scenario states that managers view aggregate demand. | Given stored requests, when a manager selects filters, then the system displays counts and excludes request descriptions, attachments, and direct identifiers. | explicit |

## Quality Requirements

### QR-01

**Requirement:** The system shall restrict request details, attachments, messages, and internal notes to approved roles for the relevant service context.

**Rationale:** Requests may contain sensitive information that should not be visible merely because a person can use the platform.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario requires sensitive information to be limited to authorised roles. | Given a user without an approved role, when protected request content is requested, then access is denied and the attempt is recorded. | explicit |

### QR-02

**Requirement:** The system shall support labelled controls, keyboard operation, visible focus, plain-language guidance, and layouts without horizontal page scrolling at a 480-pixel viewport.

**Rationale:** The service must be understandable and operable for first-time non-technical users and people using different devices or input methods.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario requires an interface suitable for first-time users while remaining efficient for staff. | Given the primary requester flow at 480 pixels, when a keyboard-only reviewer completes it, then every control is labelled, reachable, visibly focused, and usable without horizontal scrolling. | inferred |

### QR-03

**Requirement:** The system shall display interactive pages within two seconds for at least 95 percent of measured requests under the approved reference load.

**Rationale:** A measurable placeholder allows stakeholders to discuss responsiveness without relying on the vague word fast.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| should | Proposed quality target because the scenario says service targets are not yet agreed. | Given the approved reference environment and load profile, when a representative test is run, then at least 95 percent of measured page responses complete within two seconds. | proposed |

## Business Requirements

### BR-01

**Requirement:** The system must require authorised human confirmation before a high-impact eligibility, rejection, or service-access decision takes effect.

**Rationale:** Human confirmation prevents an automated classification or routing suggestion from becoming an unsupported high-impact decision.

| Priority | Evidence / source | Acceptance check | Confidence |
|---|---|---|---|
| must | The scenario explicitly prohibits automatic high-impact decisions. | Given an automated suggestion, when no authorised person has confirmed the decision, then the system does not apply a high-impact eligibility, rejection, or access outcome. | explicit |


## Open questions

- Which request types are in scope for the first release?
- What criteria define urgency, and who may change those criteria?
- Which roles may view each class of sensitive information?
- What retention period applies to requests, messages, attachments, and audit records?
- Which response-time, availability, and notification targets are binding?
- When may a requester cancel or update a submitted request?
- Which languages and accessibility conformance target must the first release support?

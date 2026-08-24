# RequestBridge - Data, Inputs and Outputs

## Data catalogue

### DATA-REQUEST - Service request record

The requester's submitted need, preferences, consent, status, and accountable history.

**Owner:** Service organisation
**Sensitivity:** May contain sensitive personal and service information; access is role-restricted.
**Retention:** Unresolved; a named policy owner must approve the period.
**Related requirements:** FR-02, FR-05, FR-06, FR-07, QR-01

| Field | Type | Required | Validation |
|---|---|---|---|
| trackingReference | Identifier | yes | Unique and immutable after submission. |
| requestType | Category reference | yes | Must reference an active approved category. |
| description | Text | yes | Must contain non-whitespace content within the approved size limit. |
| consentRecordedAt | DateTime | yes | Must be recorded before final submission. |

## Inputs

### IN-REQUEST - Requester submission

- Source: Verified requester
- Method: Accessible web form
- Format: Structured fields, plain text, and optional approved attachment
- Timing: Before a service request is created
- Error feedback: Keep the draft, identify each failed check in plain language, and do not create a submitted request.
- Related requirements: FR-01, FR-02, FR-04, FR-05, FR-06

**Verification rules** (is the input genuine and from the claimed source?)

- Verify the organisational account or email-link identity before protected details are displayed.
- Record the requester identity associated with consent.

**Validation rules** (is the value complete, well-formed, and allowed?)

- Require request type, description, and consent.
- Display field-specific errors and a complete review summary before submission.
- Validate attachment type and size against approved configuration.

## Outputs

### OUT-STATUS - Requester-visible reference and status history

- Audience: Verified requester
- Destination: RequestBridge status page and approved notification channels
- Format: Plain-language web content plus configured email or SMS message
- Timing: After submission and after configured status events
- Failure behaviour: Preserve the status update, record notification failure, and expose a retry or alternative channel to authorised staff.
- Related requirements: FR-07, FR-08, FR-13, QR-02

**Content**

- Tracking reference
- Current status
- Requester-visible history and next action

**Accessibility**

- Label status and action controls.
- Support keyboard operation and visible focus.
- Avoid exposing internal-only notes.

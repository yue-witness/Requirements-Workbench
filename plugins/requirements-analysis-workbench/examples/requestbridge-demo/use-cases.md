# RequestBridge - Use-Case Descriptions

## UC-01 - Submit a service request

**Primary actor:** Requester

**Goal:** Explain a need and receive a traceable submitted request.

**Trigger:** The requester selects Start a request.

### Stakeholders and interests

- Requester: wants an understandable, accessible submission process.
- Service Staff: need enough accurate information to begin triage.

### Preconditions

- The requester can use an approved identity method.

### Main flow

1. The system verifies the requester.
2. The requester selects a request type and describes the need.
3. The requester records relevant contact, language, accessibility, and availability preferences.
4. The system validates required information.
5. The system displays a review summary and consent statement.
6. The requester confirms consent and submits.
7. The system creates a unique reference and initial status.

### Alternative and exception flows

- A1: The requester saves a draft and returns later.
- A2: The requester removes or replaces an invalid attachment.
- E1: If identity verification fails, protected submission is not created.
- E2: If required information is missing, the system identifies each missing item.

### Postconditions

- One submitted request with a unique reference exists, or the draft remains unsubmitted.

### Business rules

- BR-01 requires human confirmation for any later high-impact decision.

**Related requirements:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, QR-02

## UC-02 - Triage a request

**Primary actor:** Service Staff

**Goal:** Clarify and assign a request to an appropriate service path.

**Trigger:** An untriaged request enters the staff queue.

### Stakeholders and interests

- Requester: wants a fair, understandable next step.
- Service Manager: wants approved rules used consistently.

### Preconditions

- The request is submitted and the staff member is authorised.

### Main flow

1. The system displays the request and applicable routing information.
2. The staff member reviews the request.
3. The staff member selects a category and destination.
4. The system records the assignment and decision basis.
5. The system updates the requester-visible status.

### Alternative and exception flows

- A1: The staff member asks for clarification and pauses assignment.
- A2: The staff member records a reason and rejects an unsupported request.
- E1: If no destination is available, the request remains unassigned and the conflict is visible.

### Postconditions

- The request is assigned, awaiting clarification, or rejected with a recorded reason.

### Business rules

- Only effective approved routing rules may be applied.
- BR-01 prevents an automated suggestion from taking effect without human confirmation.

**Related requirements:** FR-09, FR-10, FR-12, FR-14, QR-01, BR-01

## UC-03 - Arrange an appointment

**Primary actor:** Service Staff

**Goal:** Agree a service conversation time with the requester.

**Trigger:** The staff member selects Arrange appointment.

### Stakeholders and interests

- Requester and Service Staff: need an available time and clear confirmation.

### Preconditions

- The request requires an appointment and has an assigned service team.

### Main flow

1. The system displays applicable requester availability.
2. The staff member proposes an available time.
3. The requester confirms the proposed time.
4. The system links the appointment to the request and sends approved notifications.

### Alternative and exception flows

- A1: The requester declines and supplies different availability.
- E1: If the time becomes unavailable, the system preserves the request and asks staff to propose another time.

### Postconditions

- One confirmed appointment is linked to the request, or scheduling remains pending.

### Business rules

- Notification channels and timing must follow approved configuration.

**Related requirements:** FR-03, FR-11, FR-13

## UC-04 - Maintain service rules

**Primary actor:** Service Manager

**Goal:** Keep categories and routing rules current and accountable.

**Trigger:** The manager opens service configuration.

### Stakeholders and interests

- Service Staff: need understandable current rules.
- Requesters: need consistent routing.

### Preconditions

- The manager is authenticated and authorised.

### Main flow

1. The manager creates or edits a category or routing rule.
2. The system validates the proposed effective dates and references.
3. The manager reviews and activates the rule version.
4. The system records the change and applies it to new triage decisions.

### Alternative and exception flows

- A1: The manager schedules a future effective date.
- E1: If the change would create an invalid destination, activation is blocked with an explanation.

### Postconditions

- One accountable rule version is active or scheduled.

### Business rules

- Historical decisions retain the rule version that supported them.

**Related requirements:** FR-14, FR-15

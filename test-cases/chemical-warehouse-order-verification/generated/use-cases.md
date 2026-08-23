# Chemical Warehouse Order Verification System - Use-Case Descriptions

## UC-01 - Capture order inventory evidence

**Primary actor:** Warehouse Operator

**Goal:** Create one complete order-centred record of product quantities, lot numbers, and photographs before dispatch review.

**Trigger:** The Warehouse Operator selects an order to prepare its shipment evidence.

### Stakeholders and interests

- Warehouse Operator: wants one efficient capture workflow without duplicate entry across separate tools.
- Customer: wants reliable evidence when shipment contents are disputed.

### Preconditions

- The order is available for shipment processing.
- The Warehouse Operator is permitted to work on the selected order.
- At least one stakeholder-approved product and lot capture method is available.

### Main flow

1. The system opens or creates the Order Evidence Record for the selected order.
2. The Warehouse Operator captures each product line and shipped quantity.
3. The Warehouse Operator captures the applicable lot numbers for each product line.
4. The Warehouse Operator captures or uploads order photographs.
5. The Warehouse Operator associates each photograph with the applicable product lines, quantities, and lots.
6. The system displays the consolidated order evidence for review.

### Alternative and exception flows

- A1: If barcode capture is unavailable or not approved, the Warehouse Operator uses the approved centralized mobile capture method.
- A2: The Warehouse Operator corrects a captured quantity, lot, or photo association before dispatch confirmation.
- E1: If captured data cannot be validated, the system keeps the order unconfirmed and identifies the affected field.
- E2: If a photograph cannot be stored, the system reports the failure and does not show the photograph as saved.

### Postconditions

- One Order Evidence Record contains the evidence saved for the order, or the order remains visibly incomplete.

### Business rules

- BR-01 makes the order the primary evidence unit.
- BR-03 prohibits cross-order evidence in the record.

**Related requirements:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-12, QR-01, BR-01, BR-03

## UC-02 - Review evidence and confirm dispatch

**Primary actor:** Warehouse Operator

**Goal:** Review the consolidated evidence and preserve the version representing the dispatched order.

**Trigger:** The Warehouse Operator selects Review for dispatch.

### Stakeholders and interests

- Warehouse Operator: needs a clear indication of incomplete or inconsistent evidence.
- Customer: needs later verification to use the evidence that represented the shipped order.
- Authorised Reviewer: must decide whether the proposed dispatch-blocking rule and any override are acceptable.

### Preconditions

- An Order Evidence Record exists for the order.
- The Warehouse Operator has completed the available capture steps.

### Main flow

1. The system displays the consolidated quantities, lots, photographs, and associations.
2. The system identifies any evidence defined as required but missing.
3. The Warehouse Operator reviews and corrects discrepancies before confirmation.
4. The Warehouse Operator requests dispatch confirmation.
5. The system preserves the dispatch-confirmed version of the Order Evidence Record.

### Alternative and exception flows

- A1: The Warehouse Operator returns to capture when evidence is missing or inconsistent.
- A2: If stakeholders approve an override rule, an authorised person uses it and the system records the authorised use.
- E1: While BR-02 remains unapproved, the proposed software block must not be treated as an accepted operating rule.
- E2: If preservation fails, the system does not present the order as dispatch-confirmed.

### Postconditions

- A dispatch-confirmed evidence version exists, or the order remains unconfirmed with unresolved evidence visible.

### Business rules

- BR-02 is proposed and high-impact; TraceGuard requires named approval before it becomes binding.
- BR-03 keeps the confirmed version isolated from other orders.

**Related requirements:** FR-07, FR-12, FR-13, QR-01, BR-02, BR-03

## UC-03 - Export an order report

**Primary actor:** Warehouse Operator

**Goal:** Create a portable, comprehensive report for one selected order.

**Trigger:** The Warehouse Operator requests an export for a selected order.

### Stakeholders and interests

- Warehouse Operator: needs an efficient report-generation path.
- Customer or other reviewer: needs an understandable account of what the warehouse recorded as sent.

### Preconditions

- An Order Evidence Record exists and is accessible to the Warehouse Operator.
- An approved report format has been selected.

### Main flow

1. The system loads the selected Order Evidence Record.
2. The system prepares the order identifier, product quantities, lot numbers, and photographic documentation.
3. The Warehouse Operator reviews the report preview or content summary.
4. The system creates the report in the approved format.
5. The system makes the completed report available to the Warehouse Operator.

### Alternative and exception flows

- A1: The Warehouse Operator cancels export and returns to the order record without changing it.
- E1: If report generation fails, the system identifies the failure and does not substitute evidence from another order.
- E2: If required report content is unavailable, the system identifies the omission rather than representing the report as complete.

### Postconditions

- One report for the selected order is available, or a visible export failure is recorded for the current attempt.

### Business rules

- BR-01 requires order-centred reporting.
- BR-03 prevents cross-order evidence from appearing.

**Related requirements:** FR-08, FR-09, QR-01, BR-01, BR-03

## UC-04 - Verify a customer discrepancy

**Primary actor:** Warehouse Operator

**Goal:** Retrieve and review the preserved evidence for the order identified in a customer claim.

**Trigger:** The Warehouse Operator begins investigation of a customer missing-product claim.

### Stakeholders and interests

- Warehouse Operator: wants to locate credible order evidence without reconciling separate tools.
- Customer: wants the reported missing-product issue investigated against the relevant shipment evidence.

### Preconditions

- The Warehouse Operator has the order identifier associated with the customer discrepancy.
- A preserved Order Evidence Record exists for that order.

### Main flow

1. The Warehouse Operator searches by the order identifier.
2. The system returns the matching preserved Order Evidence Record.
3. The system displays the recorded quantities, lots, photographs, and available report.
4. The Warehouse Operator compares the customer claim with the preserved evidence.
5. The Warehouse Operator exports the order report when it is required for the human resolution process.

### Alternative and exception flows

- A1: If an export is not required, the Warehouse Operator completes the evidence review in the consolidated order view.
- E1: If no matching order exists, the system reports that no exact identifier match was found without returning another order.
- E2: If evidence is incomplete, the system displays the available evidence and the omission without deciding the claim outcome.

### Postconditions

- The relevant order evidence has been presented for human review; the customer-claim outcome remains outside the currently confirmed system scope.

### Business rules

- BR-03 prevents another order's evidence from being used in the review.

**Related requirements:** FR-08, FR-09, FR-10, FR-11, FR-13, QR-01, BR-03

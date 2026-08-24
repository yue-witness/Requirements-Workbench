# Chemical Warehouse Order Verification System - Data, Inputs and Outputs

## Data catalogue

### DATA-EVIDENCE - Order Evidence Record

The consolidated quantities, lots, photographs and dispatch-confirmed version for one order.

**Owner:** Warehouse operations; accountable owner to be confirmed
**Sensitivity:** Commercial shipment evidence that may require role-restricted access; classification is unconfirmed.
**Retention:** Unresolved; a named policy owner must approve the period and deletion rules.
**Related requirements:** FR-01, FR-02, FR-03, FR-05, FR-06, FR-13, QR-01

| Field | Type | Required | Validation |
|---|---|---|---|
| orderIdentifier | Identifier | yes | Must identify exactly one selected order. |
| productLines | Collection | yes | Each line must contain an approved product identifier and shipped quantity. |
| lotNumbers | Collection | yes | Each lot must be associated with an applicable product line. |
| photographs | Media collection | yes | Each saved photograph must remain associated with the current order. |
| confirmedVersion | Version | no | Must represent the version preserved at dispatch confirmation. |
### DATA-REPORT - Comprehensive Order Report

A portable representation of evidence for one selected order.

**Owner:** Warehouse operations; distribution authority to be confirmed
**Sensitivity:** Inherits the sensitivity of the source Order Evidence Record.
**Retention:** Unresolved; must align with approved evidence and export policy.
**Related requirements:** FR-08, FR-09, BR-03

| Field | Type | Required | Validation |
|---|---|---|---|
| orderIdentifier | Identifier | yes | Must match the selected evidence record. |
| quantities | Collection | yes | Must reproduce the selected record's shipped quantities. |
| lotNumbers | Collection | yes | Must reproduce the selected record's applicable lots. |
| photographicDocumentation | Media collection | yes | Must include only photographs associated with the selected order. |

## Inputs

### IN-PRODUCT-LOT - Product, quantity and lot capture

- Source: Warehouse Operator using an approved integrated capture method
- Method: Barcode scan, centralized mobile capture, or another stakeholder-approved integrated method
- Format: Approved product identifier, numeric quantity and lot identifier
- Timing: While preparing the selected order before dispatch review
- Error feedback: Keep the order visibly incomplete, identify the affected field and do not represent rejected data as saved.
- Related requirements: FR-02, FR-03, FR-04, FR-12, BR-03

**Verification rules** (is the input genuine and from the claimed source?)

- Verify that the capture is associated with the order currently selected by the authorised operator.
- When scanning is used, verify that the symbology and identifier source are approved.

**Validation rules** (is the value complete, well-formed, and allowed?)

- Require an approved product identifier, an allowed quantity and an applicable lot identifier.
- Reject or flag data that cannot be associated with the selected order and product line.

### IN-PHOTO - Order photograph capture

- Source: Warehouse Operator using an approved warehouse mobile device
- Method: Camera capture or upload through the centralized order workflow
- Format: Approved image type and metadata; exact limits remain open
- Timing: Before dispatch review for the selected order
- Error feedback: Report the failed image check or storage operation and do not show the photograph as saved.
- Related requirements: FR-05, FR-06, FR-12, BR-03

**Verification rules** (is the input genuine and from the claimed source?)

- Verify the operator and selected order before accepting the photograph.
- Verify that the device or upload channel is approved when such policy exists.

**Validation rules** (is the value complete, well-formed, and allowed?)

- Require the image to be readable and stored successfully.
- Require an association with the current order and applicable product evidence.

## Outputs

### OUT-REVIEW - Consolidated order evidence view

- Audience: Authorised Warehouse Operator
- Destination: Order-verification workspace
- Format: Structured on-screen quantities, lots, photographs and completeness indicators
- Timing: Before dispatch confirmation and during later discrepancy review
- Failure behaviour: Identify unavailable evidence without substituting data from another order or presenting the view as complete.
- Related requirements: FR-07, FR-11, FR-12, BR-03

**Content**

- Order identifier
- Product quantities
- Applicable lot numbers
- Associated photographs
- Evidence status

**Accessibility**

- Use programmatic labels and keyboard-operable controls.
- Present validation status in text rather than colour alone.

### OUT-REPORT - Comprehensive order report

- Audience: Authorised Warehouse Operator and approved human discrepancy reviewer
- Destination: Approved export location or delivery channel; exact destination is open
- Format: Stakeholder-approved portable report format
- Timing: On request for a selected Order Evidence Record
- Failure behaviour: Report the export failure or missing content and do not substitute evidence from another order.
- Related requirements: FR-08, FR-09, BR-03

**Content**

- Order identifier
- Product quantities
- Applicable lot numbers
- Photographic documentation

**Accessibility**

- Use a navigable reading order and meaningful labels for photographic evidence.
- Do not rely on images alone to identify products, quantities or lots.

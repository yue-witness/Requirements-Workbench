# Chemical Warehouse Order Verification System - Problem, Vision and Scope

## Problem statement

The warehouse records quantities and lot numbers in Google Sheets and stores pre-dispatch photographs on a separate mobile phone, so evidence for one order must be reconciled manually when a customer reports missing product.

## Vision statement

Provide one order-centred evidence workflow in which authorised warehouse staff capture, review, preserve and export quantities, lots and photographs without duplicating the same evidence across disconnected tools.

## Affected stakeholders

- Warehouse Operator
- Customer
- Warehouse Operations Owner or Authorised Reviewer (role to be confirmed)

## Pain points

| ID | Pain point | Impact | Evidence | Confidence | Related requirements |
|---|---|---|---|---|---|
| PP-01 | Order evidence is split between Google Sheets and a separate mobile phone. | Staff must reconcile quantities, lots and photographs before an order can be verified. | The scenario explicitly describes a manual fragmented system using Google Sheets and a dedicated phone. | explicit | FR-04, FR-07, BR-01 |
| PP-02 | Manual re-entry makes order verification inefficient and time-consuming. | The operator spends avoidable effort assembling evidence instead of reviewing one record. | The scenario explicitly asks to eliminate manual entry and streamline verification. | explicit | FR-04, FR-07, FR-08 |
| PP-03 | Customer missing-product claims are difficult to investigate against consolidated dispatch evidence. | Discrepancy resolution may be slower and less consistent. | The scenario identifies recurring customer claims and requests comprehensive order reports. | explicit | FR-08, FR-09, FR-11, FR-13 |

## Objectives and success measures

| ID | Objective | Success measure | Related requirements |
|---|---|---|---|
| OBJ-01 | Consolidate shipment evidence around one selected order. | A reviewer can see the order's quantities, lots and photographs together without consulting another tracking tool. | FR-01, FR-07, BR-01, BR-03 |
| OBJ-02 | Reduce duplicate manual capture while retaining a stakeholder-approved method. | The approved capture flow records product and lot evidence without re-keying the same values between separate tools. | FR-02, FR-03, FR-04, FR-05 |
| OBJ-03 | Make preserved order evidence available for shipment-discrepancy review. | An authorised operator can retrieve one preserved order record and export its comprehensive report. | FR-08, FR-09, FR-10, FR-11, FR-13 |

## In scope

- Order-centred capture of quantities, lot numbers and photographs
- Consolidated evidence review and correction before dispatch confirmation
- Preservation, retrieval and export of shipment evidence
- Human review support for customer shipment discrepancies

## Out of scope

- Automatic decisions about customer liability or claim outcomes
- Unconfirmed integration with ERP, WMS, carrier or customer-service systems
- Historical Google Sheets and phone-photo migration unless later approved
- Unverified chemical-industry regulatory or safety rules

## Constraints

- The current workload is 25 to 30 pallet shipments per week.
- Barcode scanning, a centralized mobile application, or both remains a stakeholder choice.
- BR-02 must remain proposed until a named reviewer approves the dispatch-blocking rule.

## Open questions

- Which capture method and barcode standards are approved for the first release?
- Which roles may confirm dispatch, correct preserved evidence and export reports?
- Which report format, performance target, retention rule and legal obligations apply?

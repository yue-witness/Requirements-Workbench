# RequestBridge - Review Index

**Status:** demo draft for stakeholder review

**Review mode:** guided

## Start here

RequestBridge helps a person explain a service need, submit it safely, and follow what happens next. Staff can clarify, route, schedule, and close requests. The draft keeps unresolved policy choices visible instead of guessing them.

## Generated modules

| Module | What to review | File | SHA-256 |
|---|---|---|---|
| requirements | Check what the software must do, why each item exists, and how it can be tested. | `requirements.md` | `7e829adbf2f7190ab96f37d3039fa3b2140372a66743b762ed59020a6531d151` |
| fishbone | Check whether the possible causes are plausible hypotheses rather than confirmed facts. | `fishbone.mmd` | `15c371fa6dec3841c4d0acade2babb4c8ae66cdcf7d2934d0107e67da8bcb508` |
| context | Check the system boundary, external people and systems, and labelled information flows. | `context.mmd` | `00fa6a1e3be1d58533c8a4d493c313e59363c40a9c62df4be0dd347f960cf69b` |
| use-cases | Check goals, main steps, alternatives, exceptions, and linked requirements. | `use-cases.md` | `874ff02f0bb22a11a24f89f04383a309e50dd0dacba9ab3efabdedd89e5b562b` |
| activity | Check workflow order, decisions, guards, rejection paths, and end states. | `activity.mmd` | `eb1fe7c2a4cc84e349f5bf02e7782d73a2ca22339a0641fe28369f668b00764f` |
| wireframe | Check whether the proposed screens support the traced requirements and use-case steps. | `wireframe.html` | `1b55bd60496de4f5d198b3802e7a42c0ddc7169a09ad9cc5952fb9288e5f3669` |

## TraceGuard

**Decision state:** `abstain`

- Exact source spans: 18
- Errors: 0
- Warnings: 1
- Abstentions awaiting named approval: 2
- Review `traceguard.md` for human-readable findings and `traceguard.json` for automation.

## Glossary

| Term | Plain-language meaning |
|---|---|
| System boundary | The functions owned by RequestBridge, separated from people and external services. |
| Triage | A staff review that decides what information or service path a request needs. |
| Acceptance check | An observable test that helps reviewers decide whether a requirement has been met. |
| Confidence | Whether a requirement is explicit in the scenario, inferred from it, or proposed for discussion. |

## Reviewer checklist

- Does any output contradict the supplied scenario or stakeholder evidence?
- Which assumptions can be confirmed, rejected, or rewritten?
- Which open questions block a design or scope decision?
- Does every requirement have a clear rationale, evidence, and acceptance check?
- Are the system boundary, actors, flows, and terminology consistent across modules?
- Does the wireframe support the required user goals without introducing unsupported features?

## Assumptions

- A verified email link can identify a requester who has no organisational account.
- Service managers own the approved categories and routing rules.
- Email, SMS, and file storage are external services with separate availability and security controls.

## Open questions

- Which request types are in scope for the first release?
- What criteria define urgency, and who may change those criteria?
- Which roles may view each class of sensitive information?
- What retention period applies to requests, messages, attachments, and audit records?
- Which response-time, availability, and notification targets are binding?
- When may a requester cancel or update a submitted request?
- Which languages and accessibility conformance target must the first release support?

## Automated quality warnings

- No heuristic warnings were detected.

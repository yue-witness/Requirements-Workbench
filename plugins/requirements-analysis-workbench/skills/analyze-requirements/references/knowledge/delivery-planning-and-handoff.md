# Delivery planning and handoff

## Lifecycle and development strategy

Choose a lifecycle based on requirements stability, risk, feedback speed,
technical uncertainty, regulatory needs, delivery cadence, and stakeholder
availability. Predictive approaches emphasise up-front definition and sequenced
phases; parallel work shortens schedules but increases coordination and
integration risk; iterative approaches revisit analysis, design, and build;
prototyping reduces uncertainty through stakeholder feedback; agile approaches
prioritise incremental value and adaptation.

Prototypes may be throw-away learning tools or evolutionary foundations. State
which they are, because treating a quick experiment as production architecture
creates hidden quality and maintenance risk.

## Constraints, trade-offs, and plans

Scope, cost, and time constrain one another and affect achievable quality.
Record each trade-off, its rationale, affected requirements and quality
attributes, and the stakeholder who accepts it. Quietly cutting quality can move
risk into operation; cutting scope requires explicit reprioritisation.

A roadmap communicates goals, priorities, dependencies, milestones, and likely
risks. Break requirements into manageable tasks only after their intent is
understood. Record estimates as uncertain forecasts and improve them with
evidence. Identify critical-path dependencies where delay would affect the
delivery date.

An ordered backlog can contain requirements, defects, research, and delivery
tasks. Keep a central owner-visible record, explicit ordering rationale,
acceptance conditions, trace links, and current state. A task board visualises
flow but is not a substitute for agreed requirements.

## Analysis artefacts and handoff

Version and trace analysis artefacts such as the problem and vision statements,
glossary, stakeholder models, requirements, user stories, scenarios, use cases,
domain and context models, prototypes, SRS, decisions, and open questions. The
chosen lifecycle may change their timing and form, but not the need for shared
understanding and verifiability.

Before handoff, confirm that the project team understands the vision, scope,
priorities, terminology, system boundary, requirements, models, constraints,
risks, unresolved questions, and review ownership. Domain models may inform
design classes, exact data types, behaviours, and coordinating components, but
that transformation is a design step and must not be presented as discovered
domain fact.

## Acceptance and sign-off

Define acceptance tests and sign-off criteria early. User acceptance testing is
performed by authorised customer representatives against agreed business needs
and acceptance conditions. At closure, identify all agreed deliverables, test
results, unresolved exceptions, operational or support materials, approvers,
and the decision that marks the project complete. Sign-off controls completion
and scope creep; it does not erase known defects or waived risks.

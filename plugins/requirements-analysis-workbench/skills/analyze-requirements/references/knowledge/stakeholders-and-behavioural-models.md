# Stakeholders and behavioural models

## Stakeholders, actors, and personas

Identify direct users, indirect beneficiaries, operators, maintainers, managers,
customers, external organisations, and systems affected by or contributing to
the solution. An actor is a role interacting with the system; a persona is an
evidence-informed example of a user type. Do not treat a speculative persona as
a real stakeholder statement.

## User stories, scenarios, and use cases

A user story records a role, goal, and benefit: `As a [role], I want [goal], so
that [benefit]`. Keep it small enough to discuss and pair it with acceptance
criteria. Story points estimate relative effort or uncertainty; they are not
business priority or elapsed time.

A usage scenario narrates a realistic sequence in context and is useful for
discovering missing conditions. A use case structures a goal-oriented
interaction. Increase detail only as needed:

- simple: identifier, name, primary actor, and goal;
- expanded: trigger, preconditions, main flow, alternatives, exceptions, and
  postconditions;
- detailed: stakeholders, business rules, actor/system responsibilities, data,
  and trace links.

Check that alternatives and failures are not hidden inside an optimistic main
flow and that every introduced behaviour traces to evidence, an assumption, or
a labelled proposal.

## Process models and structured logic

Activity models show start and end states, actions, decisions, guards,
responsibilities, parallel work, and exception or rejection paths. Structured
English can express decision logic with a restricted vocabulary such as IF,
THEN, ELSE, WHILE, and DO. Both techniques should clarify behaviour without
inventing unsupported business rules.

## Wireframes and mockups

Wireframes test information hierarchy, controls, navigation, inputs, outputs,
and error recovery at low cost. Mockups add visual detail. Treat both as review
models: each actionable control should support a traced requirement or use-case
step, and visually attractive screens must not introduce unapproved features.

## Data, input, and output

For important information, identify its business meaning, structure, source,
destination, owner, lifetime, sensitivity, and relationships to other data.
Functional requirements often become clearer when expressed as input,
behaviour, and output.

For inputs, record method, format, timing, required and optional values, and
error feedback. **Verification** checks that entered data matches an external
source or identity; **validation** checks that it satisfies format, range,
presence, consistency, and business rules. Keep the distinction visible.

For outputs, identify audience, content, format, timing, channel, accessibility,
retention, and failure behaviour. Do not infer fields or channels that the
stakeholders have not requested.

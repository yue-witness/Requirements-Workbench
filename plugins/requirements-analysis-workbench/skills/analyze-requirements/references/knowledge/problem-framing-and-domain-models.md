# Problem framing and domain models

## Keep problem and solution domains separate

Requirements connect a real problem to a possible solution. Do not begin with a
requested application or technology and assume it is the right answer. First
establish who experiences the problem, the current process, the pain, its
frequency and impact, and why existing arrangements are insufficient.

Separate symptoms from plausible causes. Gather pain points through stakeholder
discussion and observation, consolidate them collaboratively, and label root
causes as hypotheses until evidence validates them. A fishbone model is useful
for grouping candidate causes under categories such as process, people,
equipment, environment, management, materials, or external forces. Adapt the
categories to the domain instead of forcing a fixed set.

## Problem statement

A reviewable problem statement should identify:

- the affected stakeholders or organisation;
- the current situation and pain points;
- the impact and why it matters;
- evidence or observations supporting the problem;
- the boundary of the problem being addressed;
- important unknowns, without embedding a preferred solution.

## Vocabulary, boundary, and models

Capture stakeholder terminology and definitions in a maintained glossary. Flag
synonyms, overloaded terms, and disagreements before they create inconsistent
requirements.

A context model places the proposed system inside one boundary and shows the
external people, organisations, devices, and systems that exchange labelled
information with it. Check what is inside, what remains outside, ownership of
each interaction, and whether the boundary conflicts with the stated scope.

A domain model describes real-world entities, attributes, and relationships in
the problem domain. Use stakeholder language, cardinality where it matters, and
refine the model as understanding grows. Do not prematurely add software
classes, methods, databases, or frameworks. For systems of systems, distinguish
horizontal interactions between independent systems from vertical nesting of
subsystems and super-systems.

## Feasibility, scope, and vision

Before committing to a solution, record constraints and risks across relevant
dimensions:

- technical capability and integration;
- operational fit with people and processes;
- schedule, staffing, and resource availability;
- legal and contractual obligations;
- political or organisational acceptance;
- economic costs and benefits, including tangible and intangible effects.

Scope states objectives, included and excluded work, resources, information,
deliverables, and planned activities. Trace scope decisions back to requirements
and label any proposed exclusion for stakeholder review.

A vision statement is brief and directional: target users or customers, their
need, the product category, its primary benefit, and the most important
difference from the current alternative. It guides trade-offs but does not
replace detailed requirements.

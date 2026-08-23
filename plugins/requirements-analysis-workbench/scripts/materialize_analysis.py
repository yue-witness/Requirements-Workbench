#!/usr/bin/env python3
"""Materialise independently revisable requirements-analysis modules.

The Codex skill produces a canonical JSON analysis. This script performs the
deterministic part of the demo: validation, file generation, and hash tracking.
It deliberately uses only the Python standard library so the plugin remains
portable and does not need an API key or network access.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


# Keep the deterministic helper importable when this file is loaded directly
# by the regression suite rather than executed as a package module.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from traceguard import write_audit


MODULE_FILES = {
    "requirements": "requirements.md",
    "fishbone": "fishbone.mmd",
    "context": "context.mmd",
    "use-cases": "use-cases.md",
    "activity": "activity.mmd",
    "wireframe": "wireframe.html",
}
MODULE_DESCRIPTIONS = {
    "requirements": "Check what the software must do, why each item exists, and how it can be tested.",
    "fishbone": "Check whether the possible causes are plausible hypotheses rather than confirmed facts.",
    "context": "Check the system boundary, external people and systems, and labelled information flows.",
    "use-cases": "Check goals, main steps, alternatives, exceptions, and linked requirements.",
    "activity": "Check workflow order, decisions, guards, rejection paths, and end states.",
    "wireframe": "Check whether the proposed screens support the traced requirements and use-case steps.",
}

CONFIDENCE_VALUES = {"explicit", "inferred", "proposed"}
REQUIREMENT_CATEGORIES = {"functional", "quality", "business"}
REVIEW_MODES = {"guided", "standard", "professional"}
REQUIRED_REQUIREMENT_FIELDS = {
    "id",
    "category",
    "priority",
    "statement",
    "rationale",
    "evidence",
    "acceptance",
    "confidence",
}
REQUIRED_USE_CASE_FIELDS = {
    "id",
    "name",
    "primary_actor",
    "goal",
    "stakeholders",
    "preconditions",
    "trigger",
    "main_flow",
    "alternatives",
    "exceptions",
    "postconditions",
    "business_rules",
    "related_requirements",
}


class AnalysisError(ValueError):
    """Raised when the canonical analysis violates the demo contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate selected requirements-analysis modules from JSON."
    )
    parser.add_argument("analysis", type=Path, help="Canonical analysis JSON file")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    parser.add_argument(
        "--only",
        choices=sorted(MODULE_FILES),
        help="Regenerate one module and preserve the other module files",
    )
    return parser.parse_args()


def load_analysis(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            value = json.load(stream)
    except FileNotFoundError as exc:
        raise AnalysisError(f"Analysis file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AnalysisError(f"Invalid JSON at line {exc.lineno}: {exc.msg}") from exc

    if not isinstance(value, dict):
        raise AnalysisError("The top-level JSON value must be an object.")
    return value


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        raise AnalysisError(f"'{key}' must be a list.")
    return value


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise AnalysisError(f"'{key}' must be an object.")
    return value


def validate_analysis(data: dict[str, Any]) -> list[str]:
    """Validate required fields and return the selected module names."""

    project = require_object(data, "project")
    if not str(project.get("name", "")).strip():
        raise AnalysisError("'project.name' must not be empty.")
    review_mode = str(project.get("review_mode", "standard")).strip().lower()
    if review_mode not in REVIEW_MODES:
        raise AnalysisError(
            "'project.review_mode' must be guided, standard, or professional."
        )

    minimum_requirements = project.get("minimum_requirements", 0)
    if not isinstance(minimum_requirements, int) or minimum_requirements < 0:
        raise AnalysisError("'project.minimum_requirements' must be a non-negative integer.")

    selected = require_list(data, "selected_modules")
    if not selected:
        raise AnalysisError("Select at least one output module.")
    if any(not isinstance(item, str) for item in selected):
        raise AnalysisError("Every selected module name must be a string.")

    duplicate_modules = sorted({name for name in selected if selected.count(name) > 1})
    if duplicate_modules:
        raise AnalysisError(
            "Duplicate selected module names: " + ", ".join(duplicate_modules)
        )

    unknown = sorted(set(selected) - set(MODULE_FILES))
    if unknown:
        raise AnalysisError(
            "Unknown module(s): "
            + ", ".join(unknown)
            + ". Valid modules: "
            + ", ".join(sorted(MODULE_FILES))
        )

    requirements = require_list(data, "requirements")
    seen_ids: set[str] = set()
    for index, requirement in enumerate(requirements, start=1):
        if not isinstance(requirement, dict):
            raise AnalysisError(f"Requirement {index} must be an object.")
        missing = REQUIRED_REQUIREMENT_FIELDS - set(requirement)
        if missing:
            raise AnalysisError(
                f"Requirement {index} is missing: {', '.join(sorted(missing))}"
            )
        requirement_id = str(requirement["id"]).strip()
        if requirement_id in seen_ids:
            raise AnalysisError(f"Duplicate requirement ID: {requirement_id}")
        seen_ids.add(requirement_id)

        confidence = str(requirement["confidence"]).strip().lower()
        if confidence not in CONFIDENCE_VALUES:
            raise AnalysisError(
                f"Requirement {requirement_id} has invalid confidence '{confidence}'."
            )
        category = str(requirement["category"]).strip().lower()
        if category not in REQUIREMENT_CATEGORIES:
            raise AnalysisError(
                f"Requirement {requirement_id} has invalid category '{category}'."
            )
        statement = str(requirement["statement"]).strip()
        if not re.match(r"^the\s+.+?\s+(?:must|shall)\s+\S+", statement, re.IGNORECASE):
            raise AnalysisError(
                f"Requirement {requirement_id} must use 'The [system] must/shall ...'."
            )
        if not str(requirement["rationale"]).strip():
            raise AnalysisError(f"Requirement {requirement_id} must have a rationale.")

    if "requirements" in selected and len(requirements) < minimum_requirements:
        raise AnalysisError(
            f"This project requires at least {minimum_requirements} requirement "
            "records when the requirements module is selected."
        )

    if "fishbone" in selected:
        fishbone = require_object(data, "fishbone")
        categories = fishbone.get("categories")
        if not str(fishbone.get("problem", "")).strip():
            raise AnalysisError("'fishbone.problem' must not be empty.")
        if not isinstance(categories, list) or len(categories) < 4:
            raise AnalysisError("Fishbone output requires at least four categories.")
        for category in categories:
            if not isinstance(category, dict) or len(category.get("causes", [])) < 2:
                raise AnalysisError(
                    "Each fishbone category must contain a name and at least two causes."
                )

    if "context" in selected:
        context = require_object(data, "context")
        if not str(context.get("system", "")).strip():
            raise AnalysisError("'context.system' must not be empty.")
        if not isinstance(context.get("actors"), list) or not context["actors"]:
            raise AnalysisError("'context.actors' must contain at least one actor.")
        if not isinstance(context.get("flows"), list) or not context["flows"]:
            raise AnalysisError("'context.flows' must contain at least one flow.")

    if "use-cases" in selected:
        use_cases = require_list(data, "use_cases")
        if not use_cases:
            raise AnalysisError("'use_cases' must contain at least one use case.")
        seen_use_case_ids: set[str] = set()
        for index, use_case in enumerate(use_cases, start=1):
            if not isinstance(use_case, dict):
                raise AnalysisError(f"Use case {index} must be an object.")
            missing = REQUIRED_USE_CASE_FIELDS - set(use_case)
            if missing:
                raise AnalysisError(
                    f"Use case {index} is missing: {', '.join(sorted(missing))}"
                )
            use_case_id = str(use_case["id"]).strip()
            if use_case_id in seen_use_case_ids:
                raise AnalysisError(f"Duplicate use-case ID: {use_case_id}")
            seen_use_case_ids.add(use_case_id)
            dangling = sorted(set(use_case["related_requirements"]) - seen_ids)
            if dangling:
                raise AnalysisError(
                    f"Use case {use_case_id} references unknown requirement(s): "
                    + ", ".join(dangling)
                )

    if "activity" in selected:
        activity = require_object(data, "activity")
        if not str(activity.get("start", "")).strip():
            raise AnalysisError("'activity.start' must not be empty.")
        if not isinstance(activity.get("steps"), list) or not activity["steps"]:
            raise AnalysisError("'activity.steps' must contain at least one step.")

    if "wireframe" in selected:
        wireframe = require_object(data, "wireframe")
        if not isinstance(wireframe.get("screens"), list) or not wireframe["screens"]:
            raise AnalysisError("'wireframe.screens' must contain at least one screen.")
        traceable_ids = seen_ids | {
            str(use_case.get("id")) for use_case in data.get("use_cases", [])
        }
        for screen in wireframe["screens"]:
            for component in screen.get("components", []):
                dangling = sorted(set(component.get("trace_ids", [])) - traceable_ids)
                if dangling:
                    raise AnalysisError(
                        "Wireframe component references unknown trace ID(s): "
                        + ", ".join(dangling)
                    )

    return selected


def safe_mermaid_text(value: Any) -> str:
    """Keep Mermaid labels readable and prevent accidental syntax injection."""

    text = re.sub(r"\s+", " ", str(value)).strip()
    return text.replace('"', "'").replace("[", "(").replace("]", ")")


def node_id(prefix: str, value: Any) -> str:
    digest = hashlib.sha1(str(value).encode("utf-8")).hexdigest()[:8]
    return f"{prefix}_{digest}"


def markdown_cell(value: Any) -> str:
    text = " ".join(str(value).split())
    return text.replace("|", "\\|")


def render_requirements(data: dict[str, Any]) -> str:
    project = data["project"]
    lines = [
        f"# {project['name']} - Requirements Specification",
        "",
        f"> **Binding language:** {project.get('binding_terms', 'Must and shall are binding requirements.')}",
        "",
    ]

    category_titles = {
        "functional": "Functional Requirements",
        "quality": "Quality Requirements",
        "business": "Business Requirements",
    }
    for category, heading in category_titles.items():
        category_requirements = [
            requirement
            for requirement in data["requirements"]
            if str(requirement["category"]).lower() == category
        ]
        if not category_requirements:
            continue
        lines.extend([f"## {heading}", ""])
        for requirement in category_requirements:
            lines.extend(
                [
                    f"### {requirement['id']}",
                    "",
                    f"**Requirement:** {requirement['statement']}",
                    "",
                    f"**Rationale:** {requirement['rationale']}",
                    "",
                    "| Priority | Evidence / source | Acceptance check | Confidence |",
                    "|---|---|---|---|",
                    "| "
                    + " | ".join(
                        markdown_cell(requirement[field])
                        for field in ("priority", "evidence", "acceptance", "confidence")
                    )
                    + " |",
                    "",
                ]
            )

    lines.extend(["", "## Open questions", ""])
    for question in data.get("open_questions", []):
        lines.append(f"- {question}")
    lines.append("")
    return "\n".join(lines)


def render_fishbone(data: dict[str, Any]) -> str:
    fishbone = data["fishbone"]
    effect_id = "EFFECT"
    lines = [
        "flowchart LR",
        f'    {effect_id}(["{safe_mermaid_text(fishbone["problem"])}"])',
    ]
    for category_index, category in enumerate(fishbone["categories"], start=1):
        category_id = f"CAT{category_index}"
        lines.append(
            f'    {category_id}["{safe_mermaid_text(category["name"])}"] --> {effect_id}'
        )
        for cause_index, cause in enumerate(category["causes"], start=1):
            cause_id = f"C{category_index}_{cause_index}"
            lines.append(
                f'    {cause_id}["{safe_mermaid_text(cause)}"] --> {category_id}'
            )
    lines.extend(
        [
            "    classDef effect fill:#fee2e2,stroke:#991b1b,stroke-width:2px;",
            "    classDef category fill:#dbeafe,stroke:#1d4ed8;",
            f"    class {effect_id} effect;",
            "    class "
            + ",".join(f"CAT{i}" for i in range(1, len(fishbone["categories"]) + 1))
            + " category;",
            "",
        ]
    )
    return "\n".join(lines)


def render_context(data: dict[str, Any]) -> str:
    context = data["context"]
    system_name = str(context["system"])
    identifiers = {system_name: "SYSTEM"}
    lines = [
        "flowchart LR",
        "    subgraph BOUNDARY[System boundary]",
        f'        SYSTEM["{safe_mermaid_text(system_name)}"]',
        "    end",
    ]
    for actor in context["actors"]:
        actor_key = node_id("ACT", actor)
        identifiers[str(actor)] = actor_key
        lines.append(f'    {actor_key}["{safe_mermaid_text(actor)}"]')
    for flow in context["flows"]:
        source = identifiers.get(str(flow.get("from")))
        target = identifiers.get(str(flow.get("to")))
        if not source or not target:
            raise AnalysisError(
                "Context flow references an unknown endpoint: "
                f"{flow.get('from')} -> {flow.get('to')}"
            )
        lines.append(
            f'    {source} -->|"{safe_mermaid_text(flow.get("label", "flow"))}"| {target}'
        )
    lines.append("")
    return "\n".join(lines)


def render_use_cases(data: dict[str, Any]) -> str:
    lines = [f"# {data['project']['name']} - Use-Case Descriptions", ""]
    for use_case in data["use_cases"]:
        lines.extend(
            [
                f"## {use_case['id']} - {use_case['name']}",
                "",
                f"**Primary actor:** {use_case['primary_actor']}",
                "",
                f"**Goal:** {use_case['goal']}",
                "",
                f"**Trigger:** {use_case['trigger']}",
                "",
                "### Stakeholders and interests",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in use_case.get("stakeholders", []))
        lines.extend(
            [
                "",
                "### Preconditions",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in use_case.get("preconditions", []))
        lines.extend(["", "### Main flow", ""])
        lines.extend(
            f"{index}. {item}"
            for index, item in enumerate(use_case.get("main_flow", []), start=1)
        )
        lines.extend(["", "### Alternative and exception flows", ""])
        lines.extend(f"- {item}" for item in use_case.get("alternatives", []))
        lines.extend(f"- {item}" for item in use_case.get("exceptions", []))
        lines.extend(["", "### Postconditions", ""])
        lines.extend(f"- {item}" for item in use_case.get("postconditions", []))
        lines.extend(["", "### Business rules", ""])
        lines.extend(f"- {item}" for item in use_case.get("business_rules", []))
        related = ", ".join(use_case.get("related_requirements", []))
        lines.extend(["", f"**Related requirements:** {related}", ""])
    return "\n".join(lines)


def render_activity(data: dict[str, Any]) -> str:
    activity = data["activity"]
    steps = {str(step["id"]): step for step in activity["steps"]}
    start = str(activity["start"])
    if start not in steps:
        raise AnalysisError(f"Activity start step '{start}' does not exist.")

    lines = [
        "flowchart TD",
        f'    START(["Start: {safe_mermaid_text(activity.get("title", "Activity"))}"])',
        "    END_NODE([End])",
    ]
    for step_id, step in steps.items():
        label = safe_mermaid_text(step.get("label", step_id))
        if "condition" in step:
            condition = safe_mermaid_text(step["condition"])
            lines.append(f'    {step_id}{{"{label}: {condition}"}}')
        else:
            lines.append(f'    {step_id}["{label}"]')

    lines.append(f"    START --> {start}")
    for step_id, step in steps.items():
        if "condition" in step:
            for branch_name in ("yes", "no"):
                target = str(step.get(branch_name, ""))
                if not target:
                    raise AnalysisError(
                        f"Decision step '{step_id}' is missing '{branch_name}'."
                    )
                target_id = "END_NODE" if target == "END" else target
                if target != "END" and target not in steps:
                    raise AnalysisError(
                        f"Decision step '{step_id}' references unknown step '{target}'."
                    )
                lines.append(f"    {step_id} -->|{branch_name.title()}| {target_id}")
        else:
            target = str(step.get("next", ""))
            if not target:
                raise AnalysisError(f"Activity step '{step_id}' has no next target.")
            target_id = "END_NODE" if target == "END" else target
            if target != "END" and target not in steps:
                raise AnalysisError(
                    f"Activity step '{step_id}' references unknown step '{target}'."
                )
            lines.append(f"    {step_id} --> {target_id}")
    lines.append("")
    return "\n".join(lines)


def render_component(component: dict[str, Any]) -> str:
    kind = str(component.get("kind", "text"))
    label = html.escape(str(component.get("label", "")))
    element_id = "field-" + hashlib.sha1(label.encode("utf-8")).hexdigest()[:8]

    trace_ids = ", ".join(str(item) for item in component.get("trace_ids", []))
    trace = f'<span class="trace">Trace: {html.escape(trace_ids)}</span>' if trace_ids else ""

    if kind == "heading":
        return f"<h3>{label}</h3>{trace}"
    if kind == "text":
        return f"<p>{label}</p>{trace}"
    if kind == "note":
        return f'<p class="note" role="note">{label}</p>{trace}'
    if kind == "input":
        input_type = str(component.get("input_type", "multiline")).lower()
        if input_type != "multiline":
            allowed_types = {"text", "email", "tel", "url", "number", "date", "time"}
            if input_type not in allowed_types:
                raise AnalysisError(f"Unsupported wireframe input type: {input_type}")
            return (
                f'<label for="{element_id}">{label}</label>'
                f'<input id="{element_id}" type="{input_type}">{trace}'
            )
        return (
            f'<label for="{element_id}">{label}</label>'
            f'<textarea id="{element_id}" rows="4" placeholder="Enter details"></textarea>{trace}'
        )
    if kind == "select":
        options = "".join(
            f"<option>{html.escape(str(option))}</option>"
            for option in component.get("options", [])
        )
        return (
            f'<label for="{element_id}">{label}</label>'
            f'<select id="{element_id}"><option value="">Select an option</option>{options}</select>{trace}'
        )
    if kind == "button":
        return f'<button type="button">{label}</button>{trace}'
    if kind == "list":
        items = "".join(
            f"<li><label><input type=\"radio\" name=\"slot\"> "
            f"{html.escape(str(item))}</label></li>"
            for item in component.get("items", [])
        )
        return f'<fieldset><legend>{label}</legend><ul class="choices">{items}</ul></fieldset>{trace}'
    raise AnalysisError(f"Unsupported wireframe component kind: {kind}")


def render_wireframe(data: dict[str, Any]) -> str:
    wireframe = data["wireframe"]
    cards = []
    for screen_index, screen in enumerate(wireframe["screens"], start=1):
        components = "\n".join(
            render_component(component) for component in screen.get("components", [])
        )
        cards.append(
            f"""<section class="screen" aria-labelledby="screen-{screen_index}">
  <div class="screen-tag">Screen {screen_index}</div>
  <h2 id="screen-{screen_index}">{html.escape(str(screen.get('name', 'Screen')))}</h2>
  <div class="screen-body">
    {components}
  </div>
</section>"""
        )

    title = html.escape(str(wireframe.get("title", "Requirements wireframe")))
    body = "\n".join(cards)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #f4f6f8; color: #172033; overflow-wrap: anywhere; }}
    header {{ padding: 2rem max(1rem, calc((100% - 1120px) / 2)); background: #173f5f; color: white; }}
    header p {{ max-width: 70ch; margin-bottom: 0; }}
    main {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; max-width: 1120px; margin: 0 auto; padding: 1.5rem 1rem 3rem; }}
    .screen {{ background: white; border: 2px solid #b8c2cc; border-radius: 14px; box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08); overflow: hidden; }}
    .screen-tag {{ display: inline-block; margin: 1rem 1rem 0; padding: 0.25rem 0.5rem; background: #e6eef5; border-radius: 999px; font-size: 0.8rem; font-weight: 700; }}
    .screen > h2 {{ margin: 0.75rem 1rem; font-size: 1.25rem; }}
    .screen-body {{ border-top: 1px solid #d8dee5; padding: 1rem; }}
    h3 {{ margin-top: 0; }}
    label, legend {{ display: block; margin-top: 0.9rem; font-weight: 700; }}
    input, textarea, select {{ width: 100%; margin-top: 0.35rem; padding: 0.7rem; border: 2px solid #7c8794; border-radius: 6px; background: white; color: #172033; }}
    button {{ width: 100%; margin-top: 0.8rem; padding: 0.75rem; border: 2px solid #173f5f; border-radius: 6px; background: #173f5f; color: white; font-weight: 700; }}
    button + button {{ background: white; color: #173f5f; }}
    .note {{ padding: 0.75rem; border-left: 4px solid #b45309; background: #fff7ed; }}
    fieldset {{ margin: 0.9rem 0 0; border: 1px solid #9aa5b1; border-radius: 6px; }}
    .choices {{ list-style: none; padding: 0; }}
    .choices label {{ font-weight: 400; }}
    .trace {{ display: block; margin-top: 0.3rem; color: #4b5563; font-size: 0.72rem; }}
    :focus-visible {{ outline: 4px solid #f59e0b; outline-offset: 2px; }}
    @media (max-width: 520px) {{
      header {{ padding: 1.25rem 1rem; }}
      header h1 {{ font-size: 1.65rem; }}
      main {{ grid-template-columns: minmax(0, 1fr); padding: 1rem; }}
      .screen {{ min-width: 0; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p>Low-fidelity review artefact. Controls are illustrative and intentionally have no JavaScript behaviour.</p>
  </header>
  <main>
    {body}
  </main>
</body>
</html>
"""


RENDERERS = {
    "requirements": render_requirements,
    "fishbone": render_fishbone,
    "context": render_context,
    "use-cases": render_use_cases,
    "activity": render_activity,
    "wireframe": render_wireframe,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def write_traceability(data: dict[str, Any], output_path: Path) -> None:
    use_case_links: dict[str, list[str]] = {}
    for use_case in data.get("use_cases", []):
        for requirement_id in use_case.get("related_requirements", []):
            use_case_links.setdefault(str(requirement_id), []).append(str(use_case["id"]))

    with output_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "requirement_id",
                "category",
                "evidence",
                "use_cases",
                "selected_artefacts",
                "confidence",
            ]
        )
        selected_artefacts = ";".join(data["selected_modules"])
        for requirement in data["requirements"]:
            requirement_id = str(requirement["id"])
            writer.writerow(
                [
                    requirement_id,
                    requirement["category"],
                    requirement["evidence"],
                    ";".join(use_case_links.get(requirement_id, [])),
                    selected_artefacts,
                    requirement["confidence"],
                ]
            )


def write_review_index(
    data: dict[str, Any],
    out_dir: Path,
    module_hashes: dict[str, str],
    quality_warnings: list[str],
    traceguard_report: dict[str, Any],
) -> None:
    lines = [
        f"# {data['project']['name']} - Review Index",
        "",
        f"**Status:** {data['project'].get('analysis_status', 'draft for review')}",
        "",
        f"**Review mode:** {data['project'].get('review_mode', 'standard')}",
        "",
        "## Start here",
        "",
        str(data.get("plain_language_summary", "Review the assumptions, open questions, and selected modules below.")),
        "",
        "## Generated modules",
        "",
        "| Module | What to review | File | SHA-256 |",
        "|---|---|---|---|",
    ]
    for module in data["selected_modules"]:
        module_file = MODULE_FILES[module]
        file_hash = module_hashes.get(module, "not generated in this run")
        lines.append(
            f"| {module} | {MODULE_DESCRIPTIONS[module]} | "
            f"`{module_file}` | `{file_hash}` |"
        )

    traceguard_summary = traceguard_report["summary"]
    lines.extend(
        [
            "",
            "## TraceGuard",
            "",
            f"**Decision state:** `{traceguard_report['status']}`",
            "",
            f"- Exact source spans: {traceguard_summary['exact_source_spans']}",
            f"- Errors: {traceguard_summary['error']}",
            f"- Warnings: {traceguard_summary['warning']}",
            f"- Abstentions awaiting named approval: {traceguard_summary['abstain']}",
            "- Review `traceguard.md` for human-readable findings and `traceguard.json` for automation.",
        ]
    )

    glossary = data.get("glossary", [])
    if glossary:
        lines.extend(["", "## Glossary", "", "| Term | Plain-language meaning |", "|---|---|"])
        for item in glossary:
            lines.append(
                f"| {markdown_cell(item.get('term', ''))} | "
                f"{markdown_cell(item.get('meaning', ''))} |"
            )

    lines.extend(
        [
            "",
            "## Reviewer checklist",
            "",
            "- Does any output contradict the supplied scenario or stakeholder evidence?",
            "- Which assumptions can be confirmed, rejected, or rewritten?",
            "- Which open questions block a design or scope decision?",
            "- Does every requirement have a clear rationale, evidence, and acceptance check?",
            "- Are the system boundary, actors, flows, and terminology consistent across modules?",
            "- Does the wireframe support the required user goals without introducing unsupported features?",
        ]
    )

    lines.extend(["", "## Assumptions", ""])
    lines.extend(f"- {item}" for item in data.get("assumptions", []))
    lines.extend(["", "## Open questions", ""])
    lines.extend(f"- {item}" for item in data.get("open_questions", []))
    lines.extend(["", "## Automated quality warnings", ""])
    if quality_warnings:
        lines.extend(f"- {item}" for item in quality_warnings)
    else:
        lines.append("- No heuristic warnings were detected.")
    lines.append("")
    write_text(out_dir / "review-index.md", "\n".join(lines))


def lint_requirement_warnings(data: dict[str, Any]) -> list[str]:
    """Return non-blocking warnings for requirement statements worth review."""

    action_after_conjunction = re.compile(
        r"\b(?:and|or)\s+(?:allow|create|delete|display|explain|generate|notify|"
        r"provide|record|reject|restrict|route|send|store|update|validate)\b",
        flags=re.IGNORECASE,
    )
    warnings = []
    for requirement in data.get("requirements", []):
        statement = str(requirement.get("statement", ""))
        if action_after_conjunction.search(statement):
            warnings.append(
                f"{requirement.get('id', 'Unknown ID')} may contain more than one "
                "obligation; review whether it should be split."
            )
    return warnings


def existing_module_hashes(out_dir: Path, selected: Iterable[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for module in selected:
        path = out_dir / MODULE_FILES[module]
        if path.exists():
            hashes[module] = sha256_file(path)
    return hashes


def materialise(data: dict[str, Any], out_dir: Path, only: str | None) -> None:
    selected = validate_analysis(data)
    if only and only not in selected:
        raise AnalysisError(
            f"Cannot regenerate '{only}' because it is not in selected_modules."
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    before_hashes = existing_module_hashes(out_dir, selected)
    targets = [only] if only else selected

    canonical_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    canonical_path = out_dir / "analysis.json"
    rollback_path: Path | None = None
    if only and canonical_path.exists():
        previous_text = canonical_path.read_text(encoding="utf-8")
        if previous_text != canonical_text:
            history_dir = out_dir / ".traceguard" / "history"
            history_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            rollback_path = history_dir / f"{timestamp}-analysis.json"
            rollback_path.write_text(previous_text, encoding="utf-8", newline="\n")

    for module in targets:
        output_path = out_dir / MODULE_FILES[module]
        write_text(output_path, RENDERERS[module](data))

    # The canonical analysis and index may change during a targeted revision;
    # non-target module files remain byte-for-byte untouched.
    write_text(canonical_path, canonical_text)
    write_traceability(data, out_dir / "traceability.csv")
    traceguard_report = write_audit(data, out_dir)

    after_hashes = existing_module_hashes(out_dir, selected)
    quality_warnings = lint_requirement_warnings(data)
    untouched = []
    if only:
        for module in selected:
            if module == only or module not in before_hashes:
                continue
            if before_hashes[module] != after_hashes.get(module):
                raise AnalysisError(
                    f"Non-target module changed unexpectedly during revision: {module}"
                )
            untouched.append(module)

    manifest = {
        "schema_version": "0.3",
        "project": data["project"]["name"],
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "selected_modules": selected,
        "revision_target": only,
        "untouched_modules_verified": untouched,
        "quality_warnings": quality_warnings,
        "traceguard": {
            "status": traceguard_report["status"],
            "summary": traceguard_report["summary"],
            "human_report": "traceguard.md",
            "machine_report": "traceguard.json",
            "rollback_snapshot": (
                str(rollback_path.relative_to(out_dir)).replace("\\", "/")
                if rollback_path
                else None
            ),
        },
        "files": {
            module: {
                "path": MODULE_FILES[module],
                "sha256": after_hashes.get(module),
            }
            for module in selected
            if module in after_hashes
        },
    }
    write_text(out_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    write_review_index(
        data,
        out_dir,
        after_hashes,
        quality_warnings,
        traceguard_report,
    )


def main() -> int:
    args = parse_args()
    try:
        analysis = load_analysis(args.analysis)
        materialise(analysis, args.out, args.only)
    except AnalysisError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    target_text = f"module '{args.only}'" if args.only else "selected modules"
    print(f"Generated {target_text} in {args.out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

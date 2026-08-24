#!/usr/bin/env python3
"""Audit cross-artefact traceability and preview controlled changes.

TraceGuard is deterministic and intentionally uses only the Python standard
library. It never decides whether a requirement is semantically correct; it
surfaces missing evidence, inconsistent links, and approval gates for review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ACTIONABLE_COMPONENTS = {"button", "input", "list", "select"}
MODULE_KEYS = {
    "problem-vision-scope": "problem_vision_scope",
    "requirements": "requirements",
    "fishbone": "fishbone",
    "context": "context",
    "domain-model": "domain_model",
    "use-cases": "use_cases",
    "activity": "activity",
    "wireframe": "wireframe",
    "feasibility": "feasibility",
    "data-io": "data_io",
    "lifecycle-roadmap": "lifecycle_roadmap",
}


class TraceGuardError(ValueError):
    """Raised when TraceGuard cannot process the supplied analysis."""


def _normalise(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value)).strip().casefold()


def _finding(
    check_id: str,
    severity: str,
    message: str,
    *,
    element_id: str | None = None,
    modules: Iterable[str] = (),
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "check_id": check_id,
        "severity": severity,
        "message": message,
        "affected_modules": sorted(set(modules)),
    }
    if element_id:
        result["element_id"] = element_id
    if details:
        result["details"] = details
    return result


def _source_map(data: dict[str, Any]) -> dict[str, str]:
    sources: dict[str, str] = {}
    for source in data.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("id", "")).strip()
        text = str(source.get("text", ""))
        if source_id and text:
            sources[source_id] = text
    return sources


def _evidence_spans(data: dict[str, Any], requirement: dict[str, Any]) -> list[dict[str, Any]]:
    direct = requirement.get("evidence_spans")
    if isinstance(direct, list):
        return [item for item in direct if isinstance(item, dict)]

    configured = data.get("traceguard", {}).get("evidence_spans", {})
    spans = configured.get(str(requirement.get("id", "")), [])
    return [item for item in spans if isinstance(item, dict)] if isinstance(spans, list) else []


def _audit_evidence(data: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    sources = _source_map(data)

    for requirement in data.get("requirements", []):
        requirement_id = str(requirement.get("id", "unknown"))
        spans = _evidence_spans(data, requirement)
        if not spans:
            severity = "error" if requirement.get("confidence") == "explicit" else "warning"
            findings.append(
                _finding(
                    "TG-EVIDENCE-MISSING",
                    severity,
                    f"{requirement_id} has no exact source-span evidence.",
                    element_id=requirement_id,
                    modules=["requirements", "traceability"],
                )
            )
            continue

        for span_index, span in enumerate(spans, start=1):
            source_id = str(span.get("source_id", "")).strip()
            quote = str(span.get("quote", ""))
            source_text = sources.get(source_id)
            if source_text is None:
                findings.append(
                    _finding(
                        "TG-EVIDENCE-SOURCE",
                        "error",
                        f"{requirement_id} references unknown source {source_id or '(blank)' }.",
                        element_id=requirement_id,
                        modules=["requirements", "traceability"],
                    )
                )
                continue

            start = source_text.find(quote) if quote else -1
            if start < 0:
                findings.append(
                    _finding(
                        "TG-EVIDENCE-QUOTE",
                        "error",
                        f"{requirement_id} evidence quote is not an exact span in {source_id}.",
                        element_id=requirement_id,
                        modules=["requirements", "traceability"],
                        details={"span_index": span_index, "quote": quote},
                    )
                )
                continue

            end = start + len(quote)
            supplied_start = span.get("start")
            supplied_end = span.get("end")
            if supplied_start is not None and supplied_start != start:
                findings.append(
                    _finding(
                        "TG-EVIDENCE-OFFSET",
                        "error",
                        f"{requirement_id} supplied start offset does not match {source_id}.",
                        element_id=requirement_id,
                        modules=["requirements", "traceability"],
                    )
                )
            if supplied_end is not None and supplied_end != end:
                findings.append(
                    _finding(
                        "TG-EVIDENCE-OFFSET",
                        "error",
                        f"{requirement_id} supplied end offset does not match {source_id}.",
                        element_id=requirement_id,
                        modules=["requirements", "traceability"],
                    )
                )
            resolved.append(
                {
                    "element_id": requirement_id,
                    "source_id": source_id,
                    "quote": quote,
                    "start": start,
                    "end": end,
                }
            )

    return findings, resolved


def _audit_actors(data: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    context_actors = {
        _normalise(actor) for actor in data.get("context", {}).get("actors", [])
    }
    for use_case in data.get("use_cases", []):
        actor = str(use_case.get("primary_actor", "")).strip()
        if actor and _normalise(actor) not in context_actors:
            findings.append(
                _finding(
                    "TG-ACTOR-CONTEXT",
                    "error",
                    f"Use case {use_case.get('id', 'unknown')} uses actor '{actor}', which is absent from the context model.",
                    element_id=str(use_case.get("id", "")),
                    modules=["context", "use-cases"],
                )
            )
    return findings


def _known_trace_ids(data: dict[str, Any]) -> set[str]:
    return {
        str(item.get("id"))
        for key in ("requirements", "use_cases")
        for item in data.get(key, [])
        if isinstance(item, dict) and item.get("id")
    }


def _audit_activity(data: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    known_ids = _known_trace_ids(data)
    for step in data.get("activity", {}).get("steps", []):
        step_id = str(step.get("id", "unknown"))
        traces = {str(item) for item in step.get("trace_ids", [])}
        if not traces:
            findings.append(
                _finding(
                    "TG-ACTIVITY-TRACE",
                    "error",
                    f"Activity step {step_id} has no supporting requirement or use-case trace.",
                    element_id=step_id,
                    modules=["activity", "requirements", "use-cases"],
                )
            )
        dangling = sorted(traces - known_ids)
        if dangling:
            findings.append(
                _finding(
                    "TG-ACTIVITY-DANGLING",
                    "error",
                    f"Activity step {step_id} references unknown trace IDs: {', '.join(dangling)}.",
                    element_id=step_id,
                    modules=["activity"],
                )
            )
    return findings


def _audit_wireframe(data: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    known_ids = _known_trace_ids(data)
    for screen in data.get("wireframe", {}).get("screens", []):
        screen_name = str(screen.get("name", "unnamed screen"))
        for component in screen.get("components", []):
            kind = str(component.get("kind", "text"))
            traces = {str(item) for item in component.get("trace_ids", [])}
            label = str(component.get("label", "unnamed control"))
            if kind in ACTIONABLE_COMPONENTS and not traces:
                findings.append(
                    _finding(
                        "TG-WIREFRAME-TRACE",
                        "error",
                        f"Actionable control '{label}' on '{screen_name}' has no trace.",
                        modules=["wireframe", "requirements", "use-cases"],
                        details={"screen": screen_name, "component_kind": kind},
                    )
                )
            dangling = sorted(traces - known_ids)
            if dangling:
                findings.append(
                    _finding(
                        "TG-WIREFRAME-DANGLING",
                        "error",
                        f"Wireframe control '{label}' references unknown trace IDs: {', '.join(dangling)}.",
                        modules=["wireframe"],
                    )
                )
    return findings


def _audit_terminology(data: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    configured = data.get("traceguard", {}).get("terminology", [])
    module_text = {
        module: json.dumps(data.get(key, {}), ensure_ascii=False)
        for module, key in MODULE_KEYS.items()
    }
    for item in configured:
        if not isinstance(item, dict):
            continue
        canonical = str(item.get("canonical", "")).strip()
        for alias in item.get("aliases", []):
            alias_text = str(alias).strip()
            if not canonical or not alias_text:
                continue
            affected = [
                module
                for module, text in module_text.items()
                if re.search(rf"\b{re.escape(alias_text)}\b", text, re.IGNORECASE)
            ]
            if affected:
                findings.append(
                    _finding(
                        "TG-TERMINOLOGY",
                        "warning",
                        f"Use canonical term '{canonical}' instead of alias '{alias_text}'.",
                        modules=affected,
                        details={"canonical": canonical, "alias": alias_text},
                    )
                )
    return findings


def _audit_approval(data: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    traceguard = data.get("traceguard", {})
    high_impact_ids = {str(item) for item in traceguard.get("high_impact_ids", [])}
    approvals = {
        str(item.get("element_id")): item
        for item in traceguard.get("approvals", [])
        if isinstance(item, dict)
    }
    for element_id in sorted(high_impact_ids):
        approval = approvals.get(element_id, {})
        named_reviewer = str(approval.get("reviewer", "")).strip()
        decision = str(approval.get("decision", "")).strip().lower()
        if not named_reviewer or decision != "approved":
            findings.append(
                _finding(
                    "TG-APPROVAL-ABSTAIN",
                    "abstain",
                    f"{element_id} is high-impact and remains abstained until a named reviewer approves it.",
                    element_id=element_id,
                    modules=affected_modules(data, element_id),
                )
            )
    return findings


def affected_modules(data: dict[str, Any], element_id: str) -> list[str]:
    """Return modules that contain or reference a stable element identifier."""

    affected: set[str] = set()
    needle = str(element_id)
    for module, key in MODULE_KEYS.items():
        serialised = json.dumps(data.get(key, {}), ensure_ascii=False)
        if needle in serialised:
            affected.add(module)
    if needle.startswith(("FR-", "QR-", "BR-")):
        affected.add("requirements")
    return sorted(affected)


def audit_analysis(data: dict[str, Any]) -> dict[str, Any]:
    evidence_findings, resolved_spans = _audit_evidence(data)
    findings = evidence_findings
    findings.extend(_audit_actors(data))
    findings.extend(_audit_activity(data))
    findings.extend(_audit_wireframe(data))
    findings.extend(_audit_terminology(data))
    findings.extend(_audit_approval(data))

    counts = {
        level: sum(1 for item in findings if item["severity"] == level)
        for level in ("error", "warning", "abstain")
    }
    if counts["abstain"]:
        status = "abstain"
    elif counts["error"] or counts["warning"]:
        status = "review_required"
    else:
        status = "pass"

    return {
        "schema_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "project": data.get("project", {}).get("name", "Unnamed project"),
        "status": status,
        "summary": counts | {"exact_source_spans": len(resolved_spans)},
        "resolved_source_spans": resolved_spans,
        "findings": findings,
    }


def render_audit_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"# {report['project']} - TraceGuard Audit",
        "",
        f"**Decision state:** `{report['status']}`",
        "",
        "## Summary",
        "",
        f"- Exact source spans resolved: {summary['exact_source_spans']}",
        f"- Errors: {summary['error']}",
        f"- Warnings: {summary['warning']}",
        f"- Abstentions awaiting named approval: {summary['abstain']}",
        "",
        "## Findings",
        "",
    ]
    if not report["findings"]:
        lines.append("- All configured TraceGuard checks passed.")
    for item in report["findings"]:
        modules = ", ".join(item.get("affected_modules", [])) or "support files"
        lines.append(
            f"- **{item['severity'].upper()} {item['check_id']}**: "
            f"{item['message']} Affected: {modules}."
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "TraceGuard verifies configured evidence spans, links, terminology and approval gates. "
            "It does not prove that stakeholder statements or generated requirements are semantically correct.",
            "",
        ]
    )
    return "\n".join(lines)


def preview_impact(
    data: dict[str, Any],
    element_id: str,
    change_summary: str,
    requested_action: str,
) -> dict[str, Any]:
    if requested_action not in {"propagate", "local-override", "cancel"}:
        raise TraceGuardError(
            "requested_action must be propagate, local-override, or cancel"
        )
    modules = affected_modules(data, element_id)
    return {
        "schema_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "element_id": element_id,
        "change_summary": change_summary,
        "requested_action": requested_action,
        "affected_modules": modules,
        "patch_set": [
            {
                "module": module,
                "operation": "review-and-regenerate" if requested_action == "propagate" else "preserve",
            }
            for module in modules
        ],
        "requires_confirmation": requested_action != "cancel" and len(modules) > 1,
        "rollback_policy": "Snapshot analysis.json before an approved revision is materialised.",
    }


def write_audit(data: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    report = audit_analysis(data)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "traceguard.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "traceguard.md").write_text(
        render_audit_markdown(report), encoding="utf-8", newline="\n"
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TraceGuard audits and impact previews.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Audit evidence and cross-artefact invariants")
    audit.add_argument("analysis", type=Path)
    audit.add_argument("--out", type=Path, required=True)

    impact = subparsers.add_parser("impact", help="Preview the scope of a proposed change")
    impact.add_argument("analysis", type=Path)
    impact.add_argument("--element", required=True)
    impact.add_argument("--change", required=True)
    impact.add_argument(
        "--action",
        choices=["propagate", "local-override", "cancel"],
        default="propagate",
    )
    impact.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TraceGuardError(f"Unable to read analysis JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise TraceGuardError("Analysis JSON must contain a top-level object.")
    return value


def main() -> int:
    args = parse_args()
    try:
        data = _load(args.analysis)
        if args.command == "audit":
            report = write_audit(data, args.out)
            print(f"TraceGuard status: {report['status']}")
        else:
            preview = preview_impact(data, args.element, args.change, args.action)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(
                json.dumps(preview, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"Impact preview written to {args.out.resolve()}")
    except TraceGuardError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

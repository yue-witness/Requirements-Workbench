#!/usr/bin/env python3
"""Install the workbench into AI coding hosts other than the plugin marketplaces.

Codex and Claude Code install the plugin from their marketplaces. Other hosts
(Antigravity, DeepSeek Harness, Gemini CLI, Cursor, VS Code, Windsurf, Claude
Desktop, or any MCP host)
load two portable pieces instead, and this script wires both up:

- the MCP server (mcp/server.py), added to the host's MCP configuration; it
  also serves the workflows as MCP prompts and runs generation and TraceGuard;
- the Agent Skills folders (skills/*/SKILL.md), copied into the host's skills
  directory for hosts that support SKILL.md.

Existing configuration is merged, never replaced, and backed up first. Only the
standard library is used.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = PLUGIN_ROOT / "mcp" / "server.py"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
SERVER_KEY = "requirements_analysis_workbench"
# Written into every copied skill folder: it records where the scripts live and
# marks the folder as ours, so reinstalling or uninstalling never touches a
# same-named skill that came from somewhere else.
MARKER_NAME = "plugin-root.txt"
# DeepSeek Harness takes MCP servers as rows in a YAML patch layer. Without a
# YAML library the installer owns one delimited block and never edits outside it.
DSH_ENTRY_ID = "requirements-analysis-workbench"
DSH_BLOCK_START = "# >>> requirements-analysis-workbench (managed by install_agent.py)"
DSH_BLOCK_END = "# <<< requirements-analysis-workbench"


@dataclass(frozen=True)
class Target:
    label: str
    # Each returns a path for (home, workspace); None means unsupported scope.
    user_config: Callable[[Path], Path] | None
    workspace_config: Callable[[Path], Path] | None
    user_skills: Callable[[Path], Path] | None
    workspace_skills: Callable[[Path], Path] | None
    servers_key: str = "mcpServers"
    entry_type: str | None = None
    config_format: str = "json"
    note: str = ""


def _dsh_home(home: Path) -> Path:
    configured = os.environ.get("DSH_HOME")
    return Path(configured).expanduser() if configured else home / ".dsh"


def _claude_desktop_config(home: Path) -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or home / "AppData" / "Roaming")
        return base / "Claude" / "claude_desktop_config.json"
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    return home / ".config" / "Claude" / "claude_desktop_config.json"


TARGETS: dict[str, Target] = {
    "antigravity": Target(
        label="Google Antigravity",
        user_config=lambda home: home / ".gemini" / "antigravity" / "mcp_config.json",
        workspace_config=None,
        user_skills=lambda home: home / ".gemini" / "antigravity" / "skills",
        workspace_skills=lambda ws: ws / ".agents" / "skills",
        note=(
            "Antigravity reads MCP servers from its global mcp_config.json "
            "(Agent panel > MCP Servers > Manage MCP Servers > View raw config). "
            "If your version uses ~/.gemini/config/mcp_config.json, rerun with --config."
        ),
    ),
    "claude-code": Target(
        label="Claude Code (without the plugin marketplace)",
        user_config=None,
        workspace_config=lambda ws: ws / ".mcp.json",
        user_skills=lambda home: home / ".claude" / "skills",
        workspace_skills=lambda ws: ws / ".claude" / "skills",
        note=(
            "The plugin marketplace is the recommended Claude Code install. For user scope "
            "this script copies the skills; register the server with the command printed below."
        ),
    ),
    "claude-desktop": Target(
        label="Claude Desktop",
        user_config=_claude_desktop_config,
        workspace_config=None,
        user_skills=None,
        workspace_skills=None,
        note=(
            "Claude Desktop lists the workflows as MCP prompts. To add them as skills, "
            "upload each skills/<name> folder as a ZIP in Settings > Capabilities."
        ),
    ),
    "cursor": Target(
        label="Cursor",
        user_config=lambda home: home / ".cursor" / "mcp.json",
        workspace_config=lambda ws: ws / ".cursor" / "mcp.json",
        user_skills=lambda home: home / ".cursor" / "skills",
        workspace_skills=lambda ws: ws / ".cursor" / "skills",
    ),
    "dsh": Target(
        label="DeepSeek Harness (dsh)",
        user_config=lambda home: _dsh_home(home) / "cordis.patch.yml",
        workspace_config=None,
        user_skills=lambda home: _dsh_home(home) / "skills",
        workspace_skills=lambda ws: ws / ".dsh" / "skills",
        config_format="dsh-yaml",
        note=(
            "DSH loads the server from the home-level patch layer for every profile. "
            "For one profile only, rerun with "
            "--config $DSH_HOME/profiles/<profile>/cordis.patch.yml. DSH does not list MCP "
            "prompts, so keep the skills installed. Start a new DSH session to load them."
        ),
    ),
    "gemini-cli": Target(
        label="Gemini CLI",
        user_config=lambda home: home / ".gemini" / "settings.json",
        workspace_config=lambda ws: ws / ".gemini" / "settings.json",
        user_skills=lambda home: home / ".gemini" / "skills",
        workspace_skills=lambda ws: ws / ".gemini" / "skills",
        note=(
            "Alternatively install the bundled extension: "
            "gemini extensions install <path-to>/plugins/requirements-analysis-workbench"
        ),
    ),
    "vscode": Target(
        label="VS Code (GitHub Copilot agent mode)",
        user_config=None,
        workspace_config=lambda ws: ws / ".vscode" / "mcp.json",
        user_skills=None,
        workspace_skills=lambda ws: ws / ".github" / "skills",
        servers_key="servers",
        entry_type="stdio",
    ),
    "windsurf": Target(
        label="Windsurf",
        user_config=lambda home: home / ".codeium" / "windsurf" / "mcp_config.json",
        workspace_config=None,
        user_skills=None,
        workspace_skills=lambda ws: ws / ".windsurf" / "skills",
    ),
    "generic": Target(
        label="Any MCP host",
        user_config=None,
        workspace_config=None,
        user_skills=None,
        workspace_skills=None,
        note=(
            "Add the JSON below to the host's MCP configuration (most hosts use an "
            "\"mcpServers\" object). Use --config and --skills-dir to write files directly."
        ),
    ),
}


def server_entry(python: str, entry_type: str | None) -> dict[str, Any]:
    entry: dict[str, Any] = {}
    if entry_type:
        entry["type"] = entry_type
    entry["command"] = python
    entry["args"] = [str(SERVER_PATH)]
    return entry


def read_config(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.read_text(encoding="utf-8-sig").strip():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"ERROR: {path} is not plain JSON ({exc.msg} at line {exc.lineno}); "
            "it was left unchanged. Add the snippet printed by --print manually."
        ) from exc
    if not isinstance(value, dict):
        raise SystemExit(f"ERROR: {path} does not contain a JSON object; left unchanged.")
    return value


def write_config(path: Path, config: dict[str, Any], dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(path.name + ".bak")
        shutil.copy2(path, backup)
        print(f"Backed up {path} -> {backup}")
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {path}")


def update_config(
    path: Path, servers_key: str, entry: dict[str, Any] | None, dry_run: bool
) -> None:
    """Add (entry) or remove (None) the workbench server, keeping everything else."""

    config = read_config(path)
    servers = config.get(servers_key)
    if servers is None:
        servers = {}
    if not isinstance(servers, dict):
        raise SystemExit(f"ERROR: '{servers_key}' in {path} is not an object; left unchanged.")
    if entry is None:
        if SERVER_KEY not in servers:
            print(f"No {SERVER_KEY} entry in {path}")
            return
        del servers[SERVER_KEY]
    else:
        servers[SERVER_KEY] = entry
    config[servers_key] = servers
    write_config(path, config, dry_run)


def dsh_block(entry: dict[str, Any]) -> str:
    # JSON strings are valid YAML double-quoted scalars, so paths need no escaping rules.
    args = ", ".join(json.dumps(arg) for arg in entry["args"])
    return "\n".join(
        [
            DSH_BLOCK_START,
            "- insert:",
            f"    - id: {DSH_ENTRY_ID}",
            "      name: '@deepseek-ai/dsh-mcp-client'",
            "      config:",
            f"        serverName: {SERVER_KEY}",
            "        transport: stdio",
            f"        command: {json.dumps(entry['command'])}",
            f"        args: [{args}]",
            "        cwd: !!js process.cwd()",
            DSH_BLOCK_END,
            "",
        ]
    )


def _without_dsh_block(text: str) -> tuple[str, bool]:
    start = text.find(DSH_BLOCK_START)
    if start == -1:
        return text, False
    end = text.find(DSH_BLOCK_END, start)
    if end == -1:
        raise SystemExit("ERROR: the managed DSH block has no end marker; file left unchanged.")
    end = text.find("\n", end)
    end = len(text) if end == -1 else end + 1
    return text[:start] + text[end:], True


def update_dsh_patch(path: Path, entry: dict[str, Any] | None, dry_run: bool) -> None:
    """Add (entry) or remove (None) the workbench row in a DSH Cordis patch layer."""

    text = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    remaining, had_block = _without_dsh_block(text)
    if entry is None and not had_block:
        print(f"No {DSH_ENTRY_ID} entry in {path}")
        return

    meaningful = [
        line for line in remaining.splitlines() if line.strip() and not line.lstrip().startswith("#")
    ]
    if entry is not None and meaningful and not meaningful[0].startswith("-"):
        raise SystemExit(
            f"ERROR: {path} is not a block list of patch operations; it was left unchanged. "
            "Add the snippet printed by --print manually."
        )
    if entry is not None:
        if remaining and not remaining.endswith("\n"):
            remaining += "\n"
        remaining += dsh_block(entry)
    if dry_run:
        print(f"[dry-run] would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(path.name + ".bak")
        shutil.copy2(path, backup)
        print(f"Backed up {path} -> {backup}")
    path.write_text(remaining, encoding="utf-8")
    print(f"Updated {path}")


def _owned(skill_dir: Path) -> bool:
    return (skill_dir / MARKER_NAME).is_file()


def install_skills(skills_dir: Path, force: bool, dry_run: bool) -> None:
    for source in sorted(p for p in SKILLS_ROOT.iterdir() if (p / "SKILL.md").is_file()):
        destination = skills_dir / source.name
        if destination.exists() and not _owned(destination) and not force:
            raise SystemExit(
                f"ERROR: {destination} exists and was not installed by this script. "
                "Remove it or rerun with --force."
            )
        if dry_run:
            print(f"[dry-run] would copy skill {source.name} -> {destination}")
            continue
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(
            source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
        )
        (destination / MARKER_NAME).write_text(
            "Requirements Analysis Workbench plugin root (contains scripts/ and mcp/):\n"
            f"{PLUGIN_ROOT}\n",
            encoding="utf-8",
        )
        print(f"Installed skill {source.name} -> {destination}")


def remove_skills(skills_dir: Path, dry_run: bool) -> None:
    for source in sorted(p for p in SKILLS_ROOT.iterdir() if (p / "SKILL.md").is_file()):
        destination = skills_dir / source.name
        if not destination.exists():
            continue
        if not _owned(destination):
            print(f"Skipped {destination}: not installed by this script")
            continue
        if dry_run:
            print(f"[dry-run] would remove {destination}")
            continue
        shutil.rmtree(destination)
        print(f"Removed skill {destination}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add the Requirements Analysis Workbench MCP server and skills to an AI host.",
    )
    parser.add_argument("--target", required=True, choices=sorted(TARGETS))
    parser.add_argument(
        "--scope",
        choices=["user", "workspace"],
        default="user",
        help="Install for every project (user) or one project folder (workspace).",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Project folder for --scope workspace (default: current folder).",
    )
    parser.add_argument("--config", type=Path, help="Write this MCP config file instead.")
    parser.add_argument("--skills-dir", type=Path, help="Copy skills into this folder instead.")
    parser.add_argument("--no-skills", action="store_true", help="Configure the MCP server only.")
    parser.add_argument("--no-mcp", action="store_true", help="Copy the skills only.")
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python used to start the server (default: the one running this script).",
    )
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="Print the configuration snippet without writing files.")
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove the server entry and the skills this script installed.")
    parser.add_argument("--force", action="store_true",
                        help="Replace same-named skill folders not installed by this script.")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing.")
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = TARGETS[args.target]
    home = args.home.expanduser()
    workspace = args.workspace.expanduser().resolve()
    entry = server_entry(args.python, target.entry_type)
    if target.config_format == "dsh-yaml":
        snippet = dsh_block(entry).rstrip()
    else:
        snippet = json.dumps({target.servers_key: {SERVER_KEY: entry}}, indent=2)

    print(f"Target: {target.label} ({args.scope} scope)")
    if args.print_only:
        print(snippet)
        if target.note:
            print(target.note)
        return 0

    if args.scope == "user":
        config_factory, skills_factory, base = target.user_config, target.user_skills, home
    else:
        config_factory, skills_factory = target.workspace_config, target.workspace_skills
        base = workspace
    config_path = args.config or (config_factory(base) if config_factory else None)
    skills_dir = args.skills_dir or (skills_factory(base) if skills_factory else None)

    if not args.no_mcp:
        if config_path and target.config_format == "dsh-yaml":
            update_dsh_patch(
                config_path.expanduser(), None if args.uninstall else entry, args.dry_run
            )
        elif config_path:
            update_config(
                config_path.expanduser(),
                target.servers_key,
                None if args.uninstall else entry,
                args.dry_run,
            )
        elif args.target == "claude-code" and args.scope == "user":
            action = "remove --scope user " + SERVER_KEY if args.uninstall else (
                f'add --scope user {SERVER_KEY} -- "{args.python}" "{SERVER_PATH}"'
            )
            print(f"Run: claude mcp {action}")
        else:
            print("This target has no MCP config file for this scope. Add this snippet:")
            print(snippet)

    if not args.no_skills:
        if skills_dir:
            if args.uninstall:
                remove_skills(skills_dir.expanduser(), args.dry_run)
            else:
                install_skills(skills_dir.expanduser(), args.force, args.dry_run)
        elif not args.uninstall:
            print("Skills: this host has no skills folder for this scope; the workflows "
                  "are available as MCP prompts and via get_workflow_instructions.")

    if target.note:
        print(target.note)
    if not args.uninstall and not args.dry_run:
        print("Restart the host (or reload its MCP servers) to load the workbench.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

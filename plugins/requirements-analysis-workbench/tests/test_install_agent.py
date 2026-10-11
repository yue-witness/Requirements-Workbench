"""Tests for the cross-host installer and the per-host manifests."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "install_agent.py"

spec = importlib.util.spec_from_file_location("install_agent", SCRIPT_PATH)
assert spec and spec.loader
install_agent = importlib.util.module_from_spec(spec)
# Dataclasses resolve annotations through sys.modules.
sys.modules[spec.name] = install_agent
spec.loader.exec_module(install_agent)

SKILL_NAMES = ["analyze-requirements", "revise-requirements-module", "traceguard-audit"]


def run(*argv: str) -> str:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        install_agent.main(list(argv))
    return output.getvalue()


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.home = Path(self._temporary.name)

    def tearDown(self) -> None:
        self._temporary.cleanup()

    def test_antigravity_merges_config_and_copies_skills(self) -> None:
        config_path = self.home / ".gemini" / "antigravity" / "mcp_config.json"
        config_path.parent.mkdir(parents=True)
        existing = {"mcpServers": {"other": {"command": "node", "args": ["x.js"]}}}
        config_path.write_text(json.dumps(existing), encoding="utf-8")

        run("--target", "antigravity", "--home", str(self.home), "--python", "py")

        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(existing["mcpServers"]["other"], config["mcpServers"]["other"])
        entry = config["mcpServers"][install_agent.SERVER_KEY]
        self.assertEqual("py", entry["command"])
        self.assertEqual([str(install_agent.SERVER_PATH)], entry["args"])
        self.assertEqual(existing, json.loads(
            config_path.with_name("mcp_config.json.bak").read_text(encoding="utf-8")
        ))

        skills = self.home / ".gemini" / "antigravity" / "skills"
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                self.assertTrue((skills / name / "SKILL.md").is_file())
                marker = (skills / name / install_agent.MARKER_NAME).read_text(encoding="utf-8")
                self.assertIn(str(install_agent.PLUGIN_ROOT), marker)
        self.assertTrue(
            (skills / "analyze-requirements" / "references" / "output-contract.md").is_file()
        )

    def test_uninstall_removes_only_owned_entries(self) -> None:
        run("--target", "cursor", "--home", str(self.home))
        foreign = self.home / ".cursor" / "skills" / "unrelated"
        foreign.mkdir()

        run("--target", "cursor", "--home", str(self.home), "--uninstall")

        config = json.loads((self.home / ".cursor" / "mcp.json").read_text(encoding="utf-8"))
        self.assertEqual({}, config["mcpServers"])
        for name in SKILL_NAMES:
            self.assertFalse((self.home / ".cursor" / "skills" / name).exists())
        self.assertTrue(foreign.is_dir())

    def test_foreign_skill_folder_is_not_overwritten(self) -> None:
        clash = self.home / ".gemini" / "skills" / "traceguard-audit"
        clash.mkdir(parents=True)
        (clash / "SKILL.md").write_text("someone else's skill", encoding="utf-8")

        with self.assertRaises(SystemExit):
            run("--target", "gemini-cli", "--home", str(self.home), "--no-mcp")

        self.assertEqual("someone else's skill", (clash / "SKILL.md").read_text(encoding="utf-8"))

    def test_invalid_config_is_left_unchanged(self) -> None:
        config_path = self.home / ".codeium" / "windsurf" / "mcp_config.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text("{ // comment\n}", encoding="utf-8")

        with self.assertRaises(SystemExit):
            run("--target", "windsurf", "--home", str(self.home))

        self.assertEqual("{ // comment\n}", config_path.read_text(encoding="utf-8"))

    def test_vscode_workspace_uses_servers_key_and_github_skills(self) -> None:
        workspace = self.home / "project"
        workspace.mkdir()

        run("--target", "vscode", "--scope", "workspace", "--workspace", str(workspace))

        config = json.loads((workspace / ".vscode" / "mcp.json").read_text(encoding="utf-8"))
        self.assertEqual("stdio", config["servers"][install_agent.SERVER_KEY]["type"])
        self.assertTrue((workspace / ".github" / "skills" / "analyze-requirements").is_dir())

    def test_dsh_appends_patch_row_and_uninstall_restores_file(self) -> None:
        dsh_home = self.home / ".dsh"
        dsh_home.mkdir()
        patch_path = dsh_home / "cordis.patch.yml"
        existing = "# my overrides\n- insert:\n    - id: other-row\n      name: x\n"
        patch_path.write_text(existing, encoding="utf-8")

        with unittest.mock.patch.dict("os.environ", {}, clear=False) as environ:
            environ.pop("DSH_HOME", None)
            run("--target", "dsh", "--home", str(self.home), "--python", "C:\\Py\\python.exe")

            text = patch_path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith(existing))
            self.assertIn("name: '@deepseek-ai/dsh-mcp-client'", text)
            self.assertIn(f"serverName: {install_agent.SERVER_KEY}", text)
            self.assertIn('command: "C:\\\\Py\\\\python.exe"', text)
            self.assertIn("transport: stdio", text)
            self.assertTrue((dsh_home / "skills" / "analyze-requirements" / "SKILL.md").is_file())

            # Reinstalling replaces the managed block instead of adding a second row.
            run("--target", "dsh", "--home", str(self.home))
            self.assertEqual(
                1, patch_path.read_text(encoding="utf-8").count(install_agent.DSH_BLOCK_START)
            )

            run("--target", "dsh", "--home", str(self.home), "--uninstall")
            self.assertEqual(existing, patch_path.read_text(encoding="utf-8"))
            self.assertFalse((dsh_home / "skills" / "analyze-requirements").exists())

    def test_dsh_refuses_patch_that_is_not_a_block_list(self) -> None:
        patch_path = self.home / "custom.patch.yml"
        patch_path.write_text("profile: web\n", encoding="utf-8")

        with self.assertRaises(SystemExit):
            run("--target", "dsh", "--config", str(patch_path), "--no-skills")

        self.assertEqual("profile: web\n", patch_path.read_text(encoding="utf-8"))

    def test_dry_run_and_print_write_nothing(self) -> None:
        output = run("--target", "claude-desktop", "--print", "--home", str(self.home))
        self.assertIn(install_agent.SERVER_KEY, output)
        run("--target", "antigravity", "--dry-run", "--home", str(self.home))
        self.assertEqual([], list(self.home.iterdir()))


class HostManifestTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_every_host_manifest_shares_one_version(self) -> None:
        codex = self.load(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        claude = self.load(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
        gemini = self.load(PLUGIN_ROOT / "gemini-extension.json")
        server_text = (PLUGIN_ROOT / "mcp" / "server.py").read_text(encoding="utf-8")

        self.assertEqual(codex["version"], claude["version"])
        self.assertEqual(codex["version"], gemini["version"])
        self.assertIn(f'SERVER_VERSION = "{codex["version"]}"', server_text)
        self.assertEqual(PLUGIN_ROOT.name, gemini["name"])

    def test_host_server_entries_point_at_the_bundled_server(self) -> None:
        claude = self.load(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
        gemini = self.load(PLUGIN_ROOT / "gemini-extension.json")
        codex = self.load(PLUGIN_ROOT / ".mcp.json")
        key = install_agent.SERVER_KEY

        self.assertEqual(
            ["${CLAUDE_PLUGIN_ROOT}/mcp/server.py"], claude["mcpServers"][key]["args"]
        )
        self.assertEqual(
            ["${extensionPath}${/}mcp${/}server.py"], gemini["mcpServers"][key]["args"]
        )
        self.assertIn(key, codex["mcpServers"])

    def test_claude_marketplace_lists_the_plugin_folder(self) -> None:
        marketplace = self.load(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        plugin = marketplace["plugins"][0]

        self.assertEqual("requirements-analysis-workbench", plugin["name"])
        self.assertTrue((REPO_ROOT / plugin["source"] / ".claude-plugin" / "plugin.json").is_file())


if __name__ == "__main__":
    unittest.main()

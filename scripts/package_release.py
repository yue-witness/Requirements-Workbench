#!/usr/bin/env python3
"""Build a reproducible, standalone marketplace release archive."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "requirements-workbench"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
DIST_DIR = ROOT / "dist"
FIXED_TIMESTAMP = (2026, 8, 23, 0, 0, 0)


def release_files() -> list[tuple[Path, Path]]:
    """Return source files and their paths inside the release root."""

    top_level = [
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ROOT / "README.md",
        ROOT / "README.zh-CN.md",
        ROOT / "CHANGELOG.md",
        ROOT / "LICENSE",
    ]
    files = [(path, path.relative_to(ROOT)) for path in top_level]

    for path in sorted(PLUGIN_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        files.append((path, path.relative_to(ROOT)))

    return files


def add_file(archive: ZipFile, source: Path, archive_path: Path) -> None:
    """Add one file with stable metadata so repeated builds are identical."""

    info = ZipInfo(archive_path.as_posix(), date_time=FIXED_TIMESTAMP)
    info.compress_type = ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes())


def sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    """Validate release metadata and write the ZIP plus checksum file."""

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    version = str(manifest["version"])
    archive_root = Path(f"requirements-workbench-v{version}")
    archive_path = DIST_DIR / f"requirements-workbench-v{version}.zip"
    checksum_path = DIST_DIR / "SHA256SUMS.txt"

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path, "w") as archive:
        for source, relative_path in release_files():
            add_file(archive, source, archive_root / relative_path)

    checksum_path.write_text(
        f"{sha256(archive_path)}  {archive_path.name}\n",
        encoding="utf-8",
        newline="\n",
    )
    print(archive_path.resolve())
    print(checksum_path.resolve())


if __name__ == "__main__":
    main()

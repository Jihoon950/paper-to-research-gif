#!/usr/bin/env python3
"""Build a portable skills-only ZIP without example or research media."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    skill = ROOT / "skills" / manifest["name"]
    if not (skill / "SKILL.md").is_file():
        raise SystemExit("Manifest name and skill folder do not match")
    files = [ROOT / "plugin.json"] + sorted(path for path in (ROOT / "assets").rglob("*") if path.is_file()) + sorted(path for path in skill.rglob("*") if path.is_file())
    forbidden = {"node_modules", "out", ".git", "__pycache__"}
    for path in files:
        if any(part in forbidden for part in path.relative_to(ROOT).parts):
            raise SystemExit(f"Refusing to package generated or private tree: {path}")
        if path.suffix.lower() in {".mp4", ".mov", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".zip"}:
            raise SystemExit(f"Refusing to package research media: {path}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(rel, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    print(f"Packaged {len(files)} files: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

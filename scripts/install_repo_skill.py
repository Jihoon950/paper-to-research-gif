#!/usr/bin/env python3
"""Install this plugin's skill into a chosen repository's .agents/skills folder."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "paper-to-research-gif"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    if not repository.is_dir():
        raise SystemExit(f"Repository directory does not exist: {repository}")
    destination = repository / ".agents" / "skills" / SOURCE.name
    if destination.exists():
        raise SystemExit(f"Refusing to overwrite existing skill: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "out"))
    print(f"Installed: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

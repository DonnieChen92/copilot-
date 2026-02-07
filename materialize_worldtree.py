#!/usr/bin/env python3
"""
materialize_worldtree.py
Writes the WORLD_TREE dictionary to disk, creating directories and files.
"""
import json
import stat
from pathlib import Path

try:
    from worldtree_dictionary import WORLD_TREE
except Exception:
    raise SystemExit(
        "Place worldtree_dictionary.py with WORLD_TREE variable in same dir"
    )


def create_entry(base_path: Path, name: str, value):
    path = base_path / name
    if isinstance(value, dict):
        path.mkdir(parents=True, exist_ok=True)
        for k, v in value.items():
            create_entry(path, k, v)
    elif isinstance(value, str):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(value)
        if name.endswith(".sh") or (value.startswith("#!") and name.endswith(".py")):
            mode = path.stat().st_mode
            path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(value, indent=2))


def materialize(world_tree: dict, base_dir: str = "."):
    base = Path(base_dir).resolve()
    for top, val in world_tree.items():
        create_entry(base, top, val)
    print(f"Materialized worldtree into {base}")


if __name__ == "__main__":
    materialize(WORLD_TREE, ".")

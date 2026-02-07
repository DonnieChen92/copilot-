#!/usr/bin/env python3
"""
dropbox_normalizer.py
Converts Dropbox file downloads into normalized nodes under
external-conservations/normalized/nodes/.
"""

import json
import argparse
from pathlib import Path


def normalize_dropbox_dir(root, timestamp):
    base = (
        Path(root)
        / "external-conservations"
        / "imports"
        / "raw"
        / "dropbox"
        / timestamp
    )
    out = Path(root) / "external-conservations" / "normalized" / "nodes"
    out.mkdir(parents=True, exist_ok=True)

    for f in base.rglob("*"):
        if f.is_file():
            rel = f.relative_to(base)
            node = {
                "id": f"dropbox:{str(rel)}",
                "platform": "dropbox",
                "name": f.name,
                "size": f.stat().st_size,
                "path": str(f.relative_to(Path(root))),
                "provenance": {},
            }
            out_file = out / (str(rel).replace("/", "_") + ".json")
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as fh:
                json.dump(node, fh, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--timestamp", required=True)
    args = parser.parse_args()
    normalize_dropbox_dir(args.root, args.timestamp)
    print("Dropbox normalization done.")

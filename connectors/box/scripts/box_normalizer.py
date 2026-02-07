#!/usr/bin/env python3
"""
box_normalizer.py
Converts Box item metadata + files into normalized nodes under
external-conservations/normalized/nodes/.
"""

import json
import argparse
from pathlib import Path


def normalize_box_dir(root, timestamp):
    base = (
        Path(root)
        / "external-conservations"
        / "imports"
        / "raw"
        / "box"
        / timestamp
    )
    out = Path(root) / "external-conservations" / "normalized" / "nodes"
    out.mkdir(parents=True, exist_ok=True)

    for meta in base.glob("item-*.json"):
        with open(meta, "r", encoding="utf-8") as fh:
            info = json.load(fh)
        node = {
            "id": f"box:{info.get('id')}",
            "platform": "box",
            "name": info.get("name"),
            "type": info.get("type"),
            "provenance": {},
        }
        # try to find the downloaded file content
        possible = list((base / "files").glob(f"{info.get('id')}-*"))
        if possible:
            p = possible[0]
            node["size"] = p.stat().st_size
            node["path"] = str(p.relative_to(Path(root)))
        out_file = out / f"{info.get('id')}.json"
        with open(out_file, "w", encoding="utf-8") as fh:
            json.dump(node, fh, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--timestamp", required=True)
    args = parser.parse_args()
    normalize_box_dir(args.root, args.timestamp)
    print("Box normalization done.")

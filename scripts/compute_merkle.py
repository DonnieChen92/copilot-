#!/usr/bin/env python3
"""
compute_merkle.py
Compute Merkle root for a manifest (list of file sha256s) and write the root
to projects/JCD01-evidence-vault/integrity/merkle-roots/.
"""

import json
import hashlib
import argparse
from pathlib import Path


def merkle_root(hashes):
    """Simple binary Merkle tree (duplicate last leaf when odd)."""
    nodes = [bytes.fromhex(h) for h in hashes]
    if not nodes:
        return None
    while len(nodes) > 1:
        next_nodes = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
            next_nodes.append(hashlib.sha256(left + right).digest())
        nodes = next_nodes
    return nodes[0].hex()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Path to worldtree root")
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to manifest JSON file",
    )
    args = parser.parse_args()

    root = Path(args.root)
    manifest = Path(args.manifest)
    manifest_json = json.load(open(manifest))
    hashes = [f["sha256"] for f in manifest_json.get("files", [])]
    root_hash = merkle_root(hashes)

    outdir = root / "projects" / "JCD01-evidence-vault" / "integrity" / "merkle-roots"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / (manifest.name + ".merkle")
    with open(outpath, "w", encoding="utf-8") as fh:
        fh.write(root_hash or "")
    print("Merkle root written to", outpath)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
sign_manifest.py
Signs a manifest file with a GPG key (requires gpg installed and configured).
Outputs a detached ASCII-armored signature under
projects/JCD01-evidence-vault/integrity/manifests-signatures/.
"""

import argparse
import subprocess
import shlex
from pathlib import Path


def sign_file(manifest_path, fingerprint, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (manifest_path.name + ".asc")
    cmd = (
        f"gpg --default-key {fingerprint} --armor "
        f"--output {shlex.quote(str(out_path))} "
        f"--detach-sign {shlex.quote(str(manifest_path))}"
    )
    subprocess.check_call(cmd, shell=True)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="Path to manifest file")
    parser.add_argument("--fingerprint", required=True, help="GPG key fingerprint")
    parser.add_argument("--root", required=True, help="Path to worldtree root")
    args = parser.parse_args()

    out_dir = (
        Path(args.root)
        / "projects"
        / "JCD01-evidence-vault"
        / "integrity"
        / "manifests-signatures"
    )
    signed = sign_file(Path(args.manifest), args.fingerprint, out_dir)
    print("Signed manifest at:", signed)

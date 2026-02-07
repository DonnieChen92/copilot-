#!/usr/bin/env python3
"""
ingest_chats_extended.py
Supports:
 - local-export ingestion (--exported_dir)
 - slack API download (--api-mode slack)
 - box API download (--api-mode box)
 - dropbox API download (--api-mode dropbox)
"""

import os
import argparse
import json
import shutil
import hashlib
import time
import logging
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Optional SDK imports
try:
    from slack_sdk import WebClient as SlackClient
except Exception:
    SlackClient = None

try:
    from boxsdk import Client as BoxClient, OAuth2 as BoxOAuth2
except Exception:
    BoxClient = None
    BoxOAuth2 = None

try:
    import dropbox as dropbox_sdk
    from dropbox.files import FileMetadata, FolderMetadata
except Exception:
    dropbox_sdk = None
    FileMetadata = None
    FolderMetadata = None


def sha256_file(path, block_size=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def human_bytes(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024.0:
            return f"{n:.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"


def write_manifest_provenance(root, platform, files, agent, extra=None):
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    manifests_dir = Path(root) / "external-conservations" / "imports" / "manifests"
    provenance_dir = Path(root) / "external-conservations" / "imports" / "provenance"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    provenance_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "platform": platform,
        "ingested_at": timestamp,
        "agent": agent,
        "files": files,
    }
    if extra:
        manifest["extra"] = extra

    manifest_path = manifests_dir / f"{platform}-manifest-{timestamp}.json"
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    provenance = {
        "platform": platform,
        "ingested_at": timestamp,
        "agent": agent,
        "manifest": str(manifest_path.relative_to(root)),
    }
    if extra:
        provenance["extra"] = extra
    prov_path = provenance_dir / f"{platform}-provenance-{timestamp}.json"
    with open(prov_path, "w", encoding="utf-8") as fh:
        json.dump(provenance, fh, indent=2)

    return manifest_path, prov_path


def copy_exports(root, platform, exported_dir, agent):
    exported_dir = Path(exported_dir)
    if not exported_dir.exists():
        raise SystemExit(f"Exported dir does not exist: {exported_dir}")
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    imports_raw = (
        Path(root) / "external-conservations" / "imports" / "raw" / platform / ts
    )
    imports_raw.mkdir(parents=True, exist_ok=True)
    files_meta = []
    for src in sorted(exported_dir.iterdir()):
        if src.is_dir():
            dest_dir = imports_raw / src.name
            shutil.copytree(src, dest_dir)
            for f in dest_dir.rglob("*"):
                if f.is_file():
                    sha = sha256_file(f)
                    files_meta.append(
                        {
                            "original_filename": str(f.relative_to(exported_dir)),
                            "import_path": str(f.relative_to(root)),
                            "size_bytes": f.stat().st_size,
                            "size": human_bytes(f.stat().st_size),
                            "sha256": sha,
                            "imported_at": ts,
                        }
                    )
        else:
            dest = imports_raw / src.name
            shutil.copy2(src, dest)
            sha = sha256_file(dest)
            files_meta.append(
                {
                    "original_filename": src.name,
                    "import_path": str(dest.relative_to(root)),
                    "size_bytes": dest.stat().st_size,
                    "size": human_bytes(dest.stat().st_size),
                    "sha256": sha,
                    "imported_at": ts,
                }
            )
    manifest_path, prov_path = write_manifest_provenance(
        root, platform, files_meta, agent
    )
    logging.info(f"Copied exports to {imports_raw}, manifest {manifest_path}")
    return imports_raw, manifest_path, prov_path


# ---------------------------------------------------------------------------
# Slack helpers
# ---------------------------------------------------------------------------


def download_slack_file(client, file_meta, channel_dir, root, files_meta, ts):
    url = file_meta.get("url_private")
    if not url:
        return
    import requests

    filename = file_meta.get("id") + "_" + file_meta.get("name", "file")
    dest = channel_dir / "attachments" / filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    headers = {"Authorization": f"Bearer {client.token}"}
    r = requests.get(url, headers=headers, stream=True)
    if r.status_code == 200:
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(1024 * 64):
                fh.write(chunk)
        files_meta.append(
            {
                "original_filename": filename,
                "import_path": str(dest.relative_to(root)),
                "size_bytes": dest.stat().st_size,
                "size": human_bytes(dest.stat().st_size),
                "sha256": sha256_file(dest),
                "imported_at": ts,
            }
        )
    else:
        logging.warning(f"Failed to download slack file {url}: {r.status_code}")


def slack_api_download(root, agent):
    if SlackClient is None:
        raise SystemExit("slack_sdk not installed")
    token = os.getenv("SLACK_BOT_TOKEN") or os.getenv("SLACK_USER_TOKEN")
    if not token:
        raise SystemExit("SLACK_BOT_TOKEN or SLACK_USER_TOKEN must be set")
    client = SlackClient(token=token)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = (
        Path(root) / "external-conservations" / "imports" / "raw" / "slack" / ts
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    files_meta = []
    types = "public_channel,private_channel,im,mpim"
    cursor = None
    while True:
        resp = client.conversations_list(types=types, limit=1000, cursor=cursor)
        for ch in resp.get("channels", []):
            ch_id = ch.get("id")
            ch_name = ch.get("name") or ch_id
            logging.info(f"Fetching channel: {ch_name} ({ch_id})")
            channel_dir = out_dir / ch_name
            channel_dir.mkdir(parents=True, exist_ok=True)
            has_more = True
            oldest_cursor = None
            page = 0
            while has_more:
                page += 1
                history = client.conversations_history(
                    channel=ch_id, limit=200, cursor=oldest_cursor
                )
                msgs = history.get("messages", [])
                page_file = channel_dir / f"messages-page-{page}.json"
                with open(page_file, "w", encoding="utf-8") as fh:
                    json.dump(history, fh)
                files_meta.append(
                    {
                        "original_filename": str(page_file.name),
                        "import_path": str(page_file.relative_to(root)),
                        "size_bytes": page_file.stat().st_size,
                        "size": human_bytes(page_file.stat().st_size),
                        "sha256": sha256_file(page_file),
                        "imported_at": ts,
                    }
                )
                # threads
                for m in msgs:
                    if m.get("thread_ts") and m.get("thread_ts") == m.get("ts"):
                        replies = client.conversations_replies(
                            channel=ch_id, ts=m["ts"]
                        )
                        thread_file = channel_dir / f"thread-{m['ts']}.json"
                        with open(thread_file, "w", encoding="utf-8") as tf:
                            json.dump(replies, tf)
                        files_meta.append(
                            {
                                "original_filename": str(thread_file.name),
                                "import_path": str(thread_file.relative_to(root)),
                                "size_bytes": thread_file.stat().st_size,
                                "size": human_bytes(thread_file.stat().st_size),
                                "sha256": sha256_file(thread_file),
                                "imported_at": ts,
                            }
                        )
                        for msg in replies.get("messages", []):
                            if "files" in msg:
                                for f in msg["files"]:
                                    download_slack_file(
                                        client, f, channel_dir, root, files_meta, ts
                                    )
                has_more = history.get("has_more", False)
                oldest_cursor = None
                time.sleep(0.5)
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    manifest_path, prov_path = write_manifest_provenance(
        root, "slack", files_meta, agent
    )
    logging.info(f"Slack download complete: manifest={manifest_path}")
    return out_dir, manifest_path, prov_path


# ---------------------------------------------------------------------------
# Box helpers
# ---------------------------------------------------------------------------


def box_api_download(root, agent):
    if BoxClient is None:
        raise SystemExit("boxsdk not installed")
    developer_token = os.getenv("BOX_DEVELOPER_TOKEN")
    if developer_token:
        oauth = BoxOAuth2(
            client_id=None, client_secret=None, access_token=developer_token
        )
        client = BoxClient(oauth)
    else:
        client_id = os.getenv("BOX_CLIENT_ID")
        client_secret = os.getenv("BOX_CLIENT_SECRET")
        if not (client_id and client_secret):
            raise SystemExit("BOX_CLIENT_ID and BOX_CLIENT_SECRET are required")
        oauth = BoxOAuth2(client_id=client_id, client_secret=client_secret)
        client = BoxClient(oauth)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(root) / "external-conservations" / "imports" / "raw" / "box" / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    files_meta = []
    root_folder = client.folder(folder_id="0")
    items = root_folder.get_items(limit=1000, offset=0)
    for it in items:
        meta = {"id": it.id, "name": it.name, "type": it.type}
        meta_file = out_dir / f"item-{it.id}.json"
        with open(meta_file, "w", encoding="utf-8") as fh:
            json.dump(meta, fh)
        files_meta.append(
            {
                "original_filename": meta_file.name,
                "import_path": str(meta_file.relative_to(root)),
                "size_bytes": meta_file.stat().st_size,
                "size": human_bytes(meta_file.stat().st_size),
                "sha256": sha256_file(meta_file),
                "imported_at": ts,
            }
        )
        if it.type == "file":
            fhpath = out_dir / "files" / f"{it.id}-{it.name}"
            fhpath.parent.mkdir(parents=True, exist_ok=True)
            with open(fhpath, "wb") as outfh:
                client.file(file_id=it.id).download_to(outfh)
            files_meta.append(
                {
                    "original_filename": fhpath.name,
                    "import_path": str(fhpath.relative_to(root)),
                    "size_bytes": fhpath.stat().st_size,
                    "size": human_bytes(fhpath.stat().st_size),
                    "sha256": sha256_file(fhpath),
                    "imported_at": ts,
                }
            )
    manifest_path, prov_path = write_manifest_provenance(
        root, "box", files_meta, agent
    )
    logging.info(f"Box download complete: manifest={manifest_path}")
    return out_dir, manifest_path, prov_path


# ---------------------------------------------------------------------------
# Dropbox helpers
# ---------------------------------------------------------------------------


def dropbox_api_download(root, agent):
    if dropbox_sdk is None:
        raise SystemExit("dropbox SDK not installed")
    token = os.getenv("DROPBOX_OAUTH_TOKEN")
    if not token:
        raise SystemExit("DROPBOX_OAUTH_TOKEN required")
    dbx = dropbox_sdk.Dropbox(token)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = (
        Path(root) / "external-conservations" / "imports" / "raw" / "dropbox" / ts
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    files_meta = []

    def walk(path=""):
        try:
            res = dbx.files_list_folder(path, recursive=False)
        except Exception as e:
            logging.error(f"list_folder error for {path}: {e}")
            return
        for entry in res.entries:
            if isinstance(entry, FileMetadata):
                dest = out_dir / "files" / entry.path_lower.lstrip("/")
                dest.parent.mkdir(parents=True, exist_ok=True)
                _md, res2 = dbx.files_download(entry.path_lower)
                with open(dest, "wb") as fh:
                    fh.write(res2.content)
                files_meta.append(
                    {
                        "original_filename": dest.name,
                        "import_path": str(dest.relative_to(root)),
                        "size_bytes": dest.stat().st_size,
                        "size": human_bytes(dest.stat().st_size),
                        "sha256": sha256_file(dest),
                        "imported_at": ts,
                    }
                )
            elif isinstance(entry, FolderMetadata):
                walk(entry.path_lower)
        cursor = getattr(res, "cursor", None)
        while getattr(res, "has_more", False):
            res = dbx.files_list_folder_continue(cursor)
            for entry in res.entries:
                if isinstance(entry, FileMetadata):
                    dest = out_dir / "files" / entry.path_lower.lstrip("/")
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    _md, res2 = dbx.files_download(entry.path_lower)
                    with open(dest, "wb") as fh:
                        fh.write(res2.content)
                    files_meta.append(
                        {
                            "original_filename": dest.name,
                            "import_path": str(dest.relative_to(root)),
                            "size_bytes": dest.stat().st_size,
                            "size": human_bytes(dest.stat().st_size),
                            "sha256": sha256_file(dest),
                            "imported_at": ts,
                        }
                    )

    walk("")
    manifest_path, prov_path = write_manifest_provenance(
        root, "dropbox", files_meta, agent
    )
    logging.info(f"Dropbox download complete: manifest={manifest_path}")
    return out_dir, manifest_path, prov_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Ingest chat exports from Slack, Box, Dropbox, and other platforms"
    )
    parser.add_argument("--root", required=True, help="Path to worldtree root")
    parser.add_argument(
        "--platform",
        required=True,
        choices=[
            "slack",
            "box",
            "dropbox",
            "chatgpt",
            "email",
            "whatsapp",
            "telegram",
            "other",
        ],
    )
    parser.add_argument("--agent", required=True, help="Agent email / identifier")
    parser.add_argument(
        "--exported_dir", help="Local export directory (if available)"
    )
    parser.add_argument(
        "--api-mode",
        help="Use API mode for platform: slack, box, dropbox",
        choices=["slack", "box", "dropbox"],
    )
    args = parser.parse_args()

    if args.exported_dir:
        copy_exports(args.root, args.platform, args.exported_dir, args.agent)
    elif args.api_mode == "slack":
        slack_api_download(args.root, args.agent)
    elif args.api_mode == "box":
        box_api_download(args.root, args.agent)
    elif args.api_mode == "dropbox":
        dropbox_api_download(args.root, args.agent)
    else:
        raise SystemExit(
            "Either --exported_dir or --api-mode must be provided for Slack/Box/Dropbox"
        )


if __name__ == "__main__":
    main()

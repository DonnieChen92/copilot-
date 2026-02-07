#!/usr/bin/env python3
"""
slack_normalizer.py
Reads raw Slack exports under external-conservations/imports/raw/slack/<timestamp>/<channel>/
and writes normalized conversation-record JSON files into
external-conservations/normalized/threads/.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def ts_to_iso(ts):
    sec = float(ts)
    return datetime.utcfromtimestamp(sec).isoformat() + "Z"


def read_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def normalize_channel(channel_dir: Path, out_dir: Path):
    channel_name = channel_dir.name
    record = {
        "id": f"slack:{channel_name}",
        "platform": "slack",
        "thread_id": None,
        "participants": [],
        "messages": [],
        "provenance": {},
    }

    # load all pages
    for page in sorted(channel_dir.glob("messages-page-*.json")):
        data = read_json(page)
        for m in data.get("messages", []):
            author = (
                m.get("user")
                or m.get("bot_id")
                or m.get("username")
                or "system"
            )
            msg = {
                "message_id": f"slack:{channel_name}:{m.get('ts')}",
                "timestamp": ts_to_iso(m.get("ts")),
                "author": f"user:{author}",
                "text": m.get("text", ""),
                "attachments": [],
            }
            # attachments
            if "files" in m:
                for f in m["files"]:
                    fname = f.get("id") + "_" + f.get("name", "file")
                    found = list(channel_dir.glob(f"**/{fname}"))
                    if found:
                        msg["attachments"].append(
                            str(
                                found[0].relative_to(
                                    channel_dir.parent.parent.parent
                                )
                            )
                        )
            # thread id resolution
            if m.get("thread_ts") and m.get("thread_ts") != m.get("ts"):
                msg["thread_id"] = f"slack:{channel_name}:{m.get('thread_ts')}"

            record["participants"].append(msg["author"])
            record["messages"].append(msg)

    record["participants"] = sorted(list(set(record["participants"])))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{channel_name}.json"
    with open(out_file, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    return out_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument(
        "--timestamp",
        required=True,
        help="Timestamp dir under imports/raw/slack/",
    )
    args = parser.parse_args()

    root = Path(args.root)
    raw_base = (
        root
        / "external-conservations"
        / "imports"
        / "raw"
        / "slack"
        / args.timestamp
    )
    out_base = root / "external-conservations" / "normalized" / "threads"

    for ch in raw_base.iterdir():
        if ch.is_dir():
            print("Normalizing", ch.name)
            normalize_channel(ch, out_base)
    print("Slack normalization done.")


if __name__ == "__main__":
    main()

# worldtree.root.window/jiadongchendonnie.ai

Canonical workspace for projects, schemas, samples, conservations, and external-conservations.

## Quick start

1. Install dependencies:

```bash
python3 -m pip install slack_sdk boxsdk dropbox requests python-dotenv python-gnupg
```

2. Copy `.env.example` to `.env` and fill in your secrets.

3. Create the directory skeleton:

```bash
make mkdir
```

4. Ingest data (pick one or more):

```bash
# From local exports
python3 scripts/ingest_chats_extended.py \
  --root $WORLDROOT --platform slack --agent $AGENT_EMAIL \
  --exported_dir /path/to/slack-export

# From APIs
make ingest_slack
make ingest_box
make ingest_dropbox
```

5. Normalize:

```bash
make normalize_slack TS=20260101T120000Z
make normalize_box TS=20260101T120000Z
make normalize_dropbox TS=20260101T120000Z
```

6. Compute integrity artifacts:

```bash
make merkle MANIFEST=$WORLDROOT/external-conservations/imports/manifests/slack-manifest-20260101T120000Z.json
make sign_all MANIFEST=$WORLDROOT/external-conservations/imports/manifests/slack-manifest-20260101T120000Z.json PGP_FINGERPRINT=<your-key>
```

## Domain ownership

| Field | Value |
|-------|-------|
| Domain | `jiadongchendonnie.ai` |
| Registrar | Squarespace |
| Registrar login | `donniechen92@gmail.com` |
| Legal owner | CHEN, JIADONG |

See `worldtree.root.window/jiadongchendonnie.ai/identity/domain-ownership.json` for full details.

## Structure

- `scripts/` — Ingest, integrity, and materializer scripts
- `connectors/` — Platform-specific normalizers (slack, box, dropbox)
- `simulations/` — Radiation, redundancy, orbital, autonomy, and utility simulations
- `worldtree.root.window/jiadongchendonnie.ai/` — The worldtree data root
  - `identity/` — Domain ownership and registrar records
  - `projects/` — JCD01 through JCD06 project directories
  - `schemas/` — Canonical JSON schemas (conversation-record, etc.)
  - `samples/` — Example records and templates
  - `conservations/` — Local conversation storage, shared links, memory layer, logs
  - `external-conservations/` — Imported data, normalized records, redactions, indexes

## Keep secrets in `.env` and never commit them.

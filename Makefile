.PHONY: mkdir ingest_slack ingest_box ingest_dropbox normalize_slack normalize_box normalize_dropbox merkle sign_all

WORLDROOT ?= $(shell pwd)/worldtree.root.window/jiadongchendonnie.ai
AGENT ?= jiadongchen.donnie@outlook.com
TS ?= $(shell date -u +%Y%m%dT%H%M%SZ)

mkdir:
	@WORLDROOT=$(WORLDROOT) bash ./scripts/mkdir_tree.sh

ingest_slack:
	python3 scripts/ingest_chats_extended.py --root $(WORLDROOT) --platform slack --agent $(AGENT) --api-mode slack

ingest_box:
	python3 scripts/ingest_chats_extended.py --root $(WORLDROOT) --platform box --agent $(AGENT) --api-mode box

ingest_dropbox:
	python3 scripts/ingest_chats_extended.py --root $(WORLDROOT) --platform dropbox --agent $(AGENT) --api-mode dropbox

normalize_slack:
	python3 connectors/slack/scripts/slack_normalizer.py --root $(WORLDROOT) --timestamp $(TS)

normalize_box:
	python3 connectors/box/scripts/box_normalizer.py --root $(WORLDROOT) --timestamp $(TS)

normalize_dropbox:
	python3 connectors/dropbox/scripts/dropbox_normalizer.py --root $(WORLDROOT) --timestamp $(TS)

merkle:
	python3 scripts/compute_merkle.py --root $(WORLDROOT) --manifest $(MANIFEST)

sign_all:
	python3 scripts/sign_manifest.py --manifest $(MANIFEST) --fingerprint $(PGP_FINGERPRINT) --root $(WORLDROOT)

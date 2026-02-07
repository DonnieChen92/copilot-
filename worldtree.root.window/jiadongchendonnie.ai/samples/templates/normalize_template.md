# Normalizer Template

Use this template as a starting point for new platform normalizers.

## Required output format

Each normalizer must produce JSON files conforming to `schemas/conversation-record/schema.json`.

## Steps

1. Read raw imports from `external-conservations/imports/raw/<platform>/<timestamp>/`
2. Parse platform-specific format
3. Map to canonical `conversation-record` schema
4. Write normalized records to `external-conservations/normalized/threads/` or `normalized/nodes/`
5. Log normalization run to `conservations/logs/remap/`

import json
import pytest
from pathlib import Path
from SACA_Dossier.py.saca_runtime import AuditLog, AuditEvent

def test_audit_log_init(tmp_path):
    log_file = tmp_path / "audit.log.jsonl"
    audit = AuditLog(log_file)
    assert audit.prev_hash == "GENESIS"
    assert log_file.parent.exists()

def test_audit_log_emit_chain(tmp_path):
    log_file = tmp_path / "audit.log.jsonl"
    audit = AuditLog(log_file)

    # First event
    e1 = audit.emit("TEST_EVENT_1", {"foo": "bar"})
    assert e1.prev_hash == "GENESIS"
    assert e1.event == "TEST_EVENT_1"

    # Second event
    e2 = audit.emit("TEST_EVENT_2", {"baz": 123})
    assert e2.prev_hash == e1.hash
    assert e2.event == "TEST_EVENT_2"

    # Verify content in file
    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    j1 = json.loads(lines[0])
    j2 = json.loads(lines[1])
    assert j1["hash"] == e1.hash
    assert j2["hash"] == e2.hash
    assert j2["prev_hash"] == e1.hash

def test_audit_log_persistence(tmp_path):
    log_file = tmp_path / "audit.log.jsonl"
    audit = AuditLog(log_file)
    e1 = audit.emit("E1", {})

    # New instance, same file
    audit2 = AuditLog(log_file)
    assert audit2.prev_hash == e1.hash

    e2 = audit2.emit("E2", {})
    assert e2.prev_hash == e1.hash

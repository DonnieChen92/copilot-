import pytest
import json
import yaml
from pathlib import Path
from SACA_Dossier.py.saca_runtime import PolicyEngine, PolicyDecision

# Mock Policy Document for testing logic without depending on external file
MOCK_POLICY_DOC = {
    "defaults": {"action": "allow", "require": ["audit_log"]},
    "hard_denies": [
        {
            "id": "HD_TEST",
            "when": {"topic": "forbidden"},
            "decision": {"require": ["shutdown"], "reason": "Forbidden topic"}
        }
    ],
    "policies": [
        {
            "id": "POL_HIGH",
            "priority": 100,
            "when": {"risk": "high"},
            "decision": {"action": "deny", "reason": "High risk"}
        },
        {
            "id": "POL_MED",
            "priority": 50,
            "when": {"risk": "medium"},
            "decision": {"action": "degrade", "reason": "Medium risk"}
        }
    ]
}

@pytest.fixture
def policy_engine():
    return PolicyEngine(MOCK_POLICY_DOC)

def test_defaults(policy_engine):
    ctx = {"risk": "low", "topic": "safe"}
    dec = policy_engine.eval(ctx)
    assert dec.action == "allow"
    assert "audit_log" in dec.require

def test_hard_deny(policy_engine):
    ctx = {"topic": "forbidden", "risk": "low"}
    dec = policy_engine.eval(ctx)
    assert dec.action == "deny"
    assert "HD_TEST" in dec.hits
    assert "shutdown" in dec.require

def test_policy_priority(policy_engine):
    # Both match logic, but priorities are handled by sorting in Engine
    # However, in current implementation, precedence overrides: halt > deny > degrade > allow
    # If priority 100 sets deny and 50 sets degrade, deny wins because deny > degrade in precedence.

    # Let's test precedence logic.
    # Case: High risk -> deny
    ctx = {"risk": "high"}
    dec = policy_engine.eval(ctx)
    assert dec.action == "deny"

    # Case: Medium risk -> degrade
    ctx = {"risk": "medium"}
    dec = policy_engine.eval(ctx)
    assert dec.action == "degrade"

def test_integration_with_real_yaml():
    # Load actual policy file to ensure it's valid and logic works as expected
    path = Path("SACA_Dossier/policies/v18_v21_policy.yaml")
    if not path.exists():
        pytest.skip("Policy file not found")

    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    engine = PolicyEngine(doc)

    # Test Sovereignty Hard Deny
    ctx = {"intent": "set_own_goals"}
    dec = engine.eval(ctx)
    assert dec.action == "deny"
    assert "HD_SOVEREIGNTY" in dec.hits

    # Test HHM S4 Halt
    ctx = {"hhms": {"status": "S4"}}
    dec = engine.eval(ctx)
    assert dec.action == "halt"
    assert "HHM_S4_HALT" in dec.hits

    # Test Evolution degrade
    ctx = {"topic": "system_evolution"}
    dec = engine.eval(ctx)
    assert dec.action == "degrade"
    assert "human_arbitration" in dec.require

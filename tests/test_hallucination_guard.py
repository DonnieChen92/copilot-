"""
Test Hallucination Guard / 測試幻覺防護
=======================================
"""
import pytest
from unittest.mock import MagicMock
from src.llm_api.base_client import BaseLLMClient, LLMResponse
from src.governance.stc.hallucination_guard import HallucinationGuard

class MockClient(BaseLLMClient):
    def _env_key(self): return "TEST_KEY"
    def _provider_name(self): return "mock"
    def chat(self, messages, model=None, **kwargs):
        return LLMResponse(content="<thinking>Step 1: Check facts.</thinking>Verified content.", model=model or "gpt-4")
    def embed(self, texts, model=None): return []

@pytest.fixture
def mock_client():
    return MockClient()

@pytest.fixture
def guard(mock_client):
    # Ensure template path is correct relative to test execution
    return HallucinationGuard(mock_client, template_path="schemas/governance/anti_hallucination.yaml")

def test_initialization(guard):
    assert guard.client._provider_name() == "mock"
    assert guard._provider_name() == "mock-guarded"

def test_template_injection_standard(guard):
    messages = [{"role": "user", "content": "Hello"}]
    # We mock the internal prepare method to verify it injects prompts
    prepared = guard._prepare_messages(messages, model="gpt-4")

    # Check System Prompt
    assert prepared[0]["role"] == "system"
    assert "SACA" in prepared[0]["content"]
    assert "<thinking>" in prepared[0]["content"] # Standard CoT instruction

def test_template_injection_reasoning(guard):
    messages = [{"role": "user", "content": "Hello"}]
    # For reasoning models, we expect DIFFERENT instructions
    prepared = guard._prepare_messages(messages, model="o1-preview")

    assert prepared[0]["role"] == "system"
    # Should use the simpler instruction
    assert "(Use native reasoning capabilities" in prepared[0]["content"]

def test_chat_flow(guard):
    messages = [{"role": "user", "content": "Test query"}]
    response = guard.chat(messages, model="gpt-4")

    assert response.content == "<thinking>Step 1: Check facts.</thinking>Verified content."
    assert response.metadata["guarded"] is True
    assert response.metadata["verification_status"] == "screened"

"""
Tests for LLM API Base Client / LLM API 基礎客戶端測試
"""

from src.llm_api.base_client import BaseLLMClient, LLMResponse


class TestLLMResponse:
    """Test LLMResponse dataclass / 測試 LLMResponse 資料類別"""

    def test_basic_response(self):
        """Test response creation / 測試回應建立"""
        resp = LLMResponse(
            content="Hello!",
            model="test-model",
            provider="test",
            input_tokens=10,
            output_tokens=5,
        )
        assert resp.content == "Hello!"
        assert resp.model == "test-model"
        assert resp.provider == "test"
        assert resp.input_tokens == 10
        assert resp.output_tokens == 5

    def test_default_values(self):
        """Test default values / 測試預設值"""
        resp = LLMResponse(content="test")
        assert resp.model == ""
        assert resp.provider == ""
        assert resp.input_tokens == 0
        assert resp.latency_ms == 0
        assert resp.metadata == {}


class MockLLMClient(BaseLLMClient):
    """Mock client for testing / 測試用模擬客戶端"""

    def _env_key(self) -> str:
        return "MOCK_API_KEY"

    def _provider_name(self) -> str:
        return "mock"

    def chat(self, messages, model=None, **kwargs):
        return LLMResponse(
            content="mock response",
            model=model or "mock-model",
            provider="mock",
        )

    def embed(self, texts, model=None):
        return [[0.1, 0.2, 0.3] for _ in texts]


class TestBaseLLMClient:
    """Test BaseLLMClient via mock / 透過模擬測試 BaseLLMClient"""

    def test_chat(self):
        """Test chat method / 測試聊天方法"""
        client = MockLLMClient(api_key="test-key")
        resp = client.chat([{"role": "user", "content": "hello"}])
        assert resp.content == "mock response"
        assert resp.provider == "mock"

    def test_embed(self):
        """Test embed method / 測試嵌入方法"""
        client = MockLLMClient(api_key="test-key")
        results = client.embed(["hello", "world"])
        assert len(results) == 2
        assert len(results[0]) == 3

    def test_health_check(self):
        """Test health check / 測試健康檢查"""
        client = MockLLMClient(api_key="test-key")
        assert client.health_check() is True

"""
X.AI / Grok Client / X.AI Grok 客戶端
======================================
Supports: Grok-2, Grok-3 (OpenAI-compatible API)
支援：Grok-2、Grok-3（OpenAI 相容 API）
"""

import time
from typing import Any

from openai import OpenAI

from .base_client import BaseLLMClient, LLMResponse


class XAIClient(BaseLLMClient):
    """X.AI Grok API client (OpenAI-compatible) / X.AI Grok API 客戶端"""

    DEFAULT_MODEL = "grok-3"
    BASE_URL = "https://api.x.ai/v1"

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        super().__init__(api_key, **kwargs)
        self.client = OpenAI(api_key=self.api_key, base_url=self.BASE_URL)

    def _env_key(self) -> str:
        return "XAI_API_KEY"

    def _provider_name(self) -> str:
        return "xai"

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        model = model or self.DEFAULT_MODEL
        start = time.time()
        response = self.client.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        latency = int((time.time() - start) * 1000)
        choice = response.choices[0]
        usage = response.usage
        return LLMResponse(
            content=choice.message.content or "",
            model=model,
            provider=self._provider_name(),
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            latency_ms=latency,
        )

    def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
        """X.AI embedding (if available) / X.AI 嵌入（如可用）"""
        model = model or "grok-embedding"
        response = self.client.embeddings.create(model=model, input=texts)
        return [item.embedding for item in response.data]

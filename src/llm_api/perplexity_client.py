"""
Perplexity AI Client / Perplexity AI 客戶端
============================================
Supports: pplx-70b-online, sonar (OpenAI-compatible API)
支援：pplx-70b-online、sonar（OpenAI 相容 API）
"""

import time
from typing import Any

from openai import OpenAI

from .base_client import BaseLLMClient, LLMResponse


class PerplexityClient(BaseLLMClient):
    """Perplexity AI API client / Perplexity AI API 客戶端"""

    DEFAULT_MODEL = "sonar"
    BASE_URL = "https://api.perplexity.ai"

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        super().__init__(api_key, **kwargs)
        self.client = OpenAI(api_key=self.api_key, base_url=self.BASE_URL)

    def _env_key(self) -> str:
        return "PERPLEXITY_API_KEY"

    def _provider_name(self) -> str:
        return "perplexity"

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
        raise NotImplementedError(
            "Perplexity does not provide an embedding API. "
            "Perplexity 不提供嵌入 API。"
        )

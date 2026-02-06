"""
Anthropic / Claude AI Client / Anthropic Claude 客戶端
======================================================
Supports: Claude Opus 4, Claude Sonnet 4, Claude Haiku
支援：Claude Opus 4、Claude Sonnet 4、Claude Haiku
"""

import time
from typing import Any

from anthropic import Anthropic

from .base_client import BaseLLMClient, LLMResponse


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude API client / Anthropic Claude API 客戶端"""

    DEFAULT_MODEL = "claude-sonnet-4-20250514"

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        super().__init__(api_key, **kwargs)
        self.client = Anthropic(api_key=self.api_key)

    def _env_key(self) -> str:
        return "ANTHROPIC_API_KEY"

    def _provider_name(self) -> str:
        return "anthropic"

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Claude chat completion via Messages API.
        透過 Messages API 進行 Claude 聊天完成。
        """
        model = model or self.DEFAULT_MODEL
        max_tokens = kwargs.pop("max_tokens", 4096)
        start = time.time()

        # Separate system message if present
        # 如果存在則分離系統訊息
        system_msg = ""
        chat_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                chat_messages.append(msg)

        create_kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": chat_messages,
        }
        if system_msg:
            create_kwargs["system"] = system_msg

        response = self.client.messages.create(**create_kwargs, **kwargs)

        latency = int((time.time() - start) * 1000)

        return LLMResponse(
            content=response.content[0].text if response.content else "",
            model=model,
            provider=self._provider_name(),
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            latency_ms=latency,
        )

    def embed(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> list[list[float]]:
        """
        Anthropic does not provide embedding API directly.
        Use sentence-transformers or OpenAI embeddings as fallback.
        Anthropic 不直接提供嵌入 API，使用 sentence-transformers 或 OpenAI 嵌入作為備選。
        """
        raise NotImplementedError(
            "Anthropic does not offer an embedding API. "
            "Use OpenAI or sentence-transformers instead. "
            "Anthropic 不提供嵌入 API，請改用 OpenAI 或 sentence-transformers。"
        )

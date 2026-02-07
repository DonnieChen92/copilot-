"""
OpenAI Client / OpenAI 客戶端 / OpenAI 客户端
==============================================
Supports: GPT-4o, GPT-4-turbo, o1, o3, DALL-E 3, text-embedding-ada-002
支援：GPT-4o、GPT-4-turbo、o1、o3、DALL-E 3、text-embedding-ada-002
"""

import time
from typing import Any

from openai import OpenAI

from .base_client import BaseLLMClient, LLMResponse


class OpenAIClient(BaseLLMClient):
    """OpenAI API client / OpenAI API 客戶端"""

    DEFAULT_MODEL = "gpt-4o"
    DEFAULT_EMBED_MODEL = "text-embedding-ada-002"

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        super().__init__(api_key, **kwargs)
        self.client = OpenAI(api_key=self.api_key)

    def _env_key(self) -> str:
        return "OPENAI_API_KEY"

    def _provider_name(self) -> str:
        return "openai"

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        OpenAI chat completion.
        OpenAI 聊天完成。
        """
        model = model or self.DEFAULT_MODEL
        start = time.time()

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,
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

    def embed(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> list[list[float]]:
        """
        Generate OpenAI embeddings.
        生成 OpenAI 嵌入向量。
        """
        model = model or self.DEFAULT_EMBED_MODEL
        response = self.client.embeddings.create(
            model=model,
            input=texts,
        )
        return [item.embedding for item in response.data]

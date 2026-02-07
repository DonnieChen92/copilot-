"""
Azure OpenAI Client / Azure OpenAI 客戶端
==========================================
Supports: GPT-4, Phi-3, Azure Copilot via Azure OpenAI Service
支援：GPT-4、Phi-3、Azure Copilot（透過 Azure OpenAI 服務）
"""

import time
from typing import Any

from openai import AzureOpenAI

from .base_client import BaseLLMClient, LLMResponse


class AzureClient(BaseLLMClient):
    """Azure OpenAI API client / Azure OpenAI API 客戶端"""

    DEFAULT_MODEL = "gpt-4"

    def __init__(
        self,
        api_key: str | None = None,
        endpoint: str | None = None,
        api_version: str = "2024-02-01",
        **kwargs: Any,
    ):
        super().__init__(api_key, **kwargs)
        import os
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=api_version,
        )

    def _env_key(self) -> str:
        return "AZURE_OPENAI_API_KEY"

    def _provider_name(self) -> str:
        return "azure"

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Azure OpenAI chat completion.
        Azure OpenAI 聊天完成。
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
        Azure OpenAI embeddings.
        Azure OpenAI 嵌入向量。
        """
        model = model or "text-embedding-ada-002"
        response = self.client.embeddings.create(model=model, input=texts)
        return [item.embedding for item in response.data]

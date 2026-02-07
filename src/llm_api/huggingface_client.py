"""
Hugging Face Client / Hugging Face 客戶端
==========================================
Supports: Any open model (Llama, Mistral, Mixtral, etc.) via Inference API
支援：任何開放模型（Llama、Mistral、Mixtral 等）透過推論 API
"""

import time
from typing import Any

from huggingface_hub import InferenceClient

from .base_client import BaseLLMClient, LLMResponse


class HuggingFaceClient(BaseLLMClient):
    """Hugging Face Inference API client / Hugging Face 推論 API 客戶端"""

    DEFAULT_MODEL = "meta-llama/Llama-3.1-70B-Instruct"
    DEFAULT_EMBED_MODEL = "BAAI/bge-large-en-v1.5"

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        super().__init__(api_key, **kwargs)
        self.client = InferenceClient(token=self.api_key)

    def _env_key(self) -> str:
        return "HUGGINGFACE_API_KEY"

    def _provider_name(self) -> str:
        return "huggingface"

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Hugging Face chat completion via Inference API.
        透過推論 API 進行 Hugging Face 聊天完成。
        """
        model_name = model or self.DEFAULT_MODEL
        start = time.time()

        response = self.client.chat_completion(
            model=model_name,
            messages=messages,
            **kwargs,
        )

        latency = int((time.time() - start) * 1000)
        content = response.choices[0].message.content if response.choices else ""
        usage = response.usage

        return LLMResponse(
            content=content or "",
            model=model_name,
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
        Hugging Face embedding via Inference API.
        透過推論 API 生成 Hugging Face 嵌入向量。
        """
        model_name = model or self.DEFAULT_EMBED_MODEL
        results = []
        for text in texts:
            embedding = self.client.feature_extraction(text, model=model_name)
            # feature_extraction returns nested list; take mean pooling
            # 取平均池化
            if isinstance(embedding[0], list):
                import numpy as np
                embedding = np.mean(embedding, axis=0).tolist()
            results.append(embedding)
        return results

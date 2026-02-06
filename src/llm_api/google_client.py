"""
Google AI / Gemini Client / Google AI Gemini 客戶端
===================================================
Supports: Gemini 2.0 Flash, Gemini Pro, Imagen 3
支援：Gemini 2.0 Flash、Gemini Pro、Imagen 3
"""

import time
from typing import Any

import google.generativeai as genai

from .base_client import BaseLLMClient, LLMResponse


class GoogleAIClient(BaseLLMClient):
    """Google Gemini API client / Google Gemini API 客戶端"""

    DEFAULT_MODEL = "gemini-2.0-flash"
    DEFAULT_EMBED_MODEL = "models/embedding-001"

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        super().__init__(api_key, **kwargs)
        genai.configure(api_key=self.api_key)

    def _env_key(self) -> str:
        return "GOOGLE_AI_API_KEY"

    def _provider_name(self) -> str:
        return "google"

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Google Gemini chat completion.
        Google Gemini 聊天完成。
        """
        model_name = model or self.DEFAULT_MODEL
        start = time.time()

        gmodel = genai.GenerativeModel(model_name)

        # Convert messages to Gemini format / 轉換訊息為 Gemini 格式
        history = []
        last_content = ""
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            if msg == messages[-1]:
                last_content = msg["content"]
            else:
                history.append({"role": role, "parts": [msg["content"]]})

        chat = gmodel.start_chat(history=history)
        response = chat.send_message(last_content)
        latency = int((time.time() - start) * 1000)

        return LLMResponse(
            content=response.text,
            model=model_name,
            provider=self._provider_name(),
            latency_ms=latency,
        )

    def embed(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> list[list[float]]:
        """
        Google embedding generation.
        Google 嵌入向量生成。
        """
        model_name = model or self.DEFAULT_EMBED_MODEL
        results = []
        for text in texts:
            result = genai.embed_content(model=model_name, content=text)
            results.append(result["embedding"])
        return results

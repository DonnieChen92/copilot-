"""
Tencent AI / Hunyuan Client / 騰訊AI混元客戶端 / 腾讯AI混元客户端
=================================================================
Supports: Hunyuan-Large, Hunyuan-Pro
支援：混元-Large、混元-Pro
"""

import json
import time
from typing import Any

from .base_client import BaseLLMClient, LLMResponse


class TencentClient(BaseLLMClient):
    """
    Tencent Hunyuan API client.
    騰訊混元 API 客戶端。
    腾讯混元 API 客户端。

    Uses tencentcloud-sdk-python for authentication.
    使用 tencentcloud-sdk-python 進行身份驗證。
    """

    DEFAULT_MODEL = "hunyuan-pro"

    def __init__(
        self,
        api_key: str | None = None,
        secret_id: str | None = None,
        secret_key: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(api_key, **kwargs)
        import os
        self.secret_id = secret_id or os.getenv("TENCENT_SECRET_ID", "")
        self.secret_key = secret_key or os.getenv("TENCENT_SECRET_KEY", "")

    def _env_key(self) -> str:
        return "TENCENT_API_KEY"

    def _provider_name(self) -> str:
        return "tencent"

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Tencent Hunyuan chat completion.
        騰訊混元聊天完成。
        腾讯混元聊天完成。
        """
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

        model_name = model or self.DEFAULT_MODEL
        start = time.time()

        cred = credential.Credential(self.secret_id, self.secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        client = hunyuan_client.HunyuanClient(cred, "", clientProfile)
        req = models.ChatCompletionsRequest()
        req.Model = model_name
        req.Messages = [
            {"Role": msg["role"], "Content": msg["content"]} for msg in messages
        ]

        resp = client.ChatCompletions(req)
        latency = int((time.time() - start) * 1000)

        result = json.loads(resp.to_json_string())
        content = result.get("Choices", [{}])[0].get("Message", {}).get("Content", "")
        usage = result.get("Usage", {})

        return LLMResponse(
            content=content,
            model=model_name,
            provider=self._provider_name(),
            input_tokens=usage.get("PromptTokens", 0),
            output_tokens=usage.get("CompletionTokens", 0),
            latency_ms=latency,
        )

    def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
        """
        Tencent Hunyuan embedding.
        騰訊混元嵌入向量。
        """
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

        cred = credential.Credential(self.secret_id, self.secret_key)
        clientProfile = ClientProfile()
        client = hunyuan_client.HunyuanClient(cred, "", clientProfile)

        results = []
        for text in texts:
            req = models.GetEmbeddingRequest()
            req.Input = text
            resp = client.GetEmbedding(req)
            data = json.loads(resp.to_json_string())
            results.append(data.get("Data", [{}])[0].get("Embedding", []))
        return results

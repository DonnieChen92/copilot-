"""
Base LLM Client / 基礎 LLM 客戶端 / 基础 LLM 客户端
=====================================================
Abstract base class for all LLM provider clients.
所有 LLM 提供者客戶端的抽象基底類別。
所有 LLM 提供者客户端的抽象基类。
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMResponse:
    """
    Standardized LLM response / 標準化 LLM 回應 / 标准化 LLM 响应
    """
    content: str                          # Response text / 回應文本 / 响应文本
    model: str = ""                       # Model used / 使用的模型 / 使用的模型
    provider: str = ""                    # Provider name / 提供者名稱 / 提供者名称
    input_tokens: int = 0                 # Input token count / 輸入令牌數 / 输入令牌数
    output_tokens: int = 0               # Output token count / 輸出令牌數 / 输出令牌数
    latency_ms: int = 0                  # Response latency / 回應延遲 / 响应延迟
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseLLMClient(ABC):
    """
    Abstract base for LLM clients.
    LLM 客戶端的抽象基底。
    LLM 客户端的抽象基类。

    All provider-specific clients inherit from this base.
    所有特定提供者的客戶端都繼承此基底。
    所有特定提供者的客户端都继承此基类。
    """

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        self.api_key = api_key or os.getenv(self._env_key(), "")
        self.config = kwargs

    @abstractmethod
    def _env_key(self) -> str:
        """Environment variable name for API key / API 金鑰的環境變數名稱"""
        ...

    @abstractmethod
    def _provider_name(self) -> str:
        """Provider identifier / 提供者識別碼 / 提供者标识符"""
        ...

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Send chat completion request.
        傳送聊天完成請求。
        发送聊天完成请求。

        Args:
            messages: [{"role": "user", "content": "..."}]
            model: Model name override / 模型名稱覆蓋
        """
        ...

    @abstractmethod
    def embed(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> list[list[float]]:
        """
        Generate embeddings for texts.
        為文本生成嵌入向量。
        为文本生成嵌入向量。

        Args:
            texts: List of text strings / 文本字串列表 / 文本字符串列表
            model: Embedding model name / 嵌入模型名稱
        """
        ...

    def health_check(self) -> bool:
        """
        Verify API connectivity.
        驗證 API 連線。
        验证 API 连接。
        """
        try:
            resp = self.chat(
                [{"role": "user", "content": "ping"}],
                max_tokens=5,
            )
            return bool(resp.content)
        except Exception:
            return False

"""
LLM API Integration Layer / LLM API 整合層 / LLM API 整合层
============================================================
Multi-provider LLM client supporting:
多提供者 LLM 客戶端，支援：
多提供者 LLM 客户端，支持：

- OpenAI (GPT-4o, o1, o3, DALL-E 3)
- Google AI / Gemini (Gemini 2.0 Flash, Pro, Imagen 3)
- Microsoft Azure AI (GPT-4, Phi-3, Copilot)
- Anthropic / Claude AI (Opus, Sonnet, Haiku)
- X.AI / Grok (Grok-2, Grok-3)
- Perplexity AI (pplx-70b-online, sonar)
- DeepSeek (V3, R1)
- Tencent AI / Hunyuan (Hunyuan-Large, Hunyuan-Pro)
- Hugging Face (open models: Llama, Mistral, etc.)
"""

from .base_client import BaseLLMClient

__all__ = ["BaseLLMClient"]

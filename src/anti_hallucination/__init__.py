"""
Anti-Hallucination Module / 反幻覺模組 / 反幻觉模块
====================================================
Provides query templates, check filters, and screening tools
to reduce hallucination in LLM responses, especially for
ChatGPT / GPT Thinking models (o1, o3) via Codex integration.

提供查詢模板、檢查過濾器和篩選工具，
以減少 LLM 回應中的幻覺，特別針對
ChatGPT / GPT Thinking 模型 (o1, o3) 透過 Codex 整合。
"""

from .template_engine import (
    AntiHallucinationTemplate,
    TemplatePlaceholder,
    TemplateLibrary,
)
from .check_filter import (
    HallucinationCheckFilter,
    CheckResult,
    ClaimVerification,
)
from .codex_query_builder import CodexQueryBuilder
from .filter_screen import FilterScreen, ScreenReport
from .thinking_model_handler import ThinkingModelHandler

__all__ = [
    "AntiHallucinationTemplate",
    "TemplatePlaceholder",
    "TemplateLibrary",
    "HallucinationCheckFilter",
    "CheckResult",
    "ClaimVerification",
    "CodexQueryBuilder",
    "FilterScreen",
    "ScreenReport",
    "ThinkingModelHandler",
]

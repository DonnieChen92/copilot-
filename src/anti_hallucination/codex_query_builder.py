"""
Codex Query Builder / Codex 查詢構建器 / Codex 查询构建器
=========================================================
Builds structured, anti-hallucination queries for OpenAI
Codex / GPT models. Wraps template rendering with automatic
filter triggering and response validation.

為 OpenAI Codex / GPT 模型構建結構化的反幻覺查詢。
封裝模板渲染與自動過濾觸發和回應驗證。

Workflow:
1. Select template & fill placeholders  →  build_query()
2. Send to LLM via execute()            →  get raw response
3. Auto-run check filters               →  get CheckResult
4. Return validated response or retry    →  QueryResult
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .template_engine import (
    AntiHallucinationTemplate,
    ModelTier,
    TemplateCategory,
    TemplateLibrary,
)
from .check_filter import (
    CheckResult,
    FilterType,
    HallucinationCheckFilter,
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class QueryResult:
    """
    Complete result from a Codex anti-hallucination query cycle.
    Codex 反幻覺查詢週期的完整結果。
    """
    response_text: str
    check_result: CheckResult
    template_name: str
    model_used: str
    attempt: int = 1
    total_latency_ms: int = 0
    retried: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.check_result.passed

    @property
    def score(self) -> float:
        return self.check_result.overall_score


# ---------------------------------------------------------------------------
# Codex Query Builder
# ---------------------------------------------------------------------------

class CodexQueryBuilder:
    """
    Builds and executes anti-hallucination queries through Codex / GPT models.
    透過 Codex / GPT 模型構建並執行反幻覺查詢。

    This class integrates three core components:
    - TemplateLibrary: selects and renders prompts
    - LLM Client: sends the rendered prompt to OpenAI
    - HallucinationCheckFilter: validates the response

    Usage:
        from src.llm_api.openai_client import OpenAIClient
        from src.anti_hallucination import CodexQueryBuilder

        client = OpenAIClient(api_key="sk-...")
        builder = CodexQueryBuilder(llm_client=client)

        # Quick factual query
        result = builder.factual_query(
            context="The Great Wall is over 13,000 miles long...",
            question="How long is the Great Wall?",
        )
        print(result.response_text)
        print(result.check_result.summary())

        # Code generation query
        result = builder.code_query(
            language="Python 3.11",
            libraries="pandas, openpyxl",
            task_description="Read an Excel file and return column means.",
        )
    """

    DEFAULT_MODEL_MAP = {
        ModelTier.STANDARD: "gpt-4o",
        ModelTier.THINKING: "o3",
        ModelTier.CODEX: "gpt-4o",
    }

    def __init__(
        self,
        llm_client: Any | None = None,
        *,
        template_library: TemplateLibrary | None = None,
        check_filter: HallucinationCheckFilter | None = None,
        pass_threshold: float = 0.6,
        max_retries: int = 2,
        model_overrides: dict[str, str] | None = None,
    ):
        """
        Args:
            llm_client: Any LLM client with a `.chat(messages, model=...)` method.
            template_library: Custom template library (default: built-in).
            check_filter: Custom check filter (default: built-in).
            pass_threshold: Minimum score to pass check filter.
            max_retries: Number of retry attempts if validation fails.
            model_overrides: Override model per tier, e.g. {"thinking": "o1"}.
        """
        self.llm_client = llm_client
        self.library = template_library or TemplateLibrary()
        self.checker = check_filter or HallucinationCheckFilter(
            pass_threshold=pass_threshold,
        )
        self.max_retries = max_retries
        self.pass_threshold = pass_threshold

        # Model resolution
        self._models = dict(self.DEFAULT_MODEL_MAP)
        if model_overrides:
            for tier_key, model_name in model_overrides.items():
                try:
                    tier = ModelTier(tier_key)
                except ValueError:
                    continue
                self._models[tier] = model_name

    # ------------------------------------------------------------------
    # Core methods
    # ------------------------------------------------------------------

    def build_query(
        self,
        template_name: str,
        values: dict[str, str],
        *,
        include_grounding: bool = True,
        include_self_check: bool = True,
    ) -> list[dict[str, str]]:
        """
        Build chat messages from a named template + placeholder values.
        從命名模板和佔位符值構建聊天訊息。

        Returns list of {"role": ..., "content": ...} dicts.
        """
        template = self.library.get(template_name)
        return template.render(
            values,
            include_grounding=include_grounding,
            include_self_check=include_self_check,
        )

    def execute(
        self,
        template_name: str,
        values: dict[str, str],
        *,
        source: str = "",
        api_reference: str = "",
        model: str | None = None,
        enabled_filters: list[FilterType] | None = None,
        auto_retry: bool = True,
        extra_kwargs: dict[str, Any] | None = None,
    ) -> QueryResult:
        """
        Full cycle: render → send to LLM → check → (retry if needed).
        完整週期：渲染 → 發送到 LLM → 檢查 → （需要時重試）。

        Args:
            template_name: Name of the template to use.
            values: Placeholder fill values.
            source: Source material for grounding checks.
            api_reference: API docs for code verification.
            model: Override the model for this call.
            enabled_filters: Subset of filters to apply.
            auto_retry: Whether to retry on failed checks.
            extra_kwargs: Additional kwargs for the LLM client.

        Returns:
            QueryResult with response, check results, and metadata.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "No LLM client configured. Pass llm_client= to constructor "
                "or use build_query() for message-only generation."
            )

        template = self.library.get(template_name)
        resolved_model = model or self._models.get(template.model_tier, "gpt-4o")
        kwargs = extra_kwargs or {}

        # Source for grounding: prefer explicit source, fall back to context placeholder
        grounding_source = source or values.get("context", "")

        best_result: QueryResult | None = None

        for attempt in range(1, self.max_retries + 1):
            messages = template.render(values)
            start = time.time()
            llm_response = self.llm_client.chat(
                messages, model=resolved_model, **kwargs
            )
            latency = int((time.time() - start) * 1000)

            response_text = llm_response.content

            # Run checks
            check_result = self.checker.check(
                response=response_text,
                source=grounding_source,
                api_reference=api_reference,
                enabled_filters=enabled_filters,
            )

            result = QueryResult(
                response_text=response_text,
                check_result=check_result,
                template_name=template_name,
                model_used=resolved_model,
                attempt=attempt,
                total_latency_ms=latency,
                retried=attempt > 1,
                metadata={
                    "input_tokens": llm_response.input_tokens,
                    "output_tokens": llm_response.output_tokens,
                },
            )

            if check_result.passed or not auto_retry:
                return result

            # Track best result so far
            if best_result is None or check_result.overall_score > best_result.score:
                best_result = result

            # On retry: add feedback to prompt
            values = dict(values)  # don't mutate caller's dict
            feedback = self._build_retry_feedback(check_result)
            if "context" in values:
                values["context"] += f"\n\n[SYSTEM FEEDBACK]\n{feedback}"

        # Return best attempt
        return best_result or result  # type: ignore[possibly-undefined]

    # ------------------------------------------------------------------
    # Convenience methods for common query patterns
    # ------------------------------------------------------------------

    def factual_query(
        self,
        context: str,
        question: str,
        *,
        model: str | None = None,
        use_thinking: bool = False,
    ) -> QueryResult:
        """
        Quick factual QA query.
        快速事實問答查詢。
        """
        template_name = "factual_qa_thinking" if use_thinking else "factual_qa"
        return self.execute(
            template_name=template_name,
            values={"context": context, "question": question},
            source=context,
            model=model,
        )

    def code_query(
        self,
        language: str,
        libraries: str,
        task_description: str,
        *,
        api_reference: str = "",
        constraints: str = "",
        model: str | None = None,
    ) -> QueryResult:
        """
        Code generation query with API verification.
        帶 API 驗證的代碼生成查詢。
        """
        values = {
            "language": language,
            "libraries": libraries,
            "task_description": task_description,
        }
        if api_reference:
            values["api_reference"] = api_reference
        if constraints:
            values["constraints"] = constraints

        lib_list = [lib.strip().split(">=")[0].split("==")[0]
                    for lib in libraries.split(",")]

        checker = HallucinationCheckFilter(
            pass_threshold=self.pass_threshold,
            known_libraries=lib_list,
        )

        return self.execute(
            template_name="code_generation",
            values=values,
            api_reference=api_reference,
            model=model,
            enabled_filters=[
                FilterType.CODE_API_VERIFY,
                FilterType.CONFIDENCE_CALIBRATION,
            ],
        )

    def reasoning_query(
        self,
        problem: str,
        known_facts: str,
        *,
        domain: str = "General",
        model: str | None = None,
    ) -> QueryResult:
        """
        Chain-of-thought reasoning query for Thinking models.
        適用於 Thinking 模型的思維鏈推理查詢。
        """
        return self.execute(
            template_name="reasoning_cot",
            values={
                "domain": domain,
                "known_facts": known_facts,
                "problem": problem,
            },
            source=known_facts,
            model=model,
        )

    def summarize_query(
        self,
        source_text: str,
        *,
        target_length: str = "3-5 sentences",
        focus_areas: str = "All key points",
        model: str | None = None,
    ) -> QueryResult:
        """
        Summarization query with source fidelity checks.
        帶源忠實度檢查的摘要查詢。
        """
        return self.execute(
            template_name="summarization",
            values={
                "source_text": source_text,
                "target_length": target_length,
                "focus_areas": focus_areas,
            },
            source=source_text,
            model=model,
        )

    def entity_extraction_query(
        self,
        text: str,
        *,
        entity_types: str = "PERSON, ORGANIZATION, LOCATION, DATE, PRODUCT",
        model: str | None = None,
    ) -> QueryResult:
        """
        Entity extraction query with verbatim verification.
        帶逐字驗證的實體提取查詢。
        """
        return self.execute(
            template_name="entity_extraction",
            values={
                "text": text,
                "entity_types": entity_types,
            },
            source=text,
            model=model,
        )

    def multilingual_query(
        self,
        context: str,
        question: str,
        *,
        response_language: str = "Same as the question",
        model: str | None = None,
    ) -> QueryResult:
        """
        Multilingual QA query.
        多語言問答查詢。
        """
        return self.execute(
            template_name="multilingual_qa",
            values={
                "context": context,
                "question": question,
                "response_language": response_language,
            },
            source=context,
            model=model,
        )

    def code_review_query(
        self,
        language: str,
        code: str,
        *,
        model: str | None = None,
    ) -> QueryResult:
        """
        Code review query with anti-hallucination.
        帶反幻覺的代碼審查查詢。
        """
        return self.execute(
            template_name="code_review",
            values={
                "language": language,
                "code": code,
            },
            source=code,
            model=model,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_retry_feedback(self, check_result: CheckResult) -> str:
        """Build feedback text from failed check to guide retry."""
        lines = [
            "Your previous response had hallucination issues. Please fix:",
        ]
        for claim in check_result.claims:
            if claim.is_problematic():
                lines.append(
                    f"- {claim.status.value.upper()}: \"{claim.claim_text[:80]}\" "
                    f"({claim.notes or claim.evidence})"
                )
        lines.append(
            "\nPlease regenerate your response ensuring all claims "
            "are grounded in the provided source material."
        )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Batch operations
    # ------------------------------------------------------------------

    def batch_execute(
        self,
        queries: list[dict[str, Any]],
    ) -> list[QueryResult]:
        """
        Execute multiple queries sequentially.
        依序執行多個查詢。

        Each item in queries is a dict with keys matching execute() params:
            {"template_name": "...", "values": {...}, "source": "...", ...}
        """
        results = []
        for q in queries:
            template_name = q.pop("template_name")
            values = q.pop("values")
            result = self.execute(template_name, values, **q)
            results.append(result)
        return results

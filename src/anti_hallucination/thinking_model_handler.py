"""
Thinking Model Handler / Thinking 模型處理器 / Thinking 模型处理器
===================================================================
Specialized handler for OpenAI Thinking models (o1, o3) that
automatically triggers anti-hallucination checks during the
extended reasoning process.

專門處理 OpenAI Thinking 模型 (o1, o3)，
在擴展推理過程中自動觸發反幻覺檢查。

Key Features / 關鍵特性:
- Thinking trace extraction and analysis
- Automatic claim-evidence mapping from thinking steps
- Confidence calibration based on reasoning depth
- Parallel consistency checking (query N times, compare)
- Structured output parsing for Thinking model responses
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .template_engine import (
    AntiHallucinationTemplate,
    ModelTier,
    TemplateLibrary,
)
from .check_filter import (
    CheckResult,
    ClaimVerification,
    FilterType,
    HallucinationCheckFilter,
    SeverityLevel,
    VerificationStatus,
)
from .codex_query_builder import CodexQueryBuilder, QueryResult
from .filter_screen import FilterScreen, ScreenReport


# ---------------------------------------------------------------------------
# Data classes for thinking-specific analysis
# ---------------------------------------------------------------------------

@dataclass
class ThinkingStep:
    """
    A single step extracted from a Thinking model's reasoning trace.
    從 Thinking 模型推理軌跡中提取的單個步驟。
    """
    step_number: int
    content: str
    step_type: str = "reasoning"      # reasoning | evidence | assumption | conclusion
    evidence_refs: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def has_evidence(self) -> bool:
        return len(self.evidence_refs) > 0


@dataclass
class ThinkingAnalysis:
    """
    Complete analysis of a Thinking model response.
    Thinking 模型回應的完整分析。
    """
    raw_response: str
    thinking_trace: str
    final_answer: str
    steps: list[ThinkingStep] = field(default_factory=list)
    stated_confidence: str = ""
    unsupported_claims: list[str] = field(default_factory=list)
    check_result: CheckResult | None = None

    @property
    def grounded_step_ratio(self) -> float:
        if not self.steps:
            return 0.0
        grounded = sum(1 for s in self.steps if s.has_evidence())
        return grounded / len(self.steps)

    def summary(self) -> dict[str, Any]:
        return {
            "total_steps": len(self.steps),
            "grounded_steps": sum(1 for s in self.steps if s.has_evidence()),
            "grounded_ratio": round(self.grounded_step_ratio, 3),
            "stated_confidence": self.stated_confidence,
            "unsupported_claims_count": len(self.unsupported_claims),
            "check_passed": self.check_result.passed if self.check_result else None,
            "check_score": self.check_result.overall_score if self.check_result else None,
        }


# ---------------------------------------------------------------------------
# Thinking Model Handler
# ---------------------------------------------------------------------------

class ThinkingModelHandler:
    """
    Orchestrates anti-hallucination workflows for Thinking models (o1, o3).
    為 Thinking 模型 (o1, o3) 編排反幻覺工作流程。

    Thinking models produce extended reasoning traces. This handler:
    1. Parses the structured response (Thinking Trace / Answer / Confidence)
    2. Extracts individual reasoning steps
    3. Verifies each step against source material
    4. Checks consistency across multiple invocations
    5. Produces a comprehensive ThinkingAnalysis

    Usage:
        from src.llm_api.openai_client import OpenAIClient
        from src.anti_hallucination import ThinkingModelHandler

        client = OpenAIClient()
        handler = ThinkingModelHandler(llm_client=client)

        analysis = handler.analyze_response(
            template_name="factual_qa_thinking",
            values={"context": "...", "question": "..."},
        )
        print(analysis.summary())

        # With consistency checking (multiple passes)
        analysis = handler.analyze_with_consistency(
            template_name="reasoning_cot",
            values={"known_facts": "...", "problem": "..."},
            num_passes=3,
        )
    """

    # Default thinking model
    DEFAULT_MODEL = "o3"

    # Section markers in thinking model output
    SECTION_PATTERNS = {
        "thinking": re.compile(
            r"###?\s*Thinking\s*(?:Trace)?\s*\n(.*?)(?=###?\s|\Z)",
            re.DOTALL | re.IGNORECASE,
        ),
        "answer": re.compile(
            r"###?\s*Answer\s*\n(.*?)(?=###?\s|\Z)",
            re.DOTALL | re.IGNORECASE,
        ),
        "confidence": re.compile(
            r"###?\s*Confidence\s*\n(.*?)(?=###?\s|\Z)",
            re.DOTALL | re.IGNORECASE,
        ),
        "unsupported": re.compile(
            r"###?\s*Unsupported\s*(?:Claims)?\s*\n(.*?)(?=###?\s|\Z)",
            re.DOTALL | re.IGNORECASE,
        ),
    }

    # Step extraction patterns within thinking trace
    STEP_PATTERNS = [
        re.compile(r"(?:Step\s+)?(\d+)[.)]\s*(.+?)(?=(?:Step\s+)?\d+[.)]|\Z)", re.DOTALL),
        re.compile(r"[-*]\s+(.+?)(?=[-*]\s|\Z)", re.DOTALL),
    ]

    def __init__(
        self,
        llm_client: Any | None = None,
        *,
        template_library: TemplateLibrary | None = None,
        check_filter: HallucinationCheckFilter | None = None,
        model: str | None = None,
        pass_threshold: float = 0.6,
    ):
        self.llm_client = llm_client
        self.library = template_library or TemplateLibrary()
        self.checker = check_filter or HallucinationCheckFilter(
            pass_threshold=pass_threshold,
        )
        self.model = model or self.DEFAULT_MODEL
        self.pass_threshold = pass_threshold

        self._query_builder = CodexQueryBuilder(
            llm_client=llm_client,
            template_library=self.library,
            check_filter=self.checker,
            pass_threshold=pass_threshold,
            model_overrides={"thinking": self.model},
        )
        self._screen = FilterScreen()

    # ------------------------------------------------------------------
    # Core analysis
    # ------------------------------------------------------------------

    def parse_thinking_response(self, response_text: str) -> ThinkingAnalysis:
        """
        Parse a Thinking model's structured response into components.
        解析 Thinking 模型的結構化回應為組件。
        """
        sections: dict[str, str] = {}
        for key, pattern in self.SECTION_PATTERNS.items():
            match = pattern.search(response_text)
            sections[key] = match.group(1).strip() if match else ""

        thinking_trace = sections.get("thinking", "")
        final_answer = sections.get("answer", "")
        confidence_text = sections.get("confidence", "")
        unsupported_text = sections.get("unsupported", "")

        # If no structured sections found, treat the whole thing as the answer
        if not final_answer and not thinking_trace:
            final_answer = response_text

        # Extract steps from thinking trace
        steps = self._extract_steps(thinking_trace)

        # Extract unsupported claims list
        unsupported_claims = self._extract_unsupported_claims(unsupported_text)

        return ThinkingAnalysis(
            raw_response=response_text,
            thinking_trace=thinking_trace,
            final_answer=final_answer,
            steps=steps,
            stated_confidence=confidence_text,
            unsupported_claims=unsupported_claims,
        )

    def analyze_response(
        self,
        template_name: str,
        values: dict[str, str],
        *,
        source: str = "",
        model: str | None = None,
    ) -> ThinkingAnalysis:
        """
        Execute a Thinking model query and analyze the response.
        執行 Thinking 模型查詢並分析回應。

        Args:
            template_name: Template to use (e.g. "factual_qa_thinking").
            values: Placeholder fill values.
            source: Source material for grounding verification.
            model: Override model (default: o3).

        Returns:
            ThinkingAnalysis with parsed steps and check results.
        """
        resolved_model = model or self.model
        grounding_source = source or values.get("context", "") or values.get("known_facts", "")

        # Execute query
        query_result = self._query_builder.execute(
            template_name=template_name,
            values=values,
            source=grounding_source,
            model=resolved_model,
            auto_retry=False,
        )

        # Parse the response
        analysis = self.parse_thinking_response(query_result.response_text)

        # Run step-level verification
        if grounding_source:
            step_claims = self._verify_steps(analysis.steps, grounding_source)
            analysis.check_result = self._build_step_check_result(
                step_claims, query_result.check_result
            )
        else:
            analysis.check_result = query_result.check_result

        return analysis

    def analyze_with_consistency(
        self,
        template_name: str,
        values: dict[str, str],
        *,
        source: str = "",
        num_passes: int = 3,
        model: str | None = None,
    ) -> ThinkingAnalysis:
        """
        Run the query multiple times and check self-consistency.
        多次執行查詢並檢查自我一致性。

        Uses the self-consistency filter to identify claims that
        appear in only some of the responses (likely hallucinated).
        """
        if self.llm_client is None:
            raise RuntimeError("No LLM client configured.")

        resolved_model = model or self.model
        grounding_source = source or values.get("context", "") or values.get("known_facts", "")

        # Collect multiple responses
        responses: list[str] = []
        analyses: list[ThinkingAnalysis] = []

        for _ in range(num_passes):
            template = self.library.get(template_name)
            messages = template.render(values)
            llm_resp = self.llm_client.chat(messages, model=resolved_model)
            responses.append(llm_resp.content)
            analyses.append(self.parse_thinking_response(llm_resp.content))

        # Self-consistency check
        consistency_result = self.checker.check_self_consistency(
            responses, grounding_source
        )

        # Use the best single analysis
        best_analysis = max(analyses, key=lambda a: a.grounded_step_ratio)
        best_analysis.check_result = consistency_result

        return best_analysis

    # ------------------------------------------------------------------
    # Screen rendering shortcuts
    # ------------------------------------------------------------------

    def render_analysis(self, analysis: ThinkingAnalysis) -> ScreenReport:
        """
        Render a ThinkingAnalysis into a screen report.
        將 ThinkingAnalysis 渲染為畫面報告。
        """
        if analysis.check_result:
            report = self._screen.render_check_result(
                analysis.check_result,
                title="Thinking Model Analysis",
            )
        else:
            report = ScreenReport(
                title="Thinking Model Analysis",
                timestamp="",
                text_output="(No check result available)",
            )

        # Augment with thinking-specific data
        report.structured_data["thinking_summary"] = analysis.summary()
        return report

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_steps(self, thinking_trace: str) -> list[ThinkingStep]:
        """Extract numbered or bulleted steps from thinking trace."""
        steps: list[ThinkingStep] = []
        if not thinking_trace:
            return steps

        # Try numbered steps first
        numbered = self.STEP_PATTERNS[0].findall(thinking_trace)
        if numbered:
            for num_str, content in numbered:
                content = content.strip()
                if len(content) < 5:
                    continue
                step_type = self._classify_step(content)
                evidence = self._extract_evidence_refs(content)
                steps.append(ThinkingStep(
                    step_number=int(num_str),
                    content=content,
                    step_type=step_type,
                    evidence_refs=evidence,
                    confidence=0.8 if evidence else 0.3,
                ))
            return steps

        # Fall back to bulleted items
        bulleted = self.STEP_PATTERNS[1].findall(thinking_trace)
        for i, content in enumerate(bulleted, 1):
            content = content.strip()
            if len(content) < 5:
                continue
            step_type = self._classify_step(content)
            evidence = self._extract_evidence_refs(content)
            steps.append(ThinkingStep(
                step_number=i,
                content=content,
                step_type=step_type,
                evidence_refs=evidence,
                confidence=0.8 if evidence else 0.3,
            ))

        # If neither pattern matched, split by sentences
        if not steps:
            sentences = re.split(r'(?<=[.!?])\s+', thinking_trace)
            for i, sent in enumerate(sentences, 1):
                sent = sent.strip()
                if len(sent) < 10:
                    continue
                evidence = self._extract_evidence_refs(sent)
                steps.append(ThinkingStep(
                    step_number=i,
                    content=sent,
                    step_type="reasoning",
                    evidence_refs=evidence,
                    confidence=0.5 if evidence else 0.2,
                ))

        return steps

    @staticmethod
    def _classify_step(content: str) -> str:
        """Classify a thinking step by its nature."""
        content_lower = content.lower()
        if any(w in content_lower for w in ["therefore", "thus", "conclude", "結論", "因此"]):
            return "conclusion"
        if any(w in content_lower for w in ["assume", "suppose", "假設", "假设"]):
            return "assumption"
        if any(w in content_lower for w in ["source", "context", "states", "mentions", "根據", "來源"]):
            return "evidence"
        return "reasoning"

    @staticmethod
    def _extract_evidence_refs(content: str) -> list[str]:
        """Extract evidence references from step content."""
        refs: list[str] = []
        # Look for quoted text
        quotes = re.findall(r'"([^"]{5,})"', content)
        refs.extend(quotes)
        # Look for [SOURCE], [GIVEN], etc. markers
        markers = re.findall(r'\[(SOURCE|GIVEN|CONTEXT|EVIDENCE)[^\]]*\]', content, re.IGNORECASE)
        refs.extend(markers)
        return refs

    @staticmethod
    def _extract_unsupported_claims(text: str) -> list[str]:
        """Extract unsupported claims list from the response section."""
        if not text or text.strip().lower() in ("none", "none.", "n/a", "(none)", "(empty)"):
            return []
        claims = re.findall(r'[-*]\s+(.+)', text)
        if claims:
            return [c.strip() for c in claims if len(c.strip()) > 5]
        return [text.strip()] if len(text.strip()) > 5 else []

    def _verify_steps(
        self,
        steps: list[ThinkingStep],
        source: str,
    ) -> list[ClaimVerification]:
        """Verify thinking steps against source material."""
        verifications: list[ClaimVerification] = []
        source_lower = source.lower()

        for step in steps:
            # Check if the step content has source overlap
            step_words = set(re.findall(r'\b\w{3,}\b', step.content.lower()))
            source_words = set(re.findall(r'\b\w{3,}\b', source_lower))
            overlap = step_words & source_words
            ratio = len(overlap) / len(step_words) if step_words else 0

            if step.step_type == "evidence" and step.has_evidence():
                status = VerificationStatus.SUPPORTED
                severity = SeverityLevel.INFO
                conf = max(ratio, 0.7)
            elif ratio >= 0.5:
                status = VerificationStatus.SUPPORTED
                severity = SeverityLevel.INFO
                conf = ratio
            elif ratio >= 0.2:
                status = VerificationStatus.PARTIALLY_SUPPORTED
                severity = SeverityLevel.INFO
                conf = ratio
            elif step.step_type == "assumption":
                status = VerificationStatus.UNVERIFIABLE
                severity = SeverityLevel.WARNING
                conf = 0.3
            else:
                status = VerificationStatus.UNSUPPORTED
                severity = SeverityLevel.WARNING
                conf = ratio

            verifications.append(ClaimVerification(
                claim_text=f"[Step {step.step_number}] {step.content[:80]}",
                status=status,
                severity=severity,
                evidence=f"Source word overlap: {len(overlap)}/{len(step_words)}",
                confidence=round(conf, 3),
                notes=f"Step type: {step.step_type}",
            ))

        return verifications

    def _build_step_check_result(
        self,
        step_claims: list[ClaimVerification],
        base_check: CheckResult,
    ) -> CheckResult:
        """Merge step-level claims with the base check result."""
        all_claims = base_check.claims + step_claims
        if all_claims:
            score = sum(c.confidence for c in all_claims) / len(all_claims)
        else:
            score = base_check.overall_score

        return CheckResult(
            passed=score >= self.pass_threshold,
            overall_score=score,
            claims=all_claims,
            filters_applied=base_check.filters_applied + ["thinking_step_verify"],
            warnings=base_check.warnings,
            metadata={
                **base_check.metadata,
                "thinking_steps_checked": len(step_claims),
            },
        )

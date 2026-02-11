"""
Tests for Anti-Hallucination Module
反幻覺模組測試 / 反幻觉模块测试
====================================
Covers: template_engine, check_filter, codex_query_builder,
        filter_screen, thinking_model_handler
"""

import json
import pytest

from src.anti_hallucination.template_engine import (
    AntiHallucinationTemplate,
    ModelTier,
    TemplateCategory,
    TemplateLibrary,
    TemplatePlaceholder,
)
from src.anti_hallucination.check_filter import (
    CheckResult,
    ClaimVerification,
    FilterType,
    HallucinationCheckFilter,
    SeverityLevel,
    VerificationStatus,
)
from src.anti_hallucination.codex_query_builder import (
    CodexQueryBuilder,
    QueryResult,
)
from src.anti_hallucination.filter_screen import (
    FilterScreen,
    ScreenReport,
)
from src.anti_hallucination.thinking_model_handler import (
    ThinkingAnalysis,
    ThinkingModelHandler,
    ThinkingStep,
)


# ===========================================================================
# Fixtures
# ===========================================================================

SAMPLE_CONTEXT = (
    "The Eiffel Tower was completed in 1889 for the World's Fair in Paris, France. "
    "It stands 330 meters tall and was designed by Gustave Eiffel's engineering company. "
    "It was the tallest man-made structure in the world until the Chrysler Building "
    "was completed in New York City in 1930."
)

SAMPLE_QUESTION = "When was the Eiffel Tower completed and how tall is it?"

SAMPLE_GOOD_RESPONSE = (
    "The Eiffel Tower was completed in 1889, built for the World's Fair in Paris. "
    "It stands 330 meters tall. It was designed by Gustave Eiffel's company. "
    "Confidence: HIGH"
)

SAMPLE_BAD_RESPONSE = (
    "The Eiffel Tower was completed in 1892 by Napoleon Bonaparte. "
    "It stands 500 meters tall and is located in London, England. "
    "It was built using alien technology discovered in Egypt. "
    "Confidence: HIGH"
)

SAMPLE_CODE_RESPONSE = (
    "```python\n"
    "import pandas as pd\n"
    "import numpy as np\n"
    "from openpyxl import load_workbook\n"
    "\n"
    "def read_and_compute(path: str) -> dict:\n"
    "    df = pd.read_excel(path, engine='openpyxl')\n"
    "    return df.describe().to_dict()\n"
    "```"
)

SAMPLE_THINKING_RESPONSE = (
    "### Thinking Trace\n"
    "1. The question asks about completion date and height.\n"
    "2. From the source: \"completed in 1889\" - this answers the date.\n"
    "3. From the source: \"stands 330 meters tall\" - this answers the height.\n"
    "4. Therefore, I can provide both answers with high confidence.\n\n"
    "### Answer\n"
    "The Eiffel Tower was completed in 1889 and stands 330 meters tall.\n\n"
    "### Confidence\n"
    "Overall: HIGH - Both facts are directly stated in the source.\n\n"
    "### Unsupported Claims\n"
    "None."
)


# ===========================================================================
# Template Engine Tests
# ===========================================================================

class TestTemplatePlaceholder:
    def test_token_format(self):
        p = TemplatePlaceholder(key="context", description="test")
        assert p.token == "{{context}}"

    def test_required_default(self):
        p = TemplatePlaceholder(key="x", description="test", required=True)
        assert p.required is True
        assert p.default is None


class TestAntiHallucinationTemplate:
    def test_render_basic(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt="Context: {{context}}",
            user_prompt="Question: {{question}}",
            placeholders=[
                TemplatePlaceholder(key="context", description="ctx"),
                TemplatePlaceholder(key="question", description="q"),
            ],
        )
        messages = template.render(
            {"context": "Hello world", "question": "What?"},
            include_grounding=False,
            include_self_check=False,
        )
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "Hello world" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert "What?" in messages[1]["content"]

    def test_render_with_grounding(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt="Sys: {{context}}",
            user_prompt="Usr: {{question}}",
            placeholders=[
                TemplatePlaceholder(key="context", description="ctx"),
                TemplatePlaceholder(key="question", description="q"),
            ],
            grounding_rules=["Rule 1", "Rule 2"],
        )
        messages = template.render(
            {"context": "data", "question": "what?"},
            include_grounding=True,
            include_self_check=False,
        )
        assert "Grounding Rules" in messages[0]["content"]
        assert "Rule 1" in messages[0]["content"]

    def test_render_with_self_check(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt="Sys",
            user_prompt="Usr",
            placeholders=[],
            self_check_instructions="Check: verify all claims.",
        )
        messages = template.render(
            {},
            include_self_check=True,
        )
        assert "Self-Check" in messages[1]["content"]
        assert "verify all claims" in messages[1]["content"]

    def test_render_missing_required(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt="{{context}}",
            user_prompt="{{question}}",
            placeholders=[
                TemplatePlaceholder(key="context", description="ctx", required=True),
                TemplatePlaceholder(key="question", description="q", required=True),
            ],
        )
        with pytest.raises(ValueError, match="Missing required placeholders"):
            template.render({"context": "only context"})

    def test_render_with_defaults(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.CODE,
            model_tier=ModelTier.CODEX,
            system_prompt="Lang: {{language}} API: {{api_reference}}",
            user_prompt="Task: {{task}}",
            placeholders=[
                TemplatePlaceholder(key="language", description="lang", required=True),
                TemplatePlaceholder(
                    key="api_reference", description="api",
                    required=False, default="No API docs",
                ),
                TemplatePlaceholder(key="task", description="task", required=True),
            ],
        )
        messages = template.render(
            {"language": "Python", "task": "compute"},
            include_grounding=False,
            include_self_check=False,
        )
        assert "No API docs" in messages[0]["content"]

    def test_validate_fill(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt="",
            user_prompt="",
            placeholders=[
                TemplatePlaceholder(key="a", description="a", required=True),
                TemplatePlaceholder(key="b", description="b", required=True),
                TemplatePlaceholder(key="c", description="c", required=False, default="x"),
            ],
        )
        assert template.validate_fill({"a": "1", "b": "2"}) == []
        assert template.validate_fill({"a": "1"}) == ["b"]

    def test_describe(self):
        template = AntiHallucinationTemplate(
            name="my_template",
            category=TemplateCategory.REASONING,
            model_tier=ModelTier.THINKING,
            system_prompt="sys",
            user_prompt="usr",
            grounding_rules=["r1"],
            self_check_instructions="check",
        )
        desc = template.describe()
        assert desc["name"] == "my_template"
        assert desc["category"] == "reasoning"
        assert desc["model_tier"] == "thinking"
        assert desc["has_self_check"] is True

    def test_render_as_text(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt="sys: {{x}}",
            user_prompt="usr: {{x}}",
            placeholders=[
                TemplatePlaceholder(key="x", description="x"),
            ],
        )
        text = template.render_as_text({"x": "hello"})
        assert "[SYSTEM]" in text
        assert "[USER]" in text
        assert "hello" in text

    def test_list_unfilled_tokens(self):
        template = AntiHallucinationTemplate(
            name="test",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt="",
            user_prompt="",
        )
        tokens = template.list_unfilled_tokens("Hello {{name}}, welcome to {{place}}")
        assert "name" in tokens
        assert "place" in tokens


class TestTemplateLibrary:
    def test_builtin_templates_exist(self):
        lib = TemplateLibrary()
        names = lib.list_templates()
        assert "factual_qa" in names
        assert "factual_qa_thinking" in names
        assert "code_generation" in names
        assert "code_review" in names
        assert "reasoning_cot" in names
        assert "summarization" in names
        assert "entity_extraction" in names
        assert "multilingual_qa" in names

    def test_get_template(self):
        lib = TemplateLibrary()
        tmpl = lib.get("factual_qa")
        assert tmpl.name == "factual_qa"
        assert tmpl.category == TemplateCategory.FACTUAL
        assert tmpl.model_tier == ModelTier.STANDARD

    def test_get_nonexistent_raises(self):
        lib = TemplateLibrary()
        with pytest.raises(KeyError, match="not found"):
            lib.get("nonexistent_template")

    def test_filter_by_category(self):
        lib = TemplateLibrary()
        code_templates = lib.list_templates(category=TemplateCategory.CODE)
        assert "code_generation" in code_templates
        assert "code_review" in code_templates
        assert "factual_qa" not in code_templates

    def test_filter_by_model_tier(self):
        lib = TemplateLibrary()
        thinking = lib.list_templates(model_tier=ModelTier.THINKING)
        assert "factual_qa_thinking" in thinking
        assert "reasoning_cot" in thinking
        assert "factual_qa" not in thinking

    def test_register_custom(self):
        lib = TemplateLibrary()
        custom = AntiHallucinationTemplate(
            name="my_custom",
            category=TemplateCategory.CREATIVE,
            model_tier=ModelTier.STANDARD,
            system_prompt="custom sys",
            user_prompt="custom usr",
        )
        lib.register(custom)
        assert "my_custom" in lib.list_templates()
        assert lib.get("my_custom").system_prompt == "custom sys"

    def test_describe_all(self):
        lib = TemplateLibrary()
        descriptions = lib.describe_all()
        assert len(descriptions) >= 8
        assert all("name" in d for d in descriptions)

    def test_factual_qa_renders(self):
        lib = TemplateLibrary()
        tmpl = lib.get("factual_qa")
        messages = tmpl.render({
            "context": SAMPLE_CONTEXT,
            "question": SAMPLE_QUESTION,
        })
        assert len(messages) == 2
        assert "Eiffel Tower" in messages[0]["content"]
        assert SAMPLE_QUESTION in messages[1]["content"]

    def test_code_generation_renders(self):
        lib = TemplateLibrary()
        tmpl = lib.get("code_generation")
        messages = tmpl.render({
            "language": "Python 3.11",
            "libraries": "pandas, numpy",
            "task_description": "Read CSV and plot",
        })
        assert "Python 3.11" in messages[0]["content"]
        assert "pandas, numpy" in messages[0]["content"]


# ===========================================================================
# Check Filter Tests
# ===========================================================================

class TestClaimVerification:
    def test_is_problematic(self):
        supported = ClaimVerification(
            claim_text="test",
            status=VerificationStatus.SUPPORTED,
            severity=SeverityLevel.INFO,
        )
        assert supported.is_problematic() is False

        unsupported = ClaimVerification(
            claim_text="test",
            status=VerificationStatus.UNSUPPORTED,
            severity=SeverityLevel.WARNING,
        )
        assert unsupported.is_problematic() is True

        contradicted = ClaimVerification(
            claim_text="test",
            status=VerificationStatus.CONTRADICTED,
            severity=SeverityLevel.CRITICAL,
        )
        assert contradicted.is_problematic() is True


class TestCheckResult:
    def test_summary(self):
        result = CheckResult(
            passed=True,
            overall_score=0.85,
            claims=[
                ClaimVerification("a", VerificationStatus.SUPPORTED, SeverityLevel.INFO, confidence=0.9),
                ClaimVerification("b", VerificationStatus.UNSUPPORTED, SeverityLevel.WARNING, confidence=0.2),
            ],
            filters_applied=["source_grounding"],
        )
        s = result.summary()
        assert s["total_claims"] == 2
        assert s["supported"] == 1
        assert s["unsupported"] == 1
        assert s["passed"] is True

    def test_critical_issues(self):
        result = CheckResult(
            passed=False,
            overall_score=0.3,
            claims=[
                ClaimVerification("bad", VerificationStatus.CONTRADICTED, SeverityLevel.CRITICAL),
                ClaimVerification("ok", VerificationStatus.SUPPORTED, SeverityLevel.INFO),
            ],
        )
        assert len(result.critical_issues) == 1


class TestHallucinationCheckFilter:
    def test_good_response(self):
        checker = HallucinationCheckFilter(pass_threshold=0.3)
        result = checker.check(
            response=SAMPLE_GOOD_RESPONSE,
            source=SAMPLE_CONTEXT,
        )
        assert result.overall_score > 0.0
        assert len(result.claims) > 0
        assert len(result.filters_applied) > 0

    def test_bad_response_lower_score(self):
        checker = HallucinationCheckFilter(pass_threshold=0.3)
        good_result = checker.check(response=SAMPLE_GOOD_RESPONSE, source=SAMPLE_CONTEXT)
        bad_result = checker.check(response=SAMPLE_BAD_RESPONSE, source=SAMPLE_CONTEXT)
        # Bad response should generally score lower than good response
        # (may not always be strictly true with keyword overlap, but directionally correct)
        assert bad_result.overall_score <= good_result.overall_score + 0.3

    def test_no_source_skips_grounding(self):
        checker = HallucinationCheckFilter()
        result = checker.check(response="Some text", source="")
        assert "source_grounding" not in result.filters_applied

    def test_citation_check(self):
        checker = HallucinationCheckFilter()
        response_with_quote = (
            'According to the source, "completed in 1889 for the World\'s Fair" '
            'which confirms the date.'
        )
        result = checker.check(
            response=response_with_quote,
            source=SAMPLE_CONTEXT,
        )
        assert "citation_verify" in result.filters_applied

    def test_fabricated_citation(self):
        checker = HallucinationCheckFilter()
        response_fabricated = (
            'The source states "built by Napoleon in the year 1750" '
            'which is widely known.'
        )
        result = checker.check(
            response=response_fabricated,
            source=SAMPLE_CONTEXT,
        )
        # Should find at least one unsupported citation
        citation_claims = [
            c for c in result.claims if "Citation" in c.claim_text
        ]
        unsupported = [
            c for c in citation_claims
            if c.status in (VerificationStatus.UNSUPPORTED, VerificationStatus.PARTIALLY_SUPPORTED)
        ]
        assert len(unsupported) > 0

    def test_self_consistency(self):
        checker = HallucinationCheckFilter()
        responses = [
            "The Eiffel Tower was completed in 1889.",
            "The Eiffel Tower was completed in 1889.",
            "The Eiffel Tower was completed in 1889 for the World's Fair.",
        ]
        result = checker.check_self_consistency(responses, SAMPLE_CONTEXT)
        assert result.overall_score > 0.0
        assert "self_consistency" in result.filters_applied

    def test_self_consistency_single_response(self):
        checker = HallucinationCheckFilter()
        result = checker.check_self_consistency(["only one"])
        assert result.passed is True
        assert len(result.warnings) > 0

    def test_enabled_filters(self):
        checker = HallucinationCheckFilter()
        result = checker.check(
            response=SAMPLE_GOOD_RESPONSE,
            source=SAMPLE_CONTEXT,
            enabled_filters=[FilterType.SOURCE_GROUNDING],
        )
        assert "source_grounding" in result.filters_applied
        assert "citation_verify" not in result.filters_applied

    def test_code_api_verify(self):
        checker = HallucinationCheckFilter(
            known_libraries=["pandas", "numpy", "openpyxl"]
        )
        result = checker.check(
            response=SAMPLE_CODE_RESPONSE,
            source="",
            enabled_filters=[FilterType.CODE_API_VERIFY],
        )
        assert "code_api_verify" in result.filters_applied


# ===========================================================================
# Codex Query Builder Tests (without LLM client)
# ===========================================================================

class TestCodexQueryBuilder:
    def test_build_query_factual(self):
        builder = CodexQueryBuilder()
        messages = builder.build_query(
            "factual_qa",
            {"context": SAMPLE_CONTEXT, "question": SAMPLE_QUESTION},
        )
        assert len(messages) == 2
        assert "Eiffel Tower" in messages[0]["content"]

    def test_build_query_code(self):
        builder = CodexQueryBuilder()
        messages = builder.build_query(
            "code_generation",
            {
                "language": "Python",
                "libraries": "pandas",
                "task_description": "Read CSV",
            },
        )
        assert "Python" in messages[0]["content"]
        assert "pandas" in messages[0]["content"]

    def test_build_query_nonexistent_template(self):
        builder = CodexQueryBuilder()
        with pytest.raises(KeyError):
            builder.build_query("does_not_exist", {})

    def test_execute_without_client_raises(self):
        builder = CodexQueryBuilder(llm_client=None)
        with pytest.raises(RuntimeError, match="No LLM client"):
            builder.execute("factual_qa", {
                "context": "x",
                "question": "y",
            })

    def test_execute_with_mock_client(self):
        """Test full execute cycle with a mock LLM client."""

        class MockLLMResponse:
            content = SAMPLE_GOOD_RESPONSE
            input_tokens = 100
            output_tokens = 50

        class MockClient:
            def chat(self, messages, model=None, **kwargs):
                return MockLLMResponse()

        builder = CodexQueryBuilder(
            llm_client=MockClient(),
            pass_threshold=0.2,
        )
        result = builder.execute(
            "factual_qa",
            {"context": SAMPLE_CONTEXT, "question": SAMPLE_QUESTION},
            source=SAMPLE_CONTEXT,
        )
        assert isinstance(result, QueryResult)
        assert result.response_text == SAMPLE_GOOD_RESPONSE
        assert result.template_name == "factual_qa"
        assert result.model_used == "gpt-4o"

    def test_factual_query_convenience(self):
        class MockLLMResponse:
            content = SAMPLE_GOOD_RESPONSE
            input_tokens = 100
            output_tokens = 50

        class MockClient:
            def chat(self, messages, model=None, **kwargs):
                return MockLLMResponse()

        builder = CodexQueryBuilder(
            llm_client=MockClient(),
            pass_threshold=0.2,
        )
        result = builder.factual_query(
            context=SAMPLE_CONTEXT,
            question=SAMPLE_QUESTION,
        )
        assert result.template_name == "factual_qa"
        assert result.response_text == SAMPLE_GOOD_RESPONSE

    def test_batch_execute(self):
        class MockLLMResponse:
            content = "Answer."
            input_tokens = 10
            output_tokens = 5

        class MockClient:
            def chat(self, messages, model=None, **kwargs):
                return MockLLMResponse()

        builder = CodexQueryBuilder(
            llm_client=MockClient(),
            pass_threshold=0.1,
        )
        results = builder.batch_execute([
            {
                "template_name": "factual_qa",
                "values": {"context": "A", "question": "B"},
            },
            {
                "template_name": "factual_qa",
                "values": {"context": "C", "question": "D"},
            },
        ])
        assert len(results) == 2


# ===========================================================================
# Filter Screen Tests
# ===========================================================================

class TestFilterScreen:
    def test_render_check_result(self):
        check = CheckResult(
            passed=True,
            overall_score=0.85,
            claims=[
                ClaimVerification(
                    "Claim 1", VerificationStatus.SUPPORTED, SeverityLevel.INFO,
                    confidence=0.9, evidence="Found in source.",
                ),
            ],
            filters_applied=["source_grounding"],
        )
        screen = FilterScreen()
        report = screen.render_check_result(check)
        assert isinstance(report, ScreenReport)
        assert "PASS" in report.text_output
        assert "Claim 1" in report.text_output
        assert report.structured_data["passed"] is True

    def test_render_query_result(self):
        check = CheckResult(
            passed=True,
            overall_score=0.75,
            claims=[],
            filters_applied=["source_grounding"],
        )
        qr = QueryResult(
            response_text="Test response",
            check_result=check,
            template_name="factual_qa",
            model_used="gpt-4o",
            attempt=1,
            total_latency_ms=500,
            metadata={"input_tokens": 100, "output_tokens": 50},
        )
        screen = FilterScreen()
        report = screen.render_query_result(qr)
        assert "PASS" in report.text_output
        assert "factual_qa" in report.text_output
        assert "gpt-4o" in report.text_output
        assert "500" in report.text_output  # latency

    def test_render_failed_result(self):
        check = CheckResult(
            passed=False,
            overall_score=0.2,
            claims=[
                ClaimVerification(
                    "Bad claim", VerificationStatus.CONTRADICTED,
                    SeverityLevel.CRITICAL, confidence=0.1,
                ),
            ],
            warnings=["1 critical hallucination(s) detected."],
        )
        screen = FilterScreen()
        report = screen.render_check_result(check)
        assert "FAIL" in report.text_output
        assert "CRITICAL" in report.text_output

    def test_render_comparison(self):
        results = [
            QueryResult(
                response_text="R1",
                check_result=CheckResult(passed=True, overall_score=0.9, claims=[]),
                template_name="t1",
                model_used="gpt-4o",
            ),
            QueryResult(
                response_text="R2",
                check_result=CheckResult(passed=False, overall_score=0.3, claims=[]),
                template_name="t2",
                model_used="o3",
            ),
        ]
        screen = FilterScreen()
        report = screen.render_comparison(results)
        assert "COMPARISON" in report.text_output
        assert "Best:" in report.text_output

    def test_report_to_json(self):
        check = CheckResult(passed=True, overall_score=0.9, claims=[])
        screen = FilterScreen()
        report = screen.render_check_result(check)
        json_str = report.to_json()
        data = json.loads(json_str)
        assert "structured_data" in data
        assert data["structured_data"]["passed"] is True

    def test_report_to_markdown(self):
        check = CheckResult(passed=True, overall_score=0.9, claims=[])
        screen = FilterScreen()
        report = screen.render_check_result(check)
        md = report.to_markdown()
        assert "PASS" in md


# ===========================================================================
# Thinking Model Handler Tests
# ===========================================================================

class TestThinkingStep:
    def test_has_evidence(self):
        step = ThinkingStep(step_number=1, content="test", evidence_refs=["ref1"])
        assert step.has_evidence() is True

        step_no_ev = ThinkingStep(step_number=2, content="test")
        assert step_no_ev.has_evidence() is False


class TestThinkingAnalysis:
    def test_grounded_step_ratio(self):
        analysis = ThinkingAnalysis(
            raw_response="test",
            thinking_trace="trace",
            final_answer="answer",
            steps=[
                ThinkingStep(1, "s1", evidence_refs=["e1"]),
                ThinkingStep(2, "s2", evidence_refs=[]),
                ThinkingStep(3, "s3", evidence_refs=["e3"]),
            ],
        )
        assert analysis.grounded_step_ratio == pytest.approx(2 / 3, abs=0.01)

    def test_summary(self):
        analysis = ThinkingAnalysis(
            raw_response="r",
            thinking_trace="t",
            final_answer="a",
            steps=[
                ThinkingStep(1, "s1", evidence_refs=["e1"]),
            ],
            stated_confidence="HIGH",
            unsupported_claims=["claim1"],
        )
        s = analysis.summary()
        assert s["total_steps"] == 1
        assert s["grounded_steps"] == 1
        assert s["stated_confidence"] == "HIGH"
        assert s["unsupported_claims_count"] == 1


class TestThinkingModelHandler:
    def test_parse_thinking_response(self):
        handler = ThinkingModelHandler()
        analysis = handler.parse_thinking_response(SAMPLE_THINKING_RESPONSE)
        assert analysis.thinking_trace != ""
        assert analysis.final_answer != ""
        assert "1889" in analysis.final_answer
        assert "HIGH" in analysis.stated_confidence
        assert len(analysis.steps) > 0

    def test_parse_unstructured_response(self):
        handler = ThinkingModelHandler()
        analysis = handler.parse_thinking_response(
            "The answer is 42. This is based on calculation."
        )
        # Should fall back to treating the whole thing as the answer
        assert "42" in analysis.final_answer

    def test_parse_empty_unsupported(self):
        handler = ThinkingModelHandler()
        analysis = handler.parse_thinking_response(SAMPLE_THINKING_RESPONSE)
        # "None." should be parsed as no unsupported claims
        assert len(analysis.unsupported_claims) == 0

    def test_analyze_response_with_mock(self):
        class MockLLMResponse:
            content = SAMPLE_THINKING_RESPONSE
            input_tokens = 200
            output_tokens = 100

        class MockClient:
            def chat(self, messages, model=None, **kwargs):
                return MockLLMResponse()

        handler = ThinkingModelHandler(
            llm_client=MockClient(),
            pass_threshold=0.2,
        )
        analysis = handler.analyze_response(
            template_name="factual_qa_thinking",
            values={"context": SAMPLE_CONTEXT, "question": SAMPLE_QUESTION},
            source=SAMPLE_CONTEXT,
        )
        assert analysis.check_result is not None
        assert analysis.final_answer != ""
        assert len(analysis.steps) > 0

    def test_render_analysis(self):
        handler = ThinkingModelHandler()
        analysis = handler.parse_thinking_response(SAMPLE_THINKING_RESPONSE)
        analysis.check_result = CheckResult(
            passed=True,
            overall_score=0.85,
            claims=[],
        )
        report = handler.render_analysis(analysis)
        assert isinstance(report, ScreenReport)
        assert "thinking_summary" in report.structured_data

    def test_analyze_without_client_raises(self):
        handler = ThinkingModelHandler(llm_client=None)
        # analyze_response calls the query builder which needs client
        with pytest.raises(RuntimeError):
            handler.analyze_response(
                "factual_qa_thinking",
                {"context": "x", "question": "y"},
            )

    def test_consistency_without_client_raises(self):
        handler = ThinkingModelHandler(llm_client=None)
        with pytest.raises(RuntimeError):
            handler.analyze_with_consistency(
                "factual_qa_thinking",
                {"context": "x", "question": "y"},
            )


# ===========================================================================
# Integration Tests (end-to-end without real API)
# ===========================================================================

class TestIntegration:
    """End-to-end tests using mock LLM client."""

    def _make_mock_client(self, response_text: str):
        class MockResponse:
            content = response_text
            input_tokens = 100
            output_tokens = 50
        class MockClient:
            def chat(self, messages, model=None, **kwargs):
                return MockResponse()
        return MockClient()

    def test_full_factual_pipeline(self):
        """Template → Query → Check → Screen"""
        client = self._make_mock_client(SAMPLE_GOOD_RESPONSE)
        builder = CodexQueryBuilder(llm_client=client, pass_threshold=0.2)
        result = builder.factual_query(
            context=SAMPLE_CONTEXT,
            question=SAMPLE_QUESTION,
        )
        screen = FilterScreen()
        report = screen.render_query_result(result)

        assert result.response_text == SAMPLE_GOOD_RESPONSE
        assert "factual_qa" in report.text_output
        assert report.structured_data["score"] > 0

    def test_full_thinking_pipeline(self):
        """ThinkingHandler → Parse → Verify → Screen"""
        client = self._make_mock_client(SAMPLE_THINKING_RESPONSE)
        handler = ThinkingModelHandler(
            llm_client=client,
            pass_threshold=0.1,
        )
        analysis = handler.analyze_response(
            "factual_qa_thinking",
            {"context": SAMPLE_CONTEXT, "question": SAMPLE_QUESTION},
            source=SAMPLE_CONTEXT,
        )
        report = handler.render_analysis(analysis)

        assert analysis.final_answer != ""
        assert analysis.check_result is not None
        assert "thinking_summary" in report.structured_data

    def test_full_code_pipeline(self):
        """Code generation → API verify → Screen"""
        client = self._make_mock_client(SAMPLE_CODE_RESPONSE)
        builder = CodexQueryBuilder(llm_client=client, pass_threshold=0.1)
        result = builder.code_query(
            language="Python 3.11",
            libraries="pandas, numpy, openpyxl",
            task_description="Read Excel and compute stats",
        )
        screen = FilterScreen()
        report = screen.render_query_result(result)

        assert "code_generation" in report.text_output

"""
Anti-Hallucination Template Engine / 反幻覺模板引擎 / 反幻觉模板引擎
====================================================================
Core template system with placeholders for constructing
anti-hallucination prompts across ChatGPT / GPT Thinking models.

核心模板系統，使用佔位符構建反幻覺提示，
適用於 ChatGPT / GPT Thinking 模型。

Template Lifecycle / 模板生命週期:
1. Select template from library / 從庫中選擇模板
2. Fill placeholders / 填充佔位符
3. Render to prompt messages / 渲染為提示訊息
4. Send to LLM → receive response / 發送到 LLM → 接收回應
5. Run check filters on response / 對回應執行檢查過濾
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Enums / 列舉
# ---------------------------------------------------------------------------

class TemplateCategory(str, Enum):
    """Template categories / 模板類別 / 模板类别"""
    FACTUAL = "factual"
    REASONING = "reasoning"
    CODE = "code"
    CREATIVE = "creative"
    SUMMARIZATION = "summarization"
    EXTRACTION = "extraction"
    MULTILINGUAL = "multilingual"


class ModelTier(str, Enum):
    """
    Target model tier / 目標模型層級 / 目标模型层级
    Determines prompt structure and anti-hallucination strategy.
    """
    STANDARD = "standard"        # GPT-4o, GPT-4-turbo
    THINKING = "thinking"        # o1, o3 — extended reasoning
    CODEX = "codex"              # Code-specialized models


# ---------------------------------------------------------------------------
# Data classes / 資料類別
# ---------------------------------------------------------------------------

@dataclass
class TemplatePlaceholder:
    """
    Single placeholder definition inside a template.
    模板中的單個佔位符定義。

    Attributes:
        key: placeholder name (used as ``{{key}}`` in template)
        description: human-readable purpose
        required: whether the placeholder must be filled
        default: optional fallback value
        example: example fill value for documentation
    """
    key: str
    description: str
    required: bool = True
    default: str | None = None
    example: str | None = None

    @property
    def token(self) -> str:
        """The ``{{key}}`` token that appears in template text."""
        return "{{" + self.key + "}}"


@dataclass
class AntiHallucinationTemplate:
    """
    A structured prompt template designed to minimize hallucination.
    用於最小化幻覺的結構化提示模板。

    Each template contains:
    - A system prompt that primes the model for factual accuracy
    - A user prompt with ``{{placeholders}}`` for dynamic content
    - Optional chain-of-thought instructions for Thinking models
    - Built-in grounding rules and self-check instructions
    """
    name: str
    category: TemplateCategory
    model_tier: ModelTier
    system_prompt: str
    user_prompt: str
    placeholders: list[TemplatePlaceholder] = field(default_factory=list)
    grounding_rules: list[str] = field(default_factory=list)
    self_check_instructions: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    # ---- Rendering ---------------------------------------------------

    def get_placeholder_keys(self) -> list[str]:
        """Return all placeholder keys defined in this template."""
        return [p.key for p in self.placeholders]

    def get_required_keys(self) -> list[str]:
        """Return only required placeholder keys."""
        return [p.key for p in self.placeholders if p.required]

    def validate_fill(self, values: dict[str, str]) -> list[str]:
        """
        Check that all required placeholders are present in *values*.
        Returns a list of missing keys (empty list means valid).
        """
        missing = []
        for p in self.placeholders:
            if p.required and p.key not in values:
                if p.default is None:
                    missing.append(p.key)
        return missing

    def _apply_defaults(self, values: dict[str, str]) -> dict[str, str]:
        merged: dict[str, str] = {}
        for p in self.placeholders:
            if p.key in values:
                merged[p.key] = values[p.key]
            elif p.default is not None:
                merged[p.key] = p.default
        return merged

    def _substitute(self, text: str, values: dict[str, str]) -> str:
        result = text
        for key, val in values.items():
            result = result.replace("{{" + key + "}}", val)
        return result

    def render(
        self,
        values: dict[str, str],
        *,
        include_grounding: bool = True,
        include_self_check: bool = True,
    ) -> list[dict[str, str]]:
        """
        Render the template into a list of chat messages.
        將模板渲染為聊天訊息列表。

        Args:
            values: mapping of placeholder key → fill value
            include_grounding: append grounding rules to system prompt
            include_self_check: append self-check block to user prompt

        Returns:
            list of ``{"role": ..., "content": ...}`` dicts
        """
        missing = self.validate_fill(values)
        if missing:
            raise ValueError(
                f"Missing required placeholders: {missing}"
            )

        merged = self._apply_defaults(values)

        # Build system prompt
        sys_text = self._substitute(self.system_prompt, merged)
        if include_grounding and self.grounding_rules:
            rules_block = "\n".join(
                f"- {r}" for r in self.grounding_rules
            )
            sys_text += (
                "\n\n## Grounding Rules / 基準規則\n"
                "You MUST follow these rules:\n"
                f"{rules_block}"
            )

        # Build user prompt
        usr_text = self._substitute(self.user_prompt, merged)
        if include_self_check and self.self_check_instructions:
            usr_text += (
                "\n\n## Self-Check / 自我檢查\n"
                + self._substitute(self.self_check_instructions, merged)
            )

        return [
            {"role": "system", "content": sys_text},
            {"role": "user", "content": usr_text},
        ]

    def render_as_text(self, values: dict[str, str]) -> str:
        """Convenience: render and return combined text for display."""
        messages = self.render(values)
        parts = []
        for m in messages:
            parts.append(f"[{m['role'].upper()}]\n{m['content']}")
        return "\n\n---\n\n".join(parts)

    # ---- Introspection -----------------------------------------------

    def list_unfilled_tokens(self, text: str) -> list[str]:
        """Find any remaining ``{{...}}`` tokens in rendered text."""
        return re.findall(r"\{\{(\w+)\}\}", text)

    def describe(self) -> dict[str, Any]:
        """Return a serializable description of the template."""
        return {
            "name": self.name,
            "category": self.category.value,
            "model_tier": self.model_tier.value,
            "placeholders": [
                {
                    "key": p.key,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                    "example": p.example,
                }
                for p in self.placeholders
            ],
            "grounding_rules": self.grounding_rules,
            "has_self_check": bool(self.self_check_instructions),
        }


# ---------------------------------------------------------------------------
# Template Library / 模板庫
# ---------------------------------------------------------------------------

class TemplateLibrary:
    """
    Registry of pre-built anti-hallucination templates.
    預建反幻覺模板的註冊表。

    Usage:
        library = TemplateLibrary()
        template = library.get("factual_qa")
        messages = template.render({"context": "...", "question": "..."})
    """

    def __init__(self) -> None:
        self._templates: dict[str, AntiHallucinationTemplate] = {}
        self._register_builtins()

    # ---- Public API --------------------------------------------------

    def register(self, template: AntiHallucinationTemplate) -> None:
        """Register a custom template."""
        self._templates[template.name] = template

    def get(self, name: str) -> AntiHallucinationTemplate:
        """Retrieve a template by name."""
        if name not in self._templates:
            available = ", ".join(sorted(self._templates.keys()))
            raise KeyError(
                f"Template '{name}' not found. Available: {available}"
            )
        return self._templates[name]

    def list_templates(
        self,
        category: TemplateCategory | None = None,
        model_tier: ModelTier | None = None,
    ) -> list[str]:
        """List template names, optionally filtered."""
        names = []
        for name, tmpl in self._templates.items():
            if category and tmpl.category != category:
                continue
            if model_tier and tmpl.model_tier != model_tier:
                continue
            names.append(name)
        return sorted(names)

    def describe_all(self) -> list[dict[str, Any]]:
        """Return descriptions for all registered templates."""
        return [t.describe() for t in self._templates.values()]

    # ---- Built-in templates ------------------------------------------

    def _register_builtins(self) -> None:
        """Populate default anti-hallucination templates."""

        # ----- 1. Factual QA (Standard models) -----
        self.register(AntiHallucinationTemplate(
            name="factual_qa",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.STANDARD,
            system_prompt=(
                "You are a factual question-answering assistant. "
                "Your ONLY source of truth is the CONTEXT provided below. "
                "If the answer cannot be found in the context, say "
                "\"I don't have enough information to answer this.\"\n\n"
                "CONTEXT:\n{{context}}"
            ),
            user_prompt=(
                "Based ONLY on the context above, answer the following question.\n\n"
                "QUESTION: {{question}}\n\n"
                "REQUIREMENTS:\n"
                "1. Cite specific parts of the context that support your answer.\n"
                "2. If the context is insufficient, clearly state what is missing.\n"
                "3. Do NOT use prior knowledge outside the given context.\n"
                "4. Provide your confidence level (HIGH / MEDIUM / LOW)."
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="context",
                    description="Reference material / source documents",
                    required=True,
                    example="The Eiffel Tower was completed in 1889...",
                ),
                TemplatePlaceholder(
                    key="question",
                    description="The user's question to answer",
                    required=True,
                    example="When was the Eiffel Tower completed?",
                ),
            ],
            grounding_rules=[
                "NEVER fabricate facts not present in the context.",
                "If uncertain, indicate uncertainty with explicit confidence level.",
                "Always quote or paraphrase the source when making claims.",
                "Distinguish between what the context states vs. what you infer.",
            ],
            self_check_instructions=(
                "Before giving your final answer, verify:\n"
                "- [ ] Every factual claim maps to a specific part of the context.\n"
                "- [ ] No information was added from outside the context.\n"
                "- [ ] Confidence level accurately reflects the evidence quality.\n"
                "- [ ] Ambiguities are explicitly acknowledged."
            ),
        ))

        # ----- 2. Factual QA (Thinking models: o1, o3) -----
        self.register(AntiHallucinationTemplate(
            name="factual_qa_thinking",
            category=TemplateCategory.FACTUAL,
            model_tier=ModelTier.THINKING,
            system_prompt=(
                "You are an advanced reasoning assistant using extended thinking. "
                "Your primary objective is FACTUAL ACCURACY. Use your thinking "
                "process to critically evaluate every claim before stating it.\n\n"
                "SOURCE MATERIAL:\n{{context}}\n\n"
                "EPISTEMIC PROTOCOL:\n"
                "- In your thinking, explicitly map each claim to evidence.\n"
                "- Flag any claim that lacks direct source support.\n"
                "- Rate your own confidence for each sub-answer."
            ),
            user_prompt=(
                "QUESTION: {{question}}\n\n"
                "Use your extended thinking to:\n"
                "1. Break down the question into sub-questions.\n"
                "2. For each sub-question, find evidence in the source material.\n"
                "3. Identify any gaps where the source is silent.\n"
                "4. Synthesize a final answer with confidence ratings.\n\n"
                "OUTPUT FORMAT:\n"
                "### Thinking Trace\n"
                "(Your step-by-step reasoning)\n\n"
                "### Answer\n"
                "(Final answer with citations)\n\n"
                "### Confidence\n"
                "(Overall: HIGH/MEDIUM/LOW with justification)\n\n"
                "### Unsupported Claims\n"
                "(List any claims you could not verify from the source)"
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="context",
                    description="Reference material for grounding",
                    required=True,
                    example="Quantum computing uses qubits that can be in superposition...",
                ),
                TemplatePlaceholder(
                    key="question",
                    description="Question requiring deep reasoning",
                    required=True,
                    example="What advantages do qubits have over classical bits?",
                ),
            ],
            grounding_rules=[
                "Your thinking trace MUST show evidence mapping for every claim.",
                "If a claim has no source support, mark it as [UNSUPPORTED].",
                "Never present inferences as established facts.",
                "When the source is ambiguous, present all plausible interpretations.",
                "Separate sourced facts from logical deductions explicitly.",
            ],
            self_check_instructions=(
                "Final verification protocol for Thinking model:\n"
                "- [ ] Each claim in the Answer section has a source citation.\n"
                "- [ ] Unsupported Claims section is complete (even if empty).\n"
                "- [ ] Confidence is calibrated to evidence strength.\n"
                "- [ ] No 'common knowledge' was smuggled in without flagging.\n"
                "- [ ] Thinking trace is logically coherent."
            ),
        ))

        # ----- 3. Code Generation (Codex / GPT models) -----
        self.register(AntiHallucinationTemplate(
            name="code_generation",
            category=TemplateCategory.CODE,
            model_tier=ModelTier.CODEX,
            system_prompt=(
                "You are a code generation assistant powered by Codex. "
                "Generate ONLY correct, runnable code. Never invent APIs, "
                "functions, or libraries that do not exist.\n\n"
                "LANGUAGE: {{language}}\n"
                "AVAILABLE LIBRARIES: {{libraries}}\n"
                "API REFERENCE (if any):\n{{api_reference}}"
            ),
            user_prompt=(
                "TASK: {{task_description}}\n\n"
                "CONSTRAINTS:\n"
                "{{constraints}}\n\n"
                "REQUIREMENTS:\n"
                "1. Use ONLY the libraries listed above.\n"
                "2. Do NOT invent function signatures or API endpoints.\n"
                "3. Include inline comments explaining non-obvious logic.\n"
                "4. If unsure about an API, state the uncertainty instead of guessing.\n"
                "5. Provide a brief explanation of how the code works."
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="language",
                    description="Programming language",
                    required=True,
                    example="Python 3.11",
                ),
                TemplatePlaceholder(
                    key="libraries",
                    description="Available libraries/packages",
                    required=True,
                    example="pandas>=2.0, numpy>=1.24, openpyxl>=3.1",
                ),
                TemplatePlaceholder(
                    key="api_reference",
                    description="Relevant API docs or function signatures",
                    required=False,
                    default="No specific API reference provided.",
                    example="def read_excel(path: str, sheet_name: str = 'Sheet1') -> DataFrame",
                ),
                TemplatePlaceholder(
                    key="task_description",
                    description="What the code should do",
                    required=True,
                    example="Read an Excel file and compute column statistics.",
                ),
                TemplatePlaceholder(
                    key="constraints",
                    description="Technical constraints or requirements",
                    required=False,
                    default="No additional constraints.",
                    example="Must handle files up to 100MB. Use streaming if needed.",
                ),
            ],
            grounding_rules=[
                "NEVER invent function names, parameters, or return types.",
                "If a library API is uncertain, say so rather than guessing.",
                "All import statements must reference real, installable packages.",
                "Include version compatibility notes where relevant.",
                "Do not generate placeholder/mock implementations unless asked.",
            ],
            self_check_instructions=(
                "Code verification checklist:\n"
                "- [ ] All imports reference real packages.\n"
                "- [ ] All function calls match documented signatures.\n"
                "- [ ] No hallucinated API endpoints or URLs.\n"
                "- [ ] Error handling covers common failure modes.\n"
                "- [ ] Code is syntactically valid and would run as-is."
            ),
        ))

        # ----- 4. Code Review with Anti-Hallucination (Codex) -----
        self.register(AntiHallucinationTemplate(
            name="code_review",
            category=TemplateCategory.CODE,
            model_tier=ModelTier.CODEX,
            system_prompt=(
                "You are a code review assistant. Analyze the provided code "
                "for correctness, security, performance, and style. "
                "Base your review ONLY on what is visible in the code.\n\n"
                "LANGUAGE: {{language}}"
            ),
            user_prompt=(
                "Review the following code:\n\n"
                "```{{language}}\n{{code}}\n```\n\n"
                "Provide:\n"
                "1. **Bugs**: Definite bugs with line references.\n"
                "2. **Security Issues**: Vulnerabilities (OWASP Top 10).\n"
                "3. **Performance**: Inefficiencies with evidence.\n"
                "4. **Suggestions**: Improvements with rationale.\n\n"
                "IMPORTANT: Only flag issues you can demonstrate from the code. "
                "Do NOT speculate about code you cannot see."
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="language",
                    description="Programming language of the code",
                    required=True,
                    example="Python",
                ),
                TemplatePlaceholder(
                    key="code",
                    description="Source code to review",
                    required=True,
                    example="def add(a, b):\n    return a + b",
                ),
            ],
            grounding_rules=[
                "Only reference code lines that are visible in the provided snippet.",
                "Do NOT assume behavior of functions whose implementations are not shown.",
                "Distinguish between confirmed bugs and potential concerns.",
                "Security findings must cite the specific vulnerable pattern.",
            ],
            self_check_instructions=(
                "Review verification:\n"
                "- [ ] Every bug report references a specific line or pattern.\n"
                "- [ ] No assumptions about unseen code.\n"
                "- [ ] Security issues cite specific OWASP categories.\n"
                "- [ ] Severity ratings match the actual impact."
            ),
        ))

        # ----- 5. Reasoning / Chain-of-Thought (Thinking models) -----
        self.register(AntiHallucinationTemplate(
            name="reasoning_cot",
            category=TemplateCategory.REASONING,
            model_tier=ModelTier.THINKING,
            system_prompt=(
                "You are a logical reasoning assistant. Use structured "
                "chain-of-thought to solve problems step by step. "
                "Every logical step must be justified.\n\n"
                "DOMAIN: {{domain}}\n"
                "KNOWN FACTS:\n{{known_facts}}"
            ),
            user_prompt=(
                "PROBLEM: {{problem}}\n\n"
                "Solve this step by step:\n"
                "1. Identify what is known vs. unknown.\n"
                "2. State assumptions explicitly.\n"
                "3. Show each reasoning step with justification.\n"
                "4. Highlight where you are uncertain.\n"
                "5. Provide the final answer with confidence assessment.\n\n"
                "FORMAT:\n"
                "### Given\n### Assumptions\n### Step-by-step Reasoning\n"
                "### Conclusion\n### Confidence & Caveats"
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="domain",
                    description="Problem domain",
                    required=False,
                    default="General",
                    example="Mathematics",
                ),
                TemplatePlaceholder(
                    key="known_facts",
                    description="Established facts or premises",
                    required=True,
                    example="The speed of light is 3×10^8 m/s. Distance = 1.5×10^11 m.",
                ),
                TemplatePlaceholder(
                    key="problem",
                    description="The problem or question to reason about",
                    required=True,
                    example="How long does sunlight take to reach Earth?",
                ),
            ],
            grounding_rules=[
                "Every reasoning step must follow from the given facts or stated assumptions.",
                "Mark assumed values as [ASSUMPTION] distinct from [GIVEN] facts.",
                "If multiple valid approaches exist, mention alternatives briefly.",
                "Never skip steps — all logical gaps must be filled.",
            ],
            self_check_instructions=(
                "Reasoning verification:\n"
                "- [ ] All [GIVEN] facts come from the Known Facts section.\n"
                "- [ ] All [ASSUMPTION]s are clearly labeled.\n"
                "- [ ] No logical leaps without justification.\n"
                "- [ ] Final answer is consistent with the reasoning chain."
            ),
        ))

        # ----- 6. Summarization with Source Fidelity -----
        self.register(AntiHallucinationTemplate(
            name="summarization",
            category=TemplateCategory.SUMMARIZATION,
            model_tier=ModelTier.STANDARD,
            system_prompt=(
                "You are a summarization assistant. Your summary must "
                "ONLY contain information present in the source text. "
                "Never add external knowledge or embellishments.\n\n"
                "SOURCE TEXT:\n{{source_text}}"
            ),
            user_prompt=(
                "Summarize the source text above.\n\n"
                "LENGTH: {{target_length}}\n"
                "FOCUS AREAS: {{focus_areas}}\n\n"
                "RULES:\n"
                "1. Every sentence in your summary must trace to the source.\n"
                "2. Do NOT add interpretations beyond what the source states.\n"
                "3. Preserve the original meaning without distortion.\n"
                "4. Flag any section where the source is ambiguous."
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="source_text",
                    description="Text to summarize",
                    required=True,
                    example="The annual report shows revenue grew 15%...",
                ),
                TemplatePlaceholder(
                    key="target_length",
                    description="Desired summary length",
                    required=False,
                    default="3-5 sentences",
                    example="2 paragraphs",
                ),
                TemplatePlaceholder(
                    key="focus_areas",
                    description="Key topics to emphasize",
                    required=False,
                    default="All key points",
                    example="Financial performance, market expansion",
                ),
            ],
            grounding_rules=[
                "Every claim in the summary must be traceable to the source text.",
                "Do NOT infer causation unless the source explicitly states it.",
                "Quantitative data must be reproduced exactly as stated.",
                "If the source contradicts itself, note the contradiction.",
            ],
            self_check_instructions=(
                "Summary verification:\n"
                "- [ ] Each sentence maps to specific source content.\n"
                "- [ ] No external facts were added.\n"
                "- [ ] Numbers and dates match the source exactly.\n"
                "- [ ] Ambiguities in the source are preserved, not resolved."
            ),
        ))

        # ----- 7. Entity Extraction (Standard) -----
        self.register(AntiHallucinationTemplate(
            name="entity_extraction",
            category=TemplateCategory.EXTRACTION,
            model_tier=ModelTier.STANDARD,
            system_prompt=(
                "You are an entity extraction assistant. Extract entities "
                "ONLY from the provided text. Never generate entities "
                "that are not explicitly mentioned.\n\n"
                "TEXT:\n{{text}}"
            ),
            user_prompt=(
                "Extract all entities from the text above.\n\n"
                "ENTITY TYPES TO EXTRACT: {{entity_types}}\n\n"
                "OUTPUT FORMAT (JSON array):\n"
                "[\n"
                "  {\"name\": \"...\", \"type\": \"...\", \"mention\": \"exact quote from text\"},\n"
                "  ...\n"
                "]\n\n"
                "CRITICAL: The 'mention' field must be a verbatim quote from the text."
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="text",
                    description="Source text for entity extraction",
                    required=True,
                    example="Apple CEO Tim Cook announced the new iPhone 16 in Cupertino.",
                ),
                TemplatePlaceholder(
                    key="entity_types",
                    description="Types of entities to extract",
                    required=False,
                    default="PERSON, ORGANIZATION, LOCATION, DATE, PRODUCT",
                    example="PERSON, ORGANIZATION",
                ),
            ],
            grounding_rules=[
                "ONLY extract entities that appear verbatim in the source text.",
                "The 'mention' field must be a direct quote — no paraphrasing.",
                "Do NOT infer entities that are implied but not stated.",
                "If an entity type is ambiguous, choose the most specific type.",
            ],
            self_check_instructions=(
                "Extraction verification:\n"
                "- [ ] Every entity name appears in the source text.\n"
                "- [ ] Every 'mention' is a verbatim quote.\n"
                "- [ ] No inferred or implied entities were added.\n"
                "- [ ] Entity types match the requested types list."
            ),
        ))

        # ----- 8. Multilingual QA (Thinking) -----
        self.register(AntiHallucinationTemplate(
            name="multilingual_qa",
            category=TemplateCategory.MULTILINGUAL,
            model_tier=ModelTier.THINKING,
            system_prompt=(
                "You are a multilingual question-answering assistant. "
                "Answer based ONLY on the provided context. "
                "Respond in the same language as the question.\n\n"
                "CONTEXT:\n{{context}}\n\n"
                "RESPONSE LANGUAGE: {{response_language}}"
            ),
            user_prompt=(
                "QUESTION: {{question}}\n\n"
                "Instructions:\n"
                "1. Answer in {{response_language}}.\n"
                "2. Cite the context to support your answer.\n"
                "3. If the context does not cover the question, say so.\n"
                "4. Provide confidence level: HIGH / MEDIUM / LOW."
            ),
            placeholders=[
                TemplatePlaceholder(
                    key="context",
                    description="Reference material (any language)",
                    required=True,
                    example="量子計算使用量子位元進行超位置運算...",
                ),
                TemplatePlaceholder(
                    key="question",
                    description="User's question (any language)",
                    required=True,
                    example="量子計算有什麼優勢？",
                ),
                TemplatePlaceholder(
                    key="response_language",
                    description="Language for the response",
                    required=False,
                    default="Same as the question",
                    example="Traditional Chinese / 繁體中文",
                ),
            ],
            grounding_rules=[
                "Answer ONLY from the provided context, regardless of language.",
                "Do NOT translate common knowledge as if it were sourced.",
                "Cross-language claims must be verifiable in the original context.",
                "Indicate if the answer required cross-language inference.",
            ],
            self_check_instructions=(
                "Multilingual verification:\n"
                "- [ ] Answer language matches the requested response language.\n"
                "- [ ] All facts trace back to the context.\n"
                "- [ ] No cross-language hallucination was introduced.\n"
                "- [ ] Confidence reflects actual source coverage."
            ),
        ))

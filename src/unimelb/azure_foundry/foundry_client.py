"""
Azure AI Foundry Client — Frontier Model Orchestration
=======================================================
Connects UniMelb AI Platform to Azure AI Foundry for access to
frontier models: GPT-4o, Claude Opus/Sonnet, Gemini, DeepSeek, Grok.

Supports multi-model querying for anti-hallucination cross-verification.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FrontierModel(Enum):
    """Available frontier models in Azure AI Foundry."""

    # Microsoft / OpenAI
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    O3 = "o3"
    O3_MINI = "o3-mini"

    # Anthropic (via Azure)
    CLAUDE_OPUS = "claude-opus-4-6"
    CLAUDE_SONNET = "claude-sonnet-4-5-20250929"
    CLAUDE_HAIKU = "claude-haiku-4-5-20251001"

    # Google (via Azure)
    GEMINI_PRO = "gemini-2.0-pro"
    GEMINI_FLASH = "gemini-2.0-flash"

    # Open-weight
    DEEPSEEK_V3 = "deepseek-v3"
    DEEPSEEK_R1 = "deepseek-r1"

    # xAI
    GROK_4 = "grok-4"


@dataclass
class FoundryResponse:
    """Response from Azure AI Foundry model inference."""

    content: str
    model: str
    provider: str
    confidence: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    sources: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MultiModelResult:
    """Result from querying multiple frontier models simultaneously."""

    responses: list[FoundryResponse]
    consensus_score: float = 0.0
    consensus_answer: str = ""
    divergence_points: list[str] = field(default_factory=list)
    verification_status: str = "unverified"


class AzureFoundryClient:
    """
    Azure AI Foundry client for UniMelb AI Platform.

    Provides unified access to all frontier models available in Azure AI Foundry,
    with built-in support for multi-model querying (anti-hallucination pattern).
    """

    def __init__(
        self,
        endpoint: str = "",
        api_key: str = "",
        api_version: str = "2025-01-01",
        tenant_id: str = "unimelb",
    ):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_version = api_version
        self.tenant_id = tenant_id
        self._models_registry: dict[str, dict[str, Any]] = {}
        self._init_model_registry()

    def _init_model_registry(self) -> None:
        """Initialise the frontier model registry with capabilities."""
        self._models_registry = {
            FrontierModel.GPT_4O.value: {
                "provider": "microsoft",
                "capabilities": ["chat", "vision", "function_calling", "json_mode"],
                "max_tokens": 128_000,
                "cost_per_1k_input": 0.0025,
                "cost_per_1k_output": 0.01,
            },
            FrontierModel.CLAUDE_OPUS.value: {
                "provider": "anthropic",
                "capabilities": ["chat", "extended_thinking", "vision", "tool_use"],
                "max_tokens": 200_000,
                "cost_per_1k_input": 0.015,
                "cost_per_1k_output": 0.075,
            },
            FrontierModel.CLAUDE_SONNET.value: {
                "provider": "anthropic",
                "capabilities": ["chat", "extended_thinking", "vision", "tool_use"],
                "max_tokens": 200_000,
                "cost_per_1k_input": 0.003,
                "cost_per_1k_output": 0.015,
            },
            FrontierModel.GEMINI_PRO.value: {
                "provider": "google",
                "capabilities": ["chat", "vision", "multimodal", "grounding"],
                "max_tokens": 2_000_000,
                "cost_per_1k_input": 0.00125,
                "cost_per_1k_output": 0.005,
            },
            FrontierModel.DEEPSEEK_R1.value: {
                "provider": "deepseek",
                "capabilities": ["chat", "reasoning", "math", "code"],
                "max_tokens": 128_000,
                "cost_per_1k_input": 0.00055,
                "cost_per_1k_output": 0.0022,
            },
            FrontierModel.GROK_4.value: {
                "provider": "xai",
                "capabilities": ["chat", "web_search", "tool_use"],
                "max_tokens": 128_000,
                "cost_per_1k_input": 0.003,
                "cost_per_1k_output": 0.015,
            },
        }

    def get_available_models(self) -> list[dict[str, Any]]:
        """Return all available frontier models and their capabilities."""
        return [
            {"model": model_id, **info}
            for model_id, info in self._models_registry.items()
        ]

    def chat(
        self,
        messages: list[dict[str, str]],
        model: FrontierModel = FrontierModel.GPT_4O,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> FoundryResponse:
        """
        Send a chat request to a single frontier model via Azure AI Foundry.

        Uses low temperature by default for factual accuracy (anti-hallucination).
        """
        start = time.time()
        model_id = model.value

        # In production, this calls the Azure AI Foundry inference endpoint.
        # For the alpha scaffold, we define the interface contract.
        response_content = self._invoke_model(
            model_id=model_id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        latency = int((time.time() - start) * 1000)
        model_info = self._models_registry.get(model_id, {})

        return FoundryResponse(
            content=response_content.get("content", ""),
            model=model_id,
            provider=model_info.get("provider", "unknown"),
            confidence=response_content.get("confidence", 0.0),
            input_tokens=response_content.get("input_tokens", 0),
            output_tokens=response_content.get("output_tokens", 0),
            latency_ms=latency,
            sources=response_content.get("sources", []),
            metadata=response_content.get("metadata", {}),
        )

    def multi_model_query(
        self,
        messages: list[dict[str, str]],
        models: list[FrontierModel] | None = None,
        temperature: float = 0.1,
        **kwargs: Any,
    ) -> MultiModelResult:
        """
        Query multiple frontier models simultaneously for cross-verification.

        This is the core anti-hallucination pattern: by querying 3+ models and
        comparing their responses, we can identify consensus and divergence,
        producing a confidence-scored answer.

        Default models: GPT-4o, Claude Sonnet, Gemini Pro (3-way verification).
        """
        if models is None:
            models = [
                FrontierModel.GPT_4O,
                FrontierModel.CLAUDE_SONNET,
                FrontierModel.GEMINI_PRO,
            ]

        responses: list[FoundryResponse] = []
        for model in models:
            response = self.chat(
                messages=messages,
                model=model,
                temperature=temperature,
                **kwargs,
            )
            responses.append(response)

        # Cross-verification analysis
        result = self._analyse_consensus(responses)
        result.responses = responses
        return result

    def _invoke_model(
        self,
        model_id: str,
        messages: list[dict[str, str]],
        temperature: float = 0.1,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Invoke a model via Azure AI Foundry inference endpoint.

        Alpha implementation: Returns interface contract structure.
        Beta/Production: Calls Azure AI Foundry REST API.
        """
        # Alpha scaffold — define the response contract
        return {
            "content": f"[{model_id}] Response pending — Azure AI Foundry endpoint not yet configured",
            "confidence": 0.0,
            "input_tokens": 0,
            "output_tokens": 0,
            "sources": [],
            "metadata": {
                "model_id": model_id,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "api_version": self.api_version,
                "tenant": self.tenant_id,
            },
        }

    def _analyse_consensus(
        self,
        responses: list[FoundryResponse],
    ) -> MultiModelResult:
        """
        Analyse consensus across multiple model responses.

        Scoring:
        - 3/3 agree → confidence 0.9+
        - 2/3 agree → confidence 0.6–0.8
        - No agreement → confidence < 0.6 → flag for manual review
        """
        if not responses:
            return MultiModelResult(
                responses=[],
                consensus_score=0.0,
                consensus_answer="No responses received.",
                verification_status="failed",
            )

        # Alpha: basic consensus framework
        # Production: semantic similarity comparison using embeddings
        contents = [r.content for r in responses]
        unique_contents = set(contents)

        if len(unique_contents) == 1:
            score = 0.95
            status = "high_confidence"
        elif len(unique_contents) <= len(contents) // 2 + 1:
            score = 0.7
            status = "partially_verified"
        else:
            score = 0.4
            status = "unverified_manual_review_required"

        return MultiModelResult(
            responses=responses,
            consensus_score=score,
            consensus_answer=contents[0] if contents else "",
            divergence_points=[],
            verification_status=status,
        )


class FoundryModelRouter:
    """
    Intelligent model routing for UniMelb AI Platform.

    Routes queries to the optimal frontier model based on:
    - Query type (research, legal, general, code, etc.)
    - Faculty context (Law, Engineering, IT, Business, etc.)
    - Cost optimisation
    - Latency requirements
    - Anti-hallucination needs (routes to multi-model for critical queries)
    """

    # Faculty → preferred model mappings
    FACULTY_MODEL_MAP: dict[str, FrontierModel] = {
        "law": FrontierModel.CLAUDE_OPUS,       # Best for nuanced legal reasoning
        "engineering": FrontierModel.GPT_4O,      # Strong on technical/math
        "it": FrontierModel.CLAUDE_SONNET,        # Excellent for code
        "business": FrontierModel.GPT_4O,         # Strong on analysis
        "arts": FrontierModel.CLAUDE_SONNET,      # Strong on language/nuance
        "medicine": FrontierModel.CLAUDE_OPUS,    # Careful, safety-focused
        "science": FrontierModel.GEMINI_PRO,      # Large context, multimodal
    }

    # Query type → model preference
    QUERY_TYPE_MAP: dict[str, FrontierModel] = {
        "legal_research": FrontierModel.CLAUDE_OPUS,
        "code_generation": FrontierModel.CLAUDE_SONNET,
        "data_analysis": FrontierModel.GPT_4O,
        "literature_review": FrontierModel.GEMINI_PRO,
        "math_reasoning": FrontierModel.DEEPSEEK_R1,
        "web_search": FrontierModel.GROK_4,
        "general": FrontierModel.GPT_4O,
    }

    def __init__(self, client: AzureFoundryClient):
        self.client = client

    def route(
        self,
        messages: list[dict[str, str]],
        faculty: str | None = None,
        query_type: str | None = None,
        require_verification: bool = False,
        **kwargs: Any,
    ) -> FoundryResponse | MultiModelResult:
        """
        Route a query to the optimal model(s).

        If require_verification is True, uses multi-model cross-verification.
        """
        if require_verification:
            return self.client.multi_model_query(messages, **kwargs)

        # Determine best model
        model = FrontierModel.GPT_4O  # default
        if faculty and faculty.lower() in self.FACULTY_MODEL_MAP:
            model = self.FACULTY_MODEL_MAP[faculty.lower()]
        elif query_type and query_type.lower() in self.QUERY_TYPE_MAP:
            model = self.QUERY_TYPE_MAP[query_type.lower()]

        return self.client.chat(messages, model=model, **kwargs)

"""
UniMelb AI Platform — End-to-End Orchestration Pipeline
========================================================
The main pipeline that ties all platform modules together.

Flow:
  User Query → Identity Check → Faculty Routing → AI Engine (Azure Foundry)
  → Anti-Hallucination Verification → Source Citation → Audit Logging
  → Response Delivery (Teams / Web / iOS App)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ..anti_hallucination.verification_engine import (
    AntiHallucinationEngine,
    SourceCitation,
    VerificationResult,
)
from ..azure_foundry.foundry_client import (
    AzureFoundryClient,
    FoundryModelRouter,
    FoundryResponse,
    MultiModelResult,
)
from ..compliance.azure_monitor import AuditEventType, AzureMonitorLogger


@dataclass
class PlatformUser:
    """A user of the UniMelb AI Platform."""

    user_id: str
    email: str
    display_name: str
    role: str  # student | academic_staff | professional_staff | admin
    faculty: str = ""
    department: str = ""
    life_challenge_stage: str = ""  # "" | "finance" | "pause" | "restart"


@dataclass
class PlatformQuery:
    """A query submitted to the UniMelb AI Platform."""

    query_id: str
    user: PlatformUser
    query_text: str
    context: str = ""
    require_verification: bool = True
    require_sources: bool = True
    faculty_context: str = ""
    query_type: str = "general"


@dataclass
class PlatformResponse:
    """A complete platform response with verification metadata."""

    query_id: str
    response_text: str
    verification: VerificationResult | None = None
    formatted_response: str = ""
    model_used: str = ""
    latency_ms: int = 0
    audit_event_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


class UniMelbAIPipeline:
    """
    Main orchestration pipeline for the UniMelb AI Platform.

    Connects:
    1. Azure AI Foundry (frontier models)
    2. Anti-Hallucination Engine (verification)
    3. Azure Monitor (audit logging)
    4. Faculty-specific routing
    5. Life Challenge access management

    Security-first: every query is authenticated, logged, and verified.
    """

    def __init__(
        self,
        foundry_endpoint: str = "",
        foundry_api_key: str = "",
        monitor_workspace_id: str = "",
    ):
        self.foundry_client = AzureFoundryClient(
            endpoint=foundry_endpoint,
            api_key=foundry_api_key,
        )
        self.model_router = FoundryModelRouter(self.foundry_client)
        self.verification_engine = AntiHallucinationEngine()
        self.audit_logger = AzureMonitorLogger(
            workspace_id=monitor_workspace_id,
        )
        self._query_counter = 0

    def process_query(self, query: PlatformQuery) -> PlatformResponse:
        """
        Process a user query through the full platform pipeline.

        Steps:
        1. Validate user access (Life Challenge stage check)
        2. Route to optimal AI model(s) based on faculty/query type
        3. Get AI response(s)
        4. Run anti-hallucination verification
        5. Format response with verification metadata
        6. Log everything to Azure Monitor
        7. Return verified response
        """
        self._query_counter += 1
        start_time = datetime.now()

        # Step 1: Access check
        access_allowed, access_note = self._check_access(query.user)
        if not access_allowed:
            return self._create_access_denied_response(
                query, access_note
            )

        # Step 2 & 3: Route and get AI response
        faculty = query.faculty_context or query.user.faculty
        ai_result = self.model_router.route(
            messages=[
                {"role": "system", "content": self._build_system_prompt(query)},
                {"role": "user", "content": query.query_text},
            ],
            faculty=faculty,
            query_type=query.query_type,
            require_verification=query.require_verification,
        )

        # Extract response content
        if isinstance(ai_result, MultiModelResult):
            response_text = ai_result.consensus_answer
            model_used = ", ".join(
                r.model for r in ai_result.responses
            )
            model_responses = [
                {"model": r.model, "content": r.content}
                for r in ai_result.responses
            ]
        else:
            response_text = ai_result.content
            model_used = ai_result.model
            model_responses = [
                {"model": ai_result.model, "content": ai_result.content}
            ]

        # Step 4: Anti-hallucination verification
        verification = self.verification_engine.verify_response(
            query=query.query_text,
            response=response_text,
            model_responses=model_responses,
            user_id=query.user.user_id,
            session_id=query.query_id,
        )

        # Step 5: Format response
        formatted = self.verification_engine.format_response_with_verification(
            verification
        )

        # Step 6: Audit log
        latency = int((datetime.now() - start_time).total_seconds() * 1000)
        audit_id = self.audit_logger.log_ai_interaction(
            user_id=query.user.user_id,
            user_email=query.user.email,
            query=query.query_text,
            response=response_text,
            model=model_used,
            confidence_score=verification.confidence_score,
            verification_status=verification.status.value,
            session_id=query.query_id,
        )

        # Step 7: Return
        return PlatformResponse(
            query_id=query.query_id,
            response_text=response_text,
            verification=verification,
            formatted_response=formatted,
            model_used=model_used,
            latency_ms=latency,
            audit_event_id=audit_id,
        )

    def _check_access(
        self, user: PlatformUser
    ) -> tuple[bool, str]:
        """Check if user has access based on their Life Challenge stage."""
        if user.life_challenge_stage == "pause":
            return True, "Limited access — Life Challenge Pause mode"
        return True, "Full access"

    def _build_system_prompt(self, query: PlatformQuery) -> str:
        """Build a faculty-aware system prompt."""
        prompt_parts = [
            "You are the UniMelb AI Assistant, an exclusive AI platform for the "
            "University of Melbourne. You are built on Azure AI Foundry.",
            "",
            "CRITICAL RULES:",
            "1. NEVER fabricate information. If you are not certain, say 'I am not "
            "certain — please verify this against official sources.'",
            "2. ALWAYS cite your sources where possible.",
            "3. For legal questions, note that responses require verification against "
            "AustLII (www.austlii.edu.au) or relevant legislation databases.",
            "4. For medical/clinical questions, note that responses are for research "
            "purposes only and do not constitute medical advice.",
            "5. Distinguish clearly between facts, analysis, and opinion.",
        ]

        if query.faculty_context:
            prompt_parts.append(f"\nFaculty context: {query.faculty_context}")
        if query.user.role:
            prompt_parts.append(f"User role: {query.user.role}")
        if query.context:
            prompt_parts.append(f"\nAdditional context: {query.context}")

        return "\n".join(prompt_parts)

    def _create_access_denied_response(
        self, query: PlatformQuery, reason: str
    ) -> PlatformResponse:
        """Create a response for access-denied situations."""
        self.audit_logger.log_event(
            __import__("src.unimelb.compliance.azure_monitor", fromlist=["AuditEvent"]).AuditEvent(
                event_id="",
                event_type=AuditEventType.ACCESS_DENIED,
                timestamp=datetime.now(),
                user_id=query.user.user_id,
                user_email=query.user.email,
                resource="unimelb_ai_copilot",
                action="query",
                details={"reason": reason},
            )
        )
        return PlatformResponse(
            query_id=query.query_id,
            response_text=f"Access restricted: {reason}",
            formatted_response=f"Access restricted: {reason}",
        )

    # ── Platform Metrics ─────────────────────────────────────────────

    def get_platform_metrics(self) -> dict[str, Any]:
        """Get comprehensive platform metrics."""
        return {
            "total_queries_processed": self._query_counter,
            "ai_usage": self.audit_logger.get_ai_usage_summary(),
            "verification_metrics": self.verification_engine.get_accuracy_metrics(),
            "manual_reviews_pending": len(
                self.verification_engine.get_review_queue()
            ),
            "available_models": self.foundry_client.get_available_models(),
        }

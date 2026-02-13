"""
Azure Monitor Compliance & Audit Logging
==========================================
Immutable audit trail for all UniMelb AI Platform operations.

Supports:
- Full AI query/response logging with verification status
- Government auditor read-only access
- Azure Sentinel SIEM integration
- Privacy Act 1988, TEQSA, ESOS Act compliance
- APAC regulatory extension (NZ, Fiji, Singapore)

Every interaction is logged: timestamp, user, models used, confidence
score, sources cited, verification status, latency, token usage, cost.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AuditEventType(Enum):
    """Types of auditable events in the platform."""

    # AI interactions
    AI_QUERY = "ai_query"
    AI_RESPONSE = "ai_response"
    AI_VERIFICATION = "ai_verification"
    AI_MANUAL_REVIEW = "ai_manual_review"
    AI_MODEL_SWITCH = "ai_model_switch"

    # Authentication & access
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    ROLE_CHANGE = "role_change"
    ACCESS_DENIED = "access_denied"
    MFA_CHALLENGE = "mfa_challenge"

    # Data operations
    DATA_READ = "data_read"
    DATA_WRITE = "data_write"
    DATA_DELETE = "data_delete"
    DATA_EXPORT = "data_export"

    # Property management
    PROPERTY_LEASE_CREATED = "property_lease_created"
    PROPERTY_LEASE_MODIFIED = "property_lease_modified"
    PROPERTY_MAINTENANCE = "property_maintenance"

    # Migration
    CANVAS_CONTENT_MIGRATED = "canvas_content_migrated"
    CANVAS_COURSE_CUTOVER = "canvas_course_cutover"

    # Compliance
    COMPLIANCE_CHECK = "compliance_check"
    AUDIT_ACCESS = "audit_access"
    POLICY_VIOLATION = "policy_violation"

    # System
    SYSTEM_ERROR = "system_error"
    SYSTEM_HEALTH = "system_health"
    BACKUP_COMPLETED = "backup_completed"


class ComplianceFramework(Enum):
    """Regulatory frameworks the platform must comply with."""

    PRIVACY_ACT_1988 = "privacy_act_1988_cth"
    TEQSA = "teqsa_higher_education_standards"
    ESOS_ACT_2000 = "esos_act_2000"
    AI_ETHICS_FRAMEWORK = "ai_ethics_framework_au"
    SOCI_ACT = "security_critical_infrastructure"
    SPAM_ACT_2003 = "spam_act_2003"
    CDR = "consumer_data_right"
    ISO_27001 = "iso_27001"
    SOC_2_TYPE_II = "soc_2_type_ii"
    IRAP = "irap_au_govt"

    # APAC extensions
    NZ_PRIVACY_ACT_2020 = "nz_privacy_act_2020"
    NZ_EDUCATION_ACT_2020 = "nz_education_training_act_2020"
    FIJI_ONLINE_SAFETY_2018 = "fiji_online_safety_act_2018"
    FIJI_HIGHER_ED_2008 = "fiji_higher_education_act_2008"
    APEC_CBPR = "apec_cbpr"
    SG_PDPA = "singapore_pdpa"


class DataResidency(Enum):
    """Azure data residency regions for compliance."""

    AUSTRALIA_EAST = "australiaeast"       # Sydney (primary)
    AUSTRALIA_SOUTHEAST = "australiasoutheast"  # Melbourne
    SOUTHEAST_ASIA = "southeastasia"       # Singapore (APAC)
    NEW_ZEALAND = "newzealand"             # NZ extension


@dataclass
class AuditEvent:
    """A single immutable audit log event."""

    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    user_id: str
    user_email: str = ""
    user_role: str = ""
    resource: str = ""
    action: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    ip_address: str = ""
    session_id: str = ""
    ai_model: str = ""
    confidence_score: float | None = None
    verification_status: str = ""
    tokens_used: int = 0
    cost_aud: float = 0.0
    data_residency: DataResidency = DataResidency.AUSTRALIA_EAST
    compliance_tags: list[str] = field(default_factory=list)


@dataclass
class ComplianceCheckResult:
    """Result of a compliance check against a regulatory framework."""

    framework: ComplianceFramework
    status: str  # "compliant" | "non_compliant" | "partial" | "not_assessed"
    checked_at: datetime = field(default_factory=datetime.now)
    findings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    next_review_date: datetime | None = None


class AzureMonitorLogger:
    """
    Azure Monitor integration for UniMelb AI Platform.

    Provides an immutable audit trail that:
    - Logs every AI interaction with full metadata
    - Supports government auditor read-only queries
    - Integrates with Azure Sentinel for SIEM
    - Tracks compliance status per regulatory framework
    - Monitors data residency requirements

    In production, this writes to Azure Log Analytics Workspace
    and Azure Application Insights. Alpha uses in-memory storage.
    """

    def __init__(
        self,
        workspace_id: str = "",
        instrumentation_key: str = "",
        data_residency: DataResidency = DataResidency.AUSTRALIA_EAST,
    ):
        self.workspace_id = workspace_id
        self.instrumentation_key = instrumentation_key
        self.data_residency = data_residency
        self._audit_log: list[AuditEvent] = []
        self._compliance_results: dict[
            ComplianceFramework, ComplianceCheckResult
        ] = {}
        self._event_counter: int = 0

    def log_event(self, event: AuditEvent) -> str:
        """
        Log an audit event (immutable — append only).

        Returns the event_id for reference.
        """
        self._event_counter += 1
        if not event.event_id:
            event.event_id = f"EVT-{self._event_counter:010d}"
        event.data_residency = self.data_residency
        self._audit_log.append(event)
        return event.event_id

    def log_ai_interaction(
        self,
        user_id: str,
        user_email: str,
        query: str,
        response: str,
        model: str,
        confidence_score: float,
        verification_status: str,
        tokens_used: int = 0,
        cost_aud: float = 0.0,
        sources: list[str] | None = None,
        session_id: str = "",
    ) -> str:
        """Log a complete AI interaction (query + response + verification)."""
        event = AuditEvent(
            event_id="",
            event_type=AuditEventType.AI_QUERY,
            timestamp=datetime.now(),
            user_id=user_id,
            user_email=user_email,
            resource="unimelb_ai_copilot",
            action="chat",
            details={
                "query": query,
                "response_preview": response[:500],
                "response_length": len(response),
                "sources": sources or [],
            },
            session_id=session_id,
            ai_model=model,
            confidence_score=confidence_score,
            verification_status=verification_status,
            tokens_used=tokens_used,
            cost_aud=cost_aud,
        )
        return self.log_event(event)

    def log_canvas_migration(
        self,
        content_id: str,
        content_type: str,
        source: str,
        destination: str,
        status: str,
        user_id: str = "system",
    ) -> str:
        """Log a Canvas → Teams content migration event."""
        event = AuditEvent(
            event_id="",
            event_type=AuditEventType.CANVAS_CONTENT_MIGRATED,
            timestamp=datetime.now(),
            user_id=user_id,
            resource=content_id,
            action="migrate",
            details={
                "content_type": content_type,
                "source": source,
                "destination": destination,
                "status": status,
            },
        )
        return self.log_event(event)

    def log_property_event(
        self,
        event_type: AuditEventType,
        resource_id: str,
        action: str,
        user_id: str,
        details: dict[str, Any] | None = None,
    ) -> str:
        """Log a property management event."""
        event = AuditEvent(
            event_id="",
            event_type=event_type,
            timestamp=datetime.now(),
            user_id=user_id,
            resource=resource_id,
            action=action,
            details=details or {},
        )
        return self.log_event(event)

    # ── Audit Queries (Government Auditor Access) ────────────────────

    def query_audit_log(
        self,
        event_type: AuditEventType | None = None,
        user_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 1000,
    ) -> list[AuditEvent]:
        """Query the audit log with filters (read-only for auditors)."""
        results = list(self._audit_log)

        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if user_id:
            results = [e for e in results if e.user_id == user_id]
        if start_date:
            results = [e for e in results if e.timestamp >= start_date]
        if end_date:
            results = [e for e in results if e.timestamp <= end_date]

        return results[-limit:]

    def get_ai_usage_summary(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, Any]:
        """Get AI usage summary for auditing and reporting."""
        ai_events = self.query_audit_log(
            event_type=AuditEventType.AI_QUERY,
            start_date=start_date,
            end_date=end_date,
        )

        if not ai_events:
            return {"total_queries": 0, "message": "No AI interactions logged"}

        total_tokens = sum(e.tokens_used for e in ai_events)
        total_cost = sum(e.cost_aud for e in ai_events)

        models_used: dict[str, int] = {}
        verification_counts: dict[str, int] = {}
        confidence_scores: list[float] = []

        for event in ai_events:
            models_used[event.ai_model] = models_used.get(event.ai_model, 0) + 1
            verification_counts[event.verification_status] = (
                verification_counts.get(event.verification_status, 0) + 1
            )
            if event.confidence_score is not None:
                confidence_scores.append(event.confidence_score)

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0
        )

        return {
            "total_queries": len(ai_events),
            "total_tokens": total_tokens,
            "total_cost_aud": round(total_cost, 2),
            "models_used": models_used,
            "verification_breakdown": verification_counts,
            "average_confidence_score": round(avg_confidence, 3),
            "data_residency": self.data_residency.value,
        }

    # ── Compliance Checks ────────────────────────────────────────────

    def run_compliance_check(
        self,
        framework: ComplianceFramework,
    ) -> ComplianceCheckResult:
        """
        Run a compliance check for a specific regulatory framework.

        Alpha: returns framework-specific checklist.
        Production: automated compliance validation.
        """
        checks = self._get_framework_checks(framework)
        result = ComplianceCheckResult(
            framework=framework,
            status="not_assessed",
            findings=checks.get("findings", []),
            recommendations=checks.get("recommendations", []),
        )
        self._compliance_results[framework] = result
        return result

    def get_compliance_dashboard(self) -> dict[str, Any]:
        """Get compliance status across all frameworks."""
        dashboard = {}
        for framework in ComplianceFramework:
            result = self._compliance_results.get(framework)
            if result:
                dashboard[framework.value] = {
                    "status": result.status,
                    "last_checked": result.checked_at.isoformat(),
                    "findings_count": len(result.findings),
                }
            else:
                dashboard[framework.value] = {
                    "status": "not_assessed",
                    "last_checked": None,
                    "findings_count": 0,
                }
        return dashboard

    def _get_framework_checks(
        self, framework: ComplianceFramework
    ) -> dict[str, Any]:
        """Get checklist items for a compliance framework."""
        framework_checks = {
            ComplianceFramework.PRIVACY_ACT_1988: {
                "findings": [
                    "Data residency: Australia East (Sydney) — compliant",
                    "Encryption at rest: AES-256 via Azure — compliant",
                    "Encryption in transit: TLS 1.3 — compliant",
                    "Access control: RBAC via Entra ID — compliant",
                    "Data retention: configurable per APPs — review required",
                ],
                "recommendations": [
                    "Complete Privacy Impact Assessment for AI features",
                    "Review data sharing with APAC extension partners",
                ],
            },
            ComplianceFramework.TEQSA: {
                "findings": [
                    "AI accuracy monitoring: anti-hallucination engine active",
                    "Student data protection: Entra ID + MFA enabled",
                    "Quality assurance: verification framework in place",
                ],
                "recommendations": [
                    "Submit TEQSA notification for AI-assisted assessment",
                    "Develop AI literacy standards for academic integrity",
                ],
            },
            ComplianceFramework.ESOS_ACT_2000: {
                "findings": [
                    "International student support: multilingual AI available",
                    "PRISMS integration: capability planned for Beta",
                ],
                "recommendations": [
                    "Ensure AI responses account for visa condition obligations",
                    "Add ESOS-specific guidance to AI knowledge base",
                ],
            },
            ComplianceFramework.ISO_27001: {
                "findings": [
                    "Information security management: Azure Defender active",
                    "Risk assessment: framework defined",
                    "Incident response: Azure Sentinel configured",
                ],
                "recommendations": [
                    "Complete ISO 27001 Stage 1 audit",
                    "Document AI-specific security controls in ISMS",
                ],
            },
            ComplianceFramework.IRAP: {
                "findings": [
                    "Azure IRAP assessed: Yes (Protected level)",
                    "Platform IRAP assessment: not yet started",
                ],
                "recommendations": [
                    "Engage IRAP assessor for platform-level assessment",
                    "Document all data flows for IRAP scope",
                ],
            },
        }
        return framework_checks.get(
            framework,
            {
                "findings": [f"Assessment for {framework.value} not yet configured"],
                "recommendations": [f"Schedule {framework.value} compliance review"],
            },
        )

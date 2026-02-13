"""
Government Regulatory Compliance Framework — AU/NZ/APAC
========================================================
Full regulatory compliance module for the UniMelb AI Platform.

Covers:
- Australian regulations (Privacy Act, TEQSA, ESOS, AI Ethics)
- New Zealand regulations (Privacy Act 2020, Education Act 2020)
- Fiji regulations (Online Safety Act 2018, Higher Education Act 2008)
- APAC frameworks (APEC CBPR, Singapore PDPA)
- International standards (ISO 27001, SOC 2 Type II, IRAP)

Designed for government monitoring and potential sharing with NZ and Fiji.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Jurisdiction(Enum):
    """Regulatory jurisdictions."""

    AUSTRALIA = "australia"
    NEW_ZEALAND = "new_zealand"
    FIJI = "fiji"
    SINGAPORE = "singapore"
    APAC_REGIONAL = "apac_regional"


class ComplianceStatus(Enum):
    """Status of compliance with a specific requirement."""

    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_ASSESSED = "not_assessed"
    EXEMPTED = "exempted"
    IN_REMEDIATION = "in_remediation"


class RegulatoryDomain(Enum):
    """Categories of regulatory requirements."""

    PRIVACY = "privacy"
    EDUCATION_QUALITY = "education_quality"
    AI_GOVERNANCE = "ai_governance"
    DATA_SOVEREIGNTY = "data_sovereignty"
    CYBERSECURITY = "cybersecurity"
    CONSUMER_PROTECTION = "consumer_protection"
    ACCESSIBILITY = "accessibility"
    INTERNATIONAL_STUDENTS = "international_students"


@dataclass
class RegulatoryRequirement:
    """A specific regulatory requirement."""

    requirement_id: str
    jurisdiction: Jurisdiction
    domain: RegulatoryDomain
    regulation_name: str
    section: str
    description: str
    mandatory: bool = True
    status: ComplianceStatus = ComplianceStatus.NOT_ASSESSED
    controls: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    last_assessed: datetime | None = None
    next_review: datetime | None = None
    owner: str = ""
    notes: str = ""


@dataclass
class ComplianceReport:
    """A compliance assessment report."""

    report_id: str
    jurisdiction: Jurisdiction
    generated_at: datetime = field(default_factory=datetime.now)
    total_requirements: int = 0
    compliant_count: int = 0
    non_compliant_count: int = 0
    not_assessed_count: int = 0
    overall_score: float = 0.0  # 0.0 → 100.0
    findings: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


class RegulatoryFramework:
    """
    Government regulatory compliance manager for UniMelb AI Platform.

    Tracks compliance across all applicable regulations in Australia,
    New Zealand, Fiji, and broader APAC. Supports government auditor
    access and automated compliance reporting.
    """

    def __init__(self) -> None:
        self._requirements: list[RegulatoryRequirement] = []
        self._reports: list[ComplianceReport] = []
        self._init_requirements()

    def _init_requirements(self) -> None:
        """Initialise all regulatory requirements."""
        self._requirements = [
            # ── Australian Requirements ──────────────────────────────
            RegulatoryRequirement(
                requirement_id="AU-PRIV-001",
                jurisdiction=Jurisdiction.AUSTRALIA,
                domain=RegulatoryDomain.PRIVACY,
                regulation_name="Privacy Act 1988 (Cth)",
                section="Australian Privacy Principles (APPs)",
                description="Collection, use, disclosure, and storage of personal information must comply with all 13 APPs",
                controls=[
                    "Azure data residency in Australia East (Sydney)",
                    "Encryption at rest (AES-256) and in transit (TLS 1.3)",
                    "RBAC via Microsoft Entra ID",
                    "Data minimisation in AI model training",
                    "Privacy Impact Assessment completed",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="AU-PRIV-002",
                jurisdiction=Jurisdiction.AUSTRALIA,
                domain=RegulatoryDomain.PRIVACY,
                regulation_name="Privacy Act 1988 (Cth)",
                section="APP 8 — Cross-border disclosure",
                description="Personal information must not be disclosed overseas unless adequate protections exist",
                controls=[
                    "APAC data sharing agreements",
                    "Azure geo-fencing to AU/NZ/SG regions",
                    "Cross-border PIA for NZ and Fiji extensions",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="AU-TEQSA-001",
                jurisdiction=Jurisdiction.AUSTRALIA,
                domain=RegulatoryDomain.EDUCATION_QUALITY,
                regulation_name="TEQSA Higher Education Standards Framework",
                section="Section 2 — Learning Environment",
                description="AI tools used in teaching must maintain academic integrity and quality standards",
                controls=[
                    "Anti-hallucination verification framework",
                    "AI accuracy monitoring and reporting",
                    "Academic integrity policy for AI-assisted assessment",
                    "Student notification of AI use in grading",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="AU-TEQSA-002",
                jurisdiction=Jurisdiction.AUSTRALIA,
                domain=RegulatoryDomain.EDUCATION_QUALITY,
                regulation_name="TEQSA Higher Education Standards Framework",
                section="Section 5 — Institutional Quality Assurance",
                description="Regular review of AI tools and their impact on educational outcomes",
                controls=[
                    "Quarterly AI accuracy reports",
                    "Student feedback integration",
                    "Faculty review of AI-generated content",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="AU-ESOS-001",
                jurisdiction=Jurisdiction.AUSTRALIA,
                domain=RegulatoryDomain.INTERNATIONAL_STUDENTS,
                regulation_name="ESOS Act 2000",
                section="National Code Standard 6",
                description="Adequate support services for international students, including AI-accessible resources",
                controls=[
                    "Multilingual AI support (20+ languages)",
                    "PRISMS integration capability",
                    "International student orientation AI module",
                    "Visa condition guidance (auto-verified against legislation)",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="AU-AI-001",
                jurisdiction=Jurisdiction.AUSTRALIA,
                domain=RegulatoryDomain.AI_GOVERNANCE,
                regulation_name="AI Ethics Framework (Dept of Industry, Science and Resources)",
                section="8 AI Ethics Principles",
                description="AI systems must be: accountable, transparent, fair, contestable, reliable, safe, private, and human-centred",
                controls=[
                    "Transparency: confidence scores on all AI responses",
                    "Accountability: full audit trail via Azure Monitor",
                    "Fairness: bias detection in model outputs",
                    "Contestability: human review queue for disputed answers",
                    "Reliability: anti-hallucination multi-model verification",
                    "Safety: content filtering and harmful output prevention",
                    "Privacy: data minimisation and consent management",
                    "Human-centred: Life Challenge Programme design",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="AU-CYBER-001",
                jurisdiction=Jurisdiction.AUSTRALIA,
                domain=RegulatoryDomain.CYBERSECURITY,
                regulation_name="Security of Critical Infrastructure Act 2018",
                section="Part 2A — Critical infrastructure risk management",
                description="If classified as critical infrastructure, enhanced security obligations apply",
                controls=[
                    "Azure Defender for Cloud",
                    "Azure Sentinel (SIEM)",
                    "Zero-Trust architecture via Entra ID",
                    "MFA for all users",
                    "Conditional Access policies",
                    "IRAP assessment (planned)",
                ],
            ),
            # ── New Zealand Requirements ─────────────────────────────
            RegulatoryRequirement(
                requirement_id="NZ-PRIV-001",
                jurisdiction=Jurisdiction.NEW_ZEALAND,
                domain=RegulatoryDomain.PRIVACY,
                regulation_name="Privacy Act 2020 (NZ)",
                section="Information Privacy Principles (IPPs)",
                description="NZ extension must comply with 13 IPPs for personal information handling",
                controls=[
                    "Data residency option for NZ region",
                    "Privacy officer appointment for NZ operations",
                    "Mandatory breach notification (within 72 hours)",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="NZ-EDU-001",
                jurisdiction=Jurisdiction.NEW_ZEALAND,
                domain=RegulatoryDomain.EDUCATION_QUALITY,
                regulation_name="Education and Training Act 2020 (NZ)",
                section="Part 4 — Tertiary Education",
                description="AI tools used in NZ higher education must meet NZQA quality standards",
                controls=[
                    "NZQA consultation for AI assessment tools",
                    "Alignment with NZ Qualifications Framework",
                ],
            ),
            # ── Fiji Requirements ────────────────────────────────────
            RegulatoryRequirement(
                requirement_id="FJ-SAFE-001",
                jurisdiction=Jurisdiction.FIJI,
                domain=RegulatoryDomain.CYBERSECURITY,
                regulation_name="Online Safety Act 2018 (Fiji)",
                section="Part 2 — Online safety",
                description="Platform must ensure online safety for Fiji users",
                controls=[
                    "Content moderation aligned with Fiji standards",
                    "Harmful content filtering",
                    "User reporting mechanisms",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="FJ-EDU-001",
                jurisdiction=Jurisdiction.FIJI,
                domain=RegulatoryDomain.EDUCATION_QUALITY,
                regulation_name="Higher Education Act 2008 (Fiji)",
                section="Quality assurance provisions",
                description="AI tools deployed in Fiji higher education must meet FHEC standards",
                controls=[
                    "FHEC consultation for AI deployment",
                    "Alignment with Fiji education quality framework",
                ],
            ),
            # ── APAC Regional ────────────────────────────────────────
            RegulatoryRequirement(
                requirement_id="APAC-CBPR-001",
                jurisdiction=Jurisdiction.APAC_REGIONAL,
                domain=RegulatoryDomain.DATA_SOVEREIGNTY,
                regulation_name="APEC Cross-Border Privacy Rules (CBPR)",
                section="CBPR System Requirements",
                description="Cross-border data transfers must comply with APEC CBPR framework",
                controls=[
                    "CBPR certification (planned Year 3)",
                    "Data transfer impact assessments",
                    "Partner jurisdiction agreements",
                ],
            ),
            RegulatoryRequirement(
                requirement_id="APAC-SG-001",
                jurisdiction=Jurisdiction.SINGAPORE,
                domain=RegulatoryDomain.PRIVACY,
                regulation_name="Personal Data Protection Act (PDPA, Singapore)",
                section="Data Protection Obligations",
                description="If serving Singapore institutions, PDPA obligations apply",
                controls=[
                    "PDPA compliance assessment (planned Year 3)",
                    "Data Protection Officer for SG operations",
                    "Azure Southeast Asia region for SG data",
                ],
            ),
        ]

    # ── Requirement Management ───────────────────────────────────────

    def get_requirements(
        self,
        jurisdiction: Jurisdiction | None = None,
        domain: RegulatoryDomain | None = None,
        status: ComplianceStatus | None = None,
    ) -> list[RegulatoryRequirement]:
        """Get regulatory requirements with optional filters."""
        results = list(self._requirements)
        if jurisdiction:
            results = [r for r in results if r.jurisdiction == jurisdiction]
        if domain:
            results = [r for r in results if r.domain == domain]
        if status:
            results = [r for r in results if r.status == status]
        return results

    def update_requirement_status(
        self,
        requirement_id: str,
        status: ComplianceStatus,
        evidence: list[str] | None = None,
        notes: str = "",
    ) -> RegulatoryRequirement | None:
        """Update the compliance status of a requirement."""
        for req in self._requirements:
            if req.requirement_id == requirement_id:
                req.status = status
                req.last_assessed = datetime.now()
                if evidence:
                    req.evidence.extend(evidence)
                if notes:
                    req.notes = notes
                return req
        return None

    # ── Compliance Reporting ─────────────────────────────────────────

    def generate_compliance_report(
        self,
        jurisdiction: Jurisdiction | None = None,
    ) -> ComplianceReport:
        """Generate a compliance report for a jurisdiction (or all)."""
        reqs = self.get_requirements(jurisdiction=jurisdiction)
        total = len(reqs)
        compliant = sum(
            1 for r in reqs if r.status == ComplianceStatus.COMPLIANT
        )
        non_compliant = sum(
            1 for r in reqs if r.status == ComplianceStatus.NON_COMPLIANT
        )
        not_assessed = sum(
            1 for r in reqs if r.status == ComplianceStatus.NOT_ASSESSED
        )

        score = (compliant / total * 100) if total > 0 else 0.0

        findings = []
        recommendations = []
        for req in reqs:
            if req.status in (
                ComplianceStatus.NON_COMPLIANT,
                ComplianceStatus.PARTIALLY_COMPLIANT,
            ):
                findings.append({
                    "requirement_id": req.requirement_id,
                    "regulation": req.regulation_name,
                    "section": req.section,
                    "status": req.status.value,
                    "description": req.description,
                })
                recommendations.append(
                    f"[{req.requirement_id}] Remediate: {req.description}"
                )

        report = ComplianceReport(
            report_id=f"CR-{datetime.now():%Y%m%d-%H%M%S}",
            jurisdiction=jurisdiction or Jurisdiction.AUSTRALIA,
            total_requirements=total,
            compliant_count=compliant,
            non_compliant_count=non_compliant,
            not_assessed_count=not_assessed,
            overall_score=round(score, 1),
            findings=findings,
            recommendations=recommendations,
        )
        self._reports.append(report)
        return report

    def get_government_audit_dashboard(self) -> dict[str, Any]:
        """
        Generate a dashboard for government auditors.

        Read-only view of compliance status across all jurisdictions.
        """
        dashboard: dict[str, Any] = {"jurisdictions": {}}
        for jurisdiction in Jurisdiction:
            reqs = self.get_requirements(jurisdiction=jurisdiction)
            if not reqs:
                continue
            total = len(reqs)
            compliant = sum(
                1 for r in reqs if r.status == ComplianceStatus.COMPLIANT
            )
            dashboard["jurisdictions"][jurisdiction.value] = {
                "total_requirements": total,
                "compliant": compliant,
                "compliance_rate": round(compliant / total * 100, 1) if total else 0,
                "non_compliant": sum(
                    1
                    for r in reqs
                    if r.status == ComplianceStatus.NON_COMPLIANT
                ),
                "not_assessed": sum(
                    1
                    for r in reqs
                    if r.status == ComplianceStatus.NOT_ASSESSED
                ),
            }

        dashboard["generated_at"] = datetime.now().isoformat()
        dashboard["platform"] = "UniMelb AI Platform"
        dashboard["data_residency"] = "Azure Australia East (Sydney)"
        dashboard["audit_access"] = "read_only_immutable"
        return dashboard

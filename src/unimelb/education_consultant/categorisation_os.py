"""
Education Consultant Categorisation_OS (COS) v3.1
===================================================
Design: Jiadong Chen (陈佳栋) — Student ID: 723912

Structured "Search -> Verify -> Advise -> Document" framework for
education-pathway planning in Australia. Uses ONLY public-domain,
official sources. Separates education consulting from regulated
migration assistance.

Based on:
- DOC-20260216-Education-Consultant-Manual-V3.1

COS Architecture (8 layers):
  L1 National (AU)
  L2 State/Territory (VIC/NSW/QLD/SA/WA/TAS/ACT/NT)
  L3 Institution Type (anonymised tiers)
  L4 Course Level (AQF) + Provider Registration (TEQSA/CRICOS)
  L5 Visa Pathway (Visitor vs Student vs Skilled etc.)
  L6 Occupation Mapping (ANZSCO / lists / assessing authority)
  L7 Risk & Compliance (policy volatility, integrity, consumer law)
  L8 Ethics, Non-Discrimination, Privacy, Cyber
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# =============================================================================
# Enums — COS Layers, Domains, Confidence, Risk
# =============================================================================

class COSLayer(Enum):
    """COS architecture layers (L1–L8)."""

    L1_NATIONAL = "L1"
    L2_STATE = "L2"
    L3_INSTITUTION = "L3"
    L4_COURSE_AQF = "L4"
    L5_VISA = "L5"
    L6_OCCUPATION = "L6"
    L7_RISK_COMPLIANCE = "L7"
    L8_ETHICS_PRIVACY_CYBER = "L8"


class COSSection(Enum):
    """COS section codes (COS-00 through COS-15)."""

    COS_00 = "COS-00"  # Introduction / Purpose / Values
    COS_01 = "COS-01"  # Regulatory Alignment Map
    COS_02 = "COS-02"  # COS Architecture
    COS_03 = "COS-03"  # Higher Education (TEQSA/HESF/AQF/CRICOS/ESOS)
    COS_04 = "COS-04"  # ESOS National Code + Education Agents (Standard 4)
    COS_05 = "COS-05"  # Visa Taxonomy (Visitor 600 vs Student 500)
    COS_06 = "COS-06"  # Genuine Student (GS) + Compliance Monitoring
    COS_07 = "COS-07"  # Skilled Migration Lists + ANZSCO + Assessing Auth
    COS_08 = "COS-08"  # Visa-Course-Occupation Mapping
    COS_09 = "COS-09"  # Multi-State Comparison
    COS_10 = "COS-10"  # Consultant / Agent Job Requirements
    COS_11 = "COS-11"  # Code of Conduct Table
    COS_12 = "COS-12"  # Privacy + Data Lifecycle
    COS_13 = "COS-13"  # Cyber Security (Essential Eight)
    COS_14 = "COS-14"  # Pre-Use Safety Gate + Liability
    COS_15 = "COS-15"  # References (REF Index)


class Confidence(Enum):
    """Traceability confidence level."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Impact(Enum):
    """Impact if a claim is wrong."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class RoleType(Enum):
    """Consultant role separation."""

    EDUCATION_CONSULTANT = "Education Consultant (Non-RMA)"
    RMA = "Registered Migration Agent (RMA)"
    LEGAL_PRACTITIONER = "Australian Legal Practitioner"
    EXEMPT_PERSON = "Exempt Person"


class VisaSubclass(Enum):
    """Common visa subclasses relevant to education pathway."""

    STUDENT_500 = "500"
    VISITOR_600 = "600"
    GRADUATE_485 = "485"
    SKILLED_189 = "189"
    SKILLED_190 = "190"
    SKILLED_491 = "491"


class AQFLevel(Enum):
    """Australian Qualifications Framework levels."""

    LEVEL_1 = 1   # Certificate I
    LEVEL_2 = 2   # Certificate II
    LEVEL_3 = 3   # Certificate III
    LEVEL_4 = 4   # Certificate IV
    LEVEL_5 = 5   # Diploma
    LEVEL_6 = 6   # Advanced Diploma / Associate Degree
    LEVEL_7 = 7   # Bachelor Degree
    LEVEL_8 = 8   # Bachelor Honours / Graduate Certificate / Graduate Diploma
    LEVEL_9 = 9   # Masters Degree
    LEVEL_10 = 10  # Doctoral Degree


class StateTerritory(Enum):
    """Australian states and territories."""

    VIC = "VIC"
    NSW = "NSW"
    QLD = "QLD"
    SA = "SA"
    WA = "WA"
    TAS = "TAS"
    ACT = "ACT"
    NT = "NT"


class DataLifecycleStage(Enum):
    """Privacy data lifecycle stages (COS-12)."""

    COLLECT = "Collect"
    STORE = "Store"
    PROCESS = "Process"
    SHARE = "Share"
    RETAIN = "Retain"
    DISPOSE = "Dispose"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class TraceabilityClaim:
    """Minimum traceability field for any claim (COS-02 requirement)."""

    claim_id: str
    statement: str
    evidence_ref: str         # REF-xx source
    last_checked: str         # date last verified
    confidence: Confidence = Confidence.MEDIUM
    impact_if_wrong: Impact = Impact.MEDIUM
    mitigation: str = ""


@dataclass
class ReferenceEntry:
    """A single REF entry from COS-15."""

    ref_id: str               # e.g. "REF-HA-500"
    url: str
    category: str             # e.g. "HOME_AFFAIRS", "EDUCATION", "PRIVACY"
    retrieval_date: str = "2026-02-16"
    description: str = ""


@dataclass
class EngagementRecord:
    """Evidence/log record required per COS-00."""

    engagement_id: str
    date_time: str
    source_list: list[str] = field(default_factory=list)
    client_consent: bool = False
    advice_summary: str = ""
    risk_disclosure: str = ""
    escalation_record: str = ""


@dataclass
class ConductEntry:
    """Code of conduct table entry (COS-11)."""

    area: str
    rule: str
    evidence_log: str
    source_anchor: str


@dataclass
class SafetyGateResult:
    """Pre-use safety gate check result (COS-14)."""

    all_passed: bool = False
    checks: dict[str, bool] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)


@dataclass
class PathwayOption:
    """Visa-Course-Occupation mapping output (COS-08)."""

    label: str                # Plan A / Plan B / Plan C
    course_cricos: str = ""
    aqf_level: int = 0
    target_anzsco: str = ""
    assessing_authority: str = ""
    visa_options: list[str] = field(default_factory=list)
    risk_notes: list[str] = field(default_factory=list)
    requires_rma_referral: bool = False


# =============================================================================
# Reference Store (COS-15) — Authoritative domains and REF index
# =============================================================================

AUTHORITATIVE_DOMAINS: dict[str, list[str]] = {
    "EDUCATION": [
        "education.gov.au",
        "cricos.education.gov.au",
    ],
    "HOME_AFFAIRS": [
        "immi.homeaffairs.gov.au",
    ],
    "MIGRATION_AGENTS": [
        "mara.gov.au",
    ],
    "PRIVACY": [
        "oaic.gov.au",
        "legislation.gov.au",
    ],
    "CYBER": [
        "cyber.gov.au",
    ],
    "HIGHER_ED_STANDARDS": [
        "teqsa.gov.au",
    ],
    "HUMAN_RIGHTS": [
        "humanrights.gov.au",
        "ag.gov.au",
    ],
    "CONSUMER_LAW": [
        "accc.gov.au",
    ],
    "VIC_STATE": [
        "legislation.vic.gov.au",
        "humanrights.vic.gov.au",
    ],
    "AQF": [
        "aqf.edu.au",
    ],
}

REFERENCE_INDEX: list[ReferenceEntry] = [
    # Education / ESOS / CRICOS
    ReferenceEntry("REF-EDU-ESOS", "https://www.education.gov.au/esos-framework", "EDUCATION", description="ESOS Framework overview"),
    ReferenceEntry("REF-EDU-ESOS-LEG", "https://www.education.gov.au/esos-framework/esos-legislative-framework", "EDUCATION", description="ESOS legislative framework"),
    ReferenceEntry("REF-LEG-ESOS-ACT", "https://www.legislation.gov.au/Details/C2017C00292", "EDUCATION", description="ESOS Act compilation"),
    ReferenceEntry("REF-EDU-NATIONAL-CODE", "https://www.education.gov.au/esos-framework/national-code-practice-providers-education-and-training-overseas-students-2018", "EDUCATION", description="National Code 2018"),
    ReferenceEntry("REF-LEG-NATIONAL-CODE", "https://www.legislation.gov.au/Details/F2017L01182", "EDUCATION", description="National Code legislation"),
    ReferenceEntry("REF-EDU-STD4", "https://www.education.gov.au/esos-framework/resources/standard-4-education-agents", "EDUCATION", description="Standard 4: Education Agents"),
    ReferenceEntry("REF-CRICOS", "https://cricos.education.gov.au/", "EDUCATION", description="CRICOS Register"),
    # Home Affairs
    ReferenceEntry("REF-HA-500", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500", "HOME_AFFAIRS", description="Student visa subclass 500"),
    ReferenceEntry("REF-HA-GS", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500/genuine-student-requirement", "HOME_AFFAIRS", description="Genuine Student requirement"),
    ReferenceEntry("REF-HA-600", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/visitor-600", "HOME_AFFAIRS", description="Visitor visa subclass 600"),
    ReferenceEntry("REF-HA-CONDITIONS", "https://immi.homeaffairs.gov.au/visas/already-have-a-visa/check-visa-details-and-conditions/see-your-visa-conditions?product=500", "HOME_AFFAIRS", description="Visa conditions (500)"),
    ReferenceEntry("REF-HA-PROCESSING", "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-processing-times/visa-processing-priorities/student-visa", "HOME_AFFAIRS", description="Student visa processing priorities"),
    ReferenceEntry("REF-HA-SOL", "https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list", "HOME_AFFAIRS", description="Skilled Occupation List"),
    ReferenceEntry("REF-HA-ASSESSING-AUTH", "https://immi.homeaffairs.gov.au/visas/working-in-australia/skills-assessment/assessing-authorities", "HOME_AFFAIRS", description="Skills assessing authorities"),
    ReferenceEntry("REF-HA-SKILLS-ASSESS", "https://immi.homeaffairs.gov.au/visas/working-in-australia/skills-assessment", "HOME_AFFAIRS", description="Skills assessment overview"),
    ReferenceEntry("REF-HA-POINTS-CALC", "https://immi.homeaffairs.gov.au/help-support/tools/points-calculator", "HOME_AFFAIRS", description="Points calculator tool"),
    ReferenceEntry("REF-HA-USING-AGENT", "https://immi.homeaffairs.gov.au/help-support/who-can-help-with-your-application/using-a-migration-agent", "HOME_AFFAIRS", description="Using a migration agent"),
    # MARA
    ReferenceEntry("REF-MARA-CODE", "https://www.mara.gov.au/tools-for-registered-agents/code-of-conduct", "MIGRATION_AGENTS", description="MARA Code of Conduct"),
    ReferenceEntry("REF-MARA-HELPERS", "https://www.mara.gov.au/get-help-with-a-visa/helpers-not-registered", "MIGRATION_AGENTS", description="Rules for non-registered helpers"),
    # Privacy
    ReferenceEntry("REF-LEG-PRIVACY-ACT", "https://www.legislation.gov.au/C2004A03712/latest", "PRIVACY", description="Privacy Act 1988 full text"),
    ReferenceEntry("REF-OAIC-PRIVACY-ACT", "https://www.oaic.gov.au/privacy/privacy-legislation/the-privacy-act", "PRIVACY", description="OAIC Privacy Act overview"),
    ReferenceEntry("REF-OAIC-APP", "https://www.oaic.gov.au/privacy/australian-privacy-principles", "PRIVACY", description="Australian Privacy Principles"),
    ReferenceEntry("REF-OAIC-NDB", "https://www.oaic.gov.au/privacy/notifiable-data-breaches", "PRIVACY", description="Notifiable Data Breaches scheme"),
    # Cyber
    ReferenceEntry("REF-CYBER-E8", "https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight", "CYBER", description="Essential Eight overview"),
    ReferenceEntry("REF-CYBER-E8-EXPLAIN", "https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-explained", "CYBER", description="Essential Eight explained"),
    ReferenceEntry("REF-CYBER-E8-MATURITY", "https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model", "CYBER", description="Essential Eight maturity model"),
    # Higher Ed Standards
    ReferenceEntry("REF-TEQSA-HESF", "https://www.teqsa.gov.au/how-we-regulate/higher-education-standards-framework-2021", "HIGHER_ED_STANDARDS", description="HESF 2021"),
    ReferenceEntry("REF-LEG-HESF", "https://www.legislation.gov.au/Details/F2022C00105", "HIGHER_ED_STANDARDS", description="HESF legislation"),
    # AQF
    ReferenceEntry("REF-AQF-LEVELS", "https://www.aqf.edu.au/framework/aqf-levels", "AQF", description="AQF levels"),
    ReferenceEntry("REF-AQF-L9", "https://www.aqf.edu.au/framework/aqf-qualifications", "AQF", description="AQF qualifications (incl. Level 9)"),
    # Human Rights
    ReferenceEntry("REF-AHRC-LAWS", "https://humanrights.gov.au/our-work/legal/legislation", "HUMAN_RIGHTS", description="AHRC legislation overview"),
    ReferenceEntry("REF-AG-ANTI-DISC", "https://www.ag.gov.au/rights-and-protections/human-rights-and-anti-discrimination/australias-anti-discrimination-law", "HUMAN_RIGHTS", description="AU anti-discrimination law"),
    ReferenceEntry("REF-VIC-EOA", "https://www.legislation.vic.gov.au/in-force/acts/equal-opportunity-act-2010", "HUMAN_RIGHTS", description="VIC Equal Opportunity Act 2010"),
    # Consumer Law
    ReferenceEntry("REF-ACCC-MISLEADING", "https://www.accc.gov.au/business/advertising-and-promotions/false-or-misleading-claims", "CONSUMER_LAW", description="ACCC false/misleading claims"),
    # State connectors
    ReferenceEntry("REF-NSW-SKILLS", "https://www.nsw.gov.au/visas-and-migration/skilled-visas/nsw-skills-lists", "STATE_CONNECTORS", description="NSW skills lists"),
    ReferenceEntry("REF-SA-SOL", "https://www.migration.sa.gov.au/occupation-lists/south-australia-skilled-occupation-list", "STATE_CONNECTORS", description="SA skilled occupation list"),
]


# Code of Conduct table (COS-11)
CODE_OF_CONDUCT: list[ConductEntry] = [
    ConductEntry("Truthfulness", "No false/misleading claims; separate facts from opinion", "Advice_Summary + Source_List", "REF-ACCC-MISLEADING"),
    ConductEntry("No Guarantee", "Never promise visa outcomes", "Risk_Disclosure_Record", "REF-HA-500"),
    ConductEntry("Role Boundary", "If 'immigration assistance', refer to RMA/legal", "Escalation_Record", "REF-HA-USING-AGENT"),
    ConductEntry("Student-first", "Provide accurate education info; avoid conflicts", "Disclosure_Record", "REF-EDU-STD4"),
    ConductEntry("Privacy", "Collect minimum necessary; consent; purpose limit", "Consent_Record + Data_Map", "REF-OAIC-APP"),
    ConductEntry("Security", "Apply baseline cyber controls; MFA/patching/backups", "Security_Checklist", "REF-CYBER-E8"),
    ConductEntry("Recordkeeping", "Keep dated copies of key sources used", "Evidence_Pack", "(internal)"),
    ConductEntry("Respect & Equality", "Inclusive language; no prejudice", "Interaction_Notes", "REF-AHRC-LAWS"),
    ConductEntry("Complaint pathway", "Provide complaint/referral pathway transparently", "Complaint_Record", "REF-MARA-CODE"),
]


# Pre-use safety gate checks (COS-14)
SAFETY_GATE_CHECKS: list[str] = [
    "education_vs_immigration_understood",
    "official_sources_checked_today",
    "cricos_listing_confirmed",
    "student_500_requirements_reviewed",
    "visitor_600_study_limit_noted",
    "genuine_student_page_checked",
    "occupation_list_date_checked",
    "assessing_authority_checked",
    "privacy_consent_captured",
    "cyber_controls_applied",
    "non_discrimination_standard_stated",
    "no_misleading_claims_confirmed",
]


# =============================================================================
# Main COS Framework Class
# =============================================================================

class EducationConsultantCOS:
    """
    Education Consultant Categorisation_OS (COS) v3.1.

    Structured framework for education-pathway planning in Australia.
    Implements the 8-layer COS architecture with traceability,
    safety gates, role separation, and compliance controls.
    """

    def __init__(self) -> None:
        self.reference_index = REFERENCE_INDEX
        self.code_of_conduct = CODE_OF_CONDUCT
        self.authoritative_domains = AUTHORITATIVE_DOMAINS
        self.safety_gate_checks = SAFETY_GATE_CHECKS
        self.engagements: list[EngagementRecord] = []
        self.claims: list[TraceabilityClaim] = []

    # -----------------------------------------------------------------
    # Reference lookup
    # -----------------------------------------------------------------

    def get_reference(self, ref_id: str) -> ReferenceEntry | None:
        """Look up a reference by its REF-xx ID."""
        for ref in self.reference_index:
            if ref.ref_id == ref_id:
                return ref
        return None

    def get_references_by_category(self, category: str) -> list[ReferenceEntry]:
        """Get all references in a category (e.g. 'HOME_AFFAIRS')."""
        return [r for r in self.reference_index if r.category == category]

    def get_all_ref_ids(self) -> list[str]:
        """Get all REF IDs in the index."""
        return [r.ref_id for r in self.reference_index]

    # -----------------------------------------------------------------
    # Domain validation
    # -----------------------------------------------------------------

    def is_authoritative_domain(self, domain: str) -> bool:
        """Check if a domain is in the authoritative government domain list."""
        domain_lower = domain.lower().strip()
        for domains in self.authoritative_domains.values():
            if domain_lower in domains:
                return True
        return False

    def get_domain_category(self, domain: str) -> str:
        """Get the regulatory category for an authoritative domain."""
        domain_lower = domain.lower().strip()
        for category, domains in self.authoritative_domains.items():
            if domain_lower in domains:
                return category
        return "UNKNOWN"

    # -----------------------------------------------------------------
    # Role boundary check
    # -----------------------------------------------------------------

    def check_role_boundary(self, task_description: str) -> dict[str, Any]:
        """
        Check if a task crosses from education consulting into
        immigration assistance (requires RMA/legal referral).
        """
        immigration_signals = [
            "visa application", "visa lodgement", "lodge visa",
            "immigration assistance", "migration advice",
            "sponsor", "nomination application", "skills assessment application",
            "points test submission", "visa appeal", "visa refusal",
            "ministerial intervention", "bridging visa",
        ]
        education_signals = [
            "course comparison", "aqf level", "cricos",
            "education pathway", "study options", "admission requirements",
            "entry requirements", "course structure", "university comparison",
            "document checklist",
        ]

        task_lower = task_description.lower()
        immigration_hits = [s for s in immigration_signals if s in task_lower]
        education_hits = [s for s in education_signals if s in task_lower]

        requires_rma = len(immigration_hits) > 0
        return {
            "task": task_description,
            "role_allowed": RoleType.EDUCATION_CONSULTANT.value if not requires_rma else RoleType.RMA.value,
            "requires_rma_referral": requires_rma,
            "immigration_signals": immigration_hits,
            "education_signals": education_hits,
            "recommendation": (
                "Refer to RMA/legal practitioner for immigration assistance."
                if requires_rma
                else "Within education consultant scope."
            ),
        }

    # -----------------------------------------------------------------
    # Visa taxonomy
    # -----------------------------------------------------------------

    def get_visa_study_rights(self, subclass: str) -> dict[str, Any]:
        """Get study rights summary for a visa subclass (COS-05)."""
        visa_info = {
            "500": {
                "name": "Student Visa (Subclass 500)",
                "study_allowed": True,
                "study_limit": "Full-time study required (enrolled course)",
                "work_rights": "Limited (conditions apply)",
                "degree_pathway": True,
                "ref": "REF-HA-500",
            },
            "600": {
                "name": "Visitor Visa (Subclass 600)",
                "study_allowed": True,
                "study_limit": "Up to 3 months only",
                "work_rights": "No standard work rights",
                "degree_pathway": False,
                "ref": "REF-HA-600",
            },
        }
        info = visa_info.get(subclass)
        if info:
            return info
        return {
            "name": f"Subclass {subclass}",
            "study_allowed": "Check official page",
            "ref": "REF-HA-CONDITIONS",
        }

    # -----------------------------------------------------------------
    # Safety gate (COS-14)
    # -----------------------------------------------------------------

    def run_safety_gate(self, checks_completed: dict[str, bool]) -> SafetyGateResult:
        """
        Run the pre-use safety gate (COS-14).

        All checks must pass before giving advice.
        """
        result = SafetyGateResult()
        result.checks = {}
        result.missing = []

        for check in self.safety_gate_checks:
            passed = checks_completed.get(check, False)
            result.checks[check] = passed
            if not passed:
                result.missing.append(check)

        result.all_passed = len(result.missing) == 0
        return result

    # -----------------------------------------------------------------
    # Traceability
    # -----------------------------------------------------------------

    def add_claim(self, claim: TraceabilityClaim) -> None:
        """Add a traceable claim to the register."""
        self.claims.append(claim)

    def get_claims_by_confidence(self, confidence: Confidence) -> list[TraceabilityClaim]:
        """Get all claims at a given confidence level."""
        return [c for c in self.claims if c.confidence == confidence]

    def get_high_impact_claims(self) -> list[TraceabilityClaim]:
        """Get claims where impact-if-wrong is HIGH."""
        return [c for c in self.claims if c.impact_if_wrong == Impact.HIGH]

    # -----------------------------------------------------------------
    # Engagement records
    # -----------------------------------------------------------------

    def create_engagement(
        self,
        engagement_id: str,
        date_time: str,
        source_list: list[str] | None = None,
        client_consent: bool = False,
    ) -> EngagementRecord:
        """Create a new engagement record (COS-00 requirement)."""
        record = EngagementRecord(
            engagement_id=engagement_id,
            date_time=date_time,
            source_list=source_list or [],
            client_consent=client_consent,
        )
        self.engagements.append(record)
        return record

    # -----------------------------------------------------------------
    # Pathway mapping (COS-08)
    # -----------------------------------------------------------------

    def create_pathway_option(
        self,
        label: str,
        course_cricos: str = "",
        aqf_level: int = 0,
        target_anzsco: str = "",
        assessing_authority: str = "",
        visa_options: list[str] | None = None,
    ) -> PathwayOption:
        """Create a pathway option for visa-course-occupation mapping."""
        option = PathwayOption(
            label=label,
            course_cricos=course_cricos,
            aqf_level=aqf_level,
            target_anzsco=target_anzsco,
            assessing_authority=assessing_authority,
            visa_options=visa_options or [],
        )
        # Auto-flag if any immigration signal present
        if any(v in ("189", "190", "491") for v in option.visa_options):
            option.requires_rma_referral = True
            option.risk_notes.append(
                "Skilled visa pathway: refer to RMA for immigration assistance."
            )
        return option

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------

    def get_cos_summary(self) -> dict[str, Any]:
        """Get a full summary of the COS framework state."""
        return {
            "version": "v3.1",
            "cos_sections": len(COSSection),
            "cos_layers": len(COSLayer),
            "reference_entries": len(self.reference_index),
            "authoritative_domain_categories": len(self.authoritative_domains),
            "code_of_conduct_entries": len(self.code_of_conduct),
            "safety_gate_checks": len(self.safety_gate_checks),
            "engagements_recorded": len(self.engagements),
            "claims_recorded": len(self.claims),
            "aqf_levels": len(AQFLevel),
            "states_territories": len(StateTerritory),
            "ref_categories": list(
                set(r.category for r in self.reference_index)
            ),
        }

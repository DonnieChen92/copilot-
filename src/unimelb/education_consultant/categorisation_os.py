"""
Education Consultant Categorisation_OS (COS) v3.1 — Extended Compliance
========================================================================
Design: Jiadong Chen (陈佳栋) — Student ID: 723912

Structured "Search -> Verify -> Advise -> Document" framework for
education-pathway planning in Australia. Uses ONLY public-domain,
official sources. Separates education consulting from regulated
migration assistance.

Based on:
- DOC-20260216-Education-Consultant-Manual-V3.1
- DOC-20260216-Education-Consultant-Manual-V3.1-Extended

COS Architecture — Operational Layers (L1–L8):
  L1 National (AU)
  L2 State/Territory (VIC/NSW/QLD/SA/WA/TAS/ACT/NT)
  L3 Institution Type (anonymised tiers)
  L4 Course Level (AQF) + Provider Registration (TEQSA/CRICOS)
  L5 Visa Pathway (Visitor vs Student vs Skilled etc.)
  L6 Occupation Mapping (ANZSCO / lists / assessing authority)
  L7 Risk & Compliance (policy volatility, integrity, consumer law)
  L8 Ethics, Non-Discrimination, Privacy, Cyber

COS Expanded Architecture — Process Layers (A–H):
  A Identity & Purpose Declaration
  B Legislative Alignment
  C Education Categorisation
  D Migration Categorisation
  E Risk & Compliance Review
  F Data Governance
  G Ethical & Equality Assurance
  H Documentation & Audit Trail
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


class COSExpandedLayer(Enum):
    """COS expanded architecture layers (A–H) from v3.1 Extended."""

    A_IDENTITY_PURPOSE = "Layer A"
    B_LEGISLATIVE_ALIGNMENT = "Layer B"
    C_EDUCATION_CATEGORISATION = "Layer C"
    D_MIGRATION_CATEGORISATION = "Layer D"
    E_RISK_COMPLIANCE = "Layer E"
    F_DATA_GOVERNANCE = "Layer F"
    G_ETHICAL_EQUALITY = "Layer G"
    H_DOCUMENTATION_AUDIT = "Layer H"


class OccupationRiskCategory(Enum):
    """Skilled occupation risk categories (quarterly monitoring)."""

    LOW = "Low"          # Stable occupation
    MODERATE = "Moderate"  # Policy-sensitive
    HIGH = "High"        # Short-term list volatility


class LegislativeCategory(Enum):
    """Legislative & regulatory alignment categories."""

    FEDERAL_EDUCATION = "Federal Education Governance"
    MIGRATION = "Migration Governance"
    PRIVACY_DATA = "Privacy & Data Protection"
    CYBER_SECURITY = "Cyber Security"
    ANTI_DISCRIMINATION = "Anti-Discrimination & Equality"


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
class LegislativeEntry:
    """A legislative or regulatory instrument in the alignment matrix."""

    name: str
    category: LegislativeCategory
    short_ref: str = ""
    description: str = ""


@dataclass
class ProtectedAttribute:
    """A protected attribute under the equality charter."""

    attribute: str
    description: str = ""


@dataclass
class DataGovernanceControl:
    """Data governance control entry (Extended v3.1 Section 6)."""

    stage: DataLifecycleStage
    principles: list[str] = field(default_factory=list)


@dataclass
class AuditTrailEntry:
    """Documentation & audit trail record (Extended v3.1 Section 10)."""

    record_type: str
    description: str = ""
    required: bool = True


@dataclass
class HigherEdChecklistItem:
    """Higher education governance checklist item (Section 3)."""

    check: str
    verified: bool = False


@dataclass
class ProhibitedConductEntry:
    """Prohibited conduct entry (Extended v3.1 Section 7)."""

    conduct: str
    severity: str = "Critical"


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
# Extended Compliance v3.1 — Structured Data
# =============================================================================

# COS Expanded Architecture operational loop
COS_OPERATIONAL_LOOP: list[str] = [
    "Identify",
    "Categorise",
    "Verify Legislation",
    "Evaluate Risk",
    "Document",
    "Review",
    "Disclose",
]

# Legislative & Regulatory Alignment Matrix (Extended v3.1 Section 1)
LEGISLATIVE_ALIGNMENT_MATRIX: list[LegislativeEntry] = [
    # Federal Education Governance
    LegislativeEntry("Education Services for Overseas Students Act 2000", LegislativeCategory.FEDERAL_EDUCATION, "ESOS Act 2000", "ESOS framework for overseas student protection"),
    LegislativeEntry("Higher Education Standards Framework", LegislativeCategory.FEDERAL_EDUCATION, "HESF", "Threshold standards for higher education"),
    LegislativeEntry("Australian Qualifications Framework", LegislativeCategory.FEDERAL_EDUCATION, "AQF", "National framework of qualifications levels 1-10"),
    # Migration Governance
    LegislativeEntry("Migration Act 1958 (Cth)", LegislativeCategory.MIGRATION, "Migration Act", "Primary migration legislation"),
    LegislativeEntry("Migration Regulations 1994 (Cth)", LegislativeCategory.MIGRATION, "Migration Regs", "Regulations under Migration Act"),
    LegislativeEntry("Skilled Migration Program Settings", LegislativeCategory.MIGRATION, "Skilled Program", "Annual program settings for skilled migration"),
    LegislativeEntry("Student Visa (Subclass 500)", LegislativeCategory.MIGRATION, "Subclass 500", "Student visa for full-time study"),
    LegislativeEntry("Visitor Visa (Subclass 600)", LegislativeCategory.MIGRATION, "Subclass 600", "Visitor visa with limited study rights"),
    # Privacy & Data Protection
    LegislativeEntry("Privacy Act 1988 (Cth)", LegislativeCategory.PRIVACY_DATA, "Privacy Act", "Federal privacy legislation"),
    LegislativeEntry("Australian Privacy Principles (APP 1-13)", LegislativeCategory.PRIVACY_DATA, "APPs", "13 privacy principles under Privacy Act"),
    LegislativeEntry("Notifiable Data Breaches Scheme", LegislativeCategory.PRIVACY_DATA, "NDB", "Mandatory breach notification scheme"),
    # Cyber Security
    LegislativeEntry("Essential Eight", LegislativeCategory.CYBER_SECURITY, "E8", "ACSC baseline cyber security strategies"),
    LegislativeEntry("Australian Cyber Security Centre Guidance", LegislativeCategory.CYBER_SECURITY, "ACSC", "National cyber security guidance"),
    # Anti-Discrimination & Equality
    LegislativeEntry("Racial Discrimination Act 1975", LegislativeCategory.ANTI_DISCRIMINATION, "RDA 1975", "Prohibits racial discrimination"),
    LegislativeEntry("Sex Discrimination Act 1984", LegislativeCategory.ANTI_DISCRIMINATION, "SDA 1984", "Prohibits sex discrimination"),
    LegislativeEntry("Disability Discrimination Act 1992", LegislativeCategory.ANTI_DISCRIMINATION, "DDA 1992", "Prohibits disability discrimination"),
    LegislativeEntry("Age Discrimination Act 2004", LegislativeCategory.ANTI_DISCRIMINATION, "ADA 2004", "Prohibits age discrimination"),
    LegislativeEntry("Fair Work Act 2009", LegislativeCategory.ANTI_DISCRIMINATION, "FW Act", "Workplace relations and anti-discrimination"),
]

# Higher Education Governance Checklist (Extended v3.1 Section 3)
HIGHER_ED_GOVERNANCE_CHECKLIST: list[HigherEdChecklistItem] = [
    HigherEdChecklistItem("TEQSA registration confirmed"),
    HigherEdChecklistItem("CRICOS listing confirmed"),
    HigherEdChecklistItem("AQF level validated"),
    HigherEdChecklistItem("Course duration verified"),
    HigherEdChecklistItem("Graduate outcome data reviewed"),
]

# Academic Integrity Alignment (Extended v3.1 Section 3)
ACADEMIC_INTEGRITY_RULES: list[str] = [
    "No falsified transcripts",
    "No fabricated experience",
    "No misleading marketing",
]

# Equality, Cultural Respect & Non-Discrimination Charter (Extended v3.1 Section 8)
EQUALITY_CHARTER_PRINCIPLE: str = (
    "Every individual has equal dignity and protection under Australian law."
)

PROTECTED_ATTRIBUTES: list[ProtectedAttribute] = [
    ProtectedAttribute("Gender", "No discrimination based on gender identity"),
    ProtectedAttribute("Age", "No discrimination based on age"),
    ProtectedAttribute("Skin colour", "No discrimination based on skin colour or ethnicity"),
    ProtectedAttribute("Sexual orientation", "No discrimination based on sexual orientation"),
    ProtectedAttribute("Disability", "No discrimination based on disability"),
    ProtectedAttribute("Religion or no religion", "No discrimination based on religious belief or lack thereof"),
    ProtectedAttribute("Job status", "No discrimination based on employment or unemployment status"),
    ProtectedAttribute("Residency or passport", "No discrimination based on residency status or nationality"),
    ProtectedAttribute("Appearance", "No discrimination based on physical appearance"),
    ProtectedAttribute("Clothing", "No discrimination based on traditional or modern clothing"),
    ProtectedAttribute("Communication style", "No discrimination based on loud or quiet communication"),
    ProtectedAttribute("Punctuality differences", "No discrimination based on punctuality variations"),
    ProtectedAttribute("Cultural expression", "No discrimination based on cultural expression"),
    ProtectedAttribute("Personal background", "No discrimination based on personal history"),
    ProtectedAttribute("Past failure or setbacks", "No discrimination based on past failures"),
]

EQUALITY_RESPECT_VALUES: list[str] = [
    "Indigenous heritage of Australia",
    "Multicultural society",
    "Freedom of belief",
    "Equal opportunity principles",
]

ADVISORY_NEUTRALITY: str = (
    "Advice must not be influenced by personal bias or social status."
)

# Data Governance Controls (Extended v3.1 Section 6)
DATA_GOVERNANCE_CONTROLS: list[DataGovernanceControl] = [
    DataGovernanceControl(
        DataLifecycleStage.COLLECT,
        [
            "Only data necessary for advisory purpose",
            "Informed consent documented",
            "Purpose clearly stated",
        ],
    ),
    DataGovernanceControl(
        DataLifecycleStage.PROCESS,
        [
            "Used solely for assessment & documentation",
            "No secondary use without consent",
            "No data sale or transfer",
        ],
    ),
    DataGovernanceControl(
        DataLifecycleStage.STORE,
        [
            "Encrypted digital storage",
            "Restricted access controls",
            "Multi-factor authentication",
        ],
    ),
    DataGovernanceControl(
        DataLifecycleStage.RETAIN,
        [
            "Stored only as long as required",
            "Secure deletion after retention period",
        ],
    ),
]

# Categories of data collected (Extended v3.1 Section 6)
DATA_CATEGORIES: list[str] = [
    "Identification data",
    "Academic records",
    "English test results",
    "Employment history",
    "Visa history",
]

# Breach response steps (Extended v3.1 Section 6)
BREACH_RESPONSE_STEPS: list[str] = [
    "Immediate containment",
    "Assessment of impact",
    "Notification under NDB scheme if required",
]

# Prohibited Conduct (Extended v3.1 Section 7)
PROHIBITED_CONDUCT: list[ProhibitedConductEntry] = [
    ProhibitedConductEntry("False documentation", "Critical"),
    ProhibitedConductEntry("Omission of critical information", "Critical"),
    ProhibitedConductEntry("Exploitation of language barriers", "Critical"),
    ProhibitedConductEntry("Cultural stereotyping", "Critical"),
    ProhibitedConductEntry("Prejudice or bias in advice", "Critical"),
]

# Professional Knowledge Requirements (Extended v3.1 Section 7)
PROFESSIONAL_KNOWLEDGE_REQUIREMENTS: list[str] = [
    "Understanding of Migration Act & Regulations",
    "Familiarity with AQF & ESOS",
    "Ability to interpret ANZSCO",
    "Awareness of anti-discrimination law",
    "Cyber security awareness",
]

# Conduct Standards (Extended v3.1 Section 7)
CONDUCT_STANDARDS: list[str] = [
    "No misleading statements",
    "No outcome guarantees",
    "No discrimination",
    "No coercion or pressure",
    "Full disclosure of material facts",
    "Transparent fee structure",
]

# Skilled Occupation Quarterly Monitoring (Extended v3.1 Section 5)
QUARTERLY_MONITORING_ITEMS: list[str] = [
    "Federal occupation list updates",
    "State nomination changes",
    "English requirement updates",
    "Labour market trends",
]

# Documentation & Audit Trail (Extended v3.1 Section 10)
REQUIRED_DOCUMENTATION: list[AuditTrailEntry] = [
    AuditTrailEntry("Client intake record", "Initial client information capture"),
    AuditTrailEntry("Risk assessment sheet", "Client-specific risk evaluation"),
    AuditTrailEntry("Occupation mapping record", "ANZSCO and occupation alignment"),
    AuditTrailEntry("Visa compliance checklist", "Visa pathway compliance verification"),
    AuditTrailEntry("Disclosure acknowledgement", "Client acknowledgement of disclosures"),
]

AUDIT_TRAIL_REQUIREMENTS: list[AuditTrailEntry] = [
    AuditTrailEntry("Date of advice", "When the advice was given"),
    AuditTrailEntry("Legislative version referenced", "Which version of legislation was used"),
    AuditTrailEntry("Source website cited", "Official website URL referenced"),
    AuditTrailEntry("Update log maintained", "Record of updates to advice"),
]

# Extended Safety / Liability Checklist (Extended v3.1 Section 9)
EXTENDED_PRE_USE_CHECKLIST: list[str] = [
    "Confirm latest legislation from official sites",
    "Confirm migration planning levels",
    "Confirm privacy consent signed",
    "Confirm risk disclosure provided",
    "Confirm no guarantee implied",
    "Confirm documentation accuracy",
    "Confirm cultural respect standard applied",
]

LIABILITY_NOTICE: str = (
    "Advice based on publicly available information. "
    "Legislation may change without notice. "
    "Final responsibility rests with applicant for application accuracy."
)

# Visa compliance expansion details (Extended v3.1 Section 4)
STUDENT_500_COMPLIANCE: list[str] = [
    "Genuine Student requirement verified",
    "Financial capacity documented",
    "English evidence valid",
    "OSHC confirmed",
]

VISITOR_600_COMPLIANCE: list[str] = [
    "Short study compliance",
    "No employment activity",
]

SKILLED_MIGRATION_COMPLIANCE: list[str] = [
    "ANZSCO code validated",
    "Skills assessment authority identified",
    "Occupation list confirmed current",
    "Points test recalculated before submission",
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

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Equality Charter
    # -----------------------------------------------------------------

    def get_protected_attributes(self) -> list[ProtectedAttribute]:
        """Get all protected attributes from the equality charter."""
        return PROTECTED_ATTRIBUTES

    def get_protected_attribute_names(self) -> list[str]:
        """Get just the names of all protected attributes."""
        return [p.attribute for p in PROTECTED_ATTRIBUTES]

    def check_equality_compliance(self, description: str) -> dict[str, Any]:
        """
        Check a description for potential equality/discrimination issues.

        Flags if any protected attribute category keyword appears
        in a potentially discriminatory context.
        """
        discriminatory_signals = [
            "refuse", "reject", "deny", "exclude", "discriminate",
            "not suitable", "unsuitable", "too old", "too young",
            "wrong colour", "wrong religion", "not welcome",
        ]

        desc_lower = description.lower()
        attribute_mentions = [
            p.attribute for p in PROTECTED_ATTRIBUTES
            if p.attribute.lower() in desc_lower
        ]
        disc_signals = [s for s in discriminatory_signals if s in desc_lower]

        flagged = len(disc_signals) > 0 and len(attribute_mentions) > 0

        return {
            "description": description,
            "attribute_mentions": attribute_mentions,
            "discriminatory_signals": disc_signals,
            "flagged": flagged,
            "charter_principle": EQUALITY_CHARTER_PRINCIPLE,
            "advisory_neutrality": ADVISORY_NEUTRALITY,
        }

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Legislative Alignment
    # -----------------------------------------------------------------

    def get_legislative_matrix(self) -> list[LegislativeEntry]:
        """Get the full legislative alignment matrix."""
        return LEGISLATIVE_ALIGNMENT_MATRIX

    def get_legislation_by_category(
        self, category: LegislativeCategory
    ) -> list[LegislativeEntry]:
        """Get legislation filtered by regulatory category."""
        return [
            entry for entry in LEGISLATIVE_ALIGNMENT_MATRIX
            if entry.category == category
        ]

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Data Governance
    # -----------------------------------------------------------------

    def get_data_governance_controls(self) -> list[DataGovernanceControl]:
        """Get data governance controls by lifecycle stage."""
        return DATA_GOVERNANCE_CONTROLS

    def get_data_categories(self) -> list[str]:
        """Get the categories of data collected."""
        return DATA_CATEGORIES

    def get_breach_response_steps(self) -> list[str]:
        """Get breach response steps."""
        return BREACH_RESPONSE_STEPS

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Prohibited Conduct
    # -----------------------------------------------------------------

    def get_prohibited_conduct(self) -> list[ProhibitedConductEntry]:
        """Get all prohibited conduct entries."""
        return PROHIBITED_CONDUCT

    def get_conduct_standards(self) -> list[str]:
        """Get conduct standard rules."""
        return CONDUCT_STANDARDS

    def get_professional_requirements(self) -> list[str]:
        """Get professional knowledge requirements."""
        return PROFESSIONAL_KNOWLEDGE_REQUIREMENTS

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Higher Ed Governance
    # -----------------------------------------------------------------

    def run_higher_ed_checklist(
        self, checks: dict[str, bool]
    ) -> dict[str, Any]:
        """
        Run the higher education governance checklist.

        Returns pass/fail for each item and overall status.
        """
        results: list[dict[str, Any]] = []
        for item in HIGHER_ED_GOVERNANCE_CHECKLIST:
            passed = checks.get(item.check, False)
            results.append({"check": item.check, "passed": passed})

        all_passed = all(r["passed"] for r in results)
        missing = [r["check"] for r in results if not r["passed"]]

        return {
            "checklist": results,
            "all_passed": all_passed,
            "missing": missing,
            "academic_integrity_rules": ACADEMIC_INTEGRITY_RULES,
        }

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Occupation Risk & Monitoring
    # -----------------------------------------------------------------

    def classify_occupation_risk(
        self, volatility: str
    ) -> OccupationRiskCategory:
        """Classify an occupation's risk based on volatility description."""
        low_signals = ["stable", "established", "consistent", "secure"]
        high_signals = ["volatile", "short-term", "uncertain", "removed", "delisted"]

        vol_lower = volatility.lower()
        if any(s in vol_lower for s in high_signals):
            return OccupationRiskCategory.HIGH
        if any(s in vol_lower for s in low_signals):
            return OccupationRiskCategory.LOW
        return OccupationRiskCategory.MODERATE

    def get_quarterly_monitoring_items(self) -> list[str]:
        """Get skilled occupation quarterly monitoring items."""
        return QUARTERLY_MONITORING_ITEMS

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Audit Trail
    # -----------------------------------------------------------------

    def get_required_documentation(self) -> list[AuditTrailEntry]:
        """Get required documentation list."""
        return REQUIRED_DOCUMENTATION

    def get_audit_trail_requirements(self) -> list[AuditTrailEntry]:
        """Get audit trail requirements."""
        return AUDIT_TRAIL_REQUIREMENTS

    # -----------------------------------------------------------------
    # Extended Compliance v3.1 — Visa Compliance Expansion
    # -----------------------------------------------------------------

    def get_visa_compliance_checks(self, subclass: str) -> list[str]:
        """Get compliance checks for a given visa subclass."""
        if subclass == "500":
            return STUDENT_500_COMPLIANCE
        elif subclass == "600":
            return VISITOR_600_COMPLIANCE
        elif subclass in ("189", "190", "491"):
            return SKILLED_MIGRATION_COMPLIANCE
        return []

    # -----------------------------------------------------------------
    # Extended Safety / Liability
    # -----------------------------------------------------------------

    def run_extended_pre_use_checklist(
        self, completed: dict[str, bool]
    ) -> dict[str, Any]:
        """Run the extended pre-use safety/liability checklist."""
        results = {}
        missing = []
        for item in EXTENDED_PRE_USE_CHECKLIST:
            passed = completed.get(item, False)
            results[item] = passed
            if not passed:
                missing.append(item)

        return {
            "all_passed": len(missing) == 0,
            "checks": results,
            "missing": missing,
            "liability_notice": LIABILITY_NOTICE,
        }

    # -----------------------------------------------------------------
    # Summary (updated)
    # -----------------------------------------------------------------

    def get_cos_summary(self) -> dict[str, Any]:
        """Get a full summary of the COS framework state."""
        return {
            "version": "v3.1",
            "edition": "Extended Compliance",
            "cos_sections": len(COSSection),
            "cos_layers": len(COSLayer),
            "cos_expanded_layers": len(COSExpandedLayer),
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
            "legislative_entries": len(LEGISLATIVE_ALIGNMENT_MATRIX),
            "protected_attributes": len(PROTECTED_ATTRIBUTES),
            "prohibited_conduct_entries": len(PROHIBITED_CONDUCT),
            "data_governance_controls": len(DATA_GOVERNANCE_CONTROLS),
            "required_documentation": len(REQUIRED_DOCUMENTATION),
            "extended_pre_use_checks": len(EXTENDED_PRE_USE_CHECKLIST),
        }


# =============================================================================
# Education Search Architecture — VIC Master Level
# =============================================================================

class InstitutionProfile(Enum):
    """Anonymised institution profile tiers."""

    GROUP_OF_EIGHT = "Group of Eight profile"
    INDUSTRY_INTEGRATED = "Industry-integrated profile"
    QUANTITATIVE_EMPHASIS = "Quantitative emphasis profile"


class AcademicCluster(Enum):
    """Melbourne metropolitan academic clusters."""

    CBD = "CBD Academic Cluster"
    INNER_SUBURBAN = "Inner Suburban Academic Cluster"
    OUTER_METROPOLITAN = "Outer Metropolitan Academic Cluster"


class SearchStep(Enum):
    """Education consultant 4-step search flow."""

    GEOGRAPHIC_FILTERING = "Step 1: Geographic Filtering"
    INSTITUTION_BENCHMARKING = "Step 2: Institution Benchmarking"
    SUBJECT_EVALUATION = "Step 3: Subject Evaluation"
    STUDENT_FIT_ASSESSMENT = "Step 4: Student Fit Assessment"


@dataclass
class InstitutionEntry:
    """An anonymised institution in the search architecture."""

    label: str                          # e.g. "University A"
    profile: InstitutionProfile
    cluster: AcademicCluster
    faculties: list[str] = field(default_factory=list)
    disciplines: list[str] = field(default_factory=list)
    aqf_level: int = 9                  # default: Masters


@dataclass
class SubjectLayer:
    """Generic master subject template structure."""

    academic_foundation: list[str] = field(default_factory=list)
    analytical_layer: list[str] = field(default_factory=list)
    applied_business_context: list[str] = field(default_factory=list)
    integration_layer: list[str] = field(default_factory=list)


@dataclass
class SearchStepResult:
    """Result of a single search step evaluation."""

    step: str
    criteria: list[str] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    score: str = ""   # HIGH / MEDIUM / LOW alignment


@dataclass
class SearchArchitectureResult:
    """Full search architecture evaluation output."""

    institution_label: str = ""
    geographic_result: SearchStepResult | None = None
    benchmarking_result: SearchStepResult | None = None
    subject_result: SearchStepResult | None = None
    fit_result: SearchStepResult | None = None
    overall_alignment: str = ""   # HIGH / MEDIUM / LOW
    recommendation: str = ""


# Default institution registry (anonymised per Section 2)
INSTITUTION_REGISTRY: list[InstitutionEntry] = [
    InstitutionEntry(
        label="University A",
        profile=InstitutionProfile.GROUP_OF_EIGHT,
        cluster=AcademicCluster.CBD,
        faculties=["Business & Economics Faculty"],
        disciplines=["Data / Analytics Discipline", "Strategy & Management Discipline"],
        aqf_level=9,
    ),
    InstitutionEntry(
        label="University B",
        profile=InstitutionProfile.INDUSTRY_INTEGRATED,
        cluster=AcademicCluster.INNER_SUBURBAN,
        faculties=["Business & Law College"],
        disciplines=["Applied Analytics Stream", "Innovation & Enterprise Stream"],
        aqf_level=9,
    ),
    InstitutionEntry(
        label="University C",
        profile=InstitutionProfile.QUANTITATIVE_EMPHASIS,
        cluster=AcademicCluster.CBD,
        faculties=["Business School"],
        disciplines=["Advanced Quantitative Methods", "Global Strategy Focus"],
        aqf_level=9,
    ),
]

# Default subject template (Section 3)
DEFAULT_SUBJECT_TEMPLATE = SubjectLayer(
    academic_foundation=[
        "Theoretical Frameworks",
        "Conceptual Models",
        "Literature Integration",
    ],
    analytical_layer=[
        "Data Interpretation",
        "Statistical / Decision Models",
        "Risk & Scenario Evaluation",
    ],
    applied_business_context=[
        "Case Study Analysis",
        "Organisational Evaluation",
        "Strategic Trade-offs",
    ],
    integration_layer=[
        "Cross-topic Synthesis",
        "Professional Recommendation",
        "Ethical & Governance Consideration",
    ],
)

# Search step criteria definitions (Section 4)
SEARCH_STEP_CRITERIA: dict[str, list[str]] = {
    "geographic_filtering": [
        "State Policy (VIC)",
        "Visa / Migration Relevance",
        "Employment Outlook Alignment",
    ],
    "institution_benchmarking": [
        "Ranking & Reputation",
        "Industry Linkage",
        "Graduate Outcomes",
        "AQF Compliance",
    ],
    "subject_evaluation": [
        "Assessment Structure",
        "Skill Development Outcome",
        "Quantitative vs Strategic Balance",
        "Research Pathway Compatibility",
    ],
    "student_fit_assessment": [
        "Academic Background Match",
        "Career Objective Fit",
        "Financial & Timeline Planning",
        "Risk Scenario Planning",
    ],
}

# Professional development path (Section 5)
PROFESSIONAL_DEVELOPMENT_PATH: list[str] = [
    "Academic Depth Enhancement",
    "Analytical Capability Upgrade",
    "Communication & Presentation Standard",
    "Cross-institution Benchmark Awareness",
    "Reputation & Ethical Governance Awareness",
]


class EducationSearchArchitecture:
    """
    Education Search Architecture — VIC Master Level.

    Implements the structured search flow:
    Identify -> Compare -> Verify -> Align -> Recommend -> Document

    Four-step evaluation:
    1. Geographic Filtering
    2. Institution Benchmarking
    3. Subject Evaluation
    4. Student Fit Assessment
    """

    def __init__(self) -> None:
        self.institutions = INSTITUTION_REGISTRY
        self.subject_template = DEFAULT_SUBJECT_TEMPLATE
        self.search_criteria = SEARCH_STEP_CRITERIA
        self.professional_dev_path = PROFESSIONAL_DEVELOPMENT_PATH

    # -----------------------------------------------------------------
    # Institution registry
    # -----------------------------------------------------------------

    def get_institution(self, label: str) -> InstitutionEntry | None:
        """Get an institution by its anonymised label."""
        for inst in self.institutions:
            if inst.label == label:
                return inst
        return None

    def get_institutions_by_profile(
        self, profile: InstitutionProfile
    ) -> list[InstitutionEntry]:
        """Get all institutions with a given profile type."""
        return [i for i in self.institutions if i.profile == profile]

    def get_institutions_by_cluster(
        self, cluster: AcademicCluster
    ) -> list[InstitutionEntry]:
        """Get all institutions in an academic cluster."""
        return [i for i in self.institutions if i.cluster == cluster]

    def get_institutions_by_aqf(self, aqf_level: int) -> list[InstitutionEntry]:
        """Get all institutions offering a specific AQF level."""
        return [i for i in self.institutions if i.aqf_level == aqf_level]

    # -----------------------------------------------------------------
    # Subject template
    # -----------------------------------------------------------------

    def get_subject_layer_names(self) -> list[str]:
        """Get the four subject layer names."""
        return [
            "Academic Foundation",
            "Analytical Layer",
            "Applied Business Context",
            "Integration Layer",
        ]

    def get_subject_components(self) -> dict[str, list[str]]:
        """Get all subject template components by layer."""
        return {
            "Academic Foundation": self.subject_template.academic_foundation,
            "Analytical Layer": self.subject_template.analytical_layer,
            "Applied Business Context": self.subject_template.applied_business_context,
            "Integration Layer": self.subject_template.integration_layer,
        }

    def count_subject_components(self) -> int:
        """Count total subject components across all layers."""
        components = self.get_subject_components()
        return sum(len(v) for v in components.values())

    # -----------------------------------------------------------------
    # 4-step search flow
    # -----------------------------------------------------------------

    def evaluate_geographic(
        self, state: str = "VIC", findings: list[str] | None = None
    ) -> SearchStepResult:
        """Step 1: Geographic Filtering."""
        return SearchStepResult(
            step=SearchStep.GEOGRAPHIC_FILTERING.value,
            criteria=self.search_criteria["geographic_filtering"],
            findings=findings or [],
            score="HIGH" if state == "VIC" else "MEDIUM",
        )

    def evaluate_institution(
        self, institution_label: str, findings: list[str] | None = None
    ) -> SearchStepResult:
        """Step 2: Institution Benchmarking."""
        inst = self.get_institution(institution_label)
        score = "LOW"
        if inst:
            if inst.profile == InstitutionProfile.GROUP_OF_EIGHT:
                score = "HIGH"
            elif inst.profile == InstitutionProfile.INDUSTRY_INTEGRATED:
                score = "HIGH"
            else:
                score = "MEDIUM"

        return SearchStepResult(
            step=SearchStep.INSTITUTION_BENCHMARKING.value,
            criteria=self.search_criteria["institution_benchmarking"],
            findings=findings or [],
            score=score,
        )

    def evaluate_subject(
        self, findings: list[str] | None = None
    ) -> SearchStepResult:
        """Step 3: Subject Evaluation."""
        return SearchStepResult(
            step=SearchStep.SUBJECT_EVALUATION.value,
            criteria=self.search_criteria["subject_evaluation"],
            findings=findings or [],
        )

    def evaluate_student_fit(
        self, findings: list[str] | None = None
    ) -> SearchStepResult:
        """Step 4: Student Fit Assessment."""
        return SearchStepResult(
            step=SearchStep.STUDENT_FIT_ASSESSMENT.value,
            criteria=self.search_criteria["student_fit_assessment"],
            findings=findings or [],
        )

    def run_full_search(
        self,
        institution_label: str,
        state: str = "VIC",
        geo_findings: list[str] | None = None,
        bench_findings: list[str] | None = None,
        subject_findings: list[str] | None = None,
        fit_findings: list[str] | None = None,
    ) -> SearchArchitectureResult:
        """
        Run the full 4-step search architecture evaluation.

        Identify -> Compare -> Verify -> Align -> Recommend -> Document
        """
        geo = self.evaluate_geographic(state, geo_findings)
        bench = self.evaluate_institution(institution_label, bench_findings)
        subj = self.evaluate_subject(subject_findings)
        fit = self.evaluate_student_fit(fit_findings)

        # Derive overall alignment from step scores
        scores = [geo.score, bench.score, subj.score, fit.score]
        high_count = scores.count("HIGH")
        low_count = scores.count("LOW")

        if high_count >= 3:
            overall = "HIGH"
        elif low_count >= 2:
            overall = "LOW"
        else:
            overall = "MEDIUM"

        inst = self.get_institution(institution_label)
        recommendation = ""
        if inst and overall == "HIGH":
            recommendation = (
                f"{inst.label} ({inst.profile.value}) shows strong alignment "
                f"across geographic, institutional, subject, and student fit criteria."
            )
        elif inst and overall == "MEDIUM":
            recommendation = (
                f"{inst.label} ({inst.profile.value}) shows moderate alignment; "
                f"review subject and student fit criteria for closer match."
            )
        else:
            recommendation = (
                "Further evaluation needed; consider broadening institution set."
            )

        return SearchArchitectureResult(
            institution_label=institution_label,
            geographic_result=geo,
            benchmarking_result=bench,
            subject_result=subj,
            fit_result=fit,
            overall_alignment=overall,
            recommendation=recommendation,
        )

    def get_search_summary(self) -> dict[str, Any]:
        """Get a summary of the search architecture framework."""
        return {
            "institutions": len(self.institutions),
            "profiles": list(set(i.profile.value for i in self.institutions)),
            "clusters": list(set(i.cluster.value for i in self.institutions)),
            "search_steps": len(self.search_criteria),
            "total_criteria": sum(
                len(v) for v in self.search_criteria.values()
            ),
            "subject_layers": len(self.get_subject_layer_names()),
            "subject_components": self.count_subject_components(),
            "professional_dev_items": len(self.professional_dev_path),
        }

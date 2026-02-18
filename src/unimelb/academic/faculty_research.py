"""
Academic Faculty Research Support Module
==========================================
AI-powered research support for UniMelb faculties.

Priority faculties:
- Melbourne Law School — legal research, case analysis, legislation lookup
- Engineering — simulation, CAD assistance, research paper analysis
- Computing & IT (FEIT) — code generation, security research, ML/DL training
- Melbourne Business School — market analysis, financial modelling
- Arts & Humanities — translation, archival research, digital humanities
- Medicine — clinical research, literature review

Also supports human and social harmony research subjects.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Faculty(Enum):
    """UniMelb faculties with AI research support."""

    LAW = "melbourne_law_school"
    ENGINEERING = "engineering"
    COMPUTING_IT = "computing_and_information_technology"
    BUSINESS = "melbourne_business_school"
    ARTS = "arts_and_humanities"
    MEDICINE = "medicine_dentistry_health_sciences"
    SCIENCE = "science"
    EDUCATION = "education"
    ARCHITECTURE = "architecture_building_planning"
    FINE_ARTS = "fine_arts_and_music"
    VETERINARY = "veterinary_and_agricultural_sciences"


class ResearchDomain(Enum):
    """Research domain categories."""

    LEGAL_RESEARCH = "legal_research"
    ENGINEERING_SIMULATION = "engineering_simulation"
    CODE_GENERATION = "code_generation"
    SECURITY_RESEARCH = "security_research"
    ML_DL_TRAINING = "ml_dl_training"
    MARKET_ANALYSIS = "market_analysis"
    FINANCIAL_MODELLING = "financial_modelling"
    LITERATURE_REVIEW = "literature_review"
    TRANSLATION = "translation"
    DIGITAL_HUMANITIES = "digital_humanities"
    CLINICAL_RESEARCH = "clinical_research"
    SOCIAL_HARMONY = "social_harmony"
    MENTAL_HEALTH_RESEARCH = "mental_health_research"
    CULTURAL_DIVERSITY = "cultural_diversity"
    STUDENT_WELLBEING = "student_wellbeing"


class VerificationLevel(Enum):
    """Verification level required for research queries."""

    STANDARD = "standard"               # Normal anti-hallucination
    ENHANCED = "enhanced"               # Multi-model + source citation required
    LEGAL_GRADE = "legal_grade"         # AustLII + legislation DB verification
    CLINICAL_GRADE = "clinical_grade"   # PubMed + clinical guidelines check
    CRITICAL = "critical"               # Human expert review mandatory


@dataclass
class ResearchProject:
    """A faculty research project using the AI platform."""

    project_id: str
    title: str
    faculty: Faculty
    domain: ResearchDomain
    principal_investigator: str
    team_members: list[str] = field(default_factory=list)
    description: str = ""
    ai_models_approved: list[str] = field(default_factory=list)
    verification_level: VerificationLevel = VerificationLevel.ENHANCED
    data_classification: str = "internal"  # public | internal | confidential | restricted
    ethics_approval: str = ""  # Ethics approval number
    funding_source: str = ""
    active: bool = True


@dataclass
class ResearchQuery:
    """A research query submitted to the AI platform."""

    query_id: str
    project_id: str
    faculty: Faculty
    domain: ResearchDomain
    query: str
    context: str = ""
    preferred_model: str = ""
    verification_level: VerificationLevel = VerificationLevel.ENHANCED
    sources_required: bool = True
    legislation_check: bool = False
    elibrary_check: bool = False


# Faculty → AI model preferences
FACULTY_MODEL_PREFERENCES: dict[Faculty, dict[str, Any]] = {
    Faculty.LAW: {
        "primary_model": "claude-opus-4-6",
        "reason": "Best for nuanced legal reasoning and careful analysis",
        "verification_level": VerificationLevel.LEGAL_GRADE,
        "auto_check": ["austlii", "legislation_database", "case_law"],
        "special_requirements": [
            "Citation accuracy is critical",
            "Must distinguish between jurisdictions (Cth, Vic, NSW, etc.)",
            "Never present obiter dicta as ratio decidendi",
        ],
    },
    Faculty.ENGINEERING: {
        "primary_model": "gpt-4o",
        "reason": "Strong on technical/mathematical reasoning",
        "verification_level": VerificationLevel.ENHANCED,
        "auto_check": ["ieee_xplore", "engineering_standards"],
        "special_requirements": [
            "Numerical accuracy is critical",
            "Must cite engineering standards (AS/NZS, ISO)",
            "Simulation parameters must be verifiable",
        ],
    },
    Faculty.COMPUTING_IT: {
        "primary_model": "claude-sonnet-4-5-20250929",
        "reason": "Excellent for code generation and security analysis",
        "verification_level": VerificationLevel.ENHANCED,
        "auto_check": ["github", "arxiv", "acm_dl"],
        "special_requirements": [
            "Code must be tested and runnable",
            "Security vulnerabilities must be flagged",
            "ML results must include reproducibility information",
        ],
    },
    Faculty.BUSINESS: {
        "primary_model": "gpt-4o",
        "reason": "Strong on data analysis and financial modelling",
        "verification_level": VerificationLevel.ENHANCED,
        "auto_check": ["bloomberg", "asx", "abs_data"],
        "special_requirements": [
            "Financial data must be current and sourced",
            "Market analysis must note assumptions",
            "Distinguish between analysis and financial advice",
        ],
    },
    Faculty.MEDICINE: {
        "primary_model": "claude-opus-4-6",
        "reason": "Careful, safety-focused for clinical contexts",
        "verification_level": VerificationLevel.CLINICAL_GRADE,
        "auto_check": ["pubmed", "cochrane", "therapeutic_guidelines"],
        "special_requirements": [
            "Never provide direct medical advice",
            "Always cite clinical evidence levels",
            "De-identify all patient data",
        ],
    },
}

# Human & social harmony research domains
SOCIAL_HARMONY_DOMAINS = [
    ResearchDomain.SOCIAL_HARMONY,
    ResearchDomain.MENTAL_HEALTH_RESEARCH,
    ResearchDomain.CULTURAL_DIVERSITY,
    ResearchDomain.STUDENT_WELLBEING,
]


class FacultyResearchSupport:
    """
    Faculty research support manager for UniMelb AI Platform.

    Provides faculty-specific AI model routing, verification levels,
    and research project management. Supports human and social
    harmony research with enhanced sensitivity controls.
    """

    def __init__(self) -> None:
        self._projects: dict[str, ResearchProject] = {}
        self._queries: list[ResearchQuery] = []

    def register_project(self, project: ResearchProject) -> ResearchProject:
        """Register a faculty research project."""
        # Set verification level based on faculty
        prefs = FACULTY_MODEL_PREFERENCES.get(project.faculty)
        if prefs and not project.verification_level:
            project.verification_level = prefs["verification_level"]

        # Social harmony research gets enhanced safeguards
        if project.domain in SOCIAL_HARMONY_DOMAINS:
            project.verification_level = VerificationLevel.ENHANCED

        self._projects[project.project_id] = project
        return project

    def get_project(self, project_id: str) -> ResearchProject | None:
        """Get a research project."""
        return self._projects.get(project_id)

    def get_faculty_config(self, faculty: Faculty) -> dict[str, Any]:
        """Get AI configuration for a faculty."""
        return FACULTY_MODEL_PREFERENCES.get(faculty, {
            "primary_model": "gpt-4o",
            "verification_level": VerificationLevel.STANDARD,
            "auto_check": [],
            "special_requirements": [],
        })

    def submit_research_query(
        self, query: ResearchQuery
    ) -> dict[str, Any]:
        """
        Submit a research query with faculty-specific routing.

        Returns routing configuration for the AI engine.
        """
        self._queries.append(query)
        faculty_config = self.get_faculty_config(query.faculty)

        # Determine if legislation check is needed
        needs_legislation = (
            query.legislation_check
            or query.faculty == Faculty.LAW
            or query.domain == ResearchDomain.LEGAL_RESEARCH
        )

        # Determine if e-library check is needed
        needs_elibrary = (
            query.elibrary_check
            or query.verification_level in (
                VerificationLevel.ENHANCED,
                VerificationLevel.LEGAL_GRADE,
                VerificationLevel.CLINICAL_GRADE,
            )
        )

        return {
            "query_id": query.query_id,
            "routing": {
                "model": query.preferred_model or faculty_config.get("primary_model", "gpt-4o"),
                "verification_level": query.verification_level.value,
                "multi_model": query.verification_level != VerificationLevel.STANDARD,
                "auto_checks": faculty_config.get("auto_check", []),
                "legislation_check": needs_legislation,
                "elibrary_check": needs_elibrary,
                "sources_required": query.sources_required,
            },
            "faculty_requirements": faculty_config.get("special_requirements", []),
        }

    def get_research_metrics(
        self, faculty: Faculty | None = None
    ) -> dict[str, Any]:
        """Get research usage metrics."""
        projects = list(self._projects.values())
        queries = list(self._queries)

        if faculty:
            projects = [p for p in projects if p.faculty == faculty]
            queries = [q for q in queries if q.faculty == faculty]

        domain_counts: dict[str, int] = {}
        for q in queries:
            key = q.domain.value
            domain_counts[key] = domain_counts.get(key, 0) + 1

        return {
            "faculty": faculty.value if faculty else "all",
            "active_projects": len([p for p in projects if p.active]),
            "total_queries": len(queries),
            "queries_by_domain": domain_counts,
            "social_harmony_queries": len(
                [q for q in queries if q.domain in SOCIAL_HARMONY_DOMAINS]
            ),
        }

"""
Search Authority & Website Safety Verification Framework — VIC / Melbourne
===========================================================================
Design: Jiadong Chen (陈佳栋) — Student ID: 723912

Quantitative authority scoring, website safety checks, anti-manipulation
detection, and cross-verification framework for web search within
Melbourne / Victoria / Australia — starting from VIC 3000 (City of Melbourne)
to all 79 Councils & Suburbs.

Based on:
- DOC-20260218-Search-Authority-Safety-VIC-0005

Authority Hierarchy (6 levels):
  L1 Government & Legislative Bodies
  L2 Official Bodies / Official Organisations
  L3 Company Official Publications (ABN-verified)
  L4 Academic Publications (.edu.au)
  L5 Mainstream Media
  L6 Community Sources / User Comments

Scoring Model:
  T = 0.4 × Source Authority + 0.2 × Transparency
    + 0.2 × Evidence Quality + 0.1 × Security
    + 0.1 × Cross-Verification

Safety Checks (5 items):
  A. HTTPS + Valid Certificate
  B. Domain Registration Entity
  C. Official Primary Domain
  D. No Redirect to Unknown Third-Party TLD
  E. Browser Security Alerts
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# =============================================================================
# Enums
# =============================================================================

class AuthorityLevel(Enum):
    """6-level authority source hierarchy."""

    L1_GOVERNMENT_LEGISLATIVE = 1   # .gov.au — highest authority
    L2_OFFICIAL_BODIES = 2          # ABS, DataVic, Land Use VIC, ACSC, ACCC
    L3_COMPANY_OFFICIAL = 3         # ABN-verified company websites
    L4_ACADEMIC = 4                 # .edu.au universities & research
    L5_MAINSTREAM_MEDIA = 5         # ABC News, The Age, Herald Sun
    L6_COMMUNITY_USER = 6           # Reviews, forums, social media


class SafetyCheck(Enum):
    """5-point website safety check items."""

    A_HTTPS_CERTIFICATE = "HTTPS + Valid Certificate"
    B_DOMAIN_REGISTRATION = "Domain Registration Entity"
    C_OFFICIAL_PRIMARY_DOMAIN = "Official Primary Domain"
    D_NO_MALICIOUS_REDIRECT = "No Redirect to Unknown Third-Party TLD"
    E_BROWSER_ALERTS = "Browser Security Alerts"


class DomainTrust(Enum):
    """Domain suffix trust classification."""

    GOV_AU = "gov.au"             # Government — highest trust
    VIC_GOV_AU = "vic.gov.au"     # VIC state government
    EDU_AU = "edu.au"             # Academic institutions
    ORG_AU = "org.au"             # Non-profit organisations
    COM_AU = "com.au"             # Australian commercial (ABN required)
    NET_AU = "net.au"             # Australian network
    GENERIC_COM = "com"           # Generic commercial
    OTHER = "other"               # Unknown / low trust


class ManipulationFlag(Enum):
    """Directed implantation / manipulation red flags."""

    EXTREME_STANCE = "Extreme single-stance with no authoritative refs"
    SALES_BOUND = "Information bound to sales/CTA content"
    NO_EXTERNAL_REFS = "No external references or legal citations"
    MAGIC_ANSWER = "Simple magic answer for complex problem"
    EMOTIONAL_MANIPULATION = "Emotional pressure / fear-based language"


class ScamwatchAction(Enum):
    """ACCC Scamwatch Stop-Check-Protect protocol."""

    STOP = "Don't rush to pay or enter personal info"
    CHECK = "Check domain, ABN, official channels"
    PROTECT = "Exit if anomaly found, report to Scamwatch"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class AuthorityScoringWeights:
    """Weights for the composite authority score T."""

    source_authority: float = 0.4
    transparency: float = 0.2
    evidence_quality: float = 0.2
    security: float = 0.1
    cross_verification: float = 0.1


@dataclass
class DimensionScore:
    """Score for a single scoring dimension (1-5 scale)."""

    dimension: str
    score: int             # 1-5
    justification: str = ""


@dataclass
class AuthorityAssessment:
    """Complete authority assessment result for a source."""

    url: str = ""
    domain: str = ""
    domain_trust: DomainTrust = DomainTrust.OTHER
    authority_level: AuthorityLevel = AuthorityLevel.L6_COMMUNITY_USER
    source_authority_score: int = 1
    transparency_score: int = 1
    evidence_quality_score: int = 1
    security_score: int = 1
    cross_verification_score: int = 1
    composite_score: float = 0.0
    manipulation_flags: list[str] = field(default_factory=list)
    safety_check_results: dict[str, bool] = field(default_factory=dict)
    recommendation: str = ""


@dataclass
class SafetyCheckResult:
    """Result of the 5-point website safety check."""

    all_passed: bool = False
    checks: dict[str, bool] = field(default_factory=dict)
    failed: list[str] = field(default_factory=list)
    risk_level: str = ""   # LOW / MEDIUM / HIGH / CRITICAL


@dataclass
class VICCouncilEntry:
    """A Victorian local government council entry."""

    name: str
    domain: str = ""
    postcode_start: str = ""
    lga_type: str = ""       # City / Shire / Borough


@dataclass
class CrossVerificationResult:
    """Cross-verification check result."""

    claim: str = ""
    sources_checked: list[str] = field(default_factory=list)
    sources_confirmed: list[str] = field(default_factory=list)
    verified: bool = False
    confidence: str = ""     # HIGH / MEDIUM / LOW


# =============================================================================
# VIC Government Domain Registry — Level 1 & Level 2
# =============================================================================

# Level 1: Government & Legislative Bodies
VIC_GOVERNMENT_DOMAINS: dict[str, str] = {
    "vic.gov.au": "VIC Government unified portal",
    "legislation.vic.gov.au": "VIC legislation (original legal texts)",
    "melbourne.vic.gov.au": "City of Melbourne (VIC 3000)",
    "parliament.vic.gov.au": "VIC Parliament",
    "planning.vic.gov.au": "VIC Planning",
    "health.vic.gov.au": "VIC Health",
    "education.vic.gov.au": "VIC Education",
    "dtf.vic.gov.au": "VIC Department of Treasury and Finance",
}

FEDERAL_GOVERNMENT_DOMAINS: dict[str, str] = {
    "legislation.gov.au": "Federal legislation",
    "treasury.gov.au": "Federal Treasury",
    "homeaffairs.gov.au": "Home Affairs",
    "immi.homeaffairs.gov.au": "Immigration & Citizenship",
    "ato.gov.au": "Australian Taxation Office",
    "services.gov.au": "Services Australia",
    "aph.gov.au": "Australian Parliament House",
}

# Level 2: Official Bodies / Official Organisations
OFFICIAL_BODY_DOMAINS: dict[str, str] = {
    "abs.gov.au": "Australian Bureau of Statistics",
    "data.vic.gov.au": "DataVic (VIC open data, 4800+ datasets)",
    "land.vic.gov.au": "Land Use Victoria / LANDATA",
    "consumer.vic.gov.au": "Consumer Affairs Victoria",
    "scamwatch.gov.au": "National Anti-Scam Centre / Scamwatch (ACCC)",
    "cyber.gov.au": "Australian Cyber Security Centre",
    "accc.gov.au": "Australian Competition & Consumer Commission",
    "oaic.gov.au": "Office of the Australian Information Commissioner",
    "teqsa.gov.au": "TEQSA — Higher Education Standards",
    "humanrights.gov.au": "Australian Human Rights Commission",
    "humanrights.vic.gov.au": "Victorian Equal Opportunity & Human Rights",
    "abr.business.gov.au": "Australian Business Register",
    "abr.gov.au": "ABN Lookup",
}

# Level 5: Mainstream Media (Australian context)
MAINSTREAM_MEDIA_DOMAINS: dict[str, str] = {
    "abc.net.au": "ABC News (Australian Broadcasting Corporation)",
    "theage.com.au": "The Age (Melbourne newspaper of record)",
    "heraldsun.com.au": "Herald Sun",
    "theaustralian.com.au": "The Australian",
    "sbs.com.au": "SBS News",
    "9news.com.au": "Nine News",
    "7news.com.au": "Seven News",
}

# Known suspicious TLD patterns for redirect detection
SUSPICIOUS_TLDS: list[str] = [
    ".xyz", ".top", ".buzz", ".click", ".link", ".info",
    ".tk", ".ml", ".ga", ".cf", ".gq",
    ".win", ".bid", ".loan", ".racing",
]

# VIC Council registry (selected major councils around VIC 3000)
VIC_COUNCIL_REGISTRY: list[VICCouncilEntry] = [
    VICCouncilEntry("City of Melbourne", "melbourne.vic.gov.au", "3000", "City"),
    VICCouncilEntry("City of Port Phillip", "portphillip.vic.gov.au", "3004", "City"),
    VICCouncilEntry("City of Yarra", "yarracity.vic.gov.au", "3065", "City"),
    VICCouncilEntry("City of Stonnington", "stonnington.vic.gov.au", "3141", "City"),
    VICCouncilEntry("City of Boroondara", "boroondara.vic.gov.au", "3122", "City"),
    VICCouncilEntry("City of Darebin", "darebin.vic.gov.au", "3070", "City"),
    VICCouncilEntry("City of Moreland", "moreland.vic.gov.au", "3055", "City"),
    VICCouncilEntry("City of Maribyrnong", "maribyrnong.vic.gov.au", "3011", "City"),
    VICCouncilEntry("City of Hobsons Bay", "hobsonsbay.vic.gov.au", "3015", "City"),
    VICCouncilEntry("City of Moonee Valley", "mvcc.vic.gov.au", "3032", "City"),
    VICCouncilEntry("City of Brimbank", "brimbank.vic.gov.au", "3020", "City"),
    VICCouncilEntry("City of Wyndham", "wyndham.vic.gov.au", "3029", "City"),
    VICCouncilEntry("City of Greater Dandenong", "greaterdandenong.vic.gov.au", "3175", "City"),
    VICCouncilEntry("City of Monash", "monash.vic.gov.au", "3150", "City"),
    VICCouncilEntry("City of Whitehorse", "whitehorse.vic.gov.au", "3128", "City"),
    VICCouncilEntry("City of Knox", "knox.vic.gov.au", "3152", "City"),
    VICCouncilEntry("City of Maroondah", "maroondah.vic.gov.au", "3134", "City"),
    VICCouncilEntry("City of Casey", "casey.vic.gov.au", "3805", "City"),
    VICCouncilEntry("City of Frankston", "frankston.vic.gov.au", "3199", "City"),
    VICCouncilEntry("City of Greater Geelong", "geelongaustralia.com.au", "3220", "City"),
]

# Anti-manipulation: sales pressure / emotional manipulation keywords
SALES_PRESSURE_KEYWORDS: list[str] = [
    "act now", "limited time", "don't miss out", "last chance",
    "guaranteed returns", "risk free", "no risk",
    "once in a lifetime", "exclusive offer",
    "hurry", "urgent", "expires today",
]

EMOTIONAL_MANIPULATION_KEYWORDS: list[str] = [
    "everyone is doing it", "you'll regret",
    "your family deserves", "worth any price",
    "don't you care about", "sacrifice everything",
]

# Property verification search domains (VIC 3000 example)
PROPERTY_VERIFICATION_SOURCES: dict[str, str] = {
    "land.vic.gov.au": "Title & Ownership (LANDATA / Property Report)",
    "vic.gov.au/know-your-council": "Council Info (Know Your Council)",
    "legislation.vic.gov.au": "Relevant Legislation (Property Law Act etc.)",
    "consumer.vic.gov.au": "Transaction / Regulatory Rules",
    "abr.gov.au": "ABN Lookup (Agent/Developer verification)",
}


# =============================================================================
# Full URL Registry — Victoria Public / Gov / Non-Profit / Landmark (V1.0)
# 12 categories, all free, legal, public access
# =============================================================================

@dataclass
class URLRegistryEntry:
    """A single entry in the full URL registry."""

    url: str
    category: str
    description: str = ""


@dataclass
class ComplianceSection:
    """A section in the J.OS Gov Research Compliance Map."""

    section_id: str
    title: str
    domains: list[str] = field(default_factory=list)
    ai_allowed: list[str] = field(default_factory=list)
    ai_not_allowed: list[str] = field(default_factory=list)
    security_rules: list[str] = field(default_factory=list)


class URLCategory(Enum):
    """URL registry categories."""

    GOVERNMENT = "Government (State + Federal)"
    LOCAL_GOVERNMENT = "Local Government"
    LAND_PROPERTY = "Land, Property, Planning"
    ENERGY_UTILITIES = "Energy & Utilities"
    NON_PROFIT = "Non-Profit / Humanitarian"
    ENVIRONMENT_ANIMAL = "Environmental / Animal Welfare"
    CULTURE_MUSEUMS = "Culture / Libraries / Museums"
    EDUCATION = "Education (Early -> PhD)"
    LANDMARKS = "Landmarks / Complexes"
    COMMUNITY_SERVICES = "Community Services"
    TRANSPORT = "Transport / Logistics"
    SAFETY_CYBER = "Safety / Cyber / Consumer Protection"


FULL_URL_REGISTRY: list[URLRegistryEntry] = [
    # 1. Government (State + Federal)
    URLRegistryEntry("https://www.vic.gov.au", "GOVERNMENT", "VIC Government portal"),
    URLRegistryEntry("https://www.legislation.vic.gov.au", "GOVERNMENT", "VIC legislation"),
    URLRegistryEntry("https://www.gazette.vic.gov.au", "GOVERNMENT", "VIC Government Gazette"),
    URLRegistryEntry("https://service.vic.gov.au", "GOVERNMENT", "Service Victoria"),
    URLRegistryEntry("https://www.data.vic.gov.au", "GOVERNMENT", "DataVic open data"),
    URLRegistryEntry("https://www.deeca.vic.gov.au", "GOVERNMENT", "VIC Energy, Environment & Climate"),
    URLRegistryEntry("https://www.health.vic.gov.au", "GOVERNMENT", "VIC Health"),
    URLRegistryEntry("https://www.emergency.vic.gov.au", "GOVERNMENT", "Emergency Victoria"),
    URLRegistryEntry("https://my.gov.au", "GOVERNMENT", "Federal myGov"),
    URLRegistryEntry("https://www.legislation.gov.au", "GOVERNMENT", "Federal legislation"),
    URLRegistryEntry("https://www.abs.gov.au", "GOVERNMENT", "ABS statistics"),
    # 2. Local Government
    URLRegistryEntry("https://www.melbourne.vic.gov.au", "LOCAL_GOVERNMENT", "City of Melbourne"),
    URLRegistryEntry("https://www.localgovernment.vic.gov.au", "LOCAL_GOVERNMENT", "Local Government Victoria"),
    URLRegistryEntry("https://www.vic.gov.au/know-your-council", "LOCAL_GOVERNMENT", "Know Your Council (79 councils)"),
    # 3. Land, Property, Planning
    URLRegistryEntry("https://www.land.vic.gov.au", "LAND_PROPERTY", "Land Use Victoria"),
    URLRegistryEntry("https://www.land.vic.gov.au/property-and-parcel-search", "LAND_PROPERTY", "Property & Parcel Search"),
    URLRegistryEntry("https://www.land.vic.gov.au/land-registration", "LAND_PROPERTY", "Land registration"),
    URLRegistryEntry("https://www.planning.vic.gov.au", "LAND_PROPERTY", "VIC Planning"),
    URLRegistryEntry("https://www.land.vic.gov.au/maps-and-spatial", "LAND_PROPERTY", "VicMap / spatial data"),
    # 4. Energy & Utilities
    URLRegistryEntry("https://www.esc.vic.gov.au", "ENERGY_UTILITIES", "Essential Services Commission"),
    URLRegistryEntry("https://www.originenergy.com.au", "ENERGY_UTILITIES", "Origin Energy"),
    URLRegistryEntry("https://www.agl.com.au", "ENERGY_UTILITIES", "AGL Energy"),
    URLRegistryEntry("https://www.redenergy.com.au", "ENERGY_UTILITIES", "Red Energy"),
    URLRegistryEntry("https://www.simplyenergy.com.au", "ENERGY_UTILITIES", "Simply Energy"),
    URLRegistryEntry("https://www.gww.com.au", "ENERGY_UTILITIES", "Greater Western Water"),
    URLRegistryEntry("https://southeastwater.com.au", "ENERGY_UTILITIES", "South East Water"),
    URLRegistryEntry("https://www.citipower.com.au", "ENERGY_UTILITIES", "CitiPower (electricity grid)"),
    URLRegistryEntry("https://www.unitedenergy.com.au", "ENERGY_UTILITIES", "United Energy (electricity grid)"),
    # 5. Non-Profit / Humanitarian
    URLRegistryEntry("https://www.redcross.org.au", "NON_PROFIT", "Australian Red Cross"),
    URLRegistryEntry("https://www.stjohnvic.com.au", "NON_PROFIT", "St John Ambulance"),
    URLRegistryEntry("https://www.salvationarmy.org.au", "NON_PROFIT", "The Salvation Army"),
    URLRegistryEntry("https://www.missionaustralia.com.au", "NON_PROFIT", "Mission Australia"),
    URLRegistryEntry("https://www.bsl.org.au", "NON_PROFIT", "Brotherhood of St Laurence"),
    # 6. Environmental / Animal Welfare
    URLRegistryEntry("https://www.parks.vic.gov.au", "ENVIRONMENT_ANIMAL", "Parks Victoria"),
    URLRegistryEntry("https://www.epa.vic.gov.au", "ENVIRONMENT_ANIMAL", "EPA Victoria"),
    URLRegistryEntry("https://www.rspcavic.org", "ENVIRONMENT_ANIMAL", "RSPCA Victoria"),
    URLRegistryEntry("https://www.zoo.org.au", "ENVIRONMENT_ANIMAL", "Zoos Victoria"),
    URLRegistryEntry("https://www.sustainability.vic.gov.au", "ENVIRONMENT_ANIMAL", "Sustainability Victoria"),
    # 7. Culture / Libraries / Museums
    URLRegistryEntry("https://www.slv.vic.gov.au", "CULTURE_MUSEUMS", "State Library Victoria"),
    URLRegistryEntry("https://museumsvictoria.com.au", "CULTURE_MUSEUMS", "Museums Victoria"),
    URLRegistryEntry("https://www.ngv.vic.gov.au", "CULTURE_MUSEUMS", "National Gallery of Victoria"),
    URLRegistryEntry("https://www.artscentremelbourne.com.au", "CULTURE_MUSEUMS", "Arts Centre Melbourne"),
    URLRegistryEntry("https://www.fedsquare.com", "CULTURE_MUSEUMS", "Federation Square"),
    URLRegistryEntry("https://www.shrine.org.au", "CULTURE_MUSEUMS", "Shrine of Remembrance"),
    # 8. Education (Early -> PhD)
    URLRegistryEntry("https://www.vic.gov.au/early-childhood", "EDUCATION", "VIC early childhood education"),
    URLRegistryEntry("https://www.vic.gov.au/education", "EDUCATION", "VIC Department of Education"),
    URLRegistryEntry("https://www.vcaa.vic.edu.au", "EDUCATION", "VCAA (VCE)"),
    URLRegistryEntry("https://www.tafecourses.com.au", "EDUCATION", "TAFE Victoria"),
    URLRegistryEntry("https://www.unimelb.edu.au", "EDUCATION", "University of Melbourne"),
    URLRegistryEntry("https://www.monash.edu", "EDUCATION", "Monash University"),
    URLRegistryEntry("https://www.rmit.edu.au", "EDUCATION", "RMIT University"),
    URLRegistryEntry("https://www.swinburne.edu.au", "EDUCATION", "Swinburne University"),
    URLRegistryEntry("https://www.deakin.edu.au", "EDUCATION", "Deakin University"),
    URLRegistryEntry("https://www.latrobe.edu.au", "EDUCATION", "La Trobe University"),
    URLRegistryEntry("https://www.vu.edu.au", "EDUCATION", "Victoria University"),
    # 9. Landmarks / Complexes
    URLRegistryEntry("https://marvelstadium.com.au", "LANDMARKS", "Marvel Stadium (Docklands)"),
    URLRegistryEntry("https://www.mcg.org.au", "LANDMARKS", "Melbourne Cricket Ground"),
    URLRegistryEntry("https://www.rodlaverarena.com", "LANDMARKS", "Rod Laver Arena"),
    URLRegistryEntry("https://mcec.com.au", "LANDMARKS", "Melbourne Convention Centre"),
    URLRegistryEntry("https://www.docklands.com.au", "LANDMARKS", "Docklands Precinct"),
    URLRegistryEntry("https://www.southbank.net.au", "LANDMARKS", "Southbank Precinct"),
    URLRegistryEntry("https://qvm.com.au", "LANDMARKS", "Queen Victoria Market"),
    URLRegistryEntry("https://www.rbg.vic.gov.au", "LANDMARKS", "Royal Botanic Gardens"),
    URLRegistryEntry("https://www.zoo.org.au/melbourne", "LANDMARKS", "Melbourne Zoo"),
    # 10. Community Services
    URLRegistryEntry("https://www.nhvic.org.au", "COMMUNITY_SERVICES", "Neighbourhood Houses Victoria"),
    URLRegistryEntry("https://www.volunteeringvictoria.org.au", "COMMUNITY_SERVICES", "Volunteering Victoria"),
    URLRegistryEntry("https://cisvic.org.au", "COMMUNITY_SERVICES", "Community Info & Support VIC"),
    URLRegistryEntry("https://www.homeaffairs.gov.au/amep", "COMMUNITY_SERVICES", "Adult Migrant English Program"),
    # 11. Transport / Logistics
    URLRegistryEntry("https://www.ptv.vic.gov.au", "TRANSPORT", "Public Transport Victoria"),
    URLRegistryEntry("https://www.vicroads.vic.gov.au", "TRANSPORT", "VicRoads"),
    URLRegistryEntry("https://www.melbourneairport.com.au", "TRANSPORT", "Melbourne Airport"),
    URLRegistryEntry("https://www.avalonairport.com.au", "TRANSPORT", "Avalon Airport"),
    URLRegistryEntry("https://auspost.com.au", "TRANSPORT", "Australia Post"),
    # 12. Safety / Cyber / Consumer Protection
    URLRegistryEntry("https://www.cyber.gov.au", "SAFETY_CYBER", "Australian Cyber Security Centre"),
    URLRegistryEntry("https://www.scamwatch.gov.au", "SAFETY_CYBER", "Scamwatch (ACCC)"),
    URLRegistryEntry("https://www.nasc.gov.au", "SAFETY_CYBER", "National Anti-Scam Centre"),
    URLRegistryEntry("https://www.consumer.vic.gov.au", "SAFETY_CYBER", "Consumer Affairs Victoria"),
    URLRegistryEntry("https://www.victimsofcrime.vic.gov.au", "SAFETY_CYBER", "Victims of Crime Victoria"),
]

# J.OS Gov Research Compliance Map v1.1 — Section definitions
COMPLIANCE_MAP_SECTIONS: list[ComplianceSection] = [
    ComplianceSection(
        "S1", "Government Domain Eligibility & Legal Basis",
        domains=["domainname.gov.au", "auda.org.au", "legislation.vic.gov.au", "legislation.gov.au"],
        ai_allowed=["Read & cite public info", "Summary & citation"],
        ai_not_allowed=["Bulk copy copyright content"],
        security_rules=["HTTPS required", "Trusted CA certificate", "No abnormal redirects"],
    ),
    ComplianceSection(
        "S2", "Privacy & Data Protection",
        domains=["vic.gov.au/privacy", "consumer.vic.gov.au/privacy", "cyber.gov.au", "abs.gov.au/about/privacy"],
        ai_allowed=["Process public information only"],
        ai_not_allowed=["Scrape personal sensitive data", "Reconstruct databases", "Violate robots.txt or Terms"],
        security_rules=["HTTPS enforced", "Certificate validity check", "First-party cookies only"],
    ),
    ComplianceSection(
        "S3", "Energy & Utilities (Victoria)",
        domains=["esc.vic.gov.au", "originenergy.com.au", "agl.com.au"],
        ai_allowed=["Summarise public tariff structures"],
        ai_not_allowed=["Copy full contract terms", "Access login-required pages"],
        security_rules=["Company websites must be HTTPS", "Stop extraction on marketing cookies"],
    ),
    ComplianceSection(
        "S4", "Education (Early -> PhD)",
        domains=["vic.gov.au/education", "vcaa.vic.edu.au", "unimelb.edu.au", "monash.edu"],
        ai_allowed=["Summarise admission requirements"],
        ai_not_allowed=["Copy copyright course materials", "Access student portals"],
        security_rules=["Public directories only", "No login systems"],
    ),
    ComplianceSection(
        "S5", "Landmarks & Public Facilities",
        domains=["marvelstadium.com.au", "ngv.vic.gov.au", "parks.vic.gov.au", "museumsvictoria.com.au"],
        ai_allowed=["Summarise opening times & rules"],
        ai_not_allowed=["Copy images or artworks", "Collect ticketing transaction data"],
        security_rules=["HTTPS valid", "Check Content-Security-Policy", "No external ad redirects"],
    ),
    ComplianceSection(
        "S6", "Non-Profit / Humanitarian",
        domains=["redcross.org.au", "rspcavic.org", "salvationarmy.org.au"],
        ai_allowed=["Summarise public reports"],
        ai_not_allowed=["Copy copyright images and stories"],
        security_rules=["Verify HTTPS", "Check for no malicious scripts"],
    ),
]

# AI Abstract & Extract Permission Matrix
AI_PERMISSION_ALLOW: list[str] = [
    "Public policy summaries",
    "Legislative references",
    "Public reports data citation",
    "Open data download (where permitted)",
]

AI_PERMISSION_CONDITIONAL: list[str] = [
    "Media articles (respect copyright)",
    "NGO annual reports",
]

AI_PERMISSION_NOT_ALLOWED: list[str] = [
    "Paywalled databases",
    "Login portals",
    "Personal data scraping",
    "Bulk copying",
]

# Zero Assumption Rule
ZERO_ASSUMPTION_RULES: list[str] = [
    "Do not fill gaps",
    "Do not speculate on future policy",
    "Do not generate unverified content",
]

# Legal research steps (J.OS Mode)
JOS_RESEARCH_STEPS: list[str] = [
    "Step 1: Define time / dir / loc",
    "Step 2: Restrict to official domain",
    "Step 3: Check Privacy / Terms / Disclaimer",
    "Step 4: Verify certificate",
    "Step 5: Read-only abstraction",
    "Step 6: Cite original URL",
    "Step 7: Output summary with no assumption",
]

# Signal priority for AI agents
AI_SIGNAL_PRIORITY: list[str] = [
    "Law",
    "Policy",
    "Public Institutions",
    "Datasets",
    "University / Culture",
    "Media",
    "Community",
]

# Connection security certificate validation checklist
CONNECTION_SECURITY_CHECKLIST: list[str] = [
    "HTTPS required",
    "TLS 1.2+",
    "Valid CA issuer",
    "Certificate matches domain",
    "No mixed content",
    "No suspicious 3rd-party tracking scripts",
    "Government domains preferred",
]


# =============================================================================
# Main Framework Class
# =============================================================================

class SearchAuthorityFramework:
    """
    Search Authority & Website Safety Verification Framework.

    Implements:
    - 6-level authority hierarchy
    - 5-point website safety checks
    - Quantitative scoring model (T = weighted composite)
    - Anti-manipulation / directed implantation detection
    - Cross-verification methodology
    - VIC domain registry with council mapping
    """

    def __init__(self) -> None:
        self.weights = AuthorityScoringWeights()
        self.vic_gov_domains = VIC_GOVERNMENT_DOMAINS
        self.federal_gov_domains = FEDERAL_GOVERNMENT_DOMAINS
        self.official_body_domains = OFFICIAL_BODY_DOMAINS
        self.mainstream_media = MAINSTREAM_MEDIA_DOMAINS
        self.council_registry = VIC_COUNCIL_REGISTRY
        self.suspicious_tlds = SUSPICIOUS_TLDS

    # -----------------------------------------------------------------
    # Domain Classification
    # -----------------------------------------------------------------

    def classify_domain_trust(self, domain: str) -> DomainTrust:
        """Classify a domain by its suffix into a trust level."""
        d = domain.lower().strip()
        if d.endswith(".vic.gov.au"):
            return DomainTrust.VIC_GOV_AU
        if d.endswith(".gov.au"):
            return DomainTrust.GOV_AU
        if d.endswith(".edu.au"):
            return DomainTrust.EDU_AU
        if d.endswith(".org.au"):
            return DomainTrust.ORG_AU
        if d.endswith(".com.au"):
            return DomainTrust.COM_AU
        if d.endswith(".net.au"):
            return DomainTrust.NET_AU
        if d.endswith(".com") and not d.endswith(".com.au"):
            return DomainTrust.GENERIC_COM
        return DomainTrust.OTHER

    def determine_authority_level(self, domain: str) -> AuthorityLevel:
        """
        Determine the authority level (L1-L6) for a domain.

        L1: .gov.au / .vic.gov.au government domains
        L2: Official bodies (ABS, DataVic, ACSC etc.)
        L3: .com.au commercial (ABN-verified)
        L4: .edu.au academic
        L5: Mainstream media domains
        L6: Everything else (community/user)
        """
        d = domain.lower().strip()

        # L2: Official Bodies (check first — they are .gov.au but specialised)
        if d in self.official_body_domains:
            return AuthorityLevel.L2_OFFICIAL_BODIES

        # L1: Government & Legislative
        if d in self.vic_gov_domains or d in self.federal_gov_domains:
            return AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE
        if d.endswith(".vic.gov.au") or d.endswith(".gov.au"):
            return AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE

        # L4: Academic (check before L3 to avoid .edu.au false-matching)
        if d.endswith(".edu.au"):
            return AuthorityLevel.L4_ACADEMIC

        # L5: Mainstream Media
        if d in self.mainstream_media:
            return AuthorityLevel.L5_MAINSTREAM_MEDIA

        # L3: Company official (.com.au)
        if d.endswith(".com.au") or d.endswith(".net.au"):
            return AuthorityLevel.L3_COMPANY_OFFICIAL

        # L6: Default — community/user/unknown
        return AuthorityLevel.L6_COMMUNITY_USER

    # -----------------------------------------------------------------
    # Authority Score (Dimension 1)
    # -----------------------------------------------------------------

    def score_source_authority(self, domain: str) -> int:
        """
        Score source authority based on domain (1-5 scale).

        5: .gov.au, official bodies
        4: .edu.au, government-authorised semi-official
        3: Large legitimate company (.com.au + ABN), mainstream media
        2: General .org.au, personal blogs, forums
        1: Unknown, suspicious, content farms
        """
        level = self.determine_authority_level(domain)
        score_map = {
            AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE: 5,
            AuthorityLevel.L2_OFFICIAL_BODIES: 5,
            AuthorityLevel.L3_COMPANY_OFFICIAL: 3,
            AuthorityLevel.L4_ACADEMIC: 4,
            AuthorityLevel.L5_MAINSTREAM_MEDIA: 3,
            AuthorityLevel.L6_COMMUNITY_USER: 1,
        }
        base = score_map.get(level, 1)
        # Boost .org.au slightly above pure unknown
        d = domain.lower().strip()
        if base == 1 and d.endswith(".org.au"):
            return 2
        return base

    # -----------------------------------------------------------------
    # Safety Checks (5-point)
    # -----------------------------------------------------------------

    def run_safety_checks(
        self, checks_completed: dict[str, bool]
    ) -> SafetyCheckResult:
        """
        Run the 5-point website safety check.

        Expects keys from SafetyCheck enum values.
        """
        result = SafetyCheckResult()
        result.checks = {}
        result.failed = []

        for check in SafetyCheck:
            passed = checks_completed.get(check.value, False)
            result.checks[check.value] = passed
            if not passed:
                result.failed.append(check.value)

        fail_count = len(result.failed)
        if fail_count == 0:
            result.risk_level = "LOW"
            result.all_passed = True
        elif fail_count <= 2:
            result.risk_level = "MEDIUM"
        elif fail_count <= 3:
            result.risk_level = "HIGH"
        else:
            result.risk_level = "CRITICAL"

        return result

    # -----------------------------------------------------------------
    # Manipulation Detection
    # -----------------------------------------------------------------

    def detect_manipulation(self, text: str) -> list[ManipulationFlag]:
        """
        Detect manipulation / directed implantation signals in text.

        Checks for sales pressure, emotional manipulation, lack of refs,
        and extreme single-stance patterns.
        """
        flags: list[ManipulationFlag] = []
        t = text.lower()

        # Check sales pressure
        sales_hits = [kw for kw in SALES_PRESSURE_KEYWORDS if kw in t]
        if len(sales_hits) >= 2:
            flags.append(ManipulationFlag.SALES_BOUND)

        # Check emotional manipulation
        emotional_hits = [kw for kw in EMOTIONAL_MANIPULATION_KEYWORDS if kw in t]
        if len(emotional_hits) >= 1:
            flags.append(ManipulationFlag.EMOTIONAL_MANIPULATION)

        # Check for "magic answer" pattern: very short + absolute claims
        absolute_claims = [
            "guaranteed", "100%", "always works", "never fails",
            "foolproof", "no risk",
        ]
        abs_hits = [a for a in absolute_claims if a in t]
        if len(abs_hits) >= 2:
            flags.append(ManipulationFlag.MAGIC_ANSWER)

        return flags

    def check_redirect_safety(self, final_domain: str) -> bool:
        """
        Check if a final redirected domain is suspicious.

        Returns True if safe, False if suspicious TLD detected.
        """
        d = final_domain.lower().strip()
        for tld in self.suspicious_tlds:
            if d.endswith(tld):
                return False
        return True

    # -----------------------------------------------------------------
    # Composite Scoring
    # -----------------------------------------------------------------

    def calculate_composite_score(
        self,
        source_authority: int,
        transparency: int,
        evidence_quality: int,
        security: int,
        cross_verification: int,
    ) -> float:
        """
        Calculate composite authority score T (0.0 - 5.0).

        T = 0.4 × Source Authority + 0.2 × Transparency
          + 0.2 × Evidence Quality + 0.1 × Security
          + 0.1 × Cross-Verification
        """
        for score in (source_authority, transparency, evidence_quality,
                      security, cross_verification):
            if not 1 <= score <= 5:
                raise ValueError(f"Score {score} out of 1-5 range")

        return (
            self.weights.source_authority * source_authority
            + self.weights.transparency * transparency
            + self.weights.evidence_quality * evidence_quality
            + self.weights.security * security
            + self.weights.cross_verification * cross_verification
        )

    def assess_source(
        self,
        url: str,
        domain: str,
        transparency: int = 1,
        evidence_quality: int = 1,
        security: int = 1,
        cross_verification: int = 1,
        safety_checks: dict[str, bool] | None = None,
        page_text: str = "",
    ) -> AuthorityAssessment:
        """
        Full authority assessment for a web source.

        Combines domain classification, authority scoring, safety checks,
        manipulation detection, and composite scoring.
        """
        assessment = AuthorityAssessment(url=url, domain=domain)

        # Domain classification
        assessment.domain_trust = self.classify_domain_trust(domain)
        assessment.authority_level = self.determine_authority_level(domain)
        assessment.source_authority_score = self.score_source_authority(domain)

        # Store dimension scores
        assessment.transparency_score = transparency
        assessment.evidence_quality_score = evidence_quality
        assessment.security_score = security
        assessment.cross_verification_score = cross_verification

        # Composite score
        assessment.composite_score = self.calculate_composite_score(
            assessment.source_authority_score,
            transparency,
            evidence_quality,
            security,
            cross_verification,
        )

        # Safety checks
        if safety_checks:
            safety_result = self.run_safety_checks(safety_checks)
            assessment.safety_check_results = safety_result.checks

        # Manipulation detection
        if page_text:
            flags = self.detect_manipulation(page_text)
            assessment.manipulation_flags = [f.value for f in flags]

        # Recommendation
        score = assessment.composite_score
        if score >= 4.0:
            assessment.recommendation = "High confidence source — suitable for primary reference."
        elif score >= 3.0:
            assessment.recommendation = "Moderate confidence — cross-verify with Level 1-2 sources."
        elif score >= 2.0:
            assessment.recommendation = "Low confidence — use as supplementary signal only."
        else:
            assessment.recommendation = "Very low confidence — do not use as factual basis."

        if assessment.manipulation_flags:
            assessment.recommendation += (
                " WARNING: Manipulation signals detected — exercise caution."
            )

        return assessment

    # -----------------------------------------------------------------
    # Cross-Verification
    # -----------------------------------------------------------------

    def cross_verify(
        self,
        claim: str,
        sources: list[dict[str, str]],
    ) -> CrossVerificationResult:
        """
        Cross-verify a claim against multiple sources.

        Each source is a dict with 'domain' and 'confirms' (True/False as str).
        Verified = confirmed by >=2 Level 1-2 authoritative sources.
        """
        result = CrossVerificationResult(claim=claim)

        for src in sources:
            domain = src.get("domain", "")
            confirms = src.get("confirms", "false").lower() == "true"
            result.sources_checked.append(domain)
            if confirms:
                result.sources_confirmed.append(domain)

        # Check how many confirming sources are Level 1-2
        l1_l2_confirmed = [
            d for d in result.sources_confirmed
            if self.determine_authority_level(d) in (
                AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE,
                AuthorityLevel.L2_OFFICIAL_BODIES,
            )
        ]

        if len(l1_l2_confirmed) >= 2:
            result.verified = True
            result.confidence = "HIGH"
        elif len(l1_l2_confirmed) == 1:
            result.verified = True
            result.confidence = "MEDIUM"
        elif len(result.sources_confirmed) >= 2:
            result.verified = True
            result.confidence = "LOW"
        else:
            result.verified = False
            result.confidence = "UNVERIFIED"

        return result

    # -----------------------------------------------------------------
    # VIC Council Lookup
    # -----------------------------------------------------------------

    def get_council_by_postcode(self, postcode: str) -> VICCouncilEntry | None:
        """Look up a VIC council by starting postcode."""
        for council in self.council_registry:
            if council.postcode_start == postcode:
                return council
        return None

    def get_council_by_name(self, name: str) -> VICCouncilEntry | None:
        """Look up a VIC council by name (partial match)."""
        name_lower = name.lower()
        for council in self.council_registry:
            if name_lower in council.name.lower():
                return council
        return None

    def get_all_council_domains(self) -> list[str]:
        """Get all registered VIC council domains."""
        return [c.domain for c in self.council_registry if c.domain]

    # -----------------------------------------------------------------
    # Property Verification Sources
    # -----------------------------------------------------------------

    def get_property_verification_sources(self) -> dict[str, str]:
        """Get the recommended property verification source domains."""
        return PROPERTY_VERIFICATION_SOURCES

    # -----------------------------------------------------------------
    # Search Strategy Helpers
    # -----------------------------------------------------------------

    def build_site_restricted_query(
        self, keyword: str, domain: str
    ) -> str:
        """Build a site:-restricted search query."""
        return f"site:{domain} {keyword}"

    def build_gov_search_queries(self, keyword: str) -> list[str]:
        """Build government-restricted search queries for a keyword."""
        return [
            f"site:vic.gov.au {keyword}",
            f"site:legislation.vic.gov.au {keyword}",
            f"site:data.vic.gov.au {keyword}",
            f"site:land.vic.gov.au {keyword}",
            f"site:consumer.vic.gov.au {keyword}",
        ]

    # -----------------------------------------------------------------
    # Scamwatch Protocol
    # -----------------------------------------------------------------

    def get_scamwatch_protocol(self) -> dict[str, str]:
        """Get the ACCC Scamwatch Stop-Check-Protect protocol."""
        return {
            action.name: action.value for action in ScamwatchAction
        }

    # -----------------------------------------------------------------
    # Full URL Registry
    # -----------------------------------------------------------------

    def get_url_registry(self) -> list[URLRegistryEntry]:
        """Get the full URL registry (all 12 categories)."""
        return FULL_URL_REGISTRY

    def get_urls_by_category(self, category: str) -> list[URLRegistryEntry]:
        """Get URLs filtered by category code."""
        return [u for u in FULL_URL_REGISTRY if u.category == category]

    def get_url_categories(self) -> list[str]:
        """Get all unique URL categories in the registry."""
        return sorted(set(u.category for u in FULL_URL_REGISTRY))

    def count_urls_by_category(self) -> dict[str, int]:
        """Count URLs per category."""
        counts: dict[str, int] = {}
        for entry in FULL_URL_REGISTRY:
            counts[entry.category] = counts.get(entry.category, 0) + 1
        return counts

    # -----------------------------------------------------------------
    # Compliance Map
    # -----------------------------------------------------------------

    def get_compliance_sections(self) -> list[ComplianceSection]:
        """Get all J.OS compliance map sections."""
        return COMPLIANCE_MAP_SECTIONS

    def get_compliance_section(self, section_id: str) -> ComplianceSection | None:
        """Get a compliance section by ID."""
        for section in COMPLIANCE_MAP_SECTIONS:
            if section.section_id == section_id:
                return section
        return None

    def get_ai_permissions(self) -> dict[str, list[str]]:
        """Get the AI abstraction & extraction permission matrix."""
        return {
            "allowed": AI_PERMISSION_ALLOW,
            "conditional": AI_PERMISSION_CONDITIONAL,
            "not_allowed": AI_PERMISSION_NOT_ALLOWED,
        }

    def get_zero_assumption_rules(self) -> list[str]:
        """Get the zero assumption protocol rules."""
        return ZERO_ASSUMPTION_RULES

    def get_research_steps(self) -> list[str]:
        """Get J.OS legal research steps."""
        return JOS_RESEARCH_STEPS

    def get_ai_signal_priority(self) -> list[str]:
        """Get AI signal priority ordering."""
        return AI_SIGNAL_PRIORITY

    def get_connection_security_checklist(self) -> list[str]:
        """Get the connection security certificate validation checklist."""
        return CONNECTION_SECURITY_CHECKLIST

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------

    def get_framework_summary(self) -> dict[str, Any]:
        """Get a summary of the search authority framework."""
        return {
            "version": "1.0",
            "scope": "Melbourne / VIC / Australia — from VIC 3000",
            "authority_levels": len(AuthorityLevel),
            "safety_checks": len(SafetyCheck),
            "scoring_dimensions": 5,
            "scoring_weights": {
                "source_authority": self.weights.source_authority,
                "transparency": self.weights.transparency,
                "evidence_quality": self.weights.evidence_quality,
                "security": self.weights.security,
                "cross_verification": self.weights.cross_verification,
            },
            "vic_gov_domains": len(self.vic_gov_domains),
            "federal_gov_domains": len(self.federal_gov_domains),
            "official_body_domains": len(self.official_body_domains),
            "mainstream_media_domains": len(self.mainstream_media),
            "vic_councils_registered": len(self.council_registry),
            "suspicious_tlds": len(self.suspicious_tlds),
            "manipulation_flag_types": len(ManipulationFlag),
            "property_verification_sources": len(PROPERTY_VERIFICATION_SOURCES),
            "url_registry_entries": len(FULL_URL_REGISTRY),
            "url_registry_categories": len(set(u.category for u in FULL_URL_REGISTRY)),
            "compliance_map_sections": len(COMPLIANCE_MAP_SECTIONS),
            "research_steps": len(JOS_RESEARCH_STEPS),
            "security_checklist_items": len(CONNECTION_SECURITY_CHECKLIST),
        }

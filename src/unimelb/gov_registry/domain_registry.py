"""
GOV Domain Registry & Validation Framework
=============================================
Design: Jiadong Chen (陈佳栋) — Student ID: 723912

Implements structured domain validation and research tracking
for Victorian Government (vic.gov.au) and Australian Government (.gov.au)
domains, with certificate verification workflow support.

Based on:
- DOC-20260213-Research-GOV-VIC-0001 (Signature Directive Template)
- DOC-20260213-Research-GOV-VIC-0002 (Search Map Melbourne Gov v1.0)
- DOC-20260212-Research-GOV-RBA-0001 (Search Map RBA Gov v1.0)
- DOC-20260131-Research-Domain-Register-0003 (Domain Register)
- DOC-20260213-JOS-GRID-V2-0004 (J.OS Global Digital Navigation Grid v2.0)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DomainClassification(Enum):
    """Domain classification tiers."""

    VIC_GOV = "vic.gov.au"
    AU_GOV = "gov.au"
    AU_EDU = "edu.au"
    COMMERCIAL = "commercial"
    UNKNOWN = "unknown"


class SearchMode(Enum):
    """Search mode for domain-scoped research."""

    STRICT = "strict"      # Primary gov domain only, HTTPS mandatory
    MERGED = "merged"      # Primary + other .gov.au with labels
    BOUNDARY = "boundary"  # Broader context allowed, labels advisory


class TrafficSignal(Enum):
    """J.OS Digital Signal Traffic status."""

    GREEN = "GREEN"    # Safe / Verified / Compliant
    YELLOW = "YELLOW"  # Public / Review Required
    RED = "RED"        # Restricted / Login / Sensitive / Not Allowed


class VerificationMethod(Enum):
    """Certificate verification methods."""

    BROWSER_INSPECTION = "Browser Certificate Inspection"
    CT_API = "CT API"
    MANUAL_ARCHIVE = "Manual Archive"


class AccuracyLevel(Enum):
    """Research accuracy level."""

    HIGH = "HIGH"      # Official gov domain + 2021–2026 coverage
    MEDIUM = "MEDIUM"  # Partial coverage
    LOW = "LOW"        # Non-government contextual only


@dataclass
class DomainEntry:
    """A single entry in the domain research register."""

    domain_host: str
    count: int
    registrable_domain: str
    research_owner: str = "Donnie Chen"
    research_created_date: str = "2026-01-31"


@dataclass
class CertificateRecord:
    """Security certificate verification record."""

    domain: str
    issuer_organisation: str = ""
    issuer_country: str = ""
    valid_from: str = ""
    valid_to: str = ""
    verification_date: str = ""
    verification_method: VerificationMethod = VerificationMethod.BROWSER_INSPECTION
    verified_by: str = ""


@dataclass
class GovEntity:
    """A government entity in the registry."""

    sector: str
    display_name: str
    legal_name: str = ""
    abn_acn_gov_id: str = ""
    official_url: str = ""
    domain_classification: DomainClassification = DomainClassification.UNKNOWN
    certificate: CertificateRecord | None = None


# =============================================================================
# VIC Government Domain Registry (from DOC-0002 & DOC-0003)
# =============================================================================

VIC_GOV_CATEGORIES: dict[str, list[str]] = {
    "Infrastructure & Major Projects": [
        "bigbuild.vic.gov.au",
        "levelcrossings.vic.gov.au",
        "suburbanrailloop.vic.gov.au",
        "northeastlink.vic.gov.au",
        "westgatetunnelproject.vic.gov.au",
    ],
    "Health": [
        "health.vic.gov.au",
    ],
    "Education": [
        "education.vic.gov.au",
        "schoolbuildings.vic.gov.au",
    ],
    "Housing & Development": [
        "homes.vic.gov.au",
        "development.vic.gov.au",
        "fishermansbend.vic.gov.au",
        "rdv.vic.gov.au",
    ],
    "Transport": [
        "transport.vic.gov.au",
        "ptv.vic.gov.au",
        "vicroads.vic.gov.au",
        "roads.vic.gov.au",
        "regionalroads.vic.gov.au",
    ],
    "Justice": [
        "justice.vic.gov.au",
    ],
    "Environment & Climate": [
        "deeca.vic.gov.au",
        "exploreoutdoors.vic.gov.au",
    ],
    "Finance & Treasury": [
        "dtf.vic.gov.au",
    ],
}

# Domain frequency register (from DOC-0003)
DOMAIN_REGISTER: list[DomainEntry] = [
    DomainEntry("bigbuild.vic.gov.au", 26, "vic.gov.au"),
    DomainEntry("health.vic.gov.au", 24, "vic.gov.au"),
    DomainEntry("www.vhba.vic.gov.au", 19, "vic.gov.au"),
    DomainEntry("levelcrossings.vic.gov.au", 12, "vic.gov.au"),
    DomainEntry("education.vic.gov.au", 12, "vic.gov.au"),
    DomainEntry("www.schoolbuildings.vic.gov.au", 12, "vic.gov.au"),
    DomainEntry("www.homes.vic.gov.au", 8, "vic.gov.au"),
    DomainEntry("homes.vic.gov.au", 8, "vic.gov.au"),
    DomainEntry("www.vic.gov.au", 5, "vic.gov.au"),
    DomainEntry("northeastlink.vic.gov.au", 4, "vic.gov.au"),
    DomainEntry("transport.vic.gov.au", 4, "vic.gov.au"),
    DomainEntry("www.development.vic.gov.au", 3, "vic.gov.au"),
    DomainEntry("suburbanrailloop.vic.gov.au", 2, "vic.gov.au"),
    DomainEntry("srla.vic.gov.au", 2, "vic.gov.au"),
    DomainEntry("justice.vic.gov.au", 2, "vic.gov.au"),
    DomainEntry("www.rdv.vic.gov.au", 2, "vic.gov.au"),
    DomainEntry("dcceew.gov.au", 2, "dcceew.gov.au"),
    DomainEntry("rdv.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("wgta.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("deeca.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("roads.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("federalfinancialrelations.gov.au", 1, "federalfinancialrelations.gov.au"),
    DomainEntry("www.exploreoutdoors.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("www.nationalwatergrid.gov.au", 1, "nationalwatergrid.gov.au"),
    DomainEntry("westgatetunnelproject.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("www.ptv.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("www.vicroads.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("csba.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("regionalroads.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("www.fishermansbend.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("carparks.vic.gov.au", 1, "vic.gov.au"),
    DomainEntry("www.dtf.vic.gov.au", 1, "vic.gov.au"),
]


class GovDomainRegistry:
    """
    Government Domain Registry & Validation Framework.

    Provides structured domain validation, classification, and research
    tracking for Victorian and Australian Government domains.

    Implements the three-step cross-check protocol (1+1+1):
    Step 1: Domain Verification
    Step 2: Extraction
    Step 3: Comparison Audit
    """

    def __init__(self, search_mode: SearchMode = SearchMode.MERGED) -> None:
        self.search_mode = search_mode
        self.domain_register = DOMAIN_REGISTER
        self.vic_categories = VIC_GOV_CATEGORIES
        self.entities: list[GovEntity] = []
        self.certificates: list[CertificateRecord] = []

    def classify_domain(self, domain: str) -> DomainClassification:
        """Classify a domain according to government domain validation rules."""
        domain_lower = domain.lower().strip()
        if domain_lower.endswith(".vic.gov.au"):
            return DomainClassification.VIC_GOV
        if domain_lower.endswith(".gov.au"):
            return DomainClassification.AU_GOV
        if domain_lower.endswith(".edu.au"):
            return DomainClassification.AU_EDU
        return DomainClassification.COMMERCIAL

    def get_traffic_signal(self, domain: str, has_https: bool = True) -> TrafficSignal:
        """
        Determine J.OS traffic signal for a domain.

        GREEN: HTTPS + official gov/edu domain
        YELLOW: Commercial, public but review required
        RED: No HTTPS, login required, or suspicious
        """
        if not has_https:
            return TrafficSignal.RED

        classification = self.classify_domain(domain)
        if classification in (DomainClassification.VIC_GOV, DomainClassification.AU_GOV):
            return TrafficSignal.GREEN
        if classification == DomainClassification.AU_EDU:
            return TrafficSignal.GREEN
        return TrafficSignal.YELLOW

    def is_domain_allowed(self, domain: str) -> bool:
        """Check if domain is allowed under current search mode."""
        classification = self.classify_domain(domain)

        if self.search_mode == SearchMode.STRICT:
            return classification == DomainClassification.VIC_GOV

        if self.search_mode == SearchMode.MERGED:
            return classification in (
                DomainClassification.VIC_GOV,
                DomainClassification.AU_GOV,
            )

        # BOUNDARY mode — all allowed with labels
        return True

    def get_source_label(self, domain: str) -> str:
        """Get the source classification label for a domain."""
        classification = self.classify_domain(domain)
        label_map = {
            DomainClassification.VIC_GOV: "VIC Gov Primary",
            DomainClassification.AU_GOV: "Other AU Gov",
            DomainClassification.AU_EDU: "AU Education",
            DomainClassification.COMMERCIAL: "Non-gov Context",
            DomainClassification.UNKNOWN: "Non-gov Context",
        }
        return label_map[classification]

    def get_category_for_domain(self, domain: str) -> str:
        """Find the VIC Gov category for a given domain."""
        domain_lower = domain.lower().strip()
        for category, domains in self.vic_categories.items():
            if domain_lower in domains:
                return category
        return "Uncategorised"

    def get_domain_frequency(self, domain: str) -> int:
        """Get the research frequency count for a domain."""
        for entry in self.domain_register:
            if entry.domain_host == domain:
                return entry.count
        return 0

    def get_top_domains(self, n: int = 10) -> list[DomainEntry]:
        """Get the top N most-researched domains by frequency."""
        sorted_entries = sorted(self.domain_register, key=lambda e: e.count, reverse=True)
        return sorted_entries[:n]

    def get_domains_by_registrable(self, registrable: str) -> list[DomainEntry]:
        """Get all domain entries under a registrable domain."""
        return [
            entry for entry in self.domain_register
            if entry.registrable_domain == registrable
        ]

    def get_vic_gov_domains(self) -> list[DomainEntry]:
        """Get all vic.gov.au domain entries."""
        return self.get_domains_by_registrable("vic.gov.au")

    def get_total_research_hits(self) -> int:
        """Get total research hits across all domains."""
        return sum(entry.count for entry in self.domain_register)

    def add_entity(self, entity: GovEntity) -> None:
        """Add a government entity to the registry."""
        self.entities.append(entity)

    def add_certificate(self, cert: CertificateRecord) -> None:
        """Add a certificate verification record."""
        self.certificates.append(cert)

    def verify_domain_step1(self, domain: str) -> dict[str, Any]:
        """
        Step 1 of three-step cross-check: Domain Verification.

        - Confirm domain classification
        - Confirm if allowed under search mode
        - Get traffic signal
        """
        classification = self.classify_domain(domain)
        return {
            "domain": domain,
            "classification": classification.value,
            "allowed": self.is_domain_allowed(domain),
            "source_label": self.get_source_label(domain),
            "traffic_signal": self.get_traffic_signal(domain).value,
            "category": self.get_category_for_domain(domain),
            "search_mode": self.search_mode.value,
        }

    def get_registry_summary(self) -> dict[str, Any]:
        """Get a full summary of the domain registry."""
        vic_domains = self.get_vic_gov_domains()
        return {
            "total_domains": len(self.domain_register),
            "total_hits": self.get_total_research_hits(),
            "vic_gov_domains": len(vic_domains),
            "vic_gov_hits": sum(e.count for e in vic_domains),
            "categories": list(self.vic_categories.keys()),
            "search_mode": self.search_mode.value,
            "top_5": [
                {"domain": e.domain_host, "count": e.count}
                for e in self.get_top_domains(5)
            ],
            "entities_registered": len(self.entities),
            "certificates_verified": len(self.certificates),
        }

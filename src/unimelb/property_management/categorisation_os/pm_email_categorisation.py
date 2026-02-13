"""
PM-Email-Categorisation.os v0.2.0 — Master (VIC) — RES + COM
==============================================================
AI-first email and document categorisation operating system for
property management, designed by Jiadong Chen (陈佳栋).

v0.2.0 — Enhanced Stakeholder Model:
- Explicit stakeholder vocab:
    RES: Renters / Rental Providers
    COM: Clients / Landlords / Tenants
- Stakeholder-aware cover-scan, routing, and lock escalation
- Portfolio detection (RES vs COM) from email signals
- Vault escalation for PII / ID documents / applications

Foundation:
- AI-first cover scan: Outlook email + Teams messages/channels +
  calendar invites + attachments + share-folder links
- Deterministic routing: 99-folder tree (RES + COM)
- ID-binding subfolders:
    Portfolio_ID + Building_ID + (TEN_ID or LEASE_ID) + Project_ID
- Locks/Vault:
    L3: finance / legal / disputes / PII
    L4: ID docs / 100 points / core legal evidence packs

Integrates with:
- Microsoft 365 (Outlook / Teams / SharePoint / OneDrive / Planner / Lists)
- MRI Property Tree (Residential + Commercial)
- UniMelb AI Platform (Azure Foundry / Copilot)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PropertyDomain(Enum):
    """Property domain — Residential or Commercial."""

    RES = "RES"
    COM = "COM"


class LockLevel(Enum):
    """Document security lock levels (L0–L4)."""

    L0_PUBLIC = "L0"          # Public / open access
    L1_INTERNAL = "L1"        # Internal team access
    L2_RESTRICTED = "L2"      # Restricted — named staff only
    L3_CONFIDENTIAL = "L3"    # Finance / legal / disputes / PII
    L4_VAULT = "L4"           # ID docs / 100 points / core legal evidence


class FolderCategory(Enum):
    """Top-level folder categories within RES or COM tree."""

    INBOX = "Inbox"
    LEASING = "Leasing"
    LEASE_ADMIN = "LeaseAdmin"
    STAKEHOLDERS = "Stakeholders"
    MAINTENANCE = "Maintenance"
    FACILITIES = "Facilities"
    FINANCE = "Finance"
    COMPLIANCE = "Compliance"
    LEGAL = "Legal"
    INSURANCE = "Insurance"
    VENDORS = "Vendors"
    ASSETS = "Assets"
    BUILDING = "Building"
    SHARED = "Shared"
    TEMPLATES = "Templates"
    KNOWLEDGE = "Knowledge"
    EXPORTS = "Exports"
    ARCHIVE = "Archive"
    REVIEW = "Review"


class Stakeholder(Enum):
    """Stakeholder types — orthogonal to category, influences routing and locks."""

    # Residential
    RES_RENTERS = "RESIDENTIAL.RENTERS"
    RES_RENTAL_PROVIDERS = "RESIDENTIAL.RENTAL_PROVIDERS"
    # Commercial
    COM_CLIENTS = "COMMERCIAL.CLIENTS"
    COM_LANDLORDS = "COMMERCIAL.LANDLORDS"
    COM_TENANTS = "COMMERCIAL.TENANTS"
    # Unknown
    UNKNOWN = "UNKNOWN"


class PMCategory(Enum):
    """PM taxonomy top-level categories (email-centric)."""

    PM_RES = "PM_RES"
    PM_COM = "PM_COM"
    PM_GEN = "PM_GEN"
    GOV_VIC = "GOV_VIC"
    VENDORS = "VENDORS"
    FINANCE = "FINANCE"
    LEGAL = "LEGAL"
    INSURANCE = "INSURANCE"
    UTILITIES = "UTILITIES"
    STRATA_OC = "STRATA_OC"
    SHOWINGS = "SHOWINGS"
    LEASING = "LEASING"
    MAINT = "MAINT"
    TENANCY = "TENANCY"
    BOND_RTBA = "BOND_RTBA"
    ARREARS = "ARREARS"
    SAFETY = "SAFETY"
    IT_DOCS = "IT_DOCS"
    REVIEW = "REVIEW"


# =============================================================================
# Stakeholder keywords for inference (from v0.2.0 schema appendix)
# =============================================================================

STAKEHOLDER_KEYWORDS: dict[str, list[str]] = {
    "RESIDENTIAL.RENTERS": [
        "renter", "tenant", "applicant", "application",
        "maintenance request", "bond refund", "condition report",
    ],
    "RESIDENTIAL.RENTAL_PROVIDERS": [
        "rental provider", "owner", "landlord",
        "owner approval", "owner instructions",
    ],
    "COMMERCIAL.TENANTS": [
        "tenant", "lessee", "occupier",
        "fitout", "make good", "access request",
    ],
    "COMMERCIAL.LANDLORDS": [
        "landlord", "lessor", "asset owner", "owner approval",
    ],
    "COMMERCIAL.CLIENTS": [
        "client", "portfolio", "asset management",
        "reporting pack", "capex", "budget",
    ],
}

# Portfolio detection keywords
PORTFOLIO_COMMERCIAL_KEYWORDS = [
    "outgoings", "cpi", "make good", "fitout", "option",
    "rent review", "lease admin", "occupier", "lessee", "lessor",
]
PORTFOLIO_RESIDENTIAL_KEYWORDS = [
    "renter", "bond", "rtba", "routine inspection",
    "entry notice", "fixed term", "rent increase",
    "rental provider", "condition report", "notice of entry",
]

# Vault escalation keyword groups (from v0.2.0 locks section)
VAULT_L4_KEYWORDS = [
    "passport", "visa", "immi", "home affairs", "bdm",
    "births deaths marriages", "tenant application", "application",
    "100 points", "id document", "driver licence", "medicare card",
    "bank statement", "payslip", "pay slip", "proof of identity",
]
LOCK_L3_KEYWORDS = [
    "rent arrears", "breach notice", "notice to vacate", "vcat",
    "tribunal", "police", "insurance claim", "bond claim",
    "compensation", "privacy", "complaint",
]

# Stakeholder routing folder map
STAKEHOLDER_FOLDER_MAP: dict[str, str] = {
    "RESIDENTIAL.RENTERS": "RES/20_Stakeholders/Renters/",
    "RESIDENTIAL.RENTAL_PROVIDERS": "RES/21_Stakeholders/Rental_Providers/",
    "COMMERCIAL.CLIENTS": "COM/20_Stakeholders/Clients/",
    "COMMERCIAL.LANDLORDS": "COM/21_Stakeholders/Landlords/",
    "COMMERCIAL.TENANTS": "COM/22_Stakeholders/Tenants/",
}

VAULT_FOLDER_MAP: dict[str, str] = {
    "RESIDENTIAL.RENTERS": "VAULT/Residential/Renters_ID_Applications/",
    "RESIDENTIAL.RENTAL_PROVIDERS": "VAULT/Residential/Rental_Providers_PII/",
    "COMMERCIAL.CLIENTS": "VAULT/Commercial/Clients_Confidential/",
    "COMMERCIAL.LANDLORDS": "VAULT/Commercial/Landlords_Confidential/",
    "COMMERCIAL.TENANTS": "VAULT/Commercial/Tenants_Confidential/",
}

# PMOS labels
PMOS_LABELS: dict[str, list[str]] = {
    "base": [
        "PMOS/PROFESSIONAL", "PMOS/RESIDENTIAL", "PMOS/COMMERCIAL",
        "PMOS/LOCK-L1", "PMOS/LOCK-L2", "PMOS/LOCK-L3", "PMOS/LOCK-L4-VAULT",
        "PMOS/REVIEW",
    ],
    "stakeholder": [
        "PMOS/RES-RENTERS", "PMOS/RES-RENTAL_PROVIDERS",
        "PMOS/COM-CLIENTS", "PMOS/COM-LANDLORDS", "PMOS/COM-TENANTS",
    ],
    "category": [
        "PMOS/LEASING", "PMOS/MAINT", "PMOS/SHOWINGS", "PMOS/FINANCE",
        "PMOS/LEGAL", "PMOS/ARREARS", "PMOS/BOND-RTBA", "PMOS/INSURANCE",
        "PMOS/STRATA-OC", "PMOS/UTILITIES", "PMOS/VENDORS", "PMOS/GOV-VIC",
        "PMOS/SAFETY", "PMOS/IT-DOCS",
    ],
}


@dataclass
class CoverScanResult:
    """Output of Stage-0 cover scan (stakeholder-aware)."""

    pm_category_top: str = ""
    pm_category_sub: str = ""
    portfolio_guess: str = "UNKNOWN"
    stakeholder_primary: str = "UNKNOWN"
    stakeholder_secondary: str = "NONE"
    lock_level_guess: str = "L1"
    labels: list[str] = field(default_factory=list)
    routing_folder: str = ""
    needs_deep_extraction: bool = False
    rationale: list[str] = field(default_factory=list)


@dataclass
class FolderDefinition:
    """Definition of a single folder in the 99-folder tree."""

    number: int               # 01–99
    path: str                 # e.g. "30_Maintenance_NewRequests"
    category: FolderCategory
    description: str
    lock_level: LockLevel = LockLevel.L1_INTERNAL
    stakeholder_tag: str = ""  # RES: Renters/RentalProviders; COM: Tenants/Landlords/Clients
    auto_route_keywords: list[str] = field(default_factory=list)


@dataclass
class IDFormat:
    """Standard ID format definitions for property management."""

    portfolio_id_res: str = "PORT-PM-MEL-RES-{NNNN}"
    portfolio_id_com: str = "PORT-PM-MEL-COM-{NNNN}"
    building_id: str = "BLD-{SUBURB}-{STREETNO}-{STREETNAME}-{NNN}"
    tenant_id: str = "TEN-{YYYY}-{NNNN}"
    lease_id: str = "LEASE-{YYYY}-{NNNN}"
    project_id: str = "PRJ-{YYYYMMDD}-{SHORT}-{NN}"

    @staticmethod
    def folder_binding_base(portfolio_id: str, building_id: str) -> str:
        return f"{portfolio_id}__{building_id}/"

    @staticmethod
    def folder_binding_case(
        portfolio_id: str, building_id: str, ten_or_lease_id: str
    ) -> str:
        return f"{portfolio_id}__{building_id}__{ten_or_lease_id}/"

    @staticmethod
    def folder_binding_project(
        portfolio_id: str,
        building_id: str,
        ten_or_lease_id: str,
        project_id: str,
    ) -> str:
        return f"{portfolio_id}__{building_id}__{ten_or_lease_id}__{project_id}/"


# =============================================================================
# RES Tree — 99 folders (Residential Property Management)
# =============================================================================

RES_FOLDER_TREE: list[FolderDefinition] = [
    # Inbox (01–09)
    FolderDefinition(1, "01_Inbox_New", FolderCategory.INBOX, "New unprocessed emails", auto_route_keywords=["new", "incoming"]),
    FolderDefinition(2, "02_Inbox_Triage_Today", FolderCategory.INBOX, "Items to be triaged today"),
    FolderDefinition(3, "03_Inbox_Triage_ThisWeek", FolderCategory.INBOX, "Items to be triaged this week"),
    FolderDefinition(4, "04_Inbox_WaitingOnRenter", FolderCategory.INBOX, "Awaiting renter response", stakeholder_tag="Renters"),
    FolderDefinition(5, "05_Inbox_WaitingOnRentalProvider", FolderCategory.INBOX, "Awaiting rental provider response", stakeholder_tag="RentalProviders"),
    FolderDefinition(6, "06_Inbox_WaitingOnVendor", FolderCategory.INBOX, "Awaiting vendor/contractor response", stakeholder_tag="Vendors"),
    FolderDefinition(7, "07_Inbox_WaitingOnAgency_Internal", FolderCategory.INBOX, "Awaiting internal team response"),
    FolderDefinition(8, "08_Inbox_WaitingOnGov_Regulator", FolderCategory.INBOX, "Awaiting government/regulator response", stakeholder_tag="Government"),
    FolderDefinition(9, "09_Inbox_Completed_ToFile", FolderCategory.INBOX, "Completed items ready to file"),

    # Leasing (10–19)
    FolderDefinition(10, "10_Leasing_Applications_Received", FolderCategory.LEASING, "New rental applications received", auto_route_keywords=["application", "apply"]),
    FolderDefinition(11, "11_Leasing_Applications_Screening", FolderCategory.LEASING, "Applications under screening"),
    FolderDefinition(12, "12_Leasing_Applications_ID_VaultPointer", FolderCategory.LEASING, "ID documents vault pointer", lock_level=LockLevel.L4_VAULT),
    FolderDefinition(13, "13_Leasing_Applications_ReferenceChecks", FolderCategory.LEASING, "Reference checks in progress"),
    FolderDefinition(14, "14_Leasing_Offer_Approval_RentalProvider", FolderCategory.LEASING, "Offer sent for rental provider approval", stakeholder_tag="RentalProviders"),
    FolderDefinition(15, "15_Leasing_LeaseDocs_Signing", FolderCategory.LEASING, "Lease documents for signing", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(16, "16_Leasing_MoveIn_Keys_Access", FolderCategory.LEASING, "Move-in coordination, keys, access"),
    FolderDefinition(17, "17_Leasing_ConditionReport_Entry", FolderCategory.LEASING, "Entry condition reports"),
    FolderDefinition(18, "18_Leasing_RentIncrease_Notices", FolderCategory.LEASING, "Rent increase notices", auto_route_keywords=["rent increase", "rent review"]),
    FolderDefinition(19, "19_Leasing_Renewals_FixedTerm", FolderCategory.LEASING, "Lease renewals and fixed-term extensions"),

    # Stakeholders (20–29)
    FolderDefinition(20, "20_Stakeholders_Renters_Comms", FolderCategory.STAKEHOLDERS, "Renter communications", stakeholder_tag="Renters"),
    FolderDefinition(21, "21_Stakeholders_RentalProviders_Comms", FolderCategory.STAKEHOLDERS, "Rental provider communications", stakeholder_tag="RentalProviders"),
    FolderDefinition(22, "22_Stakeholders_Neighbours_Strata_Other", FolderCategory.STAKEHOLDERS, "Neighbours, strata, other parties"),
    FolderDefinition(23, "23_Stakeholders_UtilityProviders", FolderCategory.STAKEHOLDERS, "Utility provider communications"),
    FolderDefinition(24, "24_Stakeholders_Contractors_Suppliers", FolderCategory.STAKEHOLDERS, "Contractor and supplier communications", stakeholder_tag="Vendors"),
    FolderDefinition(25, "25_Stakeholders_BuildingManagement_OwnersCorp", FolderCategory.STAKEHOLDERS, "Building management and owners corporation"),
    FolderDefinition(26, "26_Stakeholders_Insurance_Brokers", FolderCategory.STAKEHOLDERS, "Insurance broker communications"),
    FolderDefinition(27, "27_Stakeholders_Legal_Advisers", FolderCategory.STAKEHOLDERS, "Legal adviser communications", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(28, "28_Stakeholders_Government_Regulators", FolderCategory.STAKEHOLDERS, "Government and regulator communications", stakeholder_tag="Government"),
    FolderDefinition(29, "29_Stakeholders_Internal_Team", FolderCategory.STAKEHOLDERS, "Internal team communications"),

    # Maintenance (30–39)
    FolderDefinition(30, "30_Maintenance_NewRequests", FolderCategory.MAINTENANCE, "New maintenance requests", auto_route_keywords=["maintenance", "repair", "broken", "fix"]),
    FolderDefinition(31, "31_Maintenance_UrgentRepairs", FolderCategory.MAINTENANCE, "Urgent repairs (24hr response)", auto_route_keywords=["urgent", "emergency", "flood", "leak", "gas"]),
    FolderDefinition(32, "32_Maintenance_NonUrgentRepairs", FolderCategory.MAINTENANCE, "Non-urgent repairs"),
    FolderDefinition(33, "33_Maintenance_Quotes_Approvals", FolderCategory.MAINTENANCE, "Quotes and approval requests"),
    FolderDefinition(34, "34_Maintenance_WorkOrders_Issued", FolderCategory.MAINTENANCE, "Work orders issued to contractors"),
    FolderDefinition(35, "35_Maintenance_WorkInProgress", FolderCategory.MAINTENANCE, "Work currently in progress"),
    FolderDefinition(36, "36_Maintenance_WorkCompleted", FolderCategory.MAINTENANCE, "Completed maintenance work"),
    FolderDefinition(37, "37_Maintenance_Compliance_Certificates", FolderCategory.MAINTENANCE, "Compliance certificates (smoke alarms, gas, electrical)"),
    FolderDefinition(38, "38_Maintenance_Photos_Evidence", FolderCategory.MAINTENANCE, "Maintenance photos and evidence"),
    FolderDefinition(39, "39_Maintenance_FollowUps_Defects", FolderCategory.MAINTENANCE, "Follow-ups and defect rectification"),

    # Finance (40–49)
    FolderDefinition(40, "40_Finance_Invoices_In", FolderCategory.FINANCE, "Incoming invoices", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(41, "41_Finance_Remittances_Out", FolderCategory.FINANCE, "Outgoing remittances/payments", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(42, "42_Finance_Rent_Receipting", FolderCategory.FINANCE, "Rent receipting records", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(43, "43_Finance_Arrears_Statements", FolderCategory.FINANCE, "Arrears and overdue statements", lock_level=LockLevel.L3_CONFIDENTIAL, auto_route_keywords=["arrears", "overdue", "late payment"]),
    FolderDefinition(44, "44_Finance_Trust_Disbursements", FolderCategory.FINANCE, "Trust account disbursements", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(45, "45_Finance_Reconciliations", FolderCategory.FINANCE, "Financial reconciliations", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(46, "46_Finance_Fees_Management", FolderCategory.FINANCE, "Management fees", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(47, "47_Finance_Refunds_Adjustments", FolderCategory.FINANCE, "Refunds and adjustments", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(48, "48_Finance_PaymentPlans", FolderCategory.FINANCE, "Payment plan arrangements", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(49, "49_Finance_Tax_Statements_Summaries", FolderCategory.FINANCE, "Tax statements and annual summaries", lock_level=LockLevel.L3_CONFIDENTIAL),

    # Compliance (50–59)
    FolderDefinition(50, "50_Compliance_SmokeAlarms", FolderCategory.COMPLIANCE, "Smoke alarm compliance"),
    FolderDefinition(51, "51_Compliance_GasElectrical", FolderCategory.COMPLIANCE, "Gas and electrical safety compliance"),
    FolderDefinition(52, "52_Compliance_PoolSpa", FolderCategory.COMPLIANCE, "Pool and spa barrier compliance"),
    FolderDefinition(53, "53_Compliance_MinimumStandards", FolderCategory.COMPLIANCE, "Minimum rental standards compliance"),
    FolderDefinition(54, "54_Compliance_Keys_Access_Control", FolderCategory.COMPLIANCE, "Keys and access control records"),
    FolderDefinition(55, "55_Compliance_Privacy_PII_Handling", FolderCategory.COMPLIANCE, "Privacy and PII handling records", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(56, "56_Compliance_Entry_Notices", FolderCategory.COMPLIANCE, "Entry notices (s91–92 RTA)"),
    FolderDefinition(57, "57_Compliance_Mould_WaterIngress", FolderCategory.COMPLIANCE, "Mould and water ingress issues"),
    FolderDefinition(58, "58_Compliance_Safety_Hazards", FolderCategory.COMPLIANCE, "Safety hazard reports"),
    FolderDefinition(59, "59_Compliance_Audit_Checklists", FolderCategory.COMPLIANCE, "Compliance audit checklists"),

    # Legal (60–69)
    FolderDefinition(60, "60_Legal_VCAT_Preparation", FolderCategory.LEGAL, "VCAT case preparation", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(61, "61_Legal_VCAT_Applications", FolderCategory.LEGAL, "VCAT applications filed", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(62, "62_Legal_VCAT_Hearings_Orders", FolderCategory.LEGAL, "VCAT hearings and orders", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(63, "63_Legal_Breach_Notices", FolderCategory.LEGAL, "Breach of duty notices", lock_level=LockLevel.L3_CONFIDENTIAL, auto_route_keywords=["breach", "notice to remedy"]),
    FolderDefinition(64, "64_Legal_NoticeToVacate", FolderCategory.LEGAL, "Notice to vacate", lock_level=LockLevel.L3_CONFIDENTIAL, auto_route_keywords=["notice to vacate", "NTV", "eviction"]),
    FolderDefinition(65, "65_Legal_EndOfLease_ExitDisputes", FolderCategory.LEGAL, "End of lease and exit disputes", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(66, "66_Legal_Complaints_External", FolderCategory.LEGAL, "External complaints", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(67, "67_Legal_Police_Reports", FolderCategory.LEGAL, "Police reports", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(68, "68_Legal_Mediation_Settlement", FolderCategory.LEGAL, "Mediation and settlement", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(69, "69_Legal_Evidence_Index", FolderCategory.LEGAL, "Legal evidence index and packs", lock_level=LockLevel.L4_VAULT),

    # Insurance (70–79)
    FolderDefinition(70, "70_Insurance_NewClaims", FolderCategory.INSURANCE, "New insurance claims", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(71, "71_Insurance_ClaimNumbers_Register", FolderCategory.INSURANCE, "Claim numbers register", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(72, "72_Insurance_LossAdjuster_Comms", FolderCategory.INSURANCE, "Loss adjuster communications", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(73, "73_Insurance_Quotes_ScopeOfWorks", FolderCategory.INSURANCE, "Insurance quotes and scope of works"),
    FolderDefinition(74, "74_Insurance_Excess_Recovery", FolderCategory.INSURANCE, "Excess recovery", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(75, "75_Insurance_Repairs_Managed", FolderCategory.INSURANCE, "Insurance-managed repairs"),
    FolderDefinition(76, "76_Insurance_Declines_Disputes", FolderCategory.INSURANCE, "Insurance declines and disputes", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(77, "77_Insurance_IncidentReports", FolderCategory.INSURANCE, "Incident reports"),
    FolderDefinition(78, "78_Insurance_Photos_Evidence", FolderCategory.INSURANCE, "Insurance photos and evidence"),
    FolderDefinition(79, "79_Insurance_CloseOuts", FolderCategory.INSURANCE, "Insurance claim close-outs"),

    # Vendors (80–84)
    FolderDefinition(80, "80_Vendors_Preferred_List", FolderCategory.VENDORS, "Preferred vendor/contractor list"),
    FolderDefinition(81, "81_Vendors_Onboarding_ABN_Insurance", FolderCategory.VENDORS, "Vendor onboarding: ABN, insurance, compliance"),
    FolderDefinition(82, "82_Vendors_Compliance_Licences", FolderCategory.VENDORS, "Vendor compliance and licence records"),
    FolderDefinition(83, "83_Vendors_WorkQuality_Issues", FolderCategory.VENDORS, "Work quality issues and escalations"),
    FolderDefinition(84, "84_Vendors_ServiceReports", FolderCategory.VENDORS, "Vendor service reports"),

    # Assets & Building (85–87)
    FolderDefinition(85, "85_Assets_Appliances_Warranties", FolderCategory.ASSETS, "Appliance registers and warranties"),
    FolderDefinition(86, "86_Assets_Keys_Locks_Records", FolderCategory.ASSETS, "Keys and locks records"),
    FolderDefinition(87, "87_Building_OwnersCorp_Meetings_Minutes", FolderCategory.BUILDING, "Owners corporation meetings and minutes"),

    # Shared / Templates / Knowledge (88–94)
    FolderDefinition(88, "88_SharedLinks_PortalExports", FolderCategory.SHARED, "Shared links and portal exports"),
    FolderDefinition(89, "89_Templates_Forms_Scripts", FolderCategory.TEMPLATES, "Templates, forms, and scripts"),
    FolderDefinition(90, "90_Knowledge_Policies_Procedures", FolderCategory.KNOWLEDGE, "Policies and procedures"),
    FolderDefinition(91, "91_Knowledge_Checklists", FolderCategory.KNOWLEDGE, "Operational checklists"),
    FolderDefinition(92, "92_Knowledge_Email_Templates", FolderCategory.KNOWLEDGE, "Email templates"),
    FolderDefinition(93, "93_Knowledge_VCAT_Packs", FolderCategory.KNOWLEDGE, "VCAT preparation packs", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(94, "94_Knowledge_Compliance_Standards", FolderCategory.KNOWLEDGE, "Compliance standards reference"),

    # Exports & Archive (95–99)
    FolderDefinition(95, "95_Exports_Reports_Monthly", FolderCategory.EXPORTS, "Monthly reports"),
    FolderDefinition(96, "96_Exports_Reports_Quarterly", FolderCategory.EXPORTS, "Quarterly reports"),
    FolderDefinition(97, "97_Exports_Reports_Annual", FolderCategory.EXPORTS, "Annual reports"),
    FolderDefinition(98, "98_Archive_ClosedMatters", FolderCategory.ARCHIVE, "Archived closed matters"),
    FolderDefinition(99, "99_Review_Quarantine_Unclear", FolderCategory.REVIEW, "Quarantine: unclear items for review"),
]


# =============================================================================
# COM Tree — 99 folders (Commercial Property Management)
# =============================================================================

COM_FOLDER_TREE: list[FolderDefinition] = [
    # Inbox (01–09)
    FolderDefinition(1, "01_Inbox_New", FolderCategory.INBOX, "New unprocessed emails"),
    FolderDefinition(2, "02_Inbox_Triage_Today", FolderCategory.INBOX, "Items to be triaged today"),
    FolderDefinition(3, "03_Inbox_Triage_ThisWeek", FolderCategory.INBOX, "Items to be triaged this week"),
    FolderDefinition(4, "04_Inbox_WaitingOnTenant", FolderCategory.INBOX, "Awaiting tenant response", stakeholder_tag="Tenants"),
    FolderDefinition(5, "05_Inbox_WaitingOnLandlord", FolderCategory.INBOX, "Awaiting landlord response", stakeholder_tag="Landlords"),
    FolderDefinition(6, "06_Inbox_WaitingOnClient", FolderCategory.INBOX, "Awaiting client response", stakeholder_tag="Clients"),
    FolderDefinition(7, "07_Inbox_WaitingOnVendor", FolderCategory.INBOX, "Awaiting vendor/contractor response"),
    FolderDefinition(8, "08_Inbox_WaitingOnBuildingOps", FolderCategory.INBOX, "Awaiting building ops response"),
    FolderDefinition(9, "09_Inbox_Completed_ToFile", FolderCategory.INBOX, "Completed items ready to file"),

    # Lease Admin (10–19)
    FolderDefinition(10, "10_LeaseAdmin_NewRequests", FolderCategory.LEASE_ADMIN, "New lease administration requests"),
    FolderDefinition(11, "11_LeaseAdmin_Documents_Executed", FolderCategory.LEASE_ADMIN, "Executed lease documents", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(12, "12_LeaseAdmin_Variations_Deeds", FolderCategory.LEASE_ADMIN, "Lease variations and deeds of variation", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(13, "13_LeaseAdmin_Options_Exercise", FolderCategory.LEASE_ADMIN, "Option exercise and renewal", auto_route_keywords=["option", "exercise", "renewal"]),
    FolderDefinition(14, "14_LeaseAdmin_RentReview_CPI_Market", FolderCategory.LEASE_ADMIN, "Rent reviews: CPI and market", auto_route_keywords=["rent review", "CPI", "market review"]),
    FolderDefinition(15, "15_LeaseAdmin_Outgoings_Budgets", FolderCategory.LEASE_ADMIN, "Outgoings budgets and estimates", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(16, "16_LeaseAdmin_Reconciliations_Outgoings", FolderCategory.LEASE_ADMIN, "Outgoings reconciliations", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(17, "17_LeaseAdmin_MakeGood", FolderCategory.LEASE_ADMIN, "Make-good obligations and works"),
    FolderDefinition(18, "18_LeaseAdmin_Fitout_Works_Approvals", FolderCategory.LEASE_ADMIN, "Fitout works and approvals"),
    FolderDefinition(19, "19_LeaseAdmin_Access_Security_Passes", FolderCategory.LEASE_ADMIN, "Access and security pass management"),

    # Stakeholders (20–29)
    FolderDefinition(20, "20_Stakeholders_Tenants_Comms", FolderCategory.STAKEHOLDERS, "Tenant communications", stakeholder_tag="Tenants"),
    FolderDefinition(21, "21_Stakeholders_Landlords_Comms", FolderCategory.STAKEHOLDERS, "Landlord communications", stakeholder_tag="Landlords"),
    FolderDefinition(22, "22_Stakeholders_Clients_Comms", FolderCategory.STAKEHOLDERS, "Client communications", stakeholder_tag="Clients"),
    FolderDefinition(23, "23_Stakeholders_Facilities_BuildingOps", FolderCategory.STAKEHOLDERS, "Facilities and building operations"),
    FolderDefinition(24, "24_Stakeholders_BMS_Security_Providers", FolderCategory.STAKEHOLDERS, "BMS and security providers"),
    FolderDefinition(25, "25_Stakeholders_Contractors_Suppliers", FolderCategory.STAKEHOLDERS, "Contractor and supplier communications"),
    FolderDefinition(26, "26_Stakeholders_Insurance_Brokers", FolderCategory.STAKEHOLDERS, "Insurance broker communications"),
    FolderDefinition(27, "27_Stakeholders_Legal_Advisers", FolderCategory.STAKEHOLDERS, "Legal adviser communications", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(28, "28_Stakeholders_Government_Regulators", FolderCategory.STAKEHOLDERS, "Government and regulator communications"),
    FolderDefinition(29, "29_Stakeholders_Internal_Team", FolderCategory.STAKEHOLDERS, "Internal team communications"),

    # Facilities (30–39)
    FolderDefinition(30, "30_Facilities_NewRequests", FolderCategory.FACILITIES, "New facility requests", auto_route_keywords=["maintenance", "facility", "repair"]),
    FolderDefinition(31, "31_Facilities_UrgentRepairs", FolderCategory.FACILITIES, "Urgent repairs (24hr response)", auto_route_keywords=["urgent", "emergency"]),
    FolderDefinition(32, "32_Facilities_PPM_ScheduledMaintenance", FolderCategory.FACILITIES, "Planned preventive maintenance (PPM)"),
    FolderDefinition(33, "33_Facilities_Quotes_Approvals", FolderCategory.FACILITIES, "Quotes and approval requests"),
    FolderDefinition(34, "34_Facilities_WorkOrders_Issued", FolderCategory.FACILITIES, "Work orders issued"),
    FolderDefinition(35, "35_Facilities_WorkInProgress", FolderCategory.FACILITIES, "Work in progress"),
    FolderDefinition(36, "36_Facilities_WorkCompleted", FolderCategory.FACILITIES, "Completed works"),
    FolderDefinition(37, "37_Facilities_Compliance_Certificates", FolderCategory.FACILITIES, "Compliance certificates"),
    FolderDefinition(38, "38_Facilities_Photos_Evidence", FolderCategory.FACILITIES, "Facilities photos and evidence"),
    FolderDefinition(39, "39_Facilities_Defects_Snagging", FolderCategory.FACILITIES, "Defects and snagging lists"),

    # Finance (40–49)
    FolderDefinition(40, "40_Finance_Invoices_In", FolderCategory.FINANCE, "Incoming invoices", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(41, "41_Finance_Remittances_Out", FolderCategory.FINANCE, "Outgoing remittances", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(42, "42_Finance_Rent_Receipting", FolderCategory.FINANCE, "Rent receipting records", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(43, "43_Finance_Arrears_Statements", FolderCategory.FINANCE, "Arrears and overdue statements", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(44, "44_Finance_Outgoings_Charges", FolderCategory.FINANCE, "Outgoings charges", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(45, "45_Finance_Reconciliations", FolderCategory.FINANCE, "Financial reconciliations", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(46, "46_Finance_ClientFees_ManagementFees", FolderCategory.FINANCE, "Client and management fees", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(47, "47_Finance_Adjustments_Credits", FolderCategory.FINANCE, "Adjustments and credits", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(48, "48_Finance_PaymentPlans", FolderCategory.FINANCE, "Payment plan arrangements", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(49, "49_Finance_Tax_Statements_Summaries", FolderCategory.FINANCE, "Tax statements and summaries", lock_level=LockLevel.L3_CONFIDENTIAL),

    # Compliance (50–59)
    FolderDefinition(50, "50_Compliance_FireLifeSafety", FolderCategory.COMPLIANCE, "Fire and life safety compliance"),
    FolderDefinition(51, "51_Compliance_Electrical_Gas", FolderCategory.COMPLIANCE, "Electrical and gas safety"),
    FolderDefinition(52, "52_Compliance_Lifts_Escalators", FolderCategory.COMPLIANCE, "Lifts and escalators compliance"),
    FolderDefinition(53, "53_Compliance_EssentialServices_MaintLogs", FolderCategory.COMPLIANCE, "Essential services maintenance logs"),
    FolderDefinition(54, "54_Compliance_AccessControl_Security", FolderCategory.COMPLIANCE, "Access control and security"),
    FolderDefinition(55, "55_Compliance_Privacy_PII_Handling", FolderCategory.COMPLIANCE, "Privacy and PII handling", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(56, "56_Compliance_Permits_Fitout", FolderCategory.COMPLIANCE, "Permits and fitout approvals"),
    FolderDefinition(57, "57_Compliance_Environmental_Hazards", FolderCategory.COMPLIANCE, "Environmental hazards (asbestos, etc.)"),
    FolderDefinition(58, "58_Compliance_Safety_Hazards", FolderCategory.COMPLIANCE, "Safety hazard reports"),
    FolderDefinition(59, "59_Compliance_Audit_Checklists", FolderCategory.COMPLIANCE, "Compliance audit checklists"),

    # Legal (60–69)
    FolderDefinition(60, "60_Legal_Disputes_Notices", FolderCategory.LEGAL, "Disputes and formal notices", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(61, "61_Legal_Defaults_Arrears", FolderCategory.LEGAL, "Defaults and arrears actions", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(62, "62_Legal_Enforcement_Recovery", FolderCategory.LEGAL, "Enforcement and debt recovery", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(63, "63_Legal_MakeGood_Disputes", FolderCategory.LEGAL, "Make-good disputes", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(64, "64_Legal_Assignments_Subleases", FolderCategory.LEGAL, "Lease assignments and subleases", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(65, "65_Legal_Claims_Litigation", FolderCategory.LEGAL, "Claims and litigation", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(66, "66_Legal_Regulatory_Compliance", FolderCategory.LEGAL, "Regulatory compliance matters", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(67, "67_Legal_Police_Reports", FolderCategory.LEGAL, "Police reports", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(68, "68_Legal_Mediation_Settlement", FolderCategory.LEGAL, "Mediation and settlement", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(69, "69_Legal_Evidence_Index", FolderCategory.LEGAL, "Legal evidence index", lock_level=LockLevel.L4_VAULT),

    # Insurance (70–79)
    FolderDefinition(70, "70_Insurance_NewClaims", FolderCategory.INSURANCE, "New insurance claims", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(71, "71_Insurance_ClaimNumbers_Register", FolderCategory.INSURANCE, "Claim numbers register", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(72, "72_Insurance_LossAdjuster_Comms", FolderCategory.INSURANCE, "Loss adjuster communications", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(73, "73_Insurance_Quotes_ScopeOfWorks", FolderCategory.INSURANCE, "Insurance quotes and scope of works"),
    FolderDefinition(74, "74_Insurance_Excess_Recovery", FolderCategory.INSURANCE, "Excess recovery", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(75, "75_Insurance_Repairs_Managed", FolderCategory.INSURANCE, "Insurance-managed repairs"),
    FolderDefinition(76, "76_Insurance_Declines_Disputes", FolderCategory.INSURANCE, "Insurance declines and disputes", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(77, "77_Insurance_IncidentReports", FolderCategory.INSURANCE, "Incident reports"),
    FolderDefinition(78, "78_Insurance_Photos_Evidence", FolderCategory.INSURANCE, "Insurance photos and evidence"),
    FolderDefinition(79, "79_Insurance_CloseOuts", FolderCategory.INSURANCE, "Insurance claim close-outs"),

    # Vendors (80–84)
    FolderDefinition(80, "80_Vendors_Preferred_List", FolderCategory.VENDORS, "Preferred vendor list"),
    FolderDefinition(81, "81_Vendors_Onboarding_ABN_Insurance", FolderCategory.VENDORS, "Vendor onboarding: ABN, insurance"),
    FolderDefinition(82, "82_Vendors_Compliance_Licences", FolderCategory.VENDORS, "Vendor compliance and licences"),
    FolderDefinition(83, "83_Vendors_WorkQuality_Issues", FolderCategory.VENDORS, "Work quality issues"),
    FolderDefinition(84, "84_Vendors_ServiceReports", FolderCategory.VENDORS, "Vendor service reports"),

    # Assets & Building (85–87)
    FolderDefinition(85, "85_Assets_Equipment_Warranties", FolderCategory.ASSETS, "Equipment registers and warranties"),
    FolderDefinition(86, "86_Assets_AccessCards_Keys_Records", FolderCategory.ASSETS, "Access cards and keys records"),
    FolderDefinition(87, "87_BuildingOps_Meetings_Minutes", FolderCategory.BUILDING, "Building ops meetings and minutes"),

    # Shared / Templates / Knowledge (88–94)
    FolderDefinition(88, "88_SharedLinks_PortalExports", FolderCategory.SHARED, "Shared links and portal exports"),
    FolderDefinition(89, "89_Templates_Forms_Scripts", FolderCategory.TEMPLATES, "Templates, forms, and scripts"),
    FolderDefinition(90, "90_Knowledge_Policies_Procedures", FolderCategory.KNOWLEDGE, "Policies and procedures"),
    FolderDefinition(91, "91_Knowledge_Checklists", FolderCategory.KNOWLEDGE, "Operational checklists"),
    FolderDefinition(92, "92_Knowledge_Email_Templates", FolderCategory.KNOWLEDGE, "Email templates"),
    FolderDefinition(93, "93_Knowledge_LeaseAdmin_Packs", FolderCategory.KNOWLEDGE, "Lease admin packs and precedents", lock_level=LockLevel.L3_CONFIDENTIAL),
    FolderDefinition(94, "94_Knowledge_Compliance_Standards", FolderCategory.KNOWLEDGE, "Compliance standards reference"),

    # Exports & Archive (95–99)
    FolderDefinition(95, "95_Exports_Reports_Monthly", FolderCategory.EXPORTS, "Monthly reports"),
    FolderDefinition(96, "96_Exports_Reports_Quarterly", FolderCategory.EXPORTS, "Quarterly reports"),
    FolderDefinition(97, "97_Exports_Reports_Annual", FolderCategory.EXPORTS, "Annual reports"),
    FolderDefinition(98, "98_Archive_ClosedMatters", FolderCategory.ARCHIVE, "Archived closed matters"),
    FolderDefinition(99, "99_Review_Quarantine_Unclear", FolderCategory.REVIEW, "Quarantine: unclear items for review"),
]


class PMEmailCategorisationOS:
    """
    PM-Email-Categorisation Operating System.

    AI-first email and document categorisation for property management.
    Deterministic routing through 99-folder RES and COM trees with
    L0–L4 lock levels, ID-binding subfolders, and stakeholder tagging.
    """

    def __init__(self) -> None:
        self.res_tree = RES_FOLDER_TREE
        self.com_tree = COM_FOLDER_TREE
        self.id_format = IDFormat()

    def get_folder_tree(
        self, domain: PropertyDomain
    ) -> list[FolderDefinition]:
        """Get the full 99-folder tree for a domain."""
        if domain == PropertyDomain.RES:
            return self.res_tree
        return self.com_tree

    def get_folder_by_number(
        self, domain: PropertyDomain, number: int
    ) -> FolderDefinition | None:
        """Get a folder by its number (01–99)."""
        tree = self.get_folder_tree(domain)
        for folder in tree:
            if folder.number == number:
                return folder
        return None

    def get_folders_by_category(
        self, domain: PropertyDomain, category: FolderCategory
    ) -> list[FolderDefinition]:
        """Get all folders in a category."""
        tree = self.get_folder_tree(domain)
        return [f for f in tree if f.category == category]

    def get_folders_by_lock_level(
        self, domain: PropertyDomain, lock_level: LockLevel
    ) -> list[FolderDefinition]:
        """Get all folders at or above a lock level."""
        tree = self.get_folder_tree(domain)
        level_order = [LockLevel.L0_PUBLIC, LockLevel.L1_INTERNAL,
                       LockLevel.L2_RESTRICTED, LockLevel.L3_CONFIDENTIAL,
                       LockLevel.L4_VAULT]
        min_idx = level_order.index(lock_level)
        return [f for f in tree if level_order.index(f.lock_level) >= min_idx]

    def route_email(
        self, domain: PropertyDomain, subject: str, body: str = ""
    ) -> list[FolderDefinition]:
        """
        AI-first email routing: match email subject/body against folder
        auto_route_keywords to suggest destination folder(s).
        """
        tree = self.get_folder_tree(domain)
        combined = f"{subject} {body}".lower()
        matches = []
        for folder in tree:
            if folder.auto_route_keywords:
                for kw in folder.auto_route_keywords:
                    if kw.lower() in combined:
                        matches.append(folder)
                        break
        # Default to inbox if no match
        if not matches:
            matches = [tree[0]]  # 01_Inbox_New
        return matches

    def generate_folder_binding(
        self,
        domain: PropertyDomain,
        portfolio_num: int,
        suburb: str,
        street_no: str,
        street_name: str,
        building_num: int = 1,
        tenant_year: int | None = None,
        tenant_num: int | None = None,
        lease_year: int | None = None,
        lease_num: int | None = None,
    ) -> str:
        """Generate a folder binding path from ID components."""
        domain_code = domain.value
        portfolio_id = f"PORT-PM-MEL-{domain_code}-{portfolio_num:04d}"
        building_id = f"BLD-{suburb.upper()}-{street_no}-{street_name.upper()}-{building_num:03d}"
        path = IDFormat.folder_binding_base(portfolio_id, building_id)

        if tenant_year and tenant_num:
            ten_id = f"TEN-{tenant_year}-{tenant_num:04d}"
            path = IDFormat.folder_binding_case(portfolio_id, building_id, ten_id)
        elif lease_year and lease_num:
            lease_id = f"LEASE-{lease_year}-{lease_num:04d}"
            path = IDFormat.folder_binding_case(portfolio_id, building_id, lease_id)

        return path

    def get_tree_summary(self, domain: PropertyDomain) -> dict[str, Any]:
        """Get a summary of the folder tree."""
        tree = self.get_folder_tree(domain)
        categories: dict[str, int] = {}
        lock_levels: dict[str, int] = {}
        for folder in tree:
            cat = folder.category.value
            categories[cat] = categories.get(cat, 0) + 1
            ll = folder.lock_level.value
            lock_levels[ll] = lock_levels.get(ll, 0) + 1

        return {
            "domain": domain.value,
            "total_folders": len(tree),
            "by_category": categories,
            "by_lock_level": lock_levels,
            "vault_folders": len(self.get_folders_by_lock_level(domain, LockLevel.L4_VAULT)),
            "confidential_folders": len(self.get_folders_by_lock_level(domain, LockLevel.L3_CONFIDENTIAL)),
        }

    # =================================================================
    # v0.2.0 — Stakeholder-Aware Cover Scan & Lock Escalation
    # =================================================================

    def detect_portfolio(self, text: str) -> str:
        """Detect portfolio (RESIDENTIAL / COMMERCIAL) from text signals."""
        text_lower = text.lower()
        com_score = sum(1 for kw in PORTFOLIO_COMMERCIAL_KEYWORDS if kw in text_lower)
        res_score = sum(1 for kw in PORTFOLIO_RESIDENTIAL_KEYWORDS if kw in text_lower)
        if com_score > res_score:
            return "COMMERCIAL"
        if res_score > com_score:
            return "RESIDENTIAL"
        return "UNKNOWN"

    def infer_stakeholder(self, portfolio: str, text: str) -> str:
        """Infer primary stakeholder from portfolio context and text."""
        text_lower = text.lower()
        best_match = "UNKNOWN"
        best_score = 0

        for stakeholder_key, keywords in STAKEHOLDER_KEYWORDS.items():
            # Filter to matching portfolio
            if portfolio == "RESIDENTIAL" and not stakeholder_key.startswith("RESIDENTIAL"):
                continue
            if portfolio == "COMMERCIAL" and not stakeholder_key.startswith("COMMERCIAL"):
                continue

            score = sum(1 for kw in keywords if kw in text_lower)
            if score > best_score:
                best_score = score
                best_match = stakeholder_key

        return best_match

    def detect_secondary_stakeholder(self, text: str) -> str:
        """Detect if multiple counterparties are in the thread."""
        multi_party_signals = [
            "cc landlord", "cc tenant", "copied the owner",
            "copied the tenant", "forwarded to tenant", "forwarded to owner",
        ]
        text_lower = text.lower()
        if any(sig in text_lower for sig in multi_party_signals):
            return "PRESENT"
        return "NONE"

    def escalate_lock_level(self, text: str) -> str:
        """Determine lock level escalation based on vault/sensitive keywords."""
        text_lower = text.lower()
        if any(kw in text_lower for kw in VAULT_L4_KEYWORDS):
            return "L4_VAULT"
        if any(kw in text_lower for kw in LOCK_L3_KEYWORDS):
            return "L3_SENSITIVE"
        return "L1_INTERNAL"

    def get_stakeholder_folder(self, stakeholder: str) -> str:
        """Get the stakeholder-specific routing folder."""
        return STAKEHOLDER_FOLDER_MAP.get(stakeholder, "")

    def get_vault_folder(self, stakeholder: str) -> str:
        """Get the vault folder for a stakeholder."""
        return VAULT_FOLDER_MAP.get(stakeholder, "VAULT/General/")

    def cover_scan(
        self,
        subject: str,
        body: str = "",
        from_domain: str = "",
        attachment_names: list[str] | None = None,
    ) -> CoverScanResult:
        """
        Stage-0 cover scan: label portfolio, stakeholder, category,
        lock level, and routing folder from cover signals.

        This is the v0.2.0 stakeholder-aware first-pass triage.
        """
        combined = f"{subject} {body}"
        attachment_text = " ".join(attachment_names or [])
        full_text = f"{combined} {attachment_text}"

        result = CoverScanResult()
        result.labels.append("PMOS/PROFESSIONAL")

        # 1. Portfolio detection
        result.portfolio_guess = self.detect_portfolio(combined)
        if result.portfolio_guess == "RESIDENTIAL":
            result.labels.append("PMOS/RESIDENTIAL")
            result.pm_category_top = "PM_RES"
        elif result.portfolio_guess == "COMMERCIAL":
            result.labels.append("PMOS/COMMERCIAL")
            result.pm_category_top = "PM_COM"
        else:
            result.pm_category_top = "PM_GEN"

        # 2. Stakeholder inference
        result.stakeholder_primary = self.infer_stakeholder(
            result.portfolio_guess, combined
        )
        if result.stakeholder_primary != "UNKNOWN":
            # Map stakeholder to PMOS label
            stake_label_map = {
                "RESIDENTIAL.RENTERS": "PMOS/RES-RENTERS",
                "RESIDENTIAL.RENTAL_PROVIDERS": "PMOS/RES-RENTAL_PROVIDERS",
                "COMMERCIAL.CLIENTS": "PMOS/COM-CLIENTS",
                "COMMERCIAL.LANDLORDS": "PMOS/COM-LANDLORDS",
                "COMMERCIAL.TENANTS": "PMOS/COM-TENANTS",
            }
            label = stake_label_map.get(result.stakeholder_primary)
            if label:
                result.labels.append(label)
            result.rationale.append(
                f"Stakeholder inferred as {result.stakeholder_primary}."
            )

        # 3. Secondary stakeholder
        result.stakeholder_secondary = self.detect_secondary_stakeholder(combined)
        if result.stakeholder_secondary == "PRESENT":
            result.rationale.append(
                "Thread includes multiple counterparties; careful sharing controls."
            )

        # 4. Lock level escalation
        result.lock_level_guess = self.escalate_lock_level(full_text)
        if result.lock_level_guess == "L4_VAULT":
            result.labels.append("PMOS/LOCK-L4-VAULT")
            result.needs_deep_extraction = True
            result.routing_folder = self.get_vault_folder(result.stakeholder_primary)
            result.rationale.append("ID/application content => Vault only.")
        elif result.lock_level_guess == "L3_SENSITIVE":
            result.labels.append("PMOS/LOCK-L3")
            result.needs_deep_extraction = True
        else:
            result.labels.append("PMOS/LOCK-L1")

        # 5. Stakeholder routing (if not vault-routed)
        if not result.routing_folder and result.stakeholder_primary != "UNKNOWN":
            result.routing_folder = self.get_stakeholder_folder(
                result.stakeholder_primary
            )

        return result

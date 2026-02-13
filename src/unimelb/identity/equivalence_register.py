"""
1:1:1 Equivalence Register & Unified Lexicon
===============================================
Design: Jiadong Chen (陈佳栋) — Student ID: 723912

Core Principles:
  Microsoft : Google : Apple = 1 : 1 : 1
  App : Web : Cloud = 1 : 1 : 1
  iPhone : Mac : iPad = 1 : 1 : 1
  中文 : 英文 : 数字/字母 = 1 : 1 : 1

Single identity (@unimelb.edu.au) maps to all three ecosystems
through Microsoft Entra ID SSO federation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EcosystemProvider(Enum):
    """The 1:1:1 triad of ecosystem providers."""

    MICROSOFT = "microsoft"
    GOOGLE = "google"
    APPLE = "apple"


class DeviceTriad(Enum):
    """Apple device triad (1:1:1)."""

    IPHONE = "iphone"
    MAC = "mac"
    IPAD = "ipad"


class DeploymentTriad(Enum):
    """Deployment triad (1:1:1)."""

    APP = "app"
    WEB = "web"
    CLOUD = "cloud"


@dataclass
class TriadMapping:
    """A single row in the 1:1:1 equivalence table."""

    domain: str
    microsoft: str
    google: str
    apple: str


@dataclass
class LexiconEntry:
    """A single entry in the unified trilingual lexicon."""

    zh: str       # Chinese
    en: str       # English
    code: str     # Code / symbol / abbreviation


# =============================================================================
# Triad Table — Microsoft / Google / Apple
# =============================================================================

TRIAD_TABLE: list[TriadMapping] = [
    TriadMapping("Identity / Login", "Microsoft Entra ID (account login)", "Google Account (account login)", "Apple ID (account login)"),
    TriadMapping("Cloud Storage", "OneDrive / SharePoint", "Google Drive", "iCloud Drive"),
    TriadMapping("Calendar / Meetings", "Outlook Calendar + Teams", "Google Calendar + Meet", "Apple Calendar + FaceTime"),
    TriadMapping("Messaging / Collaboration", "Teams / Outlook", "Gmail / Chat / Meet", "iMessage / FaceTime"),
    TriadMapping("Device Ecosystem", "Windows / Surface", "Android / Chromebook", "iPhone / Mac / iPad"),
    TriadMapping("Notes / Docs", "Word / OneNote / Loop", "Docs / Keep", "Notes / Pages"),
    TriadMapping("Spreadsheet", "Excel", "Sheets", "Numbers"),
    TriadMapping("Presentation", "PowerPoint", "Slides", "Keynote"),
    TriadMapping("Automation", "Power Automate", "Apps Script / Zapier", "Shortcuts"),
    TriadMapping("AI Assistant", "Copilot", "Gemini", "Apple Intelligence / Siri"),
    TriadMapping("Email", "Outlook", "Gmail", "Apple Mail"),
    TriadMapping("Video Calling", "Teams", "Google Meet", "FaceTime"),
    TriadMapping("Browser", "Edge", "Chrome", "Safari"),
    TriadMapping("Code Editor", "VS Code / Visual Studio", "Android Studio / IDX", "Xcode"),
    TriadMapping("Cloud Compute", "Azure", "Google Cloud (GCP)", "CloudKit / iCloud"),
    TriadMapping("App Store", "Microsoft Store", "Google Play Store", "Apple App Store"),
    TriadMapping("Password Manager", "Authenticator", "Google Password Manager", "iCloud Keychain"),
    TriadMapping("Device Management", "Intune", "Google Admin / MDM", "Apple Business Manager"),
]


# =============================================================================
# Unified Lexicon — 中文 : 英文 : Code (1:1:1)
# =============================================================================

UNIFIED_LEXICON: list[LexiconEntry] = [
    # Numbers
    LexiconEntry("一", "One", "1"),
    LexiconEntry("壹", "One (formal)", "1"),
    LexiconEntry("二", "Two", "2"),
    LexiconEntry("贰", "Two (formal)", "2"),
    LexiconEntry("三", "Three", "3"),
    LexiconEntry("叁", "Three (formal)", "3"),

    # Identity & Access
    LexiconEntry("账户", "Account", "ID"),
    LexiconEntry("身份", "Identity", "ID"),
    LexiconEntry("锁级", "Lock Level", "L0-L4"),
    LexiconEntry("密码", "Password", "PWD"),
    LexiconEntry("验证", "Verification", "MFA"),
    LexiconEntry("权限", "Permission", "RBAC"),
    LexiconEntry("登录", "Login", "SSO"),

    # Property Management — Residential
    LexiconEntry("租客", "Renter", "RESIDENTIAL.RENTERS"),
    LexiconEntry("房东", "Rental Provider", "RESIDENTIAL.RENTAL_PROVIDERS"),
    LexiconEntry("租赁", "Lease (RES)", "LEASE"),
    LexiconEntry("押金", "Bond", "BOND"),
    LexiconEntry("租金", "Rent", "RENT"),
    LexiconEntry("维修", "Maintenance", "MAINT"),
    LexiconEntry("物业", "Property", "PROP"),
    LexiconEntry("状态报告", "Condition Report", "COND_RPT"),

    # Property Management — Commercial
    LexiconEntry("承租方", "Tenant", "COMMERCIAL.TENANTS"),
    LexiconEntry("业主", "Landlord", "COMMERCIAL.LANDLORDS"),
    LexiconEntry("客户", "Client", "COMMERCIAL.CLIENTS"),
    LexiconEntry("租约", "Lease (COM)", "LEASE_COM"),
    LexiconEntry("公共支出", "Outgoings", "OUTGOINGS"),
    LexiconEntry("设施管理", "Facilities Management", "FM"),
    LexiconEntry("消防安全", "Fire Life Safety", "FLS"),

    # Agents
    LexiconEntry("联实集团", "Lendlease", "AGENT_LL"),
    LexiconEntry("仲量联行", "JLL", "AGENT_JLL"),
    LexiconEntry("美诚物业", "MICM", "AGENT_MICM"),

    # Finance
    LexiconEntry("发票", "Invoice", "INV"),
    LexiconEntry("付款", "Payment", "PMT"),
    LexiconEntry("欠款", "Arrears", "ARR"),
    LexiconEntry("对账", "Reconciliation", "RECON"),
    LexiconEntry("信托", "Trust Account", "TRUST"),

    # Legal & Compliance
    LexiconEntry("维州民事行政仲裁庭", "VCAT", "VCAT"),
    LexiconEntry("违约通知", "Breach Notice", "BREACH"),
    LexiconEntry("搬离通知", "Notice to Vacate", "NTV"),
    LexiconEntry("调解", "Mediation", "MED"),
    LexiconEntry("合规", "Compliance", "COMP"),

    # Education
    LexiconEntry("学生", "Student", "STU"),
    LexiconEntry("教职员工", "Academic Staff", "ACAD"),
    LexiconEntry("行政员工", "Professional Staff", "PROF"),
    LexiconEntry("大学", "University", "UNI"),
    LexiconEntry("墨尔本大学", "University of Melbourne", "UNIMELB"),
]


# =============================================================================
# Airline Code Triad (1:1:1 示例)
# =============================================================================

AIRLINE_CODES: list[LexiconEntry] = [
    LexiconEntry("中国国际航空", "Air China", "CA"),
    LexiconEntry("中国南方航空", "China Southern Airlines", "CZ"),
    LexiconEntry("中国东方航空", "China Eastern Airlines", "MU"),
    LexiconEntry("澳洲航空", "Qantas", "QF"),
    LexiconEntry("维珍澳大利亚", "Virgin Australia", "VA"),
    LexiconEntry("新加坡航空", "Singapore Airlines", "SQ"),
    LexiconEntry("国泰航空", "Cathay Pacific", "CX"),
]


class EquivalenceRegister:
    """
    1:1:1 Equivalence Register for UniMelb AI Platform.

    Ensures consistency across Microsoft, Google, and Apple ecosystems.
    Provides unified trilingual lexicon (中文:English:Code).
    """

    def __init__(self) -> None:
        self.triad_table = TRIAD_TABLE
        self.lexicon = UNIFIED_LEXICON
        self.airline_codes = AIRLINE_CODES

    def get_triad_mapping(self, domain: str) -> TriadMapping | None:
        """Look up a triad mapping by domain name."""
        for mapping in self.triad_table:
            if domain.lower() in mapping.domain.lower():
                return mapping
        return None

    def lookup_lexicon(
        self, query: str, lang: str = "any"
    ) -> list[LexiconEntry]:
        """
        Search the unified lexicon.

        Args:
            query: Search term (Chinese, English, or code)
            lang: "zh" | "en" | "code" | "any"
        """
        query_lower = query.lower()
        results = []
        for entry in self.lexicon:
            if lang == "zh" and query in entry.zh:
                results.append(entry)
            elif lang == "en" and query_lower in entry.en.lower():
                results.append(entry)
            elif lang == "code" and query_lower in entry.code.lower():
                results.append(entry)
            elif lang == "any" and (
                query in entry.zh
                or query_lower in entry.en.lower()
                or query_lower in entry.code.lower()
            ):
                results.append(entry)
        return results

    def get_ecosystem_equivalent(
        self, service_name: str
    ) -> dict[str, str] | None:
        """
        Given a service name from any ecosystem, find its equivalents.

        E.g. "Teams" → {"microsoft": "Teams / Outlook", "google": "Gmail / Chat / Meet", "apple": "iMessage / FaceTime"}
        """
        service_lower = service_name.lower()
        for mapping in self.triad_table:
            if (
                service_lower in mapping.microsoft.lower()
                or service_lower in mapping.google.lower()
                or service_lower in mapping.apple.lower()
            ):
                return {
                    "domain": mapping.domain,
                    "microsoft": mapping.microsoft,
                    "google": mapping.google,
                    "apple": mapping.apple,
                }
        return None

    def print_111(self, title: str, items: list[LexiconEntry]) -> str:
        """Format lexicon entries as 1:1:1 display string."""
        lines = [f"== {title} =="]
        for item in items:
            lines.append(f"{item.zh} : {item.en} : {item.code}")
        return "\n".join(lines)

    def get_full_summary(self) -> dict[str, Any]:
        """Get summary statistics of the register."""
        return {
            "triad_mappings": len(self.triad_table),
            "lexicon_entries": len(self.lexicon),
            "airline_codes": len(self.airline_codes),
            "ecosystems": ["microsoft", "google", "apple"],
            "languages": ["zh (Chinese)", "en (English)", "code (Symbol)"],
            "principle": "1:1:1 — every concept has exactly one representation in each ecosystem and language",
        }

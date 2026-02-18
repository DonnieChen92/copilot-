"""
Education Platform Connectors
==============================
Unified connectors for Microsoft Education, Google Education,
and OpenAI Education tiers.

Single @unimelb.edu.au account provides access to all platforms
via Microsoft Entra ID SSO federation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PlatformProvider(Enum):
    """Education platform providers."""

    MICROSOFT = "microsoft"
    GOOGLE = "google"
    OPENAI = "openai"


class MicrosoftEduTier(Enum):
    """Microsoft Education licence tiers."""

    A1_FREE = "a1_free"
    A3_STANDARD = "a3_standard"
    A5_PREMIUM = "a5_premium"
    COPILOT_ADDON = "copilot_addon"


class GoogleEduTier(Enum):
    """Google Workspace for Education tiers."""

    FUNDAMENTALS = "fundamentals"         # Free
    STANDARD = "standard"
    TEACHING_LEARNING = "teaching_learning_upgrade"
    PLUS = "education_plus"


class OpenAITier(Enum):
    """OpenAI service tiers for education."""

    FREE = "free"
    STUDENT = "student"
    BUSINESS = "business"
    TEAM = "team"
    ENTERPRISE = "enterprise"
    RESEARCH = "research"
    LABS = "labs"


@dataclass
class PlatformUser:
    """A user across all education platforms (single identity)."""

    user_id: str
    email: str  # @unimelb.edu.au
    display_name: str
    role: str  # student | academic_staff | professional_staff | admin
    faculty: str = ""
    department: str = ""
    entra_id: str = ""  # Microsoft Entra ID object ID
    microsoft_tier: MicrosoftEduTier = MicrosoftEduTier.A5_PREMIUM
    google_tier: GoogleEduTier = GoogleEduTier.PLUS
    openai_tier: OpenAITier = OpenAITier.FREE
    active: bool = True
    life_challenge_status: str = ""  # "" | "finance" | "pause" | "restart"


@dataclass
class PlatformService:
    """A service available on an education platform."""

    service_id: str
    provider: PlatformProvider
    name: str
    description: str
    tier_required: str = ""
    enabled: bool = True
    url: str = ""
    features: list[str] = field(default_factory=list)


class MicrosoftEducationConnector:
    """
    Microsoft 365 Education + Copilot connector.

    Products:
    - Microsoft 365 Education A5 (full productivity suite)
    - Microsoft Teams for Education (collaboration + classes)
    - Copilot for Microsoft 365 (AI assistant)
    - Azure AI Foundry (AI model hosting)
    - Power BI Pro (analytics)
    - Intune for Education (device management)
    - Defender for Endpoint (security)
    """

    SERVICES = [
        PlatformService(
            service_id="ms_teams_edu",
            provider=PlatformProvider.MICROSOFT,
            name="Microsoft Teams for Education",
            description="Collaboration hub — replaces Canvas LMS",
            tier_required="A1+",
            features=[
                "Class Teams", "Assignments", "Gradebook", "Channels",
                "Meetings", "Whiteboard", "OneNote Class Notebook",
            ],
        ),
        PlatformService(
            service_id="ms_copilot_365",
            provider=PlatformProvider.MICROSOFT,
            name="Copilot for Microsoft 365",
            description="AI assistant embedded in all Microsoft 365 apps",
            tier_required="Copilot add-on",
            features=[
                "Word Copilot", "Excel Copilot", "PowerPoint Copilot",
                "Outlook Copilot", "Teams Copilot", "OneNote Copilot",
            ],
        ),
        PlatformService(
            service_id="ms_azure_foundry",
            provider=PlatformProvider.MICROSOFT,
            name="Azure AI Foundry",
            description="Frontier model hosting and orchestration",
            tier_required="Azure subscription",
            features=[
                "GPT-4o", "Claude via Azure", "Gemini via Azure",
                "Custom fine-tuning", "RAG deployment",
            ],
        ),
        PlatformService(
            service_id="ms_power_bi",
            provider=PlatformProvider.MICROSOFT,
            name="Power BI Pro",
            description="Business intelligence and analytics",
            tier_required="A5",
            features=[
                "Dashboards", "Reports", "Data connectors",
                "AI insights", "Copilot for Power BI",
            ],
        ),
        PlatformService(
            service_id="ms_intune_edu",
            provider=PlatformProvider.MICROSOFT,
            name="Intune for Education",
            description="Device management for university endpoints",
            tier_required="A3+",
            features=[
                "Device enrolment", "App deployment", "Policy management",
                "Conditional Access", "Compliance monitoring",
            ],
        ),
        PlatformService(
            service_id="ms_defender",
            provider=PlatformProvider.MICROSOFT,
            name="Defender for Endpoint",
            description="Endpoint security and threat protection",
            tier_required="A5",
            features=[
                "Threat detection", "Automated investigation",
                "Attack surface reduction", "Endpoint DLP",
            ],
        ),
    ]

    def get_services(self) -> list[PlatformService]:
        """Get all Microsoft Education services."""
        return self.SERVICES

    def get_user_entitlements(
        self, user: PlatformUser
    ) -> list[PlatformService]:
        """Get services available to a user based on their tier."""
        # A5 gets everything
        if user.microsoft_tier == MicrosoftEduTier.A5_PREMIUM:
            return self.SERVICES
        # Filter based on tier
        return [s for s in self.SERVICES if s.tier_required in ("A1+", "")]


class GoogleEducationConnector:
    """
    Google Workspace for Education connector.

    Products:
    - Google Workspace for Education Plus (full suite)
    - Google Classroom (course management)
    - Gemini for Education (AI assistant)
    - Google Cloud (research compute)
    """

    SERVICES = [
        PlatformService(
            service_id="google_workspace_edu",
            provider=PlatformProvider.GOOGLE,
            name="Google Workspace for Education Plus",
            description="Gmail, Drive, Docs, Sheets, Slides, Meet",
            tier_required="Education Plus",
            features=[
                "Gmail", "Google Drive (unlimited)", "Google Docs",
                "Google Sheets", "Google Slides", "Google Meet",
                "Google Calendar", "Google Chat",
            ],
        ),
        PlatformService(
            service_id="google_classroom",
            provider=PlatformProvider.GOOGLE,
            name="Google Classroom",
            description="Course management (legacy support during migration)",
            tier_required="Fundamentals+",
            features=[
                "Course creation", "Assignment management",
                "Grading", "Student analytics",
            ],
        ),
        PlatformService(
            service_id="google_gemini_edu",
            provider=PlatformProvider.GOOGLE,
            name="Gemini for Education",
            description="Google AI assistant for teaching and learning",
            tier_required="Education Plus",
            features=[
                "Gemini in Docs", "Gemini in Slides",
                "Gemini in Sheets", "Gemini in Meet",
            ],
        ),
        PlatformService(
            service_id="google_cloud_research",
            provider=PlatformProvider.GOOGLE,
            name="Google Cloud for Research",
            description="Research compute infrastructure",
            tier_required="GCP account",
            features=[
                "Vertex AI", "BigQuery", "Compute Engine",
                "TPU access", "Research credits",
            ],
        ),
    ]

    def get_services(self) -> list[PlatformService]:
        """Get all Google Education services."""
        return self.SERVICES

    def get_user_entitlements(
        self, user: PlatformUser
    ) -> list[PlatformService]:
        """Get services available to a user based on their tier."""
        if user.google_tier == GoogleEduTier.PLUS:
            return self.SERVICES
        return [
            s for s in self.SERVICES
            if s.tier_required in ("Fundamentals+", "")
        ]


class OpenAIEducationConnector:
    """
    OpenAI Education tier connector.

    Tiers:
    - Free: Basic ChatGPT access, limited queries
    - Student: Enhanced limits, GPT-4o access
    - Business: Team workspaces, admin controls
    - Team: Department-level shared workspaces
    - Enterprise: Institution SSO, data residency, audit
    - Research: API access, fine-tuning, extended limits
    - Labs: Experimental models, early access
    """

    TIER_FEATURES: dict[OpenAITier, dict[str, Any]] = {
        OpenAITier.FREE: {
            "models": ["gpt-4o-mini"],
            "rate_limit_rpm": 10,
            "features": ["Basic chat"],
            "data_retention": "standard",
            "sso": False,
        },
        OpenAITier.STUDENT: {
            "models": ["gpt-4o-mini", "gpt-4o"],
            "rate_limit_rpm": 30,
            "features": ["Enhanced chat", "Image generation", "Web browsing"],
            "data_retention": "standard",
            "sso": True,
        },
        OpenAITier.BUSINESS: {
            "models": ["gpt-4o-mini", "gpt-4o", "o3-mini"],
            "rate_limit_rpm": 60,
            "features": ["Team workspace", "Admin controls", "Usage analytics"],
            "data_retention": "business",
            "sso": True,
        },
        OpenAITier.TEAM: {
            "models": ["gpt-4o-mini", "gpt-4o", "o3-mini", "o3"],
            "rate_limit_rpm": 100,
            "features": [
                "Shared workspace", "Custom GPTs", "Department analytics",
                "File uploads",
            ],
            "data_retention": "business",
            "sso": True,
        },
        OpenAITier.ENTERPRISE: {
            "models": ["gpt-4o-mini", "gpt-4o", "o3-mini", "o3"],
            "rate_limit_rpm": 500,
            "features": [
                "SSO", "Data residency", "Audit logs", "DLP",
                "Custom data retention", "Priority support",
            ],
            "data_retention": "enterprise",
            "sso": True,
        },
        OpenAITier.RESEARCH: {
            "models": ["gpt-4o-mini", "gpt-4o", "o3-mini", "o3"],
            "rate_limit_rpm": 200,
            "features": [
                "API access", "Fine-tuning", "Extended context",
                "Research credits", "Batch API",
            ],
            "data_retention": "research",
            "sso": True,
        },
        OpenAITier.LABS: {
            "models": ["gpt-4o", "o3", "experimental-*"],
            "rate_limit_rpm": 100,
            "features": [
                "Early access models", "Experimental features",
                "Research preview", "Feedback channel",
            ],
            "data_retention": "research",
            "sso": True,
        },
    }

    def get_tier_info(self, tier: OpenAITier) -> dict[str, Any]:
        """Get feature details for an OpenAI tier."""
        return self.TIER_FEATURES.get(tier, {})

    def get_user_tier_features(
        self, user: PlatformUser
    ) -> dict[str, Any]:
        """Get OpenAI features available to a user."""
        return self.get_tier_info(user.openai_tier)

    def recommend_tier(self, user: PlatformUser) -> OpenAITier:
        """Recommend the appropriate OpenAI tier based on user role."""
        tier_map = {
            "student": OpenAITier.STUDENT,
            "academic_staff": OpenAITier.RESEARCH,
            "professional_staff": OpenAITier.BUSINESS,
            "admin": OpenAITier.ENTERPRISE,
            "researcher": OpenAITier.RESEARCH,
            "phd_candidate": OpenAITier.RESEARCH,
        }
        return tier_map.get(user.role, OpenAITier.FREE)


class UnifiedEducationPlatform:
    """
    Unified connector across all education platforms.

    Single @unimelb.edu.au account → access to:
    - Microsoft 365 Education + Copilot
    - Google Workspace for Education + Gemini
    - OpenAI (tier-based)
    - Azure AI Foundry (frontier models)

    SSO via Microsoft Entra ID → SAML/OIDC federation to Google and OpenAI.
    """

    def __init__(self) -> None:
        self.microsoft = MicrosoftEducationConnector()
        self.google = GoogleEducationConnector()
        self.openai = OpenAIEducationConnector()

    def get_all_services(self) -> dict[str, list[PlatformService]]:
        """Get all available services across all platforms."""
        return {
            "microsoft": self.microsoft.get_services(),
            "google": self.google.get_services(),
            "openai": [],  # OpenAI uses tier-based access, not service list
        }

    def get_user_entitlements(
        self, user: PlatformUser
    ) -> dict[str, Any]:
        """Get all platform entitlements for a single user."""
        return {
            "user": {
                "email": user.email,
                "role": user.role,
                "faculty": user.faculty,
                "life_challenge_status": user.life_challenge_status,
            },
            "microsoft": {
                "tier": user.microsoft_tier.value,
                "services": [
                    s.name
                    for s in self.microsoft.get_user_entitlements(user)
                ],
            },
            "google": {
                "tier": user.google_tier.value,
                "services": [
                    s.name
                    for s in self.google.get_user_entitlements(user)
                ],
            },
            "openai": {
                "tier": user.openai_tier.value,
                "recommended_tier": self.openai.recommend_tier(user).value,
                "features": self.openai.get_user_tier_features(user),
            },
            "sso_provider": "microsoft_entra_id",
            "sso_protocol": "saml_2.0_oidc",
        }

    def provision_user(self, user: PlatformUser) -> dict[str, Any]:
        """
        Provision a user across all education platforms.

        Creates/syncs accounts in Microsoft, Google, and OpenAI
        using Entra ID as the identity source.
        """
        # Determine appropriate tiers based on role
        recommended_openai = self.openai.recommend_tier(user)

        # Life Challenge: ensure access is preserved during pause
        if user.life_challenge_status == "pause":
            user.openai_tier = OpenAITier.FREE  # Reduced but not removed
            # Microsoft and Google maintain read access

        return {
            "user_id": user.user_id,
            "email": user.email,
            "provisioned": {
                "microsoft": {
                    "status": "active",
                    "tier": user.microsoft_tier.value,
                },
                "google": {
                    "status": "active",
                    "tier": user.google_tier.value,
                },
                "openai": {
                    "status": "active",
                    "tier": user.openai_tier.value,
                    "recommended": recommended_openai.value,
                },
            },
            "sso_configured": True,
            "life_challenge_accommodations": (
                user.life_challenge_status
                if user.life_challenge_status
                else "none"
            ),
        }

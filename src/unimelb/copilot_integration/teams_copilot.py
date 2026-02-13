"""
Microsoft Copilot for Education — Teams Integration
=====================================================
Integrates Microsoft Copilot capabilities directly into the
UniMelb Teams environment, replacing Canvas Spark AI and Aila.

Copilot features:
- Teams Copilot: Meeting summaries, action items, chat assistance
- Word/Excel/PowerPoint Copilot: Document AI assistance
- Outlook Copilot: Email drafting, scheduling, summaries
- Custom Copilot Agents: Faculty-specific AI assistants via Copilot Studio
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CopilotProduct(Enum):
    """Microsoft Copilot products available."""

    TEAMS_COPILOT = "teams_copilot"
    WORD_COPILOT = "word_copilot"
    EXCEL_COPILOT = "excel_copilot"
    POWERPOINT_COPILOT = "powerpoint_copilot"
    OUTLOOK_COPILOT = "outlook_copilot"
    ONENOTE_COPILOT = "onenote_copilot"
    COPILOT_STUDIO = "copilot_studio"          # Custom agents
    COPILOT_CHAT = "copilot_chat"              # Web/mobile Copilot
    POWER_BI_COPILOT = "power_bi_copilot"


class CustomAgentType(Enum):
    """Custom Copilot Studio agents for UniMelb."""

    ACADEMIC_ADVISOR = "academic_advisor"
    RESEARCH_ASSISTANT = "research_assistant"
    STUDENT_SUPPORT = "student_support"
    IT_HELPDESK = "it_helpdesk"
    LIBRARY_SEARCH = "library_search"
    PROPERTY_ASSISTANT = "property_assistant"
    ENROLMENT_GUIDE = "enrolment_guide"
    CAREER_COACH = "career_coach"
    LIFE_CHALLENGE_SUPPORT = "life_challenge_support"


@dataclass
class CopilotAgent:
    """A custom Copilot Studio agent for UniMelb."""

    agent_id: str
    agent_type: CustomAgentType
    name: str
    description: str
    data_sources: list[str] = field(default_factory=list)
    target_users: list[str] = field(default_factory=list)
    # "students", "academic_staff", "professional_staff", "all"
    teams_app_id: str = ""
    active: bool = True
    knowledge_base: str = ""  # Azure AI Search index name


@dataclass
class CanvasSparkAIMapping:
    """Mapping from Canvas Spark AI / Aila features to Copilot equivalents."""

    canvas_feature: str
    canvas_tool: str  # "spark_ai" | "aila"
    copilot_equivalent: str
    copilot_product: CopilotProduct
    migration_status: str = "planned"  # planned | in_progress | completed
    notes: str = ""


class TeamsCopilotIntegration:
    """
    Microsoft Copilot integration for UniMelb AI Platform.

    Replaces Canvas Spark AI and Aila with Copilot-based equivalents,
    enhanced with UniMelb-specific custom agents via Copilot Studio.
    """

    # Spark AI / Aila → Copilot migration mapping
    FEATURE_MIGRATION_MAP = [
        CanvasSparkAIMapping(
            canvas_feature="AI Writing Assistant",
            canvas_tool="spark_ai",
            copilot_equivalent="Word Copilot + Teams Copilot",
            copilot_product=CopilotProduct.WORD_COPILOT,
            notes="Enhanced: Copilot works across all M365 apps, not just Canvas",
        ),
        CanvasSparkAIMapping(
            canvas_feature="AI-Powered Study Help",
            canvas_tool="aila",
            copilot_equivalent="Custom Copilot Studio Agent: Academic Advisor",
            copilot_product=CopilotProduct.COPILOT_STUDIO,
            notes="Aila (Claude 3 Sonnet) replaced by custom agent backed by Azure Foundry",
        ),
        CanvasSparkAIMapping(
            canvas_feature="Quiz/Assessment Feedback",
            canvas_tool="aila",
            copilot_equivalent="Teams Assignments + Copilot Review",
            copilot_product=CopilotProduct.TEAMS_COPILOT,
            notes="AI-assisted grading and feedback via Teams Assignments",
        ),
        CanvasSparkAIMapping(
            canvas_feature="Discussion Summarisation",
            canvas_tool="spark_ai",
            copilot_equivalent="Teams Copilot Meeting/Chat Summary",
            copilot_product=CopilotProduct.TEAMS_COPILOT,
            notes="Native Teams feature: summarise channel discussions",
        ),
        CanvasSparkAIMapping(
            canvas_feature="Content Generation for Courses",
            canvas_tool="spark_ai",
            copilot_equivalent="PowerPoint Copilot + Word Copilot",
            copilot_product=CopilotProduct.POWERPOINT_COPILOT,
            notes="Generate lecture slides, handouts, and course materials",
        ),
        CanvasSparkAIMapping(
            canvas_feature="Data Analysis for Research",
            canvas_tool="spark_ai",
            copilot_equivalent="Excel Copilot + Power BI Copilot",
            copilot_product=CopilotProduct.EXCEL_COPILOT,
            notes="Advanced data analysis with natural language queries",
        ),
        CanvasSparkAIMapping(
            canvas_feature="Student Query Resolution",
            canvas_tool="aila",
            copilot_equivalent="Custom Agent: Student Support + Enrolment Guide",
            copilot_product=CopilotProduct.COPILOT_STUDIO,
            notes="24/7 AI support with anti-hallucination verification",
        ),
        CanvasSparkAIMapping(
            canvas_feature="Library Resource Search",
            canvas_tool="spark_ai",
            copilot_equivalent="Custom Agent: Library Search",
            copilot_product=CopilotProduct.COPILOT_STUDIO,
            notes="RAG-based search over UniMelb e-library catalogue",
        ),
    ]

    # Custom Copilot Studio agents for UniMelb
    CUSTOM_AGENTS = [
        CopilotAgent(
            agent_id="agent_academic_advisor",
            agent_type=CustomAgentType.ACADEMIC_ADVISOR,
            name="UniMelb Academic Advisor",
            description="AI advisor for course selection, academic planning, "
            "and study support. Anti-hallucination verified.",
            data_sources=["unimelb_handbook", "course_catalogue", "academic_policies"],
            target_users=["students", "academic_staff"],
            knowledge_base="idx-academic-advisor",
        ),
        CopilotAgent(
            agent_id="agent_research_assistant",
            agent_type=CustomAgentType.RESEARCH_ASSISTANT,
            name="UniMelb Research Assistant",
            description="AI research assistant with faculty-specific model routing "
            "and source citation. Supports Law, Engineering, IT, Medicine.",
            data_sources=["unimelb_elibrary", "pubmed", "austlii", "ieee_xplore"],
            target_users=["academic_staff"],
            knowledge_base="idx-research-assistant",
        ),
        CopilotAgent(
            agent_id="agent_student_support",
            agent_type=CustomAgentType.STUDENT_SUPPORT,
            name="UniMelb Student Support",
            description="24/7 student support covering enrolment, fees, "
            "accommodation, life challenge programme, and general queries.",
            data_sources=["student_services", "fee_schedules", "accommodation_db"],
            target_users=["students"],
            knowledge_base="idx-student-support",
        ),
        CopilotAgent(
            agent_id="agent_property",
            agent_type=CustomAgentType.PROPERTY_ASSISTANT,
            name="UniMelb Property Assistant",
            description="Property management assistant for maintenance requests, "
            "lease queries, and tenant support (Lendlease/JLL/MICM integration).",
            data_sources=["mri_property_tree", "maintenance_db", "lease_db"],
            target_users=["professional_staff"],
            knowledge_base="idx-property-assistant",
        ),
        CopilotAgent(
            agent_id="agent_life_challenge",
            agent_type=CustomAgentType.LIFE_CHALLENGE_SUPPORT,
            name="UniMelb Life Challenge Support",
            description="Compassionate AI support for students experiencing "
            "financial hardship, study pauses, or life challenges. "
            "Surfaces relevant support resources and financial aid options.",
            data_sources=["financial_aid_db", "centrelink_guide", "scholarship_db", "counselling_services"],
            target_users=["students"],
            knowledge_base="idx-life-challenge",
        ),
    ]

    def __init__(self) -> None:
        self._agents: dict[str, CopilotAgent] = {
            a.agent_id: a for a in self.CUSTOM_AGENTS
        }

    def get_feature_migration_map(self) -> list[dict[str, Any]]:
        """Get the Canvas Spark AI / Aila → Copilot migration mapping."""
        return [
            {
                "canvas_feature": m.canvas_feature,
                "canvas_tool": m.canvas_tool,
                "copilot_equivalent": m.copilot_equivalent,
                "copilot_product": m.copilot_product.value,
                "migration_status": m.migration_status,
                "notes": m.notes,
            }
            for m in self.FEATURE_MIGRATION_MAP
        ]

    def get_custom_agents(
        self, target_user: str | None = None
    ) -> list[CopilotAgent]:
        """Get custom Copilot Studio agents, optionally filtered by target user."""
        agents = list(self._agents.values())
        if target_user:
            agents = [
                a for a in agents
                if target_user in a.target_users or "all" in a.target_users
            ]
        return [a for a in agents if a.active]

    def get_copilot_products(self) -> list[dict[str, Any]]:
        """Get all Copilot products available to UniMelb."""
        return [
            {
                "product": p.value,
                "description": self._get_product_description(p),
            }
            for p in CopilotProduct
        ]

    def _get_product_description(self, product: CopilotProduct) -> str:
        """Get description for a Copilot product."""
        descriptions = {
            CopilotProduct.TEAMS_COPILOT: "AI assistant in Teams — meeting summaries, action items, chat help",
            CopilotProduct.WORD_COPILOT: "AI writing assistant in Word — drafting, rewriting, summarising",
            CopilotProduct.EXCEL_COPILOT: "AI data analyst in Excel — formulas, charts, insights",
            CopilotProduct.POWERPOINT_COPILOT: "AI presentation designer in PowerPoint",
            CopilotProduct.OUTLOOK_COPILOT: "AI email assistant — drafting, summarising, scheduling",
            CopilotProduct.ONENOTE_COPILOT: "AI note-taking assistant in OneNote",
            CopilotProduct.COPILOT_STUDIO: "Custom AI agent builder — UniMelb-specific agents",
            CopilotProduct.COPILOT_CHAT: "Standalone AI chat (web/mobile) with M365 data access",
            CopilotProduct.POWER_BI_COPILOT: "AI-powered data analysis and visualisation",
        }
        return descriptions.get(product, "")

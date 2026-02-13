"""
Financial Forecast Model — UniMelb AI Platform
================================================
Three-tier financial forecast with year-over-year projections.

Tier 1 — Conservative (Minimum Viable Platform)
Tier 2 — Standard (Full Platform with APAC Readiness)
Tier 3 — Premium (Full APAC Research Platform)

Includes Life Challenge Programme financial pause/restart modelling.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ForecastTier(Enum):
    """Financial forecast tiers."""

    TIER_1_CONSERVATIVE = "tier_1_conservative"
    TIER_2_STANDARD = "tier_2_standard"
    TIER_3_PREMIUM = "tier_3_premium"


@dataclass
class LineItem:
    """A single budget line item."""

    category: str
    description: str
    year_1_aud: float
    year_2_aud: float
    year_3_aud: float


@dataclass
class ForecastTierModel:
    """Complete financial model for a tier."""

    tier: ForecastTier
    name: str
    description: str
    line_items: list[LineItem] = field(default_factory=list)
    contingency_pct: float = 0.10

    @property
    def year_1_subtotal(self) -> float:
        return sum(i.year_1_aud for i in self.line_items)

    @property
    def year_2_subtotal(self) -> float:
        return sum(i.year_2_aud for i in self.line_items)

    @property
    def year_3_subtotal(self) -> float:
        return sum(i.year_3_aud for i in self.line_items)

    @property
    def year_1_contingency(self) -> float:
        return round(self.year_1_subtotal * self.contingency_pct, 2)

    @property
    def year_2_contingency(self) -> float:
        return round(self.year_2_subtotal * self.contingency_pct, 2)

    @property
    def year_3_contingency(self) -> float:
        return round(self.year_3_subtotal * self.contingency_pct, 2)

    @property
    def year_1_total(self) -> float:
        return self.year_1_subtotal + self.year_1_contingency

    @property
    def year_2_total(self) -> float:
        return self.year_2_subtotal + self.year_2_contingency

    @property
    def year_3_total(self) -> float:
        return self.year_3_subtotal + self.year_3_contingency

    @property
    def three_year_total(self) -> float:
        return self.year_1_total + self.year_2_total + self.year_3_total


class FinancialForecastEngine:
    """
    Financial forecast engine for the UniMelb AI Platform.

    Provides three-tier budgeting, year-over-year projections,
    and cost modelling for all platform components.
    """

    def __init__(self) -> None:
        self._tiers: dict[ForecastTier, ForecastTierModel] = {}
        self._build_forecasts()

    def _build_forecasts(self) -> None:
        """Build all three tier forecasts."""
        self._tiers[ForecastTier.TIER_1_CONSERVATIVE] = ForecastTierModel(
            tier=ForecastTier.TIER_1_CONSERVATIVE,
            name="Conservative — Minimum Viable Platform",
            description="Core features only: Teams migration, basic AI, single campus",
            contingency_pct=0.10,
            line_items=[
                LineItem("Azure Infrastructure", "Core Azure services (AU East)", 180_000, 210_000, 240_000),
                LineItem("Microsoft 365 E5 Education", "~12,000 users", 360_000, 360_000, 360_000),
                LineItem("Azure AI Foundry", "Frontier model inference", 120_000, 150_000, 180_000),
                LineItem("Copilot for Microsoft 365", "Staff subset (~600)", 180_000, 240_000, 300_000),
                LineItem("MRI Property Tree", "Licences (basic)", 85_000, 85_000, 85_000),
                LineItem("Canvas Wind-Down", "Parallel running costs", 200_000, 100_000, 0),
                LineItem("Staff", "2 FTE platform engineers", 300_000, 310_000, 320_000),
                LineItem("Training & Change Management", "Staff certification", 80_000, 40_000, 30_000),
                LineItem("Security & Compliance", "IRAP, ISO 27001 prep", 60_000, 30_000, 30_000),
            ],
        )

        self._tiers[ForecastTier.TIER_2_STANDARD] = ForecastTierModel(
            tier=ForecastTier.TIER_2_STANDARD,
            name="Standard — Full Platform with APAC Readiness",
            description="Full features: all faculties, property mgmt, external portal, NZ pilot prep",
            contingency_pct=0.15,
            line_items=[
                LineItem("Azure Infrastructure", "Multi-region (AU East + SE Asia)", 320_000, 380_000, 420_000),
                LineItem("Microsoft 365 E5 Education", "~20,000 users", 600_000, 600_000, 600_000),
                LineItem("Azure AI Foundry", "Frontier + fine-tuned models", 250_000, 300_000, 350_000),
                LineItem("Copilot for Microsoft 365", "All staff", 360_000, 360_000, 360_000),
                LineItem("OpenAI Education Tier", "Enterprise + Research", 48_000, 60_000, 72_000),
                LineItem("Google Workspace Education Plus", "Full suite", 96_000, 96_000, 96_000),
                LineItem("MRI Property Tree", "Full suite (Res + Commercial)", 150_000, 150_000, 150_000),
                LineItem("Canvas Wind-Down", "Parallel running + data archival", 200_000, 100_000, 0),
                LineItem("Staff", "5 FTE (2 eng, 1 data, 1 security, 1 PM)", 750_000, 775_000, 800_000),
                LineItem("External Agent Integration", "Lendlease/JLL/MICM onboarding", 120_000, 60_000, 40_000),
                LineItem("Training & Change Management", "Comprehensive programme", 150_000, 80_000, 60_000),
                LineItem("Security & Compliance", "ISO 27001, IRAP, SOC 2", 120_000, 80_000, 60_000),
                LineItem("NZ/Fiji Pilot Preparation", "Year 2–3 scoping and deployment", 0, 80_000, 160_000),
            ],
        )

        self._tiers[ForecastTier.TIER_3_PREMIUM] = ForecastTierModel(
            tier=ForecastTier.TIER_3_PREMIUM,
            name="Premium — Full APAC Research Platform",
            description="Everything: APAC multi-region, GPU research compute, full anti-hallucination R&D",
            contingency_pct=0.15,
            line_items=[
                LineItem("Azure Infrastructure", "APAC multi-region (AU + SG + NZ)", 500_000, 600_000, 720_000),
                LineItem("Microsoft 365 E5 Education", "50,000+ users (inc. partners)", 1_500_000, 1_500_000, 1_500_000),
                LineItem("Azure AI Foundry", "Full frontier catalogue", 480_000, 600_000, 720_000),
                LineItem("Copilot for Microsoft 365", "Universal deployment", 600_000, 600_000, 600_000),
                LineItem("OpenAI Enterprise + Research", "Full API + fine-tuning", 120_000, 150_000, 180_000),
                LineItem("Google Workspace Education Plus", "Full suite + GCP research", 180_000, 180_000, 180_000),
                LineItem("MRI Property Tree", "Enterprise multi-campus", 250_000, 250_000, 250_000),
                LineItem("Canvas Wind-Down + Archival", "Complete decommission", 250_000, 125_000, 50_000),
                LineItem("Staff", "12 FTE full team", 1_800_000, 1_860_000, 1_920_000),
                LineItem("External Ecosystem", "Agents + tenants + suppliers", 200_000, 120_000, 80_000),
                LineItem("Training & Life Challenge Programme", "Comprehensive + programme costs", 300_000, 200_000, 150_000),
                LineItem("Security & Compliance", "IRAP + ISO + SOC 2 + APAC", 200_000, 150_000, 120_000),
                LineItem("APAC Expansion", "NZ + Fiji + regional partners", 100_000, 300_000, 500_000),
                LineItem("Research AI Compute", "GPU clusters (A100/H100)", 400_000, 500_000, 600_000),
                LineItem("Anti-Hallucination R&D", "Dedicated research programme", 150_000, 180_000, 200_000),
            ],
        )

    def get_forecast(self, tier: ForecastTier) -> ForecastTierModel:
        """Get the financial forecast for a specific tier."""
        return self._tiers[tier]

    def get_all_forecasts(self) -> dict[str, Any]:
        """Get summary of all three tiers."""
        result = {}
        for tier, model in self._tiers.items():
            result[tier.value] = {
                "name": model.name,
                "description": model.description,
                "year_1_aud": model.year_1_total,
                "year_2_aud": model.year_2_total,
                "year_3_aud": model.year_3_total,
                "three_year_total_aud": model.three_year_total,
                "contingency_pct": model.contingency_pct,
            }
        return result

    def get_detailed_forecast(self, tier: ForecastTier) -> dict[str, Any]:
        """Get detailed line-by-line forecast for a tier."""
        model = self._tiers[tier]
        return {
            "tier": tier.value,
            "name": model.name,
            "description": model.description,
            "line_items": [
                {
                    "category": item.category,
                    "description": item.description,
                    "year_1_aud": item.year_1_aud,
                    "year_2_aud": item.year_2_aud,
                    "year_3_aud": item.year_3_aud,
                }
                for item in model.line_items
            ],
            "subtotals": {
                "year_1": model.year_1_subtotal,
                "year_2": model.year_2_subtotal,
                "year_3": model.year_3_subtotal,
            },
            "contingency": {
                "rate": model.contingency_pct,
                "year_1": model.year_1_contingency,
                "year_2": model.year_2_contingency,
                "year_3": model.year_3_contingency,
            },
            "totals": {
                "year_1": model.year_1_total,
                "year_2": model.year_2_total,
                "year_3": model.year_3_total,
                "three_year": model.three_year_total,
            },
        }

    def compare_tiers(self) -> dict[str, Any]:
        """Compare all three tiers side by side."""
        return {
            "comparison": {
                tier.value: {
                    "year_1": model.year_1_total,
                    "year_2": model.year_2_total,
                    "year_3": model.year_3_total,
                    "three_year": model.three_year_total,
                }
                for tier, model in self._tiers.items()
            },
            "recommendation": "tier_2_standard",
            "recommendation_rationale": (
                "Tier 2 provides the best balance of capability, cost, and "
                "APAC readiness. It includes all core features (AI, migration, "
                "property management, external portal) while keeping costs "
                "manageable and preparing for NZ/Fiji expansion in Year 2–3."
            ),
        }

"""
Life Challenge Programme
=========================
"It is to ensure to use a life hardship experiences to still not giving up
as a life challenge — life change programme."

Design: Jiadong Chen (Student ID: 723912)
Target Milestone: 12 February 2026, Melbourne, Australia

Stages:
  1. Finance  — Active but under financial stress
  2. Pause    — Study leave / intermission (up to 6 months, extendable)
  3. Restart  — Returning to study with AI-powered catch-up
  4. Complete — Graduation + alumni lifetime access

The platform NEVER fully disconnects a student during hardship.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class ChallengeStage(Enum):
    """Life Challenge Programme stages."""

    ACTIVE = "active"                   # Normal study
    FINANCE = "finance"                 # Financial stress — full access + support
    PAUSE = "pause"                     # Study leave — limited access preserved
    RESTART = "restart"                 # Returning — full access + catch-up
    COMPLETE = "complete"               # Graduated — alumni access


class SupportType(Enum):
    """Types of support available in the programme."""

    FINANCIAL_AID = "financial_aid"
    SCHOLARSHIP = "scholarship"
    FEE_DEFERRAL = "fee_deferral"
    CENTRELINK_GUIDE = "centrelink_guide"
    MENTAL_HEALTH = "mental_health"
    PEER_MENTORING = "peer_mentoring"
    AI_CATCH_UP = "ai_catch_up"
    CAREER_GUIDANCE = "career_guidance"
    ACADEMIC_ADVISOR = "academic_advisor"
    ACCESSIBILITY = "accessibility"


class AccessLevel(Enum):
    """Platform access levels during different stages."""

    FULL = "full"                       # All features
    FULL_PLUS_SUPPORT = "full_plus"     # All features + enhanced support
    READ_ONLY = "read_only"             # Materials accessible, no submissions
    LIMITED_AI = "limited_ai"           # Basic AI chat, no premium models
    ALUMNI = "alumni"                   # Lifetime alumni portal access


@dataclass
class StudentProfile:
    """Student profile in the Life Challenge Programme."""

    student_id: str
    name: str
    email: str  # @student.unimelb.edu.au
    faculty: str
    course: str
    enrolment_year: int
    current_stage: ChallengeStage = ChallengeStage.ACTIVE
    stage_history: list[dict[str, Any]] = field(default_factory=list)
    pause_start_date: datetime | None = None
    pause_end_date: datetime | None = None  # max 6 months from start
    restart_date: datetime | None = None
    target_completion: datetime | None = None
    support_active: list[SupportType] = field(default_factory=list)
    ai_catch_up_progress: float = 0.0  # 0.0 → 100.0
    notes: str = ""


@dataclass
class SupportResource:
    """A support resource available in the programme."""

    resource_id: str
    support_type: SupportType
    title: str
    description: str
    url: str = ""
    contact_email: str = ""
    available_stages: list[ChallengeStage] = field(default_factory=list)
    auto_surfaced: bool = True  # Automatically shown to eligible students


@dataclass
class CatchUpPlan:
    """AI-generated catch-up plan for a returning student."""

    student_id: str
    missed_weeks: int
    missed_topics: list[str] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    estimated_catch_up_weeks: int = 0
    peer_mentor_matched: bool = False
    ai_summary_generated: bool = False
    progress_pct: float = 0.0


# Stage → access level mapping
STAGE_ACCESS_MAP: dict[ChallengeStage, AccessLevel] = {
    ChallengeStage.ACTIVE: AccessLevel.FULL,
    ChallengeStage.FINANCE: AccessLevel.FULL_PLUS_SUPPORT,
    ChallengeStage.PAUSE: AccessLevel.LIMITED_AI,
    ChallengeStage.RESTART: AccessLevel.FULL_PLUS_SUPPORT,
    ChallengeStage.COMPLETE: AccessLevel.ALUMNI,
}

# Stage → available support types
STAGE_SUPPORT_MAP: dict[ChallengeStage, list[SupportType]] = {
    ChallengeStage.ACTIVE: [],
    ChallengeStage.FINANCE: [
        SupportType.FINANCIAL_AID,
        SupportType.SCHOLARSHIP,
        SupportType.FEE_DEFERRAL,
        SupportType.CENTRELINK_GUIDE,
        SupportType.MENTAL_HEALTH,
        SupportType.ACADEMIC_ADVISOR,
    ],
    ChallengeStage.PAUSE: [
        SupportType.MENTAL_HEALTH,
        SupportType.FINANCIAL_AID,
        SupportType.CENTRELINK_GUIDE,
        SupportType.ACADEMIC_ADVISOR,
    ],
    ChallengeStage.RESTART: [
        SupportType.AI_CATCH_UP,
        SupportType.PEER_MENTORING,
        SupportType.ACADEMIC_ADVISOR,
        SupportType.MENTAL_HEALTH,
        SupportType.CAREER_GUIDANCE,
    ],
    ChallengeStage.COMPLETE: [
        SupportType.CAREER_GUIDANCE,
        SupportType.AI_CATCH_UP,
    ],
}

# Maximum pause duration
MAX_PAUSE_MONTHS = 6
MILESTONE_DATE = datetime(2026, 2, 12)  # 12 February 2026, Melbourne


class LifeChallengeProgramme:
    """
    Life Challenge Programme Manager for UniMelb AI Platform.

    Ensures no student is left behind due to life hardships.
    The platform adapts access, surfaces support, and provides
    AI-powered catch-up when students return.
    """

    def __init__(self) -> None:
        self._students: dict[str, StudentProfile] = {}
        self._support_resources: list[SupportResource] = []
        self._catch_up_plans: dict[str, CatchUpPlan] = {}
        self._init_support_resources()

    def _init_support_resources(self) -> None:
        """Initialise default support resources."""
        self._support_resources = [
            SupportResource(
                resource_id="sr_financial_aid",
                support_type=SupportType.FINANCIAL_AID,
                title="UniMelb Financial Aid Office",
                description="Emergency financial assistance, bursaries, and hardship grants",
                url="https://students.unimelb.edu.au/student-support/financial-support",
                contact_email="financial-aid@unimelb.edu.au",
                available_stages=[
                    ChallengeStage.FINANCE,
                    ChallengeStage.PAUSE,
                    ChallengeStage.RESTART,
                ],
            ),
            SupportResource(
                resource_id="sr_centrelink",
                support_type=SupportType.CENTRELINK_GUIDE,
                title="Centrelink Support Guide",
                description="AI-assisted guide for Centrelink Youth Allowance, "
                "Austudy, and other government support applications",
                available_stages=[
                    ChallengeStage.FINANCE,
                    ChallengeStage.PAUSE,
                ],
            ),
            SupportResource(
                resource_id="sr_mental_health",
                support_type=SupportType.MENTAL_HEALTH,
                title="UniMelb Counselling & Psychological Services",
                description="Free confidential counselling for all enrolled students",
                url="https://students.unimelb.edu.au/student-support/health-and-wellbeing",
                available_stages=[
                    ChallengeStage.FINANCE,
                    ChallengeStage.PAUSE,
                    ChallengeStage.RESTART,
                ],
            ),
            SupportResource(
                resource_id="sr_ai_catchup",
                support_type=SupportType.AI_CATCH_UP,
                title="AI-Powered Study Catch-Up",
                description="Personalised AI summaries of missed content, "
                "practice questions, and progress tracking",
                available_stages=[
                    ChallengeStage.RESTART,
                    ChallengeStage.COMPLETE,
                ],
            ),
            SupportResource(
                resource_id="sr_peer_mentoring",
                support_type=SupportType.PEER_MENTORING,
                title="Peer Mentoring Programme",
                description="Matched with a peer mentor in your faculty "
                "for study support and guidance",
                available_stages=[ChallengeStage.RESTART],
            ),
            SupportResource(
                resource_id="sr_scholarship",
                support_type=SupportType.SCHOLARSHIP,
                title="AI Scholarship Matcher",
                description="AI-powered search across all available scholarships "
                "and grants you may be eligible for",
                available_stages=[ChallengeStage.FINANCE],
            ),
            SupportResource(
                resource_id="sr_career",
                support_type=SupportType.CAREER_GUIDANCE,
                title="Career AI Assistant",
                description="AI-powered career guidance, resume review, "
                "and job matching for graduates",
                available_stages=[
                    ChallengeStage.RESTART,
                    ChallengeStage.COMPLETE,
                ],
            ),
        ]

    # ── Student Management ───────────────────────────────────────────

    def enrol_student(self, student: StudentProfile) -> StudentProfile:
        """Enrol a student in the Life Challenge Programme."""
        student.stage_history.append({
            "stage": student.current_stage.value,
            "date": datetime.now().isoformat(),
            "action": "enrolled",
        })
        self._students[student.student_id] = student
        return student

    def get_student(self, student_id: str) -> StudentProfile | None:
        """Get a student's profile."""
        return self._students.get(student_id)

    def transition_stage(
        self,
        student_id: str,
        new_stage: ChallengeStage,
        reason: str = "",
    ) -> StudentProfile | None:
        """
        Transition a student to a new Life Challenge stage.

        Automatically adjusts platform access and surfaces relevant support.
        """
        student = self._students.get(student_id)
        if not student:
            return None

        old_stage = student.current_stage
        student.current_stage = new_stage
        student.stage_history.append({
            "from_stage": old_stage.value,
            "to_stage": new_stage.value,
            "date": datetime.now().isoformat(),
            "reason": reason,
        })

        # Handle stage-specific logic
        if new_stage == ChallengeStage.PAUSE:
            student.pause_start_date = datetime.now()
            student.pause_end_date = datetime.now() + timedelta(
                days=MAX_PAUSE_MONTHS * 30
            )
        elif new_stage == ChallengeStage.RESTART:
            student.restart_date = datetime.now()
            self._generate_catch_up_plan(student)

        # Update active support
        student.support_active = STAGE_SUPPORT_MAP.get(new_stage, [])

        return student

    def get_access_level(self, student_id: str) -> AccessLevel:
        """Get the current platform access level for a student."""
        student = self._students.get(student_id)
        if not student:
            return AccessLevel.READ_ONLY
        return STAGE_ACCESS_MAP.get(student.current_stage, AccessLevel.FULL)

    # ── Support Resources ────────────────────────────────────────────

    def get_available_support(
        self, student_id: str
    ) -> list[SupportResource]:
        """Get support resources available for a student's current stage."""
        student = self._students.get(student_id)
        if not student:
            return []

        return [
            r
            for r in self._support_resources
            if student.current_stage in r.available_stages
        ]

    def get_auto_surfaced_support(
        self, student_id: str
    ) -> list[SupportResource]:
        """Get support resources that should be automatically shown."""
        available = self.get_available_support(student_id)
        return [r for r in available if r.auto_surfaced]

    # ── Catch-Up Plans ───────────────────────────────────────────────

    def _generate_catch_up_plan(self, student: StudentProfile) -> CatchUpPlan:
        """Generate an AI-powered catch-up plan for a returning student."""
        missed_weeks = 0
        if student.pause_start_date:
            delta = datetime.now() - student.pause_start_date
            missed_weeks = delta.days // 7

        plan = CatchUpPlan(
            student_id=student.student_id,
            missed_weeks=missed_weeks,
            missed_topics=[
                f"Week {i + 1} content" for i in range(missed_weeks)
            ],
            recommended_actions=[
                "Review AI-generated summaries of missed lectures",
                "Complete catch-up quizzes (AI-adapted difficulty)",
                "Schedule meeting with academic advisor",
                "Connect with peer mentor",
                f"Target: full catch-up within {max(missed_weeks // 2, 2)} weeks",
            ],
            estimated_catch_up_weeks=max(missed_weeks // 2, 2),
        )
        self._catch_up_plans[student.student_id] = plan
        return plan

    def get_catch_up_plan(self, student_id: str) -> CatchUpPlan | None:
        """Get the catch-up plan for a returning student."""
        return self._catch_up_plans.get(student_id)

    def update_catch_up_progress(
        self, student_id: str, progress_pct: float
    ) -> CatchUpPlan | None:
        """Update catch-up progress for a student."""
        plan = self._catch_up_plans.get(student_id)
        if plan:
            plan.progress_pct = min(max(progress_pct, 0.0), 100.0)
        return plan

    # ── Programme Metrics ────────────────────────────────────────────

    def get_programme_metrics(self) -> dict[str, Any]:
        """Get programme-wide metrics for reporting."""
        total = len(self._students)
        if total == 0:
            return {"total_students": 0, "message": "No students enrolled"}

        stage_counts: dict[str, int] = {}
        for student in self._students.values():
            key = student.current_stage.value
            stage_counts[key] = stage_counts.get(key, 0) + 1

        active_catch_ups = len(
            [
                p
                for p in self._catch_up_plans.values()
                if 0 < p.progress_pct < 100
            ]
        )
        completed_catch_ups = len(
            [
                p
                for p in self._catch_up_plans.values()
                if p.progress_pct >= 100
            ]
        )

        return {
            "total_students": total,
            "stage_distribution": stage_counts,
            "active_catch_up_plans": active_catch_ups,
            "completed_catch_ups": completed_catch_ups,
            "milestone_date": MILESTONE_DATE.isoformat(),
            "days_to_milestone": max(
                (MILESTONE_DATE - datetime.now()).days, 0
            ),
        }

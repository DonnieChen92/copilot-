"""
Canvas LMS → Microsoft Teams Migration Toolkit
================================================
Three-plan migration framework for UniMelb:
  Plan A: Internal University (Staff + Academic Faculty)
  Plan B: External Suppliers, Retail & Commercial Tenants
  Plan C: Service Providers & Government Integration

Supports automated content migration, user mapping, and progress tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MigrationPlan(Enum):
    """The three migration plans."""

    PLAN_A_INTERNAL = "plan_a_internal"
    PLAN_B_EXTERNAL = "plan_b_external"
    PLAN_C_GOVERNMENT = "plan_c_government"


class MigrationStage(Enum):
    """Lifecycle stages for each plan."""

    # Plan A stages
    A1_DISCOVERY_AUDIT = "a1_discovery_audit"
    A2_PILOT_COHORT = "a2_pilot_cohort"
    A3_CONTENT_MIGRATION = "a3_content_migration"
    A4_TRAINING_CERTIFICATION = "a4_training_certification"
    A5_FULL_CUTOVER = "a5_full_cutover"
    A6_POST_MIGRATION_REVIEW = "a6_post_migration_review"

    # Plan B stages
    B1_STAKEHOLDER_MAPPING = "b1_stakeholder_mapping"
    B2_PORTAL_DEVELOPMENT = "b2_portal_development"
    B3_AGENT_ONBOARDING = "b3_agent_onboarding"
    B4_TENANT_MIGRATION = "b4_tenant_migration"
    B5_SUBTENANT_ROLLOUT = "b5_subtenant_rollout"
    B6_GO_LIVE_SUPPORT = "b6_go_live_support"

    # Plan C stages
    C1_REGULATORY_FRAMEWORK = "c1_regulatory_framework"
    C2_AUDIT_INFRASTRUCTURE = "c2_audit_infrastructure"
    C3_COMPLIANCE_CERTIFICATION = "c3_compliance_certification"
    C4_NZ_PILOT_EXTENSION = "c4_nz_pilot_extension"
    C5_APAC_FRAMEWORK = "c5_apac_framework"


class StageStatus(Enum):
    """Status of a migration stage."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class ContentType(Enum):
    """Canvas content types to be migrated."""

    COURSE = "course"
    MODULE = "module"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    DISCUSSION = "discussion"
    GRADE = "grade"
    FILE = "file"
    ANNOUNCEMENT = "announcement"
    CALENDAR_EVENT = "calendar_event"
    INBOX_MESSAGE = "inbox_message"
    RUBRIC = "rubric"
    PAGE = "page"


@dataclass
class CanvasContent:
    """A single piece of Canvas LMS content to be migrated."""

    content_id: str
    content_type: ContentType
    title: str
    course_id: str
    course_name: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    size_bytes: int = 0
    created_at: datetime | None = None
    migrated: bool = False
    teams_destination: str = ""  # Teams channel/resource URL


@dataclass
class TeamsMapping:
    """Mapping from Canvas structure to Teams structure."""

    canvas_course_id: str
    canvas_course_name: str
    teams_team_id: str = ""
    teams_team_name: str = ""
    channel_mappings: dict[str, str] = field(default_factory=dict)
    # canvas_module_id → teams_channel_id
    assignment_mappings: dict[str, str] = field(default_factory=dict)
    # canvas_assignment_id → teams_assignment_id
    file_mappings: dict[str, str] = field(default_factory=dict)
    # canvas_file_id → sharepoint_url


@dataclass
class StageProgress:
    """Progress tracker for a single migration stage."""

    plan: MigrationPlan
    stage: MigrationStage
    status: StageStatus = StageStatus.NOT_STARTED
    start_date: datetime | None = None
    target_end_date: datetime | None = None
    actual_end_date: datetime | None = None
    completion_pct: float = 0.0
    blockers: list[str] = field(default_factory=list)
    notes: str = ""
    owner: str = ""


@dataclass
class MigrationMetrics:
    """Migration progress metrics."""

    total_courses: int = 0
    migrated_courses: int = 0
    total_content_items: int = 0
    migrated_content_items: int = 0
    total_users: int = 0
    migrated_users: int = 0
    total_files_gb: float = 0.0
    migrated_files_gb: float = 0.0
    errors: list[dict[str, Any]] = field(default_factory=list)


class CanvasToTeamsMigrationToolkit:
    """
    Canvas LMS → Microsoft Teams migration toolkit for UniMelb.

    Manages the three-plan migration across all stakeholder groups.

    Canvas Components → Teams Equivalents:
      Courses          → Teams (one per course)
      Modules          → Channels + Tabs
      Assignments      → Teams Assignments + Rubrics
      Grades           → Teams Gradebook + Azure SQL
      Discussion Boards→ Teams Posts + Channels
      Quizzes          → MS Forms + AI-assisted grading
      SpeedGrader      → Teams Feedback + Copilot review
      Canvas Inbox     → Teams Chat + Outlook
      Turnitin         → Turnitin Teams Integration
      Spark AI / Aila  → UniMelb AI Copilot (Azure Foundry)
      Calendar         → Outlook + Teams Calendar
      Files            → SharePoint + OneDrive
      Analytics        → Power BI + Azure Monitor
    """

    # Canvas → Teams mapping rules
    CONTENT_MIGRATION_MAP = {
        ContentType.COURSE: "teams_team",
        ContentType.MODULE: "teams_channel",
        ContentType.ASSIGNMENT: "teams_assignment",
        ContentType.QUIZ: "ms_forms",
        ContentType.DISCUSSION: "teams_channel_post",
        ContentType.GRADE: "teams_gradebook",
        ContentType.FILE: "sharepoint_document",
        ContentType.ANNOUNCEMENT: "teams_channel_announcement",
        ContentType.CALENDAR_EVENT: "outlook_calendar",
        ContentType.INBOX_MESSAGE: "teams_chat",
        ContentType.RUBRIC: "teams_rubric",
        ContentType.PAGE: "sharepoint_page",
    }

    def __init__(self, canvas_api_url: str = "", canvas_api_key: str = ""):
        self.canvas_api_url = canvas_api_url
        self.canvas_api_key = canvas_api_key
        self._content_inventory: list[CanvasContent] = []
        self._team_mappings: dict[str, TeamsMapping] = {}
        self._stage_progress: dict[MigrationStage, StageProgress] = {}
        self._metrics = MigrationMetrics()
        self._init_stages()

    def _init_stages(self) -> None:
        """Initialise all migration stages across all three plans."""
        plan_stages = {
            MigrationPlan.PLAN_A_INTERNAL: [
                MigrationStage.A1_DISCOVERY_AUDIT,
                MigrationStage.A2_PILOT_COHORT,
                MigrationStage.A3_CONTENT_MIGRATION,
                MigrationStage.A4_TRAINING_CERTIFICATION,
                MigrationStage.A5_FULL_CUTOVER,
                MigrationStage.A6_POST_MIGRATION_REVIEW,
            ],
            MigrationPlan.PLAN_B_EXTERNAL: [
                MigrationStage.B1_STAKEHOLDER_MAPPING,
                MigrationStage.B2_PORTAL_DEVELOPMENT,
                MigrationStage.B3_AGENT_ONBOARDING,
                MigrationStage.B4_TENANT_MIGRATION,
                MigrationStage.B5_SUBTENANT_ROLLOUT,
                MigrationStage.B6_GO_LIVE_SUPPORT,
            ],
            MigrationPlan.PLAN_C_GOVERNMENT: [
                MigrationStage.C1_REGULATORY_FRAMEWORK,
                MigrationStage.C2_AUDIT_INFRASTRUCTURE,
                MigrationStage.C3_COMPLIANCE_CERTIFICATION,
                MigrationStage.C4_NZ_PILOT_EXTENSION,
                MigrationStage.C5_APAC_FRAMEWORK,
            ],
        }
        for plan, stages in plan_stages.items():
            for stage in stages:
                self._stage_progress[stage] = StageProgress(
                    plan=plan, stage=stage
                )

    # ── Canvas Content Inventory ─────────────────────────────────────

    def discover_canvas_content(
        self,
        course_ids: list[str] | None = None,
    ) -> list[CanvasContent]:
        """
        Discover and inventory all Canvas LMS content.

        In production, this calls the Canvas REST API to enumerate all
        courses, modules, assignments, files, etc.
        """
        # Alpha: interface contract
        # Production: Canvas API integration
        return self._content_inventory

    def add_content_to_inventory(self, content: CanvasContent) -> None:
        """Add a Canvas content item to the migration inventory."""
        self._content_inventory.append(content)
        self._metrics.total_content_items = len(self._content_inventory)

    def get_inventory_summary(self) -> dict[str, Any]:
        """Get a summary of the Canvas content inventory."""
        by_type: dict[str, int] = {}
        for item in self._content_inventory:
            key = item.content_type.value
            by_type[key] = by_type.get(key, 0) + 1

        return {
            "total_items": len(self._content_inventory),
            "by_type": by_type,
            "migrated": sum(1 for i in self._content_inventory if i.migrated),
            "pending": sum(
                1 for i in self._content_inventory if not i.migrated
            ),
            "total_size_bytes": sum(
                i.size_bytes for i in self._content_inventory
            ),
        }

    # ── Teams Mapping ────────────────────────────────────────────────

    def create_teams_mapping(self, mapping: TeamsMapping) -> TeamsMapping:
        """Create a Canvas course → Teams team mapping."""
        self._team_mappings[mapping.canvas_course_id] = mapping
        return mapping

    def get_teams_destination(
        self, content_type: ContentType
    ) -> str:
        """Get the Teams destination type for a Canvas content type."""
        return self.CONTENT_MIGRATION_MAP.get(content_type, "unknown")

    # ── Migration Execution ──────────────────────────────────────────

    def migrate_content(
        self, content: CanvasContent
    ) -> dict[str, Any]:
        """
        Migrate a single Canvas content item to its Teams equivalent.

        Returns migration result with status and destination.
        """
        destination_type = self.get_teams_destination(content.content_type)
        mapping = self._team_mappings.get(content.course_id)

        if not mapping:
            return {
                "status": "error",
                "message": f"No Teams mapping found for course {content.course_id}",
                "content_id": content.content_id,
            }

        # Alpha: mark as migrated (simulate)
        content.migrated = True
        content.teams_destination = f"{destination_type}://{mapping.teams_team_id}"
        self._metrics.migrated_content_items += 1

        return {
            "status": "success",
            "content_id": content.content_id,
            "content_type": content.content_type.value,
            "source": f"canvas://{content.course_id}/{content.content_id}",
            "destination": content.teams_destination,
            "destination_type": destination_type,
        }

    def migrate_course(self, course_id: str) -> dict[str, Any]:
        """Migrate all content for a single Canvas course."""
        items = [
            c for c in self._content_inventory if c.course_id == course_id
        ]
        results = []
        for item in items:
            result = self.migrate_content(item)
            results.append(result)

        success = sum(1 for r in results if r["status"] == "success")
        return {
            "course_id": course_id,
            "total_items": len(items),
            "migrated": success,
            "errors": len(items) - success,
            "details": results,
        }

    # ── Stage Management ─────────────────────────────────────────────

    def update_stage(
        self,
        stage: MigrationStage,
        status: StageStatus,
        completion_pct: float = 0.0,
        notes: str = "",
    ) -> StageProgress:
        """Update the status of a migration stage."""
        progress = self._stage_progress[stage]
        progress.status = status
        progress.completion_pct = completion_pct
        progress.notes = notes

        if status == StageStatus.IN_PROGRESS and not progress.start_date:
            progress.start_date = datetime.now()
        elif status == StageStatus.COMPLETED:
            progress.actual_end_date = datetime.now()
            progress.completion_pct = 100.0

        return progress

    def get_plan_progress(self, plan: MigrationPlan) -> list[StageProgress]:
        """Get progress for all stages in a given plan."""
        return [
            p for p in self._stage_progress.values() if p.plan == plan
        ]

    def get_overall_progress(self) -> dict[str, Any]:
        """Get overall migration progress across all three plans."""
        plans_summary = {}
        for plan in MigrationPlan:
            stages = self.get_plan_progress(plan)
            completed = sum(
                1 for s in stages if s.status == StageStatus.COMPLETED
            )
            total = len(stages)
            avg_pct = (
                sum(s.completion_pct for s in stages) / total if total else 0
            )
            plans_summary[plan.value] = {
                "total_stages": total,
                "completed_stages": completed,
                "average_completion_pct": round(avg_pct, 1),
                "status": (
                    "completed"
                    if completed == total
                    else "in_progress"
                    if any(
                        s.status == StageStatus.IN_PROGRESS for s in stages
                    )
                    else "not_started"
                ),
            }

        return {
            "plans": plans_summary,
            "content_metrics": {
                "total_items": self._metrics.total_content_items,
                "migrated_items": self._metrics.migrated_content_items,
                "migration_pct": (
                    round(
                        self._metrics.migrated_content_items
                        / self._metrics.total_content_items
                        * 100,
                        1,
                    )
                    if self._metrics.total_content_items > 0
                    else 0
                ),
            },
        }

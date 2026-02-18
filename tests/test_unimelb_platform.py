"""
Tests for UniMelb AI Platform modules.
=========================================
Covers: Azure Foundry, Anti-Hallucination, Property Management,
Canvas Migration, Education Platforms, Life Challenge, Compliance,
Financial Forecast, and Mobile Integration.
"""

import pytest
from datetime import datetime, timedelta

# --- Azure AI Foundry ---
from src.unimelb.azure_foundry.foundry_client import (
    AzureFoundryClient,
    FoundryModelRouter,
    FoundryResponse,
    FrontierModel,
    MultiModelResult,
)


class TestAzureFoundryClient:
    def test_init_default(self):
        client = AzureFoundryClient()
        assert client.tenant_id == "unimelb"

    def test_get_available_models(self):
        client = AzureFoundryClient()
        models = client.get_available_models()
        assert len(models) > 0
        model_ids = [m["model"] for m in models]
        assert "gpt-4o" in model_ids
        assert "claude-opus-4-6" in model_ids

    def test_chat_returns_foundry_response(self):
        client = AzureFoundryClient()
        response = client.chat(
            messages=[{"role": "user", "content": "Hello"}],
            model=FrontierModel.GPT_4O,
        )
        assert isinstance(response, FoundryResponse)
        assert response.model == "gpt-4o"
        assert response.provider == "microsoft"

    def test_multi_model_query(self):
        client = AzureFoundryClient()
        result = client.multi_model_query(
            messages=[{"role": "user", "content": "What is 2+2?"}],
        )
        assert isinstance(result, MultiModelResult)
        assert len(result.responses) == 3  # default 3 models
        assert result.verification_status in [
            "high_confidence",
            "partially_verified",
            "unverified_manual_review_required",
        ]


class TestFoundryModelRouter:
    def test_route_by_faculty(self):
        client = AzureFoundryClient()
        router = FoundryModelRouter(client)
        result = router.route(
            messages=[{"role": "user", "content": "Test"}],
            faculty="law",
        )
        assert isinstance(result, FoundryResponse)
        assert result.model == "claude-opus-4-6"

    def test_route_with_verification(self):
        client = AzureFoundryClient()
        router = FoundryModelRouter(client)
        result = router.route(
            messages=[{"role": "user", "content": "Test"}],
            require_verification=True,
        )
        assert isinstance(result, MultiModelResult)


# --- Anti-Hallucination Engine ---
from src.unimelb.anti_hallucination.verification_engine import (
    AntiHallucinationEngine,
    SourceCitation,
    SourceType,
    VerificationResult,
    VerificationStatus,
)


class TestAntiHallucinationEngine:
    def test_verify_basic_response(self):
        engine = AntiHallucinationEngine()
        result = engine.verify_response(
            query="What is Python?",
            response="Python is a programming language.",
        )
        assert isinstance(result, VerificationResult)
        assert 0.0 <= result.confidence_score <= 1.0

    def test_legal_query_requires_manual_review(self):
        engine = AntiHallucinationEngine()
        result = engine.verify_response(
            query="What does Section 51 of the Australian Constitution say about legislation?",
            response="Section 51 grants the Parliament power to make laws.",
        )
        assert result.status in (
            VerificationStatus.LEGISLATION_CHECK,
            VerificationStatus.MANUAL_REVIEW_REQUIRED,
        )

    def test_high_confidence_with_sources(self):
        engine = AntiHallucinationEngine()
        sources = [
            SourceCitation(
                source_type=SourceType.ACADEMIC_PAPER,
                title="Test Paper",
                reference="doi:10.1234/test",
                verified=True,
            ),
            SourceCitation(
                source_type=SourceType.TEXTBOOK,
                title="Test Textbook",
                reference="ISBN:123",
                verified=True,
            ),
        ]
        result = engine.verify_response(
            query="What is machine learning?",
            response="ML is a subset of AI.",
            model_responses=[
                {"model": "gpt-4o", "content": "ML is a subset of AI."},
                {"model": "claude", "content": "ML is a subset of AI."},
                {"model": "gemini", "content": "ML is a subset of AI."},
            ],
            sources=sources,
        )
        assert result.confidence_score > 0.5

    def test_format_response_includes_verification(self):
        engine = AntiHallucinationEngine()
        result = engine.verify_response(
            query="Test",
            response="Test response",
        )
        formatted = engine.format_response_with_verification(result)
        assert "Verification:" in formatted
        assert "Confidence:" in formatted

    def test_review_queue(self):
        engine = AntiHallucinationEngine()
        engine.verify_response(
            query="What does the Privacy Act 1988 legislation say?",
            response="The Act covers...",
        )
        queue = engine.get_review_queue()
        assert len(queue) > 0

    def test_accuracy_metrics(self):
        engine = AntiHallucinationEngine()
        engine.verify_response(query="Test 1", response="Response 1")
        engine.verify_response(query="Test 2", response="Response 2")
        metrics = engine.get_accuracy_metrics()
        assert metrics["total_queries"] == 2


# --- MRI Property Tree ---
from src.unimelb.property_management.mri_property_tree import (
    DeploymentEnvironment,
    Lease,
    LeaseStatus,
    MaintenanceRequest,
    MaintenanceStatus,
    MRIPropertyTreeClient,
    Property,
    PropertyType,
    Tenant,
    TenantRole,
)


class TestMRIPropertyTree:
    def test_register_and_get_property(self):
        client = MRIPropertyTreeClient()
        prop = Property(
            property_id="P001",
            name="Student Housing Block A",
            property_type=PropertyType.RESIDENTIAL_STUDENT,
            address="123 Grattan St, Parkville VIC 3010",
        )
        client.register_property(prop)
        result = client.get_property("P001")
        assert result is not None
        assert result.name == "Student Housing Block A"

    def test_register_agents(self):
        client = MRIPropertyTreeClient()
        for agent_data in [
            ("A001", "Lendlease", TenantRole.AGENT_LENDLEASE),
            ("A002", "JLL", TenantRole.AGENT_JLL),
            ("A003", "MICM", TenantRole.AGENT_MICM),
        ]:
            client.register_tenant(Tenant(
                tenant_id=agent_data[0],
                name=agent_data[1],
                role=agent_data[2],
                company=agent_data[1],
            ))
        agents = client.list_agents()
        assert len(agents) == 3

    def test_lease_lifecycle(self):
        client = MRIPropertyTreeClient()
        lease = Lease(
            lease_id="L001",
            property_id="P001",
            tenant_id="T001",
            lease_type=PropertyType.COMMERCIAL_RETAIL,
            status=LeaseStatus.ACTIVE,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            rent_amount_aud=5000.0,
        )
        client.create_lease(lease)
        expiring = client.get_expiring_leases(within_days=90)
        assert len(expiring) == 1

    def test_portfolio_summary(self):
        client = MRIPropertyTreeClient()
        client.register_property(Property(
            property_id="P001", name="Shop A",
            property_type=PropertyType.COMMERCIAL_RETAIL,
            address="Test",
        ))
        client.register_property(Property(
            property_id="P002", name="Room B",
            property_type=PropertyType.RESIDENTIAL_STUDENT,
            address="Test",
        ))
        summary = client.get_portfolio_summary()
        assert summary["total_properties"] == 2
        assert summary["residential_count"] == 1
        assert summary["commercial_count"] == 1

    def test_deployment_environments(self):
        client = MRIPropertyTreeClient()
        info = client.get_environment_info()
        assert info["environment"] == "alpha_dev"
        client.switch_environment(DeploymentEnvironment.BETA_STAGING)
        info = client.get_environment_info()
        assert info["environment"] == "beta_staging"


# --- Canvas Migration Toolkit ---
from src.unimelb.canvas_lms.migration_toolkit import (
    CanvasContent,
    CanvasToTeamsMigrationToolkit,
    ContentType,
    MigrationPlan,
    MigrationStage,
    StageStatus,
    TeamsMapping,
)


class TestCanvasMigrationToolkit:
    def test_init_stages(self):
        toolkit = CanvasToTeamsMigrationToolkit()
        plan_a = toolkit.get_plan_progress(MigrationPlan.PLAN_A_INTERNAL)
        plan_b = toolkit.get_plan_progress(MigrationPlan.PLAN_B_EXTERNAL)
        plan_c = toolkit.get_plan_progress(MigrationPlan.PLAN_C_GOVERNMENT)
        assert len(plan_a) == 6
        assert len(plan_b) == 6
        assert len(plan_c) == 5

    def test_content_migration_map(self):
        toolkit = CanvasToTeamsMigrationToolkit()
        assert toolkit.get_teams_destination(ContentType.COURSE) == "teams_team"
        assert toolkit.get_teams_destination(ContentType.QUIZ) == "ms_forms"

    def test_migrate_content(self):
        toolkit = CanvasToTeamsMigrationToolkit()
        toolkit.create_teams_mapping(TeamsMapping(
            canvas_course_id="C001",
            canvas_course_name="Test Course",
            teams_team_id="T001",
        ))
        content = CanvasContent(
            content_id="X001",
            content_type=ContentType.ASSIGNMENT,
            title="Assignment 1",
            course_id="C001",
        )
        toolkit.add_content_to_inventory(content)
        result = toolkit.migrate_content(content)
        assert result["status"] == "success"
        assert content.migrated is True

    def test_stage_update(self):
        toolkit = CanvasToTeamsMigrationToolkit()
        progress = toolkit.update_stage(
            MigrationStage.A1_DISCOVERY_AUDIT,
            StageStatus.IN_PROGRESS,
            completion_pct=50.0,
        )
        assert progress.status == StageStatus.IN_PROGRESS
        assert progress.completion_pct == 50.0

    def test_overall_progress(self):
        toolkit = CanvasToTeamsMigrationToolkit()
        progress = toolkit.get_overall_progress()
        assert "plans" in progress
        assert "content_metrics" in progress


# --- Education Platforms ---
from src.unimelb.education_platforms.platform_connectors import (
    GoogleEduTier,
    MicrosoftEduTier,
    OpenAITier,
    PlatformUser,
    UnifiedEducationPlatform,
)


class TestEducationPlatforms:
    def _make_user(self, role="student"):
        return PlatformUser(
            user_id="U001",
            email="test@unimelb.edu.au",
            display_name="Test User",
            role=role,
            faculty="Engineering",
        )

    def test_unified_platform_services(self):
        platform = UnifiedEducationPlatform()
        services = platform.get_all_services()
        assert "microsoft" in services
        assert "google" in services
        assert len(services["microsoft"]) > 0

    def test_user_entitlements(self):
        platform = UnifiedEducationPlatform()
        user = self._make_user()
        entitlements = platform.get_user_entitlements(user)
        assert entitlements["user"]["email"] == "test@unimelb.edu.au"
        assert "microsoft" in entitlements
        assert "google" in entitlements
        assert "openai" in entitlements

    def test_openai_tier_recommendation(self):
        platform = UnifiedEducationPlatform()
        student = self._make_user("student")
        staff = self._make_user("academic_staff")
        assert platform.openai.recommend_tier(student) == OpenAITier.STUDENT
        assert platform.openai.recommend_tier(staff) == OpenAITier.RESEARCH

    def test_provision_user(self):
        platform = UnifiedEducationPlatform()
        user = self._make_user()
        result = platform.provision_user(user)
        assert result["provisioned"]["microsoft"]["status"] == "active"
        assert result["sso_configured"] is True


# --- Life Challenge Programme ---
from src.unimelb.life_challenge.programme import (
    AccessLevel,
    ChallengeStage,
    LifeChallengeProgramme,
    StudentProfile,
)


class TestLifeChallengeProgramme:
    def _make_student(self):
        return StudentProfile(
            student_id="723912",
            name="Jiadong Chen",
            email="jchen@student.unimelb.edu.au",
            faculty="Engineering",
            course="Master of IT",
            enrolment_year=2023,
        )

    def test_enrol_student(self):
        programme = LifeChallengeProgramme()
        student = self._make_student()
        programme.enrol_student(student)
        result = programme.get_student("723912")
        assert result is not None
        assert result.name == "Jiadong Chen"

    def test_transition_to_pause(self):
        programme = LifeChallengeProgramme()
        student = self._make_student()
        programme.enrol_student(student)
        programme.transition_stage("723912", ChallengeStage.PAUSE, "Financial hardship")
        result = programme.get_student("723912")
        assert result.current_stage == ChallengeStage.PAUSE
        assert result.pause_start_date is not None

    def test_transition_to_restart_generates_catchup(self):
        programme = LifeChallengeProgramme()
        student = self._make_student()
        programme.enrol_student(student)
        programme.transition_stage("723912", ChallengeStage.PAUSE)
        programme.transition_stage("723912", ChallengeStage.RESTART)
        plan = programme.get_catch_up_plan("723912")
        assert plan is not None
        assert len(plan.recommended_actions) > 0

    def test_access_levels(self):
        programme = LifeChallengeProgramme()
        student = self._make_student()
        programme.enrol_student(student)
        assert programme.get_access_level("723912") == AccessLevel.FULL
        programme.transition_stage("723912", ChallengeStage.PAUSE)
        assert programme.get_access_level("723912") == AccessLevel.LIMITED_AI

    def test_available_support(self):
        programme = LifeChallengeProgramme()
        student = self._make_student()
        programme.enrol_student(student)
        programme.transition_stage("723912", ChallengeStage.FINANCE)
        support = programme.get_available_support("723912")
        assert len(support) > 0

    def test_programme_metrics(self):
        programme = LifeChallengeProgramme()
        student = self._make_student()
        programme.enrol_student(student)
        metrics = programme.get_programme_metrics()
        assert metrics["total_students"] == 1


# --- Compliance & Audit ---
from src.unimelb.compliance.azure_monitor import (
    AuditEvent,
    AuditEventType,
    AzureMonitorLogger,
    ComplianceFramework,
)
from src.unimelb.compliance.regulatory_framework import (
    ComplianceStatus,
    Jurisdiction,
    RegulatoryDomain,
    RegulatoryFramework,
)


class TestAzureMonitorLogger:
    def test_log_ai_interaction(self):
        logger = AzureMonitorLogger()
        event_id = logger.log_ai_interaction(
            user_id="U001",
            user_email="test@unimelb.edu.au",
            query="What is AI?",
            response="AI is artificial intelligence.",
            model="gpt-4o",
            confidence_score=0.85,
            verification_status="high_confidence",
        )
        assert event_id.startswith("EVT-")

    def test_query_audit_log(self):
        logger = AzureMonitorLogger()
        logger.log_ai_interaction(
            user_id="U001", user_email="", query="Q1",
            response="R1", model="gpt-4o",
            confidence_score=0.9, verification_status="high_confidence",
        )
        results = logger.query_audit_log(event_type=AuditEventType.AI_QUERY)
        assert len(results) == 1

    def test_ai_usage_summary(self):
        logger = AzureMonitorLogger()
        logger.log_ai_interaction(
            user_id="U001", user_email="", query="Q1",
            response="R1", model="gpt-4o",
            confidence_score=0.9, verification_status="high_confidence",
            tokens_used=100, cost_aud=0.01,
        )
        summary = logger.get_ai_usage_summary()
        assert summary["total_queries"] == 1
        assert summary["total_tokens"] == 100


class TestRegulatoryFramework:
    def test_get_australian_requirements(self):
        framework = RegulatoryFramework()
        reqs = framework.get_requirements(jurisdiction=Jurisdiction.AUSTRALIA)
        assert len(reqs) > 0

    def test_get_nz_requirements(self):
        framework = RegulatoryFramework()
        reqs = framework.get_requirements(jurisdiction=Jurisdiction.NEW_ZEALAND)
        assert len(reqs) > 0

    def test_generate_compliance_report(self):
        framework = RegulatoryFramework()
        report = framework.generate_compliance_report(Jurisdiction.AUSTRALIA)
        assert report.total_requirements > 0

    def test_government_audit_dashboard(self):
        framework = RegulatoryFramework()
        dashboard = framework.get_government_audit_dashboard()
        assert "jurisdictions" in dashboard
        assert "australia" in dashboard["jurisdictions"]


# --- Financial Forecast ---
from src.unimelb.professional_staff.financial_forecast import (
    FinancialForecastEngine,
    ForecastTier,
)


class TestFinancialForecast:
    def test_all_tiers_exist(self):
        engine = FinancialForecastEngine()
        forecasts = engine.get_all_forecasts()
        assert "tier_1_conservative" in forecasts
        assert "tier_2_standard" in forecasts
        assert "tier_3_premium" in forecasts

    def test_tier_1_totals(self):
        engine = FinancialForecastEngine()
        model = engine.get_forecast(ForecastTier.TIER_1_CONSERVATIVE)
        assert model.year_1_total > 0
        assert model.three_year_total > model.year_1_total

    def test_tier_2_is_recommended(self):
        engine = FinancialForecastEngine()
        comparison = engine.compare_tiers()
        assert comparison["recommendation"] == "tier_2_standard"

    def test_detailed_forecast(self):
        engine = FinancialForecastEngine()
        detail = engine.get_detailed_forecast(ForecastTier.TIER_2_STANDARD)
        assert len(detail["line_items"]) > 0
        assert detail["totals"]["three_year"] > 0

    def test_tier_3_highest(self):
        engine = FinancialForecastEngine()
        forecasts = engine.get_all_forecasts()
        assert (
            forecasts["tier_3_premium"]["three_year_total_aud"]
            > forecasts["tier_2_standard"]["three_year_total_aud"]
            > forecasts["tier_1_conservative"]["three_year_total_aud"]
        )


# --- Mobile Integration ---
from src.unimelb.mobile_integration.ios_apps import (
    NotificationType,
    iOSApp,
    iOSAppIntegrationLayer,
)


class TestiOSAppIntegration:
    def test_register_device(self):
        layer = iOSAppIntegrationLayer()
        user = layer.register_device(
            user_id="U001",
            app=iOSApp.UNIMELB_OFFICIAL,
            device_token="abc123",
            email="test@unimelb.edu.au",
        )
        assert iOSApp.UNIMELB_OFFICIAL in user.apps_installed
        assert user.device_tokens[iOSApp.UNIMELB_OFFICIAL.value] == "abc123"

    def test_send_notification(self):
        layer = iOSAppIntegrationLayer()
        layer.register_device("U001", iOSApp.UNIMELB_OFFICIAL, "tok123")
        notification = layer.send_notification(
            target_app=iOSApp.UNIMELB_OFFICIAL,
            target_user_id="U001",
            notification_type=NotificationType.AI_RESPONSE_READY,
            title="Test",
            body="Test notification",
        )
        assert notification is not None
        assert notification.delivered is True

    def test_api_spec(self):
        layer = iOSAppIntegrationLayer()
        spec = layer.get_api_spec()
        assert spec["info"]["title"] == "UniMelb AI Platform — iOS API"
        assert len(spec["paths"]) > 0

    def test_app_ids(self):
        assert iOSApp.UNIMELB_OFFICIAL.value == "904152776"
        assert iOSApp.MYMBS.value == "1095799806"

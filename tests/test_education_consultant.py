"""
Tests for Education Consultant Categorisation_OS (COS) v3.1 — Extended Compliance.
====================================================================================
"""

import pytest

from src.unimelb.education_consultant.categorisation_os import (
    ACADEMIC_INTEGRITY_RULES,
    ADVISORY_NEUTRALITY,
    AUDIT_TRAIL_REQUIREMENTS,
    AcademicCluster,
    AQFLevel,
    BREACH_RESPONSE_STEPS,
    COSExpandedLayer,
    COSLayer,
    COSSection,
    COS_OPERATIONAL_LOOP,
    CODE_OF_CONDUCT,
    CONDUCT_STANDARDS,
    Confidence,
    ConductEntry,
    DATA_CATEGORIES,
    DATA_GOVERNANCE_CONTROLS,
    DataGovernanceControl,
    DataLifecycleStage,
    DEFAULT_SUBJECT_TEMPLATE,
    EQUALITY_CHARTER_PRINCIPLE,
    EQUALITY_RESPECT_VALUES,
    EXTENDED_PRE_USE_CHECKLIST,
    EducationConsultantCOS,
    EducationSearchArchitecture,
    HIGHER_ED_GOVERNANCE_CHECKLIST,
    HigherEdChecklistItem,
    Impact,
    INSTITUTION_REGISTRY,
    InstitutionProfile,
    LEGISLATIVE_ALIGNMENT_MATRIX,
    LIABILITY_NOTICE,
    LegislativeCategory,
    LegislativeEntry,
    OccupationRiskCategory,
    PathwayOption,
    PROFESSIONAL_DEVELOPMENT_PATH,
    PROFESSIONAL_KNOWLEDGE_REQUIREMENTS,
    PROHIBITED_CONDUCT,
    PROTECTED_ATTRIBUTES,
    ProtectedAttribute,
    ProhibitedConductEntry,
    QUARTERLY_MONITORING_ITEMS,
    REFERENCE_INDEX,
    REQUIRED_DOCUMENTATION,
    ReferenceEntry,
    RoleType,
    SAFETY_GATE_CHECKS,
    SafetyGateResult,
    SEARCH_STEP_CRITERIA,
    SKILLED_MIGRATION_COMPLIANCE,
    STUDENT_500_COMPLIANCE,
    SearchStep,
    StateTerritory,
    TraceabilityClaim,
    VISITOR_600_COMPLIANCE,
    VisaSubclass,
    AUTHORITATIVE_DOMAINS,
    AuditTrailEntry,
)


class TestCOSEnums:
    """Tests for COS enumeration types."""

    def test_cos_layers_count(self):
        assert len(COSLayer) == 8

    def test_cos_sections_count(self):
        assert len(COSSection) == 16  # COS-00 through COS-15

    def test_cos_section_values(self):
        assert COSSection.COS_00.value == "COS-00"
        assert COSSection.COS_15.value == "COS-15"

    def test_aqf_levels_1_to_10(self):
        assert len(AQFLevel) == 10
        assert AQFLevel.LEVEL_1.value == 1
        assert AQFLevel.LEVEL_9.value == 9
        assert AQFLevel.LEVEL_10.value == 10

    def test_states_territories(self):
        assert len(StateTerritory) == 8
        assert StateTerritory.VIC.value == "VIC"
        assert StateTerritory.NSW.value == "NSW"

    def test_visa_subclasses(self):
        assert VisaSubclass.STUDENT_500.value == "500"
        assert VisaSubclass.VISITOR_600.value == "600"
        assert VisaSubclass.GRADUATE_485.value == "485"

    def test_role_types(self):
        assert len(RoleType) == 4
        assert "Non-RMA" in RoleType.EDUCATION_CONSULTANT.value
        assert "RMA" in RoleType.RMA.value

    def test_data_lifecycle_stages(self):
        assert len(DataLifecycleStage) == 6
        stages = [s.value for s in DataLifecycleStage]
        assert "Collect" in stages
        assert "Dispose" in stages

    def test_confidence_levels(self):
        assert Confidence.HIGH.value == "High"
        assert Confidence.MEDIUM.value == "Medium"
        assert Confidence.LOW.value == "Low"


class TestReferenceIndex:
    """Tests for the COS-15 reference index."""

    def test_reference_index_populated(self):
        assert len(REFERENCE_INDEX) >= 35

    def test_all_refs_have_url(self):
        for ref in REFERENCE_INDEX:
            assert ref.url.startswith("https://"), f"{ref.ref_id} missing HTTPS URL"

    def test_all_refs_have_category(self):
        for ref in REFERENCE_INDEX:
            assert ref.category != "", f"{ref.ref_id} missing category"

    def test_education_refs_present(self):
        edu_refs = [r for r in REFERENCE_INDEX if r.category == "EDUCATION"]
        assert len(edu_refs) >= 7

    def test_home_affairs_refs_present(self):
        ha_refs = [r for r in REFERENCE_INDEX if r.category == "HOME_AFFAIRS"]
        assert len(ha_refs) >= 10

    def test_privacy_refs_present(self):
        priv_refs = [r for r in REFERENCE_INDEX if r.category == "PRIVACY"]
        assert len(priv_refs) >= 4

    def test_cyber_refs_present(self):
        cyber_refs = [r for r in REFERENCE_INDEX if r.category == "CYBER"]
        assert len(cyber_refs) >= 3

    def test_key_refs_exist(self):
        ref_ids = [r.ref_id for r in REFERENCE_INDEX]
        assert "REF-HA-500" in ref_ids
        assert "REF-HA-600" in ref_ids
        assert "REF-HA-GS" in ref_ids
        assert "REF-CRICOS" in ref_ids
        assert "REF-OAIC-APP" in ref_ids
        assert "REF-CYBER-E8" in ref_ids
        assert "REF-MARA-CODE" in ref_ids


class TestAuthoritativeDomains:
    """Tests for authoritative domain registry."""

    def test_domain_categories_count(self):
        assert len(AUTHORITATIVE_DOMAINS) == 10

    def test_education_domains(self):
        assert "education.gov.au" in AUTHORITATIVE_DOMAINS["EDUCATION"]
        assert "cricos.education.gov.au" in AUTHORITATIVE_DOMAINS["EDUCATION"]

    def test_home_affairs_domains(self):
        assert "immi.homeaffairs.gov.au" in AUTHORITATIVE_DOMAINS["HOME_AFFAIRS"]

    def test_privacy_domains(self):
        assert "oaic.gov.au" in AUTHORITATIVE_DOMAINS["PRIVACY"]

    def test_cyber_domains(self):
        assert "cyber.gov.au" in AUTHORITATIVE_DOMAINS["CYBER"]


class TestCodeOfConduct:
    """Tests for COS-11 code of conduct table."""

    def test_conduct_entries_count(self):
        assert len(CODE_OF_CONDUCT) == 9

    def test_all_entries_have_rule(self):
        for entry in CODE_OF_CONDUCT:
            assert entry.rule != ""
            assert entry.area != ""
            assert entry.source_anchor != ""

    def test_key_conduct_areas(self):
        areas = [e.area for e in CODE_OF_CONDUCT]
        assert "Truthfulness" in areas
        assert "No Guarantee" in areas
        assert "Role Boundary" in areas
        assert "Privacy" in areas
        assert "Security" in areas


class TestSafetyGateChecks:
    """Tests for COS-14 safety gate checks."""

    def test_safety_gate_checks_count(self):
        assert len(SAFETY_GATE_CHECKS) == 12

    def test_key_checks_present(self):
        assert "education_vs_immigration_understood" in SAFETY_GATE_CHECKS
        assert "cricos_listing_confirmed" in SAFETY_GATE_CHECKS
        assert "privacy_consent_captured" in SAFETY_GATE_CHECKS
        assert "cyber_controls_applied" in SAFETY_GATE_CHECKS
        assert "no_misleading_claims_confirmed" in SAFETY_GATE_CHECKS


class TestEducationConsultantCOS:
    """Tests for the main COS framework class."""

    def test_init(self):
        cos = EducationConsultantCOS()
        assert len(cos.reference_index) >= 35
        assert len(cos.code_of_conduct) == 9
        assert len(cos.safety_gate_checks) == 12
        assert len(cos.engagements) == 0
        assert len(cos.claims) == 0

    # --- Reference lookup ---

    def test_get_reference_found(self):
        cos = EducationConsultantCOS()
        ref = cos.get_reference("REF-HA-500")
        assert ref is not None
        assert "student-500" in ref.url
        assert ref.category == "HOME_AFFAIRS"

    def test_get_reference_not_found(self):
        cos = EducationConsultantCOS()
        assert cos.get_reference("REF-NONEXISTENT") is None

    def test_get_references_by_category(self):
        cos = EducationConsultantCOS()
        edu_refs = cos.get_references_by_category("EDUCATION")
        assert len(edu_refs) >= 7
        for ref in edu_refs:
            assert ref.category == "EDUCATION"

    def test_get_all_ref_ids(self):
        cos = EducationConsultantCOS()
        ids = cos.get_all_ref_ids()
        assert "REF-HA-500" in ids
        assert "REF-CRICOS" in ids
        assert len(ids) == len(REFERENCE_INDEX)

    # --- Domain validation ---

    def test_is_authoritative_domain_true(self):
        cos = EducationConsultantCOS()
        assert cos.is_authoritative_domain("education.gov.au") is True
        assert cos.is_authoritative_domain("immi.homeaffairs.gov.au") is True
        assert cos.is_authoritative_domain("oaic.gov.au") is True

    def test_is_authoritative_domain_false(self):
        cos = EducationConsultantCOS()
        assert cos.is_authoritative_domain("example.com") is False
        assert cos.is_authoritative_domain("google.com") is False

    def test_get_domain_category(self):
        cos = EducationConsultantCOS()
        assert cos.get_domain_category("education.gov.au") == "EDUCATION"
        assert cos.get_domain_category("immi.homeaffairs.gov.au") == "HOME_AFFAIRS"
        assert cos.get_domain_category("cyber.gov.au") == "CYBER"
        assert cos.get_domain_category("unknown.com") == "UNKNOWN"

    # --- Role boundary ---

    def test_role_boundary_education_scope(self):
        cos = EducationConsultantCOS()
        result = cos.check_role_boundary("Compare AQF level 9 course structures on CRICOS")
        assert result["requires_rma_referral"] is False
        assert "Education Consultant" in result["role_allowed"]
        assert len(result["education_signals"]) > 0

    def test_role_boundary_immigration_referral(self):
        cos = EducationConsultantCOS()
        result = cos.check_role_boundary("Lodge visa application for student 500")
        assert result["requires_rma_referral"] is True
        assert "RMA" in result["role_allowed"]
        assert len(result["immigration_signals"]) > 0

    def test_role_boundary_mixed_signals(self):
        cos = EducationConsultantCOS()
        result = cos.check_role_boundary(
            "Compare course structures and then lodge visa application"
        )
        assert result["requires_rma_referral"] is True
        assert len(result["immigration_signals"]) > 0
        assert len(result["education_signals"]) > 0

    # --- Visa taxonomy ---

    def test_visa_study_rights_500(self):
        cos = EducationConsultantCOS()
        info = cos.get_visa_study_rights("500")
        assert info["study_allowed"] is True
        assert info["degree_pathway"] is True
        assert info["ref"] == "REF-HA-500"

    def test_visa_study_rights_600(self):
        cos = EducationConsultantCOS()
        info = cos.get_visa_study_rights("600")
        assert info["study_allowed"] is True
        assert "3 months" in info["study_limit"]
        assert info["degree_pathway"] is False
        assert info["ref"] == "REF-HA-600"

    def test_visa_study_rights_unknown(self):
        cos = EducationConsultantCOS()
        info = cos.get_visa_study_rights("999")
        assert "Subclass 999" in info["name"]

    # --- Safety gate ---

    def test_safety_gate_all_pass(self):
        cos = EducationConsultantCOS()
        checks = {check: True for check in SAFETY_GATE_CHECKS}
        result = cos.run_safety_gate(checks)
        assert result.all_passed is True
        assert len(result.missing) == 0

    def test_safety_gate_some_missing(self):
        cos = EducationConsultantCOS()
        checks = {check: True for check in SAFETY_GATE_CHECKS}
        checks["privacy_consent_captured"] = False
        checks["cyber_controls_applied"] = False
        result = cos.run_safety_gate(checks)
        assert result.all_passed is False
        assert "privacy_consent_captured" in result.missing
        assert "cyber_controls_applied" in result.missing
        assert len(result.missing) == 2

    def test_safety_gate_empty_checks(self):
        cos = EducationConsultantCOS()
        result = cos.run_safety_gate({})
        assert result.all_passed is False
        assert len(result.missing) == 12

    # --- Traceability ---

    def test_add_and_retrieve_claims(self):
        cos = EducationConsultantCOS()
        claim = TraceabilityClaim(
            claim_id="CLM-001",
            statement="CRICOS code 012345 is registered for provider X",
            evidence_ref="REF-CRICOS",
            last_checked="2026-02-16",
            confidence=Confidence.HIGH,
            impact_if_wrong=Impact.HIGH,
        )
        cos.add_claim(claim)
        assert len(cos.claims) == 1

        high_conf = cos.get_claims_by_confidence(Confidence.HIGH)
        assert len(high_conf) == 1
        assert high_conf[0].claim_id == "CLM-001"

        high_impact = cos.get_high_impact_claims()
        assert len(high_impact) == 1

    def test_claims_empty_initially(self):
        cos = EducationConsultantCOS()
        assert cos.get_claims_by_confidence(Confidence.HIGH) == []
        assert cos.get_high_impact_claims() == []

    # --- Engagement records ---

    def test_create_engagement(self):
        cos = EducationConsultantCOS()
        record = cos.create_engagement(
            engagement_id="ENG-2026-001",
            date_time="2026-02-16T10:00:00+11:00",
            source_list=["REF-HA-500", "REF-CRICOS"],
            client_consent=True,
        )
        assert record.engagement_id == "ENG-2026-001"
        assert record.client_consent is True
        assert len(record.source_list) == 2
        assert len(cos.engagements) == 1

    # --- Pathway mapping ---

    def test_create_pathway_education_only(self):
        cos = EducationConsultantCOS()
        option = cos.create_pathway_option(
            label="Plan A",
            course_cricos="012345",
            aqf_level=9,
            target_anzsco="261312",
            assessing_authority="ACS",
            visa_options=["500"],
        )
        assert option.label == "Plan A"
        assert option.requires_rma_referral is False

    def test_create_pathway_skilled_visa(self):
        cos = EducationConsultantCOS()
        option = cos.create_pathway_option(
            label="Plan B",
            course_cricos="012345",
            aqf_level=9,
            target_anzsco="261312",
            assessing_authority="ACS",
            visa_options=["500", "189"],
        )
        assert option.requires_rma_referral is True
        assert any("RMA" in n for n in option.risk_notes)

    def test_create_pathway_state_nomination(self):
        cos = EducationConsultantCOS()
        option = cos.create_pathway_option(
            label="Plan C",
            visa_options=["190"],
        )
        assert option.requires_rma_referral is True

    # --- Summary ---

    def test_cos_summary(self):
        cos = EducationConsultantCOS()
        summary = cos.get_cos_summary()
        assert summary["version"] == "v3.1"
        assert summary["edition"] == "Extended Compliance"
        assert summary["cos_sections"] == 16
        assert summary["cos_layers"] == 8
        assert summary["cos_expanded_layers"] == 8
        assert summary["reference_entries"] >= 35
        assert summary["code_of_conduct_entries"] == 9
        assert summary["safety_gate_checks"] == 12
        assert summary["aqf_levels"] == 10
        assert summary["states_territories"] == 8
        assert len(summary["ref_categories"]) >= 8
        assert summary["legislative_entries"] == 18
        assert summary["protected_attributes"] == 15
        assert summary["prohibited_conduct_entries"] == 5
        assert summary["data_governance_controls"] == 4
        assert summary["required_documentation"] == 5
        assert summary["extended_pre_use_checks"] == 7


# --- Education Search Architecture ---


class TestSearchArchitectureData:
    """Tests for search architecture static data."""

    def test_institution_registry_count(self):
        assert len(INSTITUTION_REGISTRY) == 3

    def test_institution_registry_labels(self):
        labels = [i.label for i in INSTITUTION_REGISTRY]
        assert "University A" in labels
        assert "University B" in labels
        assert "University C" in labels

    def test_all_institutions_aqf_9(self):
        for inst in INSTITUTION_REGISTRY:
            assert inst.aqf_level == 9

    def test_institution_profiles(self):
        profiles = [i.profile for i in INSTITUTION_REGISTRY]
        assert InstitutionProfile.GROUP_OF_EIGHT in profiles
        assert InstitutionProfile.INDUSTRY_INTEGRATED in profiles
        assert InstitutionProfile.QUANTITATIVE_EMPHASIS in profiles

    def test_institution_clusters(self):
        clusters = [i.cluster for i in INSTITUTION_REGISTRY]
        assert AcademicCluster.CBD in clusters
        assert AcademicCluster.INNER_SUBURBAN in clusters

    def test_subject_template_four_layers(self):
        assert len(DEFAULT_SUBJECT_TEMPLATE.academic_foundation) == 3
        assert len(DEFAULT_SUBJECT_TEMPLATE.analytical_layer) == 3
        assert len(DEFAULT_SUBJECT_TEMPLATE.applied_business_context) == 3
        assert len(DEFAULT_SUBJECT_TEMPLATE.integration_layer) == 3

    def test_search_step_criteria_count(self):
        assert len(SEARCH_STEP_CRITERIA) == 4
        assert "geographic_filtering" in SEARCH_STEP_CRITERIA
        assert "institution_benchmarking" in SEARCH_STEP_CRITERIA
        assert "subject_evaluation" in SEARCH_STEP_CRITERIA
        assert "student_fit_assessment" in SEARCH_STEP_CRITERIA

    def test_search_step_criteria_detail(self):
        assert len(SEARCH_STEP_CRITERIA["geographic_filtering"]) == 3
        assert len(SEARCH_STEP_CRITERIA["institution_benchmarking"]) == 4
        assert len(SEARCH_STEP_CRITERIA["subject_evaluation"]) == 4
        assert len(SEARCH_STEP_CRITERIA["student_fit_assessment"]) == 4

    def test_professional_development_path(self):
        assert len(PROFESSIONAL_DEVELOPMENT_PATH) == 5
        assert "Academic Depth Enhancement" in PROFESSIONAL_DEVELOPMENT_PATH

    def test_search_step_enum(self):
        assert len(SearchStep) == 4
        assert "Step 1" in SearchStep.GEOGRAPHIC_FILTERING.value


class TestEducationSearchArchitecture:
    """Tests for the search architecture framework class."""

    def test_init(self):
        arch = EducationSearchArchitecture()
        assert len(arch.institutions) == 3
        assert arch.subject_template is not None
        assert len(arch.search_criteria) == 4

    # --- Institution lookup ---

    def test_get_institution_found(self):
        arch = EducationSearchArchitecture()
        inst = arch.get_institution("University A")
        assert inst is not None
        assert inst.profile == InstitutionProfile.GROUP_OF_EIGHT

    def test_get_institution_not_found(self):
        arch = EducationSearchArchitecture()
        assert arch.get_institution("University Z") is None

    def test_get_institutions_by_profile(self):
        arch = EducationSearchArchitecture()
        go8 = arch.get_institutions_by_profile(InstitutionProfile.GROUP_OF_EIGHT)
        assert len(go8) == 1
        assert go8[0].label == "University A"

    def test_get_institutions_by_cluster(self):
        arch = EducationSearchArchitecture()
        cbd = arch.get_institutions_by_cluster(AcademicCluster.CBD)
        assert len(cbd) == 2  # University A and University C

    def test_get_institutions_by_aqf(self):
        arch = EducationSearchArchitecture()
        masters = arch.get_institutions_by_aqf(9)
        assert len(masters) == 3

    # --- Subject template ---

    def test_get_subject_layer_names(self):
        arch = EducationSearchArchitecture()
        names = arch.get_subject_layer_names()
        assert len(names) == 4
        assert "Academic Foundation" in names
        assert "Integration Layer" in names

    def test_get_subject_components(self):
        arch = EducationSearchArchitecture()
        components = arch.get_subject_components()
        assert len(components) == 4
        assert "Theoretical Frameworks" in components["Academic Foundation"]
        assert "Data Interpretation" in components["Analytical Layer"]

    def test_count_subject_components(self):
        arch = EducationSearchArchitecture()
        assert arch.count_subject_components() == 12  # 3 + 3 + 3 + 3

    # --- 4-step search flow ---

    def test_evaluate_geographic_vic(self):
        arch = EducationSearchArchitecture()
        result = arch.evaluate_geographic("VIC")
        assert result.score == "HIGH"
        assert len(result.criteria) == 3

    def test_evaluate_geographic_non_vic(self):
        arch = EducationSearchArchitecture()
        result = arch.evaluate_geographic("NSW")
        assert result.score == "MEDIUM"

    def test_evaluate_institution_go8(self):
        arch = EducationSearchArchitecture()
        result = arch.evaluate_institution("University A")
        assert result.score == "HIGH"
        assert len(result.criteria) == 4

    def test_evaluate_institution_unknown(self):
        arch = EducationSearchArchitecture()
        result = arch.evaluate_institution("University Z")
        assert result.score == "LOW"

    def test_evaluate_subject(self):
        arch = EducationSearchArchitecture()
        result = arch.evaluate_subject(findings=["Strong quantitative focus"])
        assert len(result.criteria) == 4
        assert "Strong quantitative focus" in result.findings

    def test_evaluate_student_fit(self):
        arch = EducationSearchArchitecture()
        result = arch.evaluate_student_fit(
            findings=["Good academic background match"]
        )
        assert len(result.criteria) == 4
        assert "Good academic background match" in result.findings

    # --- Full search ---

    def test_run_full_search_high_alignment(self):
        arch = EducationSearchArchitecture()
        result = arch.run_full_search(
            institution_label="University A",
            state="VIC",
            geo_findings=["VIC policy aligned"],
            bench_findings=["Go8 ranking confirmed"],
            subject_findings=["Strong analytics"],
            fit_findings=["Background match"],
        )
        assert result.institution_label == "University A"
        assert result.geographic_result is not None
        assert result.benchmarking_result is not None
        assert result.subject_result is not None
        assert result.fit_result is not None
        assert result.overall_alignment in ("HIGH", "MEDIUM")
        assert result.recommendation != ""

    def test_run_full_search_unknown_institution(self):
        arch = EducationSearchArchitecture()
        result = arch.run_full_search(
            institution_label="University Z",
            state="NSW",
        )
        assert result.benchmarking_result.score == "LOW"
        assert result.geographic_result.score == "MEDIUM"

    # --- Summary ---

    def test_search_summary(self):
        arch = EducationSearchArchitecture()
        summary = arch.get_search_summary()
        assert summary["institutions"] == 3
        assert summary["search_steps"] == 4
        assert summary["total_criteria"] == 15  # 3 + 4 + 4 + 4
        assert summary["subject_layers"] == 4
        assert summary["subject_components"] == 12
        assert summary["professional_dev_items"] == 5


# =============================================================================
# Extended Compliance v3.1 Tests
# =============================================================================


class TestCOSExpandedLayers:
    """Tests for COS expanded architecture layers A-H."""

    def test_expanded_layers_count(self):
        assert len(COSExpandedLayer) == 8

    def test_expanded_layer_values(self):
        assert COSExpandedLayer.A_IDENTITY_PURPOSE.value == "Layer A"
        assert COSExpandedLayer.H_DOCUMENTATION_AUDIT.value == "Layer H"

    def test_expanded_layers_distinct_from_operational(self):
        expanded_values = {l.value for l in COSExpandedLayer}
        operational_values = {l.value for l in COSLayer}
        assert expanded_values.isdisjoint(operational_values)

    def test_operational_loop(self):
        assert len(COS_OPERATIONAL_LOOP) == 7
        assert COS_OPERATIONAL_LOOP[0] == "Identify"
        assert COS_OPERATIONAL_LOOP[-1] == "Disclose"


class TestLegislativeAlignmentMatrix:
    """Tests for the legislative & regulatory alignment matrix."""

    def test_matrix_count(self):
        assert len(LEGISLATIVE_ALIGNMENT_MATRIX) == 18

    def test_all_entries_have_name(self):
        for entry in LEGISLATIVE_ALIGNMENT_MATRIX:
            assert entry.name != ""
            assert entry.category is not None

    def test_federal_education_entries(self):
        fed_ed = [
            e for e in LEGISLATIVE_ALIGNMENT_MATRIX
            if e.category == LegislativeCategory.FEDERAL_EDUCATION
        ]
        assert len(fed_ed) == 3
        names = [e.name for e in fed_ed]
        assert any("Overseas Students" in n for n in names)  # ESOS Act
        assert any("Qualifications" in n for n in names)     # AQF

    def test_migration_entries(self):
        migration = [
            e for e in LEGISLATIVE_ALIGNMENT_MATRIX
            if e.category == LegislativeCategory.MIGRATION
        ]
        assert len(migration) == 5
        names = [e.name for e in migration]
        assert any("Migration Act" in n for n in names)
        assert any("500" in n for n in names)
        assert any("600" in n for n in names)

    def test_privacy_entries(self):
        privacy = [
            e for e in LEGISLATIVE_ALIGNMENT_MATRIX
            if e.category == LegislativeCategory.PRIVACY_DATA
        ]
        assert len(privacy) == 3

    def test_anti_discrimination_entries(self):
        anti_disc = [
            e for e in LEGISLATIVE_ALIGNMENT_MATRIX
            if e.category == LegislativeCategory.ANTI_DISCRIMINATION
        ]
        assert len(anti_disc) == 5
        short_refs = [e.short_ref for e in anti_disc]
        assert "RDA 1975" in short_refs
        assert "SDA 1984" in short_refs
        assert "DDA 1992" in short_refs
        assert "ADA 2004" in short_refs

    def test_cos_get_legislative_matrix(self):
        cos = EducationConsultantCOS()
        matrix = cos.get_legislative_matrix()
        assert len(matrix) == 18

    def test_cos_get_legislation_by_category(self):
        cos = EducationConsultantCOS()
        cyber = cos.get_legislation_by_category(LegislativeCategory.CYBER_SECURITY)
        assert len(cyber) == 2
        names = [e.name for e in cyber]
        assert any("Essential Eight" in n for n in names)


class TestEqualityCharter:
    """Tests for the equality, cultural respect & non-discrimination charter."""

    def test_protected_attributes_count(self):
        assert len(PROTECTED_ATTRIBUTES) == 15

    def test_all_attributes_have_description(self):
        for attr in PROTECTED_ATTRIBUTES:
            assert attr.attribute != ""
            assert attr.description != ""

    def test_key_attributes_present(self):
        names = [p.attribute for p in PROTECTED_ATTRIBUTES]
        assert "Gender" in names
        assert "Age" in names
        assert "Skin colour" in names
        assert "Disability" in names
        assert "Religion or no religion" in names
        assert "Sexual orientation" in names
        assert "Past failure or setbacks" in names

    def test_equality_charter_principle(self):
        assert "equal dignity" in EQUALITY_CHARTER_PRINCIPLE.lower()
        assert "Australian law" in EQUALITY_CHARTER_PRINCIPLE

    def test_equality_respect_values(self):
        assert len(EQUALITY_RESPECT_VALUES) == 4
        assert "Indigenous heritage of Australia" in EQUALITY_RESPECT_VALUES
        assert "Multicultural society" in EQUALITY_RESPECT_VALUES

    def test_advisory_neutrality(self):
        assert "personal bias" in ADVISORY_NEUTRALITY.lower()
        assert "social status" in ADVISORY_NEUTRALITY.lower()

    def test_cos_get_protected_attributes(self):
        cos = EducationConsultantCOS()
        attrs = cos.get_protected_attributes()
        assert len(attrs) == 15
        assert isinstance(attrs[0], ProtectedAttribute)

    def test_cos_get_protected_attribute_names(self):
        cos = EducationConsultantCOS()
        names = cos.get_protected_attribute_names()
        assert len(names) == 15
        assert "Gender" in names
        assert "Age" in names

    def test_equality_check_no_flag(self):
        cos = EducationConsultantCOS()
        result = cos.check_equality_compliance(
            "Comparing AQF Level 9 courses for student pathway planning"
        )
        assert result["flagged"] is False
        assert len(result["discriminatory_signals"]) == 0

    def test_equality_check_flagged(self):
        cos = EducationConsultantCOS()
        result = cos.check_equality_compliance(
            "Reject applicant because of age and disability"
        )
        assert result["flagged"] is True
        assert "Age" in result["attribute_mentions"]
        assert "Disability" in result["attribute_mentions"]
        assert "reject" in result["discriminatory_signals"]


class TestDataGovernance:
    """Tests for data governance controls."""

    def test_data_governance_controls_count(self):
        assert len(DATA_GOVERNANCE_CONTROLS) == 4

    def test_all_controls_have_principles(self):
        for control in DATA_GOVERNANCE_CONTROLS:
            assert len(control.principles) >= 2
            assert control.stage is not None

    def test_collect_stage_principles(self):
        collect = [c for c in DATA_GOVERNANCE_CONTROLS if c.stage == DataLifecycleStage.COLLECT]
        assert len(collect) == 1
        assert any("consent" in p.lower() for p in collect[0].principles)

    def test_store_stage_principles(self):
        store = [c for c in DATA_GOVERNANCE_CONTROLS if c.stage == DataLifecycleStage.STORE]
        assert len(store) == 1
        assert any("encrypted" in p.lower() for p in store[0].principles)

    def test_data_categories(self):
        assert len(DATA_CATEGORIES) == 5
        assert "Identification data" in DATA_CATEGORIES
        assert "Academic records" in DATA_CATEGORIES
        assert "Visa history" in DATA_CATEGORIES

    def test_breach_response_steps(self):
        assert len(BREACH_RESPONSE_STEPS) == 3
        assert "Immediate containment" in BREACH_RESPONSE_STEPS
        assert any("NDB" in s for s in BREACH_RESPONSE_STEPS)

    def test_cos_data_governance_methods(self):
        cos = EducationConsultantCOS()
        controls = cos.get_data_governance_controls()
        assert len(controls) == 4
        assert cos.get_data_categories() == DATA_CATEGORIES
        assert cos.get_breach_response_steps() == BREACH_RESPONSE_STEPS


class TestProhibitedConduct:
    """Tests for prohibited conduct and expanded code of conduct."""

    def test_prohibited_conduct_count(self):
        assert len(PROHIBITED_CONDUCT) == 5

    def test_all_prohibited_conduct_critical(self):
        for entry in PROHIBITED_CONDUCT:
            assert entry.severity == "Critical"

    def test_key_prohibited_conduct(self):
        conducts = [e.conduct for e in PROHIBITED_CONDUCT]
        assert "False documentation" in conducts
        assert "Exploitation of language barriers" in conducts
        assert "Cultural stereotyping" in conducts
        assert "Prejudice or bias in advice" in conducts

    def test_conduct_standards_count(self):
        assert len(CONDUCT_STANDARDS) == 6
        assert "No misleading statements" in CONDUCT_STANDARDS
        assert "Transparent fee structure" in CONDUCT_STANDARDS

    def test_professional_knowledge_requirements(self):
        assert len(PROFESSIONAL_KNOWLEDGE_REQUIREMENTS) == 5
        assert any("Migration Act" in r for r in PROFESSIONAL_KNOWLEDGE_REQUIREMENTS)
        assert any("Cyber" in r for r in PROFESSIONAL_KNOWLEDGE_REQUIREMENTS)

    def test_cos_prohibited_conduct_methods(self):
        cos = EducationConsultantCOS()
        pc = cos.get_prohibited_conduct()
        assert len(pc) == 5
        assert isinstance(pc[0], ProhibitedConductEntry)
        assert cos.get_conduct_standards() == CONDUCT_STANDARDS
        assert cos.get_professional_requirements() == PROFESSIONAL_KNOWLEDGE_REQUIREMENTS


class TestHigherEdGovernance:
    """Tests for higher education governance checklist."""

    def test_checklist_count(self):
        assert len(HIGHER_ED_GOVERNANCE_CHECKLIST) == 5

    def test_key_checks(self):
        checks = [item.check for item in HIGHER_ED_GOVERNANCE_CHECKLIST]
        assert "TEQSA registration confirmed" in checks
        assert "CRICOS listing confirmed" in checks
        assert "AQF level validated" in checks

    def test_academic_integrity_rules(self):
        assert len(ACADEMIC_INTEGRITY_RULES) == 3
        assert "No falsified transcripts" in ACADEMIC_INTEGRITY_RULES
        assert "No misleading marketing" in ACADEMIC_INTEGRITY_RULES

    def test_cos_run_higher_ed_checklist_all_pass(self):
        cos = EducationConsultantCOS()
        checks = {item.check: True for item in HIGHER_ED_GOVERNANCE_CHECKLIST}
        result = cos.run_higher_ed_checklist(checks)
        assert result["all_passed"] is True
        assert len(result["missing"]) == 0
        assert result["academic_integrity_rules"] == ACADEMIC_INTEGRITY_RULES

    def test_cos_run_higher_ed_checklist_some_fail(self):
        cos = EducationConsultantCOS()
        checks = {item.check: True for item in HIGHER_ED_GOVERNANCE_CHECKLIST}
        checks["TEQSA registration confirmed"] = False
        result = cos.run_higher_ed_checklist(checks)
        assert result["all_passed"] is False
        assert "TEQSA registration confirmed" in result["missing"]

    def test_cos_run_higher_ed_checklist_empty(self):
        cos = EducationConsultantCOS()
        result = cos.run_higher_ed_checklist({})
        assert result["all_passed"] is False
        assert len(result["missing"]) == 5


class TestOccupationRiskAndMonitoring:
    """Tests for occupation risk classification and quarterly monitoring."""

    def test_occupation_risk_categories(self):
        assert len(OccupationRiskCategory) == 3
        assert OccupationRiskCategory.LOW.value == "Low"
        assert OccupationRiskCategory.MODERATE.value == "Moderate"
        assert OccupationRiskCategory.HIGH.value == "High"

    def test_classify_stable_occupation(self):
        cos = EducationConsultantCOS()
        risk = cos.classify_occupation_risk("Stable demand in labour market")
        assert risk == OccupationRiskCategory.LOW

    def test_classify_volatile_occupation(self):
        cos = EducationConsultantCOS()
        risk = cos.classify_occupation_risk("Volatile short-term list changes")
        assert risk == OccupationRiskCategory.HIGH

    def test_classify_moderate_occupation(self):
        cos = EducationConsultantCOS()
        risk = cos.classify_occupation_risk("Some policy changes expected")
        assert risk == OccupationRiskCategory.MODERATE

    def test_quarterly_monitoring_items(self):
        assert len(QUARTERLY_MONITORING_ITEMS) == 4
        assert "Federal occupation list updates" in QUARTERLY_MONITORING_ITEMS
        assert "Labour market trends" in QUARTERLY_MONITORING_ITEMS

    def test_cos_quarterly_monitoring(self):
        cos = EducationConsultantCOS()
        items = cos.get_quarterly_monitoring_items()
        assert items == QUARTERLY_MONITORING_ITEMS


class TestAuditTrail:
    """Tests for documentation and audit trail controls."""

    def test_required_documentation_count(self):
        assert len(REQUIRED_DOCUMENTATION) == 5

    def test_required_documentation_types(self):
        types = [d.record_type for d in REQUIRED_DOCUMENTATION]
        assert "Client intake record" in types
        assert "Risk assessment sheet" in types
        assert "Occupation mapping record" in types
        assert "Visa compliance checklist" in types
        assert "Disclosure acknowledgement" in types

    def test_audit_trail_requirements_count(self):
        assert len(AUDIT_TRAIL_REQUIREMENTS) == 4

    def test_audit_trail_types(self):
        types = [a.record_type for a in AUDIT_TRAIL_REQUIREMENTS]
        assert "Date of advice" in types
        assert "Legislative version referenced" in types
        assert "Source website cited" in types
        assert "Update log maintained" in types

    def test_cos_audit_methods(self):
        cos = EducationConsultantCOS()
        docs = cos.get_required_documentation()
        assert len(docs) == 5
        assert isinstance(docs[0], AuditTrailEntry)
        trail = cos.get_audit_trail_requirements()
        assert len(trail) == 4


class TestVisaComplianceExpansion:
    """Tests for visa compliance expansion checks."""

    def test_student_500_compliance(self):
        assert len(STUDENT_500_COMPLIANCE) == 4
        assert "Genuine Student requirement verified" in STUDENT_500_COMPLIANCE
        assert "OSHC confirmed" in STUDENT_500_COMPLIANCE

    def test_visitor_600_compliance(self):
        assert len(VISITOR_600_COMPLIANCE) == 2
        assert "Short study compliance" in VISITOR_600_COMPLIANCE

    def test_skilled_migration_compliance(self):
        assert len(SKILLED_MIGRATION_COMPLIANCE) == 4
        assert "ANZSCO code validated" in SKILLED_MIGRATION_COMPLIANCE
        assert "Points test recalculated before submission" in SKILLED_MIGRATION_COMPLIANCE

    def test_cos_visa_compliance_500(self):
        cos = EducationConsultantCOS()
        checks = cos.get_visa_compliance_checks("500")
        assert checks == STUDENT_500_COMPLIANCE

    def test_cos_visa_compliance_600(self):
        cos = EducationConsultantCOS()
        checks = cos.get_visa_compliance_checks("600")
        assert checks == VISITOR_600_COMPLIANCE

    def test_cos_visa_compliance_189(self):
        cos = EducationConsultantCOS()
        checks = cos.get_visa_compliance_checks("189")
        assert checks == SKILLED_MIGRATION_COMPLIANCE

    def test_cos_visa_compliance_unknown(self):
        cos = EducationConsultantCOS()
        checks = cos.get_visa_compliance_checks("999")
        assert checks == []


class TestExtendedPreUseChecklist:
    """Tests for the extended safety/liability pre-use checklist."""

    def test_extended_checklist_count(self):
        assert len(EXTENDED_PRE_USE_CHECKLIST) == 7

    def test_key_checklist_items(self):
        assert "Confirm latest legislation from official sites" in EXTENDED_PRE_USE_CHECKLIST
        assert "Confirm privacy consent signed" in EXTENDED_PRE_USE_CHECKLIST
        assert "Confirm cultural respect standard applied" in EXTENDED_PRE_USE_CHECKLIST

    def test_liability_notice(self):
        assert "publicly available" in LIABILITY_NOTICE.lower()
        assert "may change" in LIABILITY_NOTICE.lower()

    def test_cos_extended_checklist_all_pass(self):
        cos = EducationConsultantCOS()
        completed = {item: True for item in EXTENDED_PRE_USE_CHECKLIST}
        result = cos.run_extended_pre_use_checklist(completed)
        assert result["all_passed"] is True
        assert len(result["missing"]) == 0
        assert result["liability_notice"] == LIABILITY_NOTICE

    def test_cos_extended_checklist_some_missing(self):
        cos = EducationConsultantCOS()
        completed = {item: True for item in EXTENDED_PRE_USE_CHECKLIST}
        completed["Confirm privacy consent signed"] = False
        result = cos.run_extended_pre_use_checklist(completed)
        assert result["all_passed"] is False
        assert "Confirm privacy consent signed" in result["missing"]

    def test_cos_extended_checklist_empty(self):
        cos = EducationConsultantCOS()
        result = cos.run_extended_pre_use_checklist({})
        assert result["all_passed"] is False
        assert len(result["missing"]) == 7

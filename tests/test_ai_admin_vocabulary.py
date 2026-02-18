"""
Tests for A-Z AI Administration Vocabulary & Employment Impact Framework.
=========================================================================
"""

import pytest

from src.unimelb.gov_registry.ai_admin_vocabulary import (
    AI_ADOPTION_TIMELINE,
    AZ_VOCABULARY,
    BALANCE_FOUNDATIONAL_CONDITIONS,
    BALANCE_SELF_CHECK_QUESTIONS,
    BALANCE_THREE_LAYERS,
    BUSINESS_FUNCTION_AI,
    CORE_PRINCIPLE,
    EMPLOYMENT_IMPACT_CASES,
    HIGH_RISK_ROLES,
    INDUSTRY_AI_ADOPTION,
    PERSONAL_BALANCE_PRINCIPLES,
    RETRAINING_STATS,
    AIAdminTerm,
    AIAdminVocabularyFramework,
    AdminDomain,
    BalanceLayerDesign,
    BusinessFunctionAI,
    CloudProvider,
    EmploymentImpactCase,
    HumanAIBalancePrinciple,
    IndustryAIAdoption,
    VocabCategory,
)


# =============================================================================
# Enum Tests
# =============================================================================


class TestAdminDomainEnum:
    """Tests for AdminDomain enum."""

    def test_admin_domain_count(self):
        assert len(AdminDomain) == 10

    def test_key_domains_exist(self):
        assert AdminDomain.ARCHITECTURE.value == "architecture"
        assert AdminDomain.COMPLIANCE.value == "compliance"
        assert AdminDomain.GOVERNANCE.value == "governance"
        assert AdminDomain.SECURITY.value == "security"


class TestCloudProviderEnum:
    """Tests for CloudProvider enum."""

    def test_cloud_provider_count(self):
        assert len(CloudProvider) == 4

    def test_azure_exists(self):
        assert CloudProvider.AZURE.value == "microsoft_azure"

    def test_gcp_exists(self):
        assert CloudProvider.GCP.value == "google_cloud"


class TestVocabCategoryEnum:
    """Tests for VocabCategory enum."""

    def test_vocab_category_count(self):
        assert len(VocabCategory) == 16

    def test_key_categories(self):
        assert VocabCategory.ARCHITECTURE_DESIGN.value == "architecture_design"
        assert VocabCategory.COMPLIANCE_AUDIT.value == "compliance_audit"
        assert VocabCategory.CYBERSECURITY.value == "cybersecurity"
        assert VocabCategory.DATA_GOVERNANCE.value == "data_governance"
        assert VocabCategory.ETHICS_FAIRNESS.value == "ethics_fairness"
        assert VocabCategory.MODEL_MANAGEMENT.value == "model_management"
        assert VocabCategory.PRIVACY_PROTECTION.value == "privacy_protection"
        assert VocabCategory.SECURITY_ACCESS.value == "security_access"
        assert VocabCategory.TRANSPARENCY_TRUST.value == "transparency_trust"


# =============================================================================
# A-Z Vocabulary Data Tests
# =============================================================================


class TestAZVocabularyData:
    """Tests for the 104-term A-Z vocabulary matrix."""

    def test_total_terms_is_104(self):
        assert len(AZ_VOCABULARY) == 104

    def test_26_letters_covered(self):
        letters = sorted(set(t.letter for t in AZ_VOCABULARY))
        assert len(letters) == 26
        assert letters == list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_4_terms_per_letter(self):
        from collections import Counter
        counts = Counter(t.letter for t in AZ_VOCABULARY)
        for letter, count in counts.items():
            assert count == 4, f"Letter {letter} has {count} terms, expected 4"

    def test_indices_1_to_4_per_letter(self):
        from collections import defaultdict
        by_letter: dict[str, list[int]] = defaultdict(list)
        for t in AZ_VOCABULARY:
            by_letter[t.letter].append(t.index)
        for letter, indices in by_letter.items():
            assert sorted(indices) == [1, 2, 3, 4], f"Letter {letter} indices: {indices}"

    def test_all_terms_have_required_fields(self):
        for t in AZ_VOCABULARY:
            assert t.letter, f"Missing letter for term: {t.term}"
            assert t.term, f"Missing term name"
            assert t.admin_direction_zh, f"Missing admin_direction_zh for: {t.term}"
            assert t.ai_scope, f"Missing ai_scope for: {t.term}"
            assert isinstance(t.category, VocabCategory), f"Invalid category for: {t.term}"

    def test_letter_a_terms(self):
        a_terms = [t for t in AZ_VOCABULARY if t.letter == "A"]
        names = [t.term for t in a_terms]
        assert "Architecture" in names
        assert "Audit" in names
        assert "Automation" in names
        assert "Access" in names

    def test_letter_z_terms(self):
        z_terms = [t for t in AZ_VOCABULARY if t.letter == "Z"]
        names = [t.term for t in z_terms]
        assert "Zero-Trust" in names
        assert "Zoning" in names
        assert "Zettabyte" in names
        assert "Zenith" in names

    def test_architecture_term_details(self):
        arch = next(t for t in AZ_VOCABULARY if t.term == "Architecture")
        assert arch.letter == "A"
        assert arch.index == 1
        assert "系统架构管理" in arch.admin_direction_zh
        assert "Multi-cloud" in arch.ai_scope
        assert arch.category == VocabCategory.ARCHITECTURE_DESIGN

    def test_zero_trust_term_details(self):
        zt = next(t for t in AZ_VOCABULARY if t.term == "Zero-Trust")
        assert zt.letter == "Z"
        assert "零信任" in zt.admin_direction_zh
        assert "identity security" in zt.ai_scope
        assert zt.category == VocabCategory.SECURITY_ACCESS

    def test_compliance_term(self):
        comp = next(t for t in AZ_VOCABULARY if t.term == "Compliance")
        assert comp.letter == "C"
        assert "ISO 42001" in comp.ai_scope
        assert comp.category == VocabCategory.COMPLIANCE_AUDIT

    def test_ethics_term(self):
        eth = next(t for t in AZ_VOCABULARY if t.term == "Ethics")
        assert eth.letter == "E"
        assert "Responsible AI" in eth.ai_scope
        assert eth.category == VocabCategory.ETHICS_FAIRNESS

    def test_governance_term(self):
        gov = next(t for t in AZ_VOCABULARY if t.term == "Governance")
        assert gov.letter == "G"
        assert "Policy enforcement" in gov.ai_scope
        assert gov.category == VocabCategory.POLICY_REGULATION

    def test_unique_term_names(self):
        names = [t.term for t in AZ_VOCABULARY]
        assert len(names) == len(set(names)), "Duplicate term names found"

    def test_all_categories_used(self):
        used = set(t.category for t in AZ_VOCABULARY)
        assert len(used) >= 10, f"Only {len(used)} categories used, expected more coverage"


# =============================================================================
# Industry AI Adoption Tests
# =============================================================================


class TestIndustryAIAdoption:
    """Tests for 16 industry sectors."""

    def test_industry_count(self):
        assert len(INDUSTRY_AI_ADOPTION) == 16

    def test_all_industries_have_use_cases(self):
        for ind in INDUSTRY_AI_ADOPTION:
            assert len(ind.use_cases) >= 2, f"Industry {ind.industry} has too few use cases"

    def test_it_sector_highest_adoption(self):
        it = next(i for i in INDUSTRY_AI_ADOPTION if "IT" in i.industry)
        assert it.adoption_rate_2024 == "~88%"
        assert "Highest AI penetration" in (it.notes or "")

    def test_healthcare_fastest_growing(self):
        health = next(i for i in INDUSTRY_AI_ADOPTION if "Healthcare" in i.industry)
        assert "Fastest-growing" in (health.notes or "")

    def test_professional_services_growth(self):
        ps = next(i for i in INDUSTRY_AI_ADOPTION if "Professional" in i.industry)
        assert "Highest AI adoption growth rate" in (ps.notes or "")

    def test_all_industries_have_names(self):
        for ind in INDUSTRY_AI_ADOPTION:
            assert ind.industry, "Missing industry name"
            assert ind.industry_zh, "Missing Chinese industry name"

    def test_key_industries_present(self):
        names = [i.industry for i in INDUSTRY_AI_ADOPTION]
        combined = " ".join(names)
        assert "Financial" in combined
        assert "Manufacturing" in combined
        assert "Education" in combined
        assert "Real Estate" in combined
        assert "Agriculture" in combined
        assert "Energy" in combined


# =============================================================================
# Business Function Tests
# =============================================================================


class TestBusinessFunctionAI:
    """Tests for 9 business functions."""

    def test_function_count(self):
        assert len(BUSINESS_FUNCTION_AI) == 9

    def test_marketing_genai_adoption(self):
        mkt = next(f for f in BUSINESS_FUNCTION_AI if "Marketing" in f.function)
        assert mkt.genai_adoption_pct == "~40%+"

    def test_all_functions_have_applications(self):
        for func in BUSINESS_FUNCTION_AI:
            assert len(func.ai_applications) >= 2, f"Function {func.function} has too few applications"

    def test_key_functions_present(self):
        names = [f.function for f in BUSINESS_FUNCTION_AI]
        combined = " ".join(names)
        assert "Marketing" in combined
        assert "Customer Service" in combined
        assert "Risk" in combined
        assert "Human Resources" in combined
        assert "R&D" in combined


# =============================================================================
# Employment Impact Tests
# =============================================================================


class TestEmploymentImpact:
    """Tests for documented employment impact cases."""

    def test_impact_cases_count(self):
        assert len(EMPLOYMENT_IMPACT_CASES) == 5

    def test_salesforce_case(self):
        sf = next(c for c in EMPLOYMENT_IMPACT_CASES if "Salesforce" in c.company)
        assert sf.jobs_affected == 4000
        assert sf.year == 2025

    def test_ibm_case(self):
        ibm = next(c for c in EMPLOYMENT_IMPACT_CASES if "IBM" in c.company)
        assert ibm.jobs_affected == 7800

    def test_bt_case(self):
        bt = next(c for c in EMPLOYMENT_IMPACT_CASES if "BT" in c.company)
        assert bt.jobs_affected == 55000

    def test_fiverr_case(self):
        fv = next(c for c in EMPLOYMENT_IMPACT_CASES if "Fiverr" in c.company)
        assert fv.jobs_affected == 250
        assert "30%" in (fv.percentage_affected or "")

    def test_all_cases_have_descriptions(self):
        for case in EMPLOYMENT_IMPACT_CASES:
            assert case.company, "Missing company"
            assert case.impact_description, "Missing description"
            assert case.year >= 2020, f"Unexpected year: {case.year}"


# =============================================================================
# AI Adoption Timeline Tests
# =============================================================================


class TestAdoptionTimeline:
    """Tests for AI adoption timeline."""

    def test_timeline_periods(self):
        assert len(AI_ADOPTION_TIMELINE) == 4

    def test_2024_adoption_rate(self):
        assert "72%" in AI_ADOPTION_TIMELINE["2024"]

    def test_2023_genai_explosion(self):
        assert "50%" in AI_ADOPTION_TIMELINE["2023"]

    def test_2025_2026_high_adoption(self):
        assert "78-93%" in AI_ADOPTION_TIMELINE["2025-2026"]


# =============================================================================
# Human-AI Balance Framework Tests
# =============================================================================


class TestHumanAIBalance:
    """Tests for human-AI balance framework."""

    def test_foundational_conditions_count(self):
        assert len(BALANCE_FOUNDATIONAL_CONDITIONS) == 4

    def test_condition_ids(self):
        ids = [c.principle_id for c in BALANCE_FOUNDATIONAL_CONDITIONS]
        assert "LEGAL" in ids
        assert "SOCIAL" in ids
        assert "CARE" in ids
        assert "AUTHORITY" in ids

    def test_legal_condition_content(self):
        legal = next(c for c in BALANCE_FOUNDATIONAL_CONDITIONS if c.principle_id == "LEGAL")
        assert "Privacy" in legal.description
        assert "data protection" in legal.description

    def test_care_condition_content(self):
        care = next(c for c in BALANCE_FOUNDATIONAL_CONDITIONS if c.principle_id == "CARE")
        assert "Traditional practices" in care.description
        assert "Farmers" in care.description

    def test_authority_condition_content(self):
        auth = next(c for c in BALANCE_FOUNDATIONAL_CONDITIONS if c.principle_id == "AUTHORITY")
        assert "advisory only" in auth.description
        assert "humans" in auth.description.lower()

    def test_three_layers_count(self):
        assert len(BALANCE_THREE_LAYERS) == 3

    def test_layer_ordering(self):
        layers = sorted(BALANCE_THREE_LAYERS, key=lambda l: l.layer)
        assert layers[0].layer == 1
        assert layers[1].layer == 2
        assert layers[2].layer == 3

    def test_base_layer(self):
        base = next(l for l in BALANCE_THREE_LAYERS if l.layer == 1)
        assert "Human Experience" in base.name
        assert "Source of truth" in base.role

    def test_middle_layer(self):
        mid = next(l for l in BALANCE_THREE_LAYERS if l.layer == 2)
        assert "Tool & Mirror" in mid.name
        assert "Amplifier" in mid.role

    def test_surface_layer(self):
        surface = next(l for l in BALANCE_THREE_LAYERS if l.layer == 3)
        assert "Humans Make Decisions" in surface.name
        assert "guardians" in surface.role

    def test_self_check_questions_count(self):
        assert len(BALANCE_SELF_CHECK_QUESTIONS) == 3

    def test_self_check_explainability(self):
        assert any("explainable" in q for q in BALANCE_SELF_CHECK_QUESTIONS)

    def test_self_check_human_responsibility(self):
        assert any("responsibility" in q for q in BALANCE_SELF_CHECK_QUESTIONS)

    def test_self_check_human_channel(self):
        assert any("human channel" in q for q in BALANCE_SELF_CHECK_QUESTIONS)

    def test_personal_principles_count(self):
        assert len(PERSONAL_BALANCE_PRINCIPLES) == 4

    def test_core_principle(self):
        assert "插件" in CORE_PRINCIPLE
        assert "Humans are never plugins" in CORE_PRINCIPLE


# =============================================================================
# High Risk Roles & Retraining Stats Tests
# =============================================================================


class TestHighRiskAndRetraining:
    """Tests for high-risk roles and retraining statistics."""

    def test_high_risk_categories_count(self):
        assert len(HIGH_RISK_ROLES) == 4

    def test_customer_service_risk(self):
        cs = next(r for r in HIGH_RISK_ROLES if "Customer service" in r["category"])
        assert "emotional" in cs["examples"]

    def test_retraining_stats_keys(self):
        assert "wef_retraining_need" in RETRAINING_STATS
        assert "ai_fluency_growth" in RETRAINING_STATS
        assert "us_ai_jobs" in RETRAINING_STATS

    def test_wef_statistic(self):
        assert "59%" in RETRAINING_STATS["wef_retraining_need"]

    def test_ai_fluency_growth(self):
        assert "7x" in RETRAINING_STATS["ai_fluency_growth"]


# =============================================================================
# Framework Class Tests
# =============================================================================


class TestAIAdminVocabularyFramework:
    """Tests for the main framework class."""

    @pytest.fixture
    def framework(self):
        return AIAdminVocabularyFramework()

    def test_get_all_terms(self, framework):
        terms = framework.get_all_terms()
        assert len(terms) == 104

    def test_get_terms_by_letter(self, framework):
        a_terms = framework.get_terms_by_letter("A")
        assert len(a_terms) == 4
        assert all(t.letter == "A" for t in a_terms)

    def test_get_terms_by_letter_lowercase(self, framework):
        z_terms = framework.get_terms_by_letter("z")
        assert len(z_terms) == 4
        assert all(t.letter == "Z" for t in z_terms)

    def test_get_term_by_name(self, framework):
        term = framework.get_term_by_name("Architecture")
        assert term is not None
        assert term.letter == "A"
        assert term.index == 1

    def test_get_term_by_name_case_insensitive(self, framework):
        term = framework.get_term_by_name("governance")
        assert term is not None
        assert term.letter == "G"

    def test_get_term_by_name_not_found(self, framework):
        term = framework.get_term_by_name("NonExistentTerm")
        assert term is None

    def test_get_terms_by_category(self, framework):
        security_terms = framework.get_terms_by_category(VocabCategory.SECURITY_ACCESS)
        assert len(security_terms) >= 3
        assert all(t.category == VocabCategory.SECURITY_ACCESS for t in security_terms)

    def test_get_all_letters(self, framework):
        letters = framework.get_all_letters()
        assert len(letters) == 26
        assert letters[0] == "A"
        assert letters[-1] == "Z"

    def test_get_category_distribution(self, framework):
        dist = framework.get_category_distribution()
        assert len(dist) >= 10
        total = sum(dist.values())
        assert total == 104

    def test_get_all_industries(self, framework):
        industries = framework.get_all_industries()
        assert len(industries) == 16

    def test_get_industry_by_name(self, framework):
        it = framework.get_industry_by_name("IT")
        assert it is not None
        assert "Software" in it.industry

    def test_get_industry_by_name_chinese(self, framework):
        fin = framework.get_industry_by_name("金融")
        assert fin is not None
        assert "Financial" in fin.industry

    def test_get_industry_not_found(self, framework):
        result = framework.get_industry_by_name("Nonexistent Industry")
        assert result is None

    def test_get_all_business_functions(self, framework):
        funcs = framework.get_all_business_functions()
        assert len(funcs) == 9

    def test_get_impact_cases(self, framework):
        cases = framework.get_impact_cases()
        assert len(cases) == 5

    def test_get_total_jobs_affected(self, framework):
        total = framework.get_total_jobs_affected()
        assert total >= 67000  # 4000 + 250 + 7800 + 55000 = 67050

    def test_get_balance_conditions(self, framework):
        conditions = framework.get_balance_conditions()
        assert len(conditions) == 4

    def test_get_balance_layers(self, framework):
        layers = framework.get_balance_layers()
        assert len(layers) == 3

    def test_get_self_check_questions(self, framework):
        questions = framework.get_self_check_questions()
        assert len(questions) == 3

    def test_get_personal_principles(self, framework):
        principles = framework.get_personal_principles()
        assert len(principles) == 4


class TestFrameworkSummary:
    """Tests for the framework summary method."""

    @pytest.fixture
    def summary(self):
        return AIAdminVocabularyFramework().get_framework_summary()

    def test_summary_has_module_name(self, summary):
        assert "A-Z AI Administration" in summary["module"]

    def test_summary_total_terms(self, summary):
        assert summary["total_vocabulary_terms"] == 104

    def test_summary_letters_covered(self, summary):
        assert summary["letters_covered"] == 26

    def test_summary_vocab_categories(self, summary):
        assert summary["vocab_categories"] == 16

    def test_summary_industries(self, summary):
        assert summary["industries_covered"] == 16

    def test_summary_business_functions(self, summary):
        assert summary["business_functions"] == 9

    def test_summary_impact_cases(self, summary):
        assert summary["employment_impact_cases"] == 5

    def test_summary_total_jobs(self, summary):
        assert summary["total_jobs_affected"] >= 67000

    def test_summary_balance_conditions(self, summary):
        assert summary["balance_foundational_conditions"] == 4

    def test_summary_balance_layers(self, summary):
        assert summary["balance_layers"] == 3

    def test_summary_core_principle(self, summary):
        assert "Humans are never plugins" in summary["core_principle"]

    def test_summary_design_attribution(self, summary):
        assert "Jiadong Chen" in summary["design"]
        assert "723912" in summary["design"]

    def test_summary_category_distribution_totals(self, summary):
        total = sum(summary["category_distribution"].values())
        assert total == 104


# =============================================================================
# Dataclass Tests
# =============================================================================


class TestDataclasses:
    """Tests for dataclass instantiation and immutability."""

    def test_ai_admin_term_frozen(self):
        term = AIAdminTerm("T", 1, "Test", "测试", "Testing", VocabCategory.COMPLIANCE_AUDIT)
        with pytest.raises(AttributeError):
            term.term = "Modified"

    def test_industry_ai_adoption_frozen(self):
        ind = IndustryAIAdoption("Test", "测试", ["use1"])
        with pytest.raises(AttributeError):
            ind.industry = "Modified"

    def test_employment_impact_case_frozen(self):
        case = EmploymentImpactCase("TestCo", 2025, "Test impact")
        with pytest.raises(AttributeError):
            case.company = "Modified"

    def test_human_ai_balance_principle_frozen(self):
        p = HumanAIBalancePrinciple("ID1", "Title", "标题", "Description")
        with pytest.raises(AttributeError):
            p.title = "Modified"

    def test_balance_layer_design_frozen(self):
        layer = BalanceLayerDesign(1, "Test", "测试", "Desc", "Role")
        with pytest.raises(AttributeError):
            layer.name = "Modified"

    def test_business_function_ai_frozen(self):
        func = BusinessFunctionAI("Test", "测试", ["app1"])
        with pytest.raises(AttributeError):
            func.function = "Modified"

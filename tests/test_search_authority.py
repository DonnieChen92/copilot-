"""
Tests for Search Authority & Website Safety Verification Framework.
====================================================================
"""

import pytest

from src.unimelb.gov_registry.search_authority import (
    AI_PERMISSION_ALLOW,
    AI_PERMISSION_CONDITIONAL,
    AI_PERMISSION_NOT_ALLOWED,
    AI_SIGNAL_PRIORITY,
    COMPLIANCE_MAP_SECTIONS,
    CONNECTION_SECURITY_CHECKLIST,
    EMOTIONAL_MANIPULATION_KEYWORDS,
    FEDERAL_GOVERNMENT_DOMAINS,
    FULL_URL_REGISTRY,
    JOS_RESEARCH_STEPS,
    MAINSTREAM_MEDIA_DOMAINS,
    OFFICIAL_BODY_DOMAINS,
    PROPERTY_VERIFICATION_SOURCES,
    SALES_PRESSURE_KEYWORDS,
    SUSPICIOUS_TLDS,
    URLCategory,
    URLRegistryEntry,
    VIC_COUNCIL_REGISTRY,
    VIC_GOVERNMENT_DOMAINS,
    ZERO_ASSUMPTION_RULES,
    AuthorityAssessment,
    AuthorityLevel,
    AuthorityScoringWeights,
    ComplianceSection,
    CrossVerificationResult,
    DomainTrust,
    ManipulationFlag,
    SafetyCheck,
    SafetyCheckResult,
    ScamwatchAction,
    SearchAuthorityFramework,
    VICCouncilEntry,
)


class TestAuthorityLevelEnum:
    """Tests for the authority level hierarchy."""

    def test_authority_levels_count(self):
        assert len(AuthorityLevel) == 6

    def test_authority_level_ordering(self):
        assert AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE.value == 1
        assert AuthorityLevel.L6_COMMUNITY_USER.value == 6

    def test_safety_check_count(self):
        assert len(SafetyCheck) == 5

    def test_domain_trust_count(self):
        assert len(DomainTrust) == 8

    def test_manipulation_flag_count(self):
        assert len(ManipulationFlag) == 5

    def test_scamwatch_actions(self):
        assert len(ScamwatchAction) == 3
        assert ScamwatchAction.STOP.name == "STOP"
        assert ScamwatchAction.CHECK.name == "CHECK"
        assert ScamwatchAction.PROTECT.name == "PROTECT"


class TestDomainRegistries:
    """Tests for domain registry data."""

    def test_vic_gov_domains_populated(self):
        assert len(VIC_GOVERNMENT_DOMAINS) >= 8
        assert "vic.gov.au" in VIC_GOVERNMENT_DOMAINS
        assert "legislation.vic.gov.au" in VIC_GOVERNMENT_DOMAINS
        assert "melbourne.vic.gov.au" in VIC_GOVERNMENT_DOMAINS

    def test_federal_gov_domains_populated(self):
        assert len(FEDERAL_GOVERNMENT_DOMAINS) >= 7
        assert "legislation.gov.au" in FEDERAL_GOVERNMENT_DOMAINS
        assert "ato.gov.au" in FEDERAL_GOVERNMENT_DOMAINS

    def test_official_body_domains_populated(self):
        assert len(OFFICIAL_BODY_DOMAINS) >= 12
        assert "abs.gov.au" in OFFICIAL_BODY_DOMAINS
        assert "data.vic.gov.au" in OFFICIAL_BODY_DOMAINS
        assert "land.vic.gov.au" in OFFICIAL_BODY_DOMAINS
        assert "consumer.vic.gov.au" in OFFICIAL_BODY_DOMAINS
        assert "cyber.gov.au" in OFFICIAL_BODY_DOMAINS
        assert "scamwatch.gov.au" in OFFICIAL_BODY_DOMAINS

    def test_mainstream_media_domains(self):
        assert len(MAINSTREAM_MEDIA_DOMAINS) >= 5
        assert "abc.net.au" in MAINSTREAM_MEDIA_DOMAINS
        assert "theage.com.au" in MAINSTREAM_MEDIA_DOMAINS

    def test_suspicious_tlds(self):
        assert len(SUSPICIOUS_TLDS) >= 10
        assert ".xyz" in SUSPICIOUS_TLDS
        assert ".tk" in SUSPICIOUS_TLDS

    def test_property_verification_sources(self):
        assert len(PROPERTY_VERIFICATION_SOURCES) >= 5
        assert "land.vic.gov.au" in PROPERTY_VERIFICATION_SOURCES
        assert "consumer.vic.gov.au" in PROPERTY_VERIFICATION_SOURCES


class TestVICCouncilRegistry:
    """Tests for VIC council registry."""

    def test_council_registry_populated(self):
        assert len(VIC_COUNCIL_REGISTRY) >= 20

    def test_city_of_melbourne_present(self):
        names = [c.name for c in VIC_COUNCIL_REGISTRY]
        assert "City of Melbourne" in names

    def test_melbourne_is_3000(self):
        mel = [c for c in VIC_COUNCIL_REGISTRY if c.name == "City of Melbourne"]
        assert len(mel) == 1
        assert mel[0].postcode_start == "3000"
        assert mel[0].domain == "melbourne.vic.gov.au"

    def test_all_councils_have_name_and_domain(self):
        for council in VIC_COUNCIL_REGISTRY:
            assert council.name != ""
            assert council.domain != ""
            assert council.postcode_start != ""


class TestDomainClassification:
    """Tests for domain trust and authority level classification."""

    def test_classify_vic_gov(self):
        fw = SearchAuthorityFramework()
        assert fw.classify_domain_trust("melbourne.vic.gov.au") == DomainTrust.VIC_GOV_AU
        assert fw.classify_domain_trust("legislation.vic.gov.au") == DomainTrust.VIC_GOV_AU

    def test_classify_gov_au(self):
        fw = SearchAuthorityFramework()
        assert fw.classify_domain_trust("legislation.gov.au") == DomainTrust.GOV_AU
        assert fw.classify_domain_trust("ato.gov.au") == DomainTrust.GOV_AU

    def test_classify_edu_au(self):
        fw = SearchAuthorityFramework()
        assert fw.classify_domain_trust("unimelb.edu.au") == DomainTrust.EDU_AU

    def test_classify_com_au(self):
        fw = SearchAuthorityFramework()
        assert fw.classify_domain_trust("example.com.au") == DomainTrust.COM_AU

    def test_classify_generic_com(self):
        fw = SearchAuthorityFramework()
        assert fw.classify_domain_trust("example.com") == DomainTrust.GENERIC_COM

    def test_classify_other(self):
        fw = SearchAuthorityFramework()
        assert fw.classify_domain_trust("example.xyz") == DomainTrust.OTHER

    def test_authority_level_l1_vic_gov(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("vic.gov.au") == AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE
        assert fw.determine_authority_level("legislation.vic.gov.au") == AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE

    def test_authority_level_l1_federal(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("legislation.gov.au") == AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE

    def test_authority_level_l1_any_gov(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("newsite.gov.au") == AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE

    def test_authority_level_l2_official(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("abs.gov.au") == AuthorityLevel.L2_OFFICIAL_BODIES
        assert fw.determine_authority_level("data.vic.gov.au") == AuthorityLevel.L2_OFFICIAL_BODIES
        assert fw.determine_authority_level("cyber.gov.au") == AuthorityLevel.L2_OFFICIAL_BODIES

    def test_authority_level_l3_company(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("somecompany.com.au") == AuthorityLevel.L3_COMPANY_OFFICIAL

    def test_authority_level_l4_academic(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("unimelb.edu.au") == AuthorityLevel.L4_ACADEMIC
        assert fw.determine_authority_level("monash.edu.au") == AuthorityLevel.L4_ACADEMIC

    def test_authority_level_l5_media(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("abc.net.au") == AuthorityLevel.L5_MAINSTREAM_MEDIA
        assert fw.determine_authority_level("theage.com.au") == AuthorityLevel.L5_MAINSTREAM_MEDIA

    def test_authority_level_l6_unknown(self):
        fw = SearchAuthorityFramework()
        assert fw.determine_authority_level("random-blog.com") == AuthorityLevel.L6_COMMUNITY_USER
        assert fw.determine_authority_level("forum.xyz") == AuthorityLevel.L6_COMMUNITY_USER


class TestAuthorityScoring:
    """Tests for source authority scoring (1-5)."""

    def test_gov_score_5(self):
        fw = SearchAuthorityFramework()
        assert fw.score_source_authority("vic.gov.au") == 5
        assert fw.score_source_authority("abs.gov.au") == 5

    def test_edu_score_4(self):
        fw = SearchAuthorityFramework()
        assert fw.score_source_authority("unimelb.edu.au") == 4

    def test_company_score_3(self):
        fw = SearchAuthorityFramework()
        assert fw.score_source_authority("company.com.au") == 3

    def test_media_score_3(self):
        fw = SearchAuthorityFramework()
        assert fw.score_source_authority("abc.net.au") == 3

    def test_org_au_score_2(self):
        fw = SearchAuthorityFramework()
        assert fw.score_source_authority("charity.org.au") == 2

    def test_unknown_score_1(self):
        fw = SearchAuthorityFramework()
        assert fw.score_source_authority("suspicious.xyz") == 1


class TestSafetyChecks:
    """Tests for 5-point website safety checks."""

    def test_all_pass(self):
        fw = SearchAuthorityFramework()
        checks = {check.value: True for check in SafetyCheck}
        result = fw.run_safety_checks(checks)
        assert result.all_passed is True
        assert result.risk_level == "LOW"
        assert len(result.failed) == 0

    def test_some_fail(self):
        fw = SearchAuthorityFramework()
        checks = {check.value: True for check in SafetyCheck}
        checks[SafetyCheck.A_HTTPS_CERTIFICATE.value] = False
        result = fw.run_safety_checks(checks)
        assert result.all_passed is False
        assert result.risk_level == "MEDIUM"
        assert SafetyCheck.A_HTTPS_CERTIFICATE.value in result.failed

    def test_many_fail_high_risk(self):
        fw = SearchAuthorityFramework()
        checks = {check.value: False for check in SafetyCheck}
        checks[SafetyCheck.C_OFFICIAL_PRIMARY_DOMAIN.value] = True
        checks[SafetyCheck.E_BROWSER_ALERTS.value] = True
        result = fw.run_safety_checks(checks)
        assert result.risk_level == "HIGH"

    def test_all_fail_critical(self):
        fw = SearchAuthorityFramework()
        result = fw.run_safety_checks({})
        assert result.all_passed is False
        assert result.risk_level == "CRITICAL"
        assert len(result.failed) == 5

    def test_empty_defaults_false(self):
        fw = SearchAuthorityFramework()
        result = fw.run_safety_checks({})
        for check in SafetyCheck:
            assert result.checks[check.value] is False


class TestManipulationDetection:
    """Tests for manipulation / directed implantation detection."""

    def test_no_manipulation(self):
        fw = SearchAuthorityFramework()
        flags = fw.detect_manipulation(
            "The City of Melbourne provides property reports through Land Use Victoria."
        )
        assert len(flags) == 0

    def test_sales_pressure_detected(self):
        fw = SearchAuthorityFramework()
        flags = fw.detect_manipulation(
            "ACT NOW! Limited time offer! Don't miss out on this property deal!"
        )
        assert ManipulationFlag.SALES_BOUND in flags

    def test_emotional_manipulation_detected(self):
        fw = SearchAuthorityFramework()
        flags = fw.detect_manipulation(
            "Your family deserves the best, you'll regret not buying now."
        )
        assert ManipulationFlag.EMOTIONAL_MANIPULATION in flags

    def test_magic_answer_detected(self):
        fw = SearchAuthorityFramework()
        flags = fw.detect_manipulation(
            "This is a guaranteed investment. 100% returns. No risk at all."
        )
        assert ManipulationFlag.MAGIC_ANSWER in flags

    def test_sales_keywords_list(self):
        assert len(SALES_PRESSURE_KEYWORDS) >= 10
        assert "act now" in SALES_PRESSURE_KEYWORDS

    def test_emotional_keywords_list(self):
        assert len(EMOTIONAL_MANIPULATION_KEYWORDS) >= 4


class TestRedirectSafety:
    """Tests for redirect safety checking."""

    def test_safe_gov_domain(self):
        fw = SearchAuthorityFramework()
        assert fw.check_redirect_safety("vic.gov.au") is True

    def test_safe_com_au(self):
        fw = SearchAuthorityFramework()
        assert fw.check_redirect_safety("company.com.au") is True

    def test_suspicious_xyz(self):
        fw = SearchAuthorityFramework()
        assert fw.check_redirect_safety("malicious.xyz") is False

    def test_suspicious_tk(self):
        fw = SearchAuthorityFramework()
        assert fw.check_redirect_safety("phishing.tk") is False

    def test_suspicious_top(self):
        fw = SearchAuthorityFramework()
        assert fw.check_redirect_safety("scam.top") is False


class TestCompositeScoring:
    """Tests for composite authority score calculation."""

    def test_perfect_score(self):
        fw = SearchAuthorityFramework()
        score = fw.calculate_composite_score(5, 5, 5, 5, 5)
        assert score == 5.0

    def test_minimum_score(self):
        fw = SearchAuthorityFramework()
        score = fw.calculate_composite_score(1, 1, 1, 1, 1)
        assert score == 1.0

    def test_weighted_score(self):
        fw = SearchAuthorityFramework()
        # T = 0.4*5 + 0.2*4 + 0.2*3 + 0.1*5 + 0.1*3
        # T = 2.0 + 0.8 + 0.6 + 0.5 + 0.3 = 4.2
        score = fw.calculate_composite_score(5, 4, 3, 5, 3)
        assert abs(score - 4.2) < 0.01

    def test_invalid_score_raises(self):
        fw = SearchAuthorityFramework()
        with pytest.raises(ValueError):
            fw.calculate_composite_score(0, 3, 3, 3, 3)
        with pytest.raises(ValueError):
            fw.calculate_composite_score(3, 6, 3, 3, 3)

    def test_weights_sum_to_one(self):
        w = AuthorityScoringWeights()
        total = (
            w.source_authority + w.transparency
            + w.evidence_quality + w.security
            + w.cross_verification
        )
        assert abs(total - 1.0) < 0.001


class TestFullAssessment:
    """Tests for full source assessment."""

    def test_assess_gov_source(self):
        fw = SearchAuthorityFramework()
        result = fw.assess_source(
            url="https://www.vic.gov.au/planning",
            domain="vic.gov.au",
            transparency=5,
            evidence_quality=5,
            security=5,
            cross_verification=4,
        )
        assert result.authority_level == AuthorityLevel.L1_GOVERNMENT_LEGISLATIVE
        assert result.source_authority_score == 5
        assert result.composite_score >= 4.0
        assert "High confidence" in result.recommendation

    def test_assess_unknown_source(self):
        fw = SearchAuthorityFramework()
        result = fw.assess_source(
            url="https://random-blog.xyz/property-tips",
            domain="random-blog.xyz",
            transparency=1,
            evidence_quality=1,
            security=1,
            cross_verification=1,
        )
        assert result.authority_level == AuthorityLevel.L6_COMMUNITY_USER
        assert result.composite_score == 1.0
        assert "Very low confidence" in result.recommendation

    def test_assess_with_manipulation(self):
        fw = SearchAuthorityFramework()
        result = fw.assess_source(
            url="https://dodgy-deals.com.au/buy-now",
            domain="dodgy-deals.com.au",
            transparency=2,
            evidence_quality=1,
            security=3,
            cross_verification=1,
            page_text="Act now! Limited time offer! Don't miss out! Guaranteed returns!",
        )
        assert len(result.manipulation_flags) > 0
        assert "WARNING" in result.recommendation

    def test_assess_with_safety_checks(self):
        fw = SearchAuthorityFramework()
        safety = {check.value: True for check in SafetyCheck}
        result = fw.assess_source(
            url="https://www.land.vic.gov.au/",
            domain="land.vic.gov.au",
            transparency=5,
            evidence_quality=5,
            security=5,
            cross_verification=5,
            safety_checks=safety,
        )
        assert len(result.safety_check_results) == 5
        assert all(result.safety_check_results.values())


class TestCrossVerification:
    """Tests for cross-verification methodology."""

    def test_verified_high_confidence(self):
        fw = SearchAuthorityFramework()
        result = fw.cross_verify(
            claim="VIC 3000 is part of City of Melbourne LGA",
            sources=[
                {"domain": "land.vic.gov.au", "confirms": "true"},
                {"domain": "melbourne.vic.gov.au", "confirms": "true"},
                {"domain": "abs.gov.au", "confirms": "true"},
            ],
        )
        assert result.verified is True
        assert result.confidence == "HIGH"
        assert len(result.sources_confirmed) == 3

    def test_verified_medium_confidence(self):
        fw = SearchAuthorityFramework()
        result = fw.cross_verify(
            claim="New underquoting rules in effect",
            sources=[
                {"domain": "consumer.vic.gov.au", "confirms": "true"},
                {"domain": "abc.net.au", "confirms": "true"},
            ],
        )
        assert result.verified is True
        assert result.confidence == "MEDIUM"

    def test_verified_low_confidence(self):
        fw = SearchAuthorityFramework()
        result = fw.cross_verify(
            claim="Developer reputation is good",
            sources=[
                {"domain": "theage.com.au", "confirms": "true"},
                {"domain": "company.com.au", "confirms": "true"},
            ],
        )
        assert result.verified is True
        assert result.confidence == "LOW"

    def test_unverified(self):
        fw = SearchAuthorityFramework()
        result = fw.cross_verify(
            claim="Some claim",
            sources=[
                {"domain": "blog.com", "confirms": "false"},
                {"domain": "forum.xyz", "confirms": "false"},
            ],
        )
        assert result.verified is False
        assert result.confidence == "UNVERIFIED"


class TestCouncilLookup:
    """Tests for VIC council lookup."""

    def test_council_by_postcode_3000(self):
        fw = SearchAuthorityFramework()
        council = fw.get_council_by_postcode("3000")
        assert council is not None
        assert council.name == "City of Melbourne"

    def test_council_by_postcode_not_found(self):
        fw = SearchAuthorityFramework()
        assert fw.get_council_by_postcode("9999") is None

    def test_council_by_name(self):
        fw = SearchAuthorityFramework()
        council = fw.get_council_by_name("Port Phillip")
        assert council is not None
        assert "Port Phillip" in council.name

    def test_council_by_name_not_found(self):
        fw = SearchAuthorityFramework()
        assert fw.get_council_by_name("Nonexistent City") is None

    def test_all_council_domains(self):
        fw = SearchAuthorityFramework()
        domains = fw.get_all_council_domains()
        assert "melbourne.vic.gov.au" in domains
        assert len(domains) >= 20


class TestSearchHelpers:
    """Tests for search strategy helpers."""

    def test_site_restricted_query(self):
        fw = SearchAuthorityFramework()
        query = fw.build_site_restricted_query("property zoning", "vic.gov.au")
        assert query == "site:vic.gov.au property zoning"

    def test_gov_search_queries(self):
        fw = SearchAuthorityFramework()
        queries = fw.build_gov_search_queries("land title")
        assert len(queries) == 5
        assert all("site:" in q for q in queries)
        assert any("vic.gov.au" in q for q in queries)
        assert any("land.vic.gov.au" in q for q in queries)


class TestScamwatchProtocol:
    """Tests for Scamwatch Stop-Check-Protect protocol."""

    def test_protocol_keys(self):
        fw = SearchAuthorityFramework()
        protocol = fw.get_scamwatch_protocol()
        assert "STOP" in protocol
        assert "CHECK" in protocol
        assert "PROTECT" in protocol
        assert len(protocol) == 3


class TestFrameworkSummary:
    """Tests for framework summary."""

    def test_summary_structure(self):
        fw = SearchAuthorityFramework()
        summary = fw.get_framework_summary()
        assert summary["version"] == "1.0"
        assert summary["authority_levels"] == 6
        assert summary["safety_checks"] == 5
        assert summary["scoring_dimensions"] == 5
        assert summary["vic_gov_domains"] >= 8
        assert summary["federal_gov_domains"] >= 7
        assert summary["official_body_domains"] >= 12
        assert summary["vic_councils_registered"] >= 20
        assert summary["manipulation_flag_types"] == 5

    def test_scoring_weights_in_summary(self):
        fw = SearchAuthorityFramework()
        summary = fw.get_framework_summary()
        weights = summary["scoring_weights"]
        assert weights["source_authority"] == 0.4
        assert weights["transparency"] == 0.2
        assert weights["evidence_quality"] == 0.2
        assert weights["security"] == 0.1
        assert weights["cross_verification"] == 0.1

    def test_summary_includes_registry_and_compliance(self):
        fw = SearchAuthorityFramework()
        summary = fw.get_framework_summary()
        assert summary["url_registry_entries"] >= 75
        assert summary["url_registry_categories"] >= 12
        assert summary["compliance_map_sections"] == 6
        assert summary["research_steps"] == 7
        assert summary["security_checklist_items"] == 7


class TestFullURLRegistry:
    """Tests for the full URL registry (12 categories)."""

    def test_registry_populated(self):
        assert len(FULL_URL_REGISTRY) >= 75

    def test_all_entries_have_url_and_category(self):
        for entry in FULL_URL_REGISTRY:
            assert entry.url.startswith("https://") or entry.url.startswith("http://")
            assert entry.category != ""

    def test_government_category(self):
        gov = [e for e in FULL_URL_REGISTRY if e.category == "GOVERNMENT"]
        assert len(gov) >= 10
        urls = [e.url for e in gov]
        assert any("vic.gov.au" in u for u in urls)

    def test_local_government_category(self):
        local = [e for e in FULL_URL_REGISTRY if e.category == "LOCAL_GOVERNMENT"]
        assert len(local) >= 3
        urls = [e.url for e in local]
        assert any("melbourne.vic.gov.au" in u for u in urls)

    def test_land_property_category(self):
        land = [e for e in FULL_URL_REGISTRY if e.category == "LAND_PROPERTY"]
        assert len(land) >= 5

    def test_education_category(self):
        edu = [e for e in FULL_URL_REGISTRY if e.category == "EDUCATION"]
        assert len(edu) >= 10
        urls = [e.url for e in edu]
        assert any("unimelb.edu.au" in u for u in urls)
        assert any("monash.edu" in u for u in urls)

    def test_all_12_categories_present(self):
        categories = set(e.category for e in FULL_URL_REGISTRY)
        expected = {
            "GOVERNMENT", "LOCAL_GOVERNMENT", "LAND_PROPERTY",
            "ENERGY_UTILITIES", "NON_PROFIT", "ENVIRONMENT_ANIMAL",
            "CULTURE_MUSEUMS", "EDUCATION", "LANDMARKS",
            "COMMUNITY_SERVICES", "TRANSPORT", "SAFETY_CYBER",
        }
        assert expected.issubset(categories)

    def test_url_category_enum(self):
        assert len(URLCategory) == 12

    def test_framework_get_urls_by_category(self):
        fw = SearchAuthorityFramework()
        gov_urls = fw.get_urls_by_category("GOVERNMENT")
        assert len(gov_urls) >= 10
        assert all(isinstance(u, URLRegistryEntry) for u in gov_urls)

    def test_framework_get_url_categories(self):
        fw = SearchAuthorityFramework()
        categories = fw.get_url_categories()
        assert len(categories) >= 12

    def test_framework_count_urls_by_category(self):
        fw = SearchAuthorityFramework()
        counts = fw.count_urls_by_category()
        assert counts["GOVERNMENT"] >= 10
        assert counts["EDUCATION"] >= 10


class TestComplianceMap:
    """Tests for the J.OS Gov Research Compliance Map."""

    def test_compliance_sections_count(self):
        assert len(COMPLIANCE_MAP_SECTIONS) == 6

    def test_all_sections_have_title(self):
        for section in COMPLIANCE_MAP_SECTIONS:
            assert section.section_id != ""
            assert section.title != ""
            assert len(section.domains) >= 2
            assert len(section.ai_allowed) >= 1
            assert len(section.security_rules) >= 1

    def test_section_ids_unique(self):
        ids = [s.section_id for s in COMPLIANCE_MAP_SECTIONS]
        assert len(ids) == len(set(ids))

    def test_get_compliance_section(self):
        fw = SearchAuthorityFramework()
        s1 = fw.get_compliance_section("S1")
        assert s1 is not None
        assert "Government Domain" in s1.title

    def test_get_compliance_section_not_found(self):
        fw = SearchAuthorityFramework()
        assert fw.get_compliance_section("S99") is None

    def test_privacy_section(self):
        fw = SearchAuthorityFramework()
        s2 = fw.get_compliance_section("S2")
        assert s2 is not None
        assert "Privacy" in s2.title
        assert len(s2.ai_not_allowed) >= 3

    def test_education_section(self):
        fw = SearchAuthorityFramework()
        s4 = fw.get_compliance_section("S4")
        assert s4 is not None
        assert "Education" in s4.title


class TestAIPermissions:
    """Tests for AI abstraction & extraction permission matrix."""

    def test_allowed_list(self):
        assert len(AI_PERMISSION_ALLOW) >= 4
        assert "Public policy summaries" in AI_PERMISSION_ALLOW

    def test_conditional_list(self):
        assert len(AI_PERMISSION_CONDITIONAL) >= 2

    def test_not_allowed_list(self):
        assert len(AI_PERMISSION_NOT_ALLOWED) >= 4
        assert "Paywalled databases" in AI_PERMISSION_NOT_ALLOWED
        assert "Personal data scraping" in AI_PERMISSION_NOT_ALLOWED

    def test_framework_get_permissions(self):
        fw = SearchAuthorityFramework()
        perms = fw.get_ai_permissions()
        assert "allowed" in perms
        assert "conditional" in perms
        assert "not_allowed" in perms


class TestZeroAssumptionAndResearch:
    """Tests for zero assumption rules and research steps."""

    def test_zero_assumption_rules(self):
        assert len(ZERO_ASSUMPTION_RULES) == 3
        assert any("gap" in r.lower() for r in ZERO_ASSUMPTION_RULES)
        assert any("speculate" in r.lower() for r in ZERO_ASSUMPTION_RULES)

    def test_research_steps(self):
        assert len(JOS_RESEARCH_STEPS) == 7
        assert "Step 1" in JOS_RESEARCH_STEPS[0]
        assert "Step 7" in JOS_RESEARCH_STEPS[6]

    def test_ai_signal_priority(self):
        assert len(AI_SIGNAL_PRIORITY) == 7
        assert AI_SIGNAL_PRIORITY[0] == "Law"
        assert AI_SIGNAL_PRIORITY[-1] == "Community"

    def test_connection_security_checklist(self):
        assert len(CONNECTION_SECURITY_CHECKLIST) == 7
        assert "HTTPS required" in CONNECTION_SECURITY_CHECKLIST
        assert "TLS 1.2+" in CONNECTION_SECURITY_CHECKLIST

    def test_framework_methods(self):
        fw = SearchAuthorityFramework()
        assert fw.get_zero_assumption_rules() == ZERO_ASSUMPTION_RULES
        assert fw.get_research_steps() == JOS_RESEARCH_STEPS
        assert fw.get_ai_signal_priority() == AI_SIGNAL_PRIORITY
        assert fw.get_connection_security_checklist() == CONNECTION_SECURITY_CHECKLIST

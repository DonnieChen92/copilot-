"""
Tests for PM-Email-Categorisation.os, 1:1:1 Equivalence Register,
and GOV Domain Registry.
=====================================================================
"""

import pytest

# --- PM-Email-Categorisation.os ---
from src.unimelb.property_management.categorisation_os.pm_email_categorisation import (
    CoverScanResult,
    FolderCategory,
    IDFormat,
    LockLevel,
    PMEmailCategorisationOS,
    PropertyDomain,
    Stakeholder,
    STAKEHOLDER_KEYWORDS,
    STAKEHOLDER_FOLDER_MAP,
    VAULT_FOLDER_MAP,
    PMOS_LABELS,
    RES_FOLDER_TREE,
    COM_FOLDER_TREE,
)


class TestPMEmailCategorisationOS:
    """Tests for the 99-folder RES/COM trees and routing."""

    def test_res_tree_has_99_folders(self):
        assert len(RES_FOLDER_TREE) == 99

    def test_com_tree_has_99_folders(self):
        assert len(COM_FOLDER_TREE) == 99

    def test_res_folders_numbered_1_to_99(self):
        numbers = [f.number for f in RES_FOLDER_TREE]
        assert numbers == list(range(1, 100))

    def test_com_folders_numbered_1_to_99(self):
        numbers = [f.number for f in COM_FOLDER_TREE]
        assert numbers == list(range(1, 100))

    def test_get_folder_by_number(self):
        os = PMEmailCategorisationOS()
        folder = os.get_folder_by_number(PropertyDomain.RES, 30)
        assert folder is not None
        assert "Maintenance" in folder.path
        assert folder.category == FolderCategory.MAINTENANCE

    def test_get_com_lease_admin_folder(self):
        os = PMEmailCategorisationOS()
        folder = os.get_folder_by_number(PropertyDomain.COM, 14)
        assert folder is not None
        assert "RentReview" in folder.path

    def test_vault_folders_exist(self):
        os = PMEmailCategorisationOS()
        res_vault = os.get_folders_by_lock_level(PropertyDomain.RES, LockLevel.L4_VAULT)
        assert len(res_vault) > 0
        for f in res_vault:
            assert f.lock_level == LockLevel.L4_VAULT

    def test_confidential_folders_include_finance(self):
        os = PMEmailCategorisationOS()
        res_conf = os.get_folders_by_lock_level(PropertyDomain.RES, LockLevel.L3_CONFIDENTIAL)
        finance_conf = [f for f in res_conf if f.category == FolderCategory.FINANCE]
        assert len(finance_conf) > 0

    def test_route_email_maintenance(self):
        os = PMEmailCategorisationOS()
        matches = os.route_email(
            PropertyDomain.RES,
            subject="Urgent: Water leak in bathroom",
            body="There is a major leak, please send someone urgently."
        )
        folder_paths = [m.path for m in matches]
        assert any("Urgent" in p for p in folder_paths)

    def test_route_email_rent_increase(self):
        os = PMEmailCategorisationOS()
        matches = os.route_email(
            PropertyDomain.RES,
            subject="Rent increase notice for Unit 5"
        )
        folder_paths = [m.path for m in matches]
        assert any("RentIncrease" in p for p in folder_paths)

    def test_route_email_com_rent_review(self):
        os = PMEmailCategorisationOS()
        matches = os.route_email(
            PropertyDomain.COM,
            subject="CPI Rent Review Due - Level 3 Suite"
        )
        folder_paths = [m.path for m in matches]
        assert any("RentReview" in p for p in folder_paths)

    def test_route_email_default_inbox(self):
        os = PMEmailCategorisationOS()
        matches = os.route_email(
            PropertyDomain.RES,
            subject="Hello, just checking in"
        )
        assert matches[0].number == 1  # defaults to Inbox_New

    def test_get_folders_by_category(self):
        os = PMEmailCategorisationOS()
        legal = os.get_folders_by_category(PropertyDomain.RES, FolderCategory.LEGAL)
        assert len(legal) == 10  # folders 60–69

    def test_get_folders_by_category_com_facilities(self):
        os = PMEmailCategorisationOS()
        fac = os.get_folders_by_category(PropertyDomain.COM, FolderCategory.FACILITIES)
        assert len(fac) == 10  # folders 30–39

    def test_tree_summary(self):
        os = PMEmailCategorisationOS()
        summary = os.get_tree_summary(PropertyDomain.RES)
        assert summary["domain"] == "RES"
        assert summary["total_folders"] == 99
        assert "by_category" in summary
        assert "by_lock_level" in summary

    def test_com_tree_summary(self):
        os = PMEmailCategorisationOS()
        summary = os.get_tree_summary(PropertyDomain.COM)
        assert summary["domain"] == "COM"
        assert summary["total_folders"] == 99


class TestIDFormat:
    """Tests for property management ID formats."""

    def test_folder_binding_base(self):
        path = IDFormat.folder_binding_base(
            "PORT-PM-MEL-RES-0001",
            "BLD-CARLTON-123-ELGINST-001"
        )
        assert path == "PORT-PM-MEL-RES-0001__BLD-CARLTON-123-ELGINST-001/"

    def test_folder_binding_with_tenant(self):
        path = IDFormat.folder_binding_case(
            "PORT-PM-MEL-RES-0001",
            "BLD-CARLTON-123-ELGINST-001",
            "TEN-2025-0042"
        )
        assert "TEN-2025-0042" in path

    def test_folder_binding_with_project(self):
        path = IDFormat.folder_binding_project(
            "PORT-PM-MEL-COM-0002",
            "BLD-CBD-500-COLLINSST-001",
            "LEASE-2024-0015",
            "PRJ-20260212-FITOUT-01"
        )
        assert "PRJ-20260212-FITOUT-01" in path
        assert "LEASE-2024-0015" in path

    def test_generate_folder_binding_res(self):
        os = PMEmailCategorisationOS()
        path = os.generate_folder_binding(
            domain=PropertyDomain.RES,
            portfolio_num=1,
            suburb="Parkville",
            street_no="200",
            street_name="BerkeleyStreet",
            tenant_year=2025,
            tenant_num=42,
        )
        assert "PORT-PM-MEL-RES-0001" in path
        assert "PARKVILLE" in path
        assert "TEN-2025-0042" in path

    def test_generate_folder_binding_com(self):
        os = PMEmailCategorisationOS()
        path = os.generate_folder_binding(
            domain=PropertyDomain.COM,
            portfolio_num=5,
            suburb="CBD",
            street_no="500",
            street_name="CollinsStreet",
            lease_year=2024,
            lease_num=15,
        )
        assert "PORT-PM-MEL-COM-0005" in path
        assert "LEASE-2024-0015" in path


# --- 1:1:1 Equivalence Register ---
from src.unimelb.identity.equivalence_register import (
    EquivalenceRegister,
    TRIAD_TABLE,
    UNIFIED_LEXICON,
    AIRLINE_CODES,
)


class TestEquivalenceRegister:
    """Tests for 1:1:1 Equivalence Register and Unified Lexicon."""

    def test_triad_table_has_entries(self):
        assert len(TRIAD_TABLE) >= 15

    def test_unified_lexicon_has_entries(self):
        assert len(UNIFIED_LEXICON) >= 30

    def test_airline_codes_have_entries(self):
        assert len(AIRLINE_CODES) >= 5

    def test_every_triad_has_three_ecosystems(self):
        for mapping in TRIAD_TABLE:
            assert mapping.microsoft != ""
            assert mapping.google != ""
            assert mapping.apple != ""

    def test_every_lexicon_entry_trilingual(self):
        for entry in UNIFIED_LEXICON:
            assert entry.zh != ""
            assert entry.en != ""
            assert entry.code != ""

    def test_lookup_by_chinese(self):
        reg = EquivalenceRegister()
        results = reg.lookup_lexicon("租客", lang="zh")
        assert len(results) == 1
        assert results[0].en == "Renter"
        assert results[0].code == "RESIDENTIAL.RENTERS"

    def test_lookup_by_english(self):
        reg = EquivalenceRegister()
        results = reg.lookup_lexicon("Tenant", lang="en")
        assert len(results) >= 1
        assert any(r.zh == "承租方" for r in results)

    def test_lookup_by_code(self):
        reg = EquivalenceRegister()
        results = reg.lookup_lexicon("VCAT", lang="code")
        assert len(results) == 1
        assert "仲裁" in results[0].zh

    def test_lookup_any_language(self):
        reg = EquivalenceRegister()
        # Search by Chinese
        results_zh = reg.lookup_lexicon("墨尔本大学", lang="any")
        assert len(results_zh) >= 1
        # Search by English
        results_en = reg.lookup_lexicon("University of Melbourne", lang="any")
        assert len(results_en) >= 1
        # Same entry
        assert results_zh[0].code == results_en[0].code == "UNIMELB"

    def test_get_triad_mapping(self):
        reg = EquivalenceRegister()
        mapping = reg.get_triad_mapping("Calendar")
        assert mapping is not None
        assert "Outlook" in mapping.microsoft
        assert "Google Calendar" in mapping.google
        assert "Apple Calendar" in mapping.apple

    def test_get_ecosystem_equivalent(self):
        reg = EquivalenceRegister()
        result = reg.get_ecosystem_equivalent("Teams")
        assert result is not None
        assert "Teams" in result["microsoft"]
        assert result["google"] != ""
        assert result["apple"] != ""

    def test_get_ecosystem_equivalent_google(self):
        reg = EquivalenceRegister()
        result = reg.get_ecosystem_equivalent("Gmail")
        assert result is not None
        assert "Outlook" in result["microsoft"]

    def test_print_111(self):
        reg = EquivalenceRegister()
        output = reg.print_111("Agents", reg.lookup_lexicon("AGENT", lang="code"))
        assert "==" in output
        assert "Lendlease" in output
        assert "JLL" in output
        assert "MICM" in output

    def test_full_summary(self):
        reg = EquivalenceRegister()
        summary = reg.get_full_summary()
        assert summary["triad_mappings"] == len(TRIAD_TABLE)
        assert summary["lexicon_entries"] == len(UNIFIED_LEXICON)
        assert "1:1:1" in summary["principle"]

    def test_airline_triad_consistency(self):
        """Airline codes follow 1:1:1: 中文 : English : IATA code."""
        for airline in AIRLINE_CODES:
            assert len(airline.code) == 2  # IATA codes are 2 chars
            assert airline.zh != ""
            assert airline.en != ""


# --- v0.2.0 Stakeholder-Aware Cover Scan ---


class TestStakeholderCoverScan:
    """Tests for v0.2.0 stakeholder model, cover scan, and lock escalation."""

    def test_stakeholder_keywords_populated(self):
        assert len(STAKEHOLDER_KEYWORDS) == 5
        assert "RESIDENTIAL.RENTERS" in STAKEHOLDER_KEYWORDS
        assert "COMMERCIAL.CLIENTS" in STAKEHOLDER_KEYWORDS

    def test_stakeholder_folder_map_complete(self):
        assert len(STAKEHOLDER_FOLDER_MAP) == 5
        assert "RESIDENTIAL.RENTERS" in STAKEHOLDER_FOLDER_MAP
        assert "VAULT/" not in STAKEHOLDER_FOLDER_MAP["RESIDENTIAL.RENTERS"]

    def test_vault_folder_map_complete(self):
        assert len(VAULT_FOLDER_MAP) == 5
        for key, path in VAULT_FOLDER_MAP.items():
            assert path.startswith("VAULT/")

    def test_pmos_labels_have_all_groups(self):
        assert "base" in PMOS_LABELS
        assert "stakeholder" in PMOS_LABELS
        assert "category" in PMOS_LABELS
        assert len(PMOS_LABELS["stakeholder"]) == 5

    def test_detect_portfolio_residential(self):
        os = PMEmailCategorisationOS()
        assert os.detect_portfolio("Bond refund for renter") == "RESIDENTIAL"

    def test_detect_portfolio_commercial(self):
        os = PMEmailCategorisationOS()
        assert os.detect_portfolio("CPI rent review and outgoings") == "COMMERCIAL"

    def test_detect_portfolio_unknown(self):
        os = PMEmailCategorisationOS()
        assert os.detect_portfolio("Hello, checking in") == "UNKNOWN"

    def test_infer_stakeholder_res_renters(self):
        os = PMEmailCategorisationOS()
        result = os.infer_stakeholder("RESIDENTIAL", "The renter submitted a maintenance request")
        assert result == "RESIDENTIAL.RENTERS"

    def test_infer_stakeholder_res_rental_providers(self):
        os = PMEmailCategorisationOS()
        result = os.infer_stakeholder("RESIDENTIAL", "Rental provider approved the quote")
        assert result == "RESIDENTIAL.RENTAL_PROVIDERS"

    def test_infer_stakeholder_com_tenants(self):
        os = PMEmailCategorisationOS()
        result = os.infer_stakeholder("COMMERCIAL", "The lessee requested fitout approval")
        assert result == "COMMERCIAL.TENANTS"

    def test_infer_stakeholder_com_landlords(self):
        os = PMEmailCategorisationOS()
        result = os.infer_stakeholder("COMMERCIAL", "Landlord instructions for owner approval")
        assert result == "COMMERCIAL.LANDLORDS"

    def test_infer_stakeholder_com_clients(self):
        os = PMEmailCategorisationOS()
        result = os.infer_stakeholder("COMMERCIAL", "Client portfolio asset management reporting pack")
        assert result == "COMMERCIAL.CLIENTS"

    def test_detect_secondary_stakeholder_present(self):
        os = PMEmailCategorisationOS()
        result = os.detect_secondary_stakeholder("I have cc landlord on this")
        assert result == "PRESENT"

    def test_detect_secondary_stakeholder_none(self):
        os = PMEmailCategorisationOS()
        result = os.detect_secondary_stakeholder("Regular maintenance email")
        assert result == "NONE"

    def test_escalate_lock_vault(self):
        os = PMEmailCategorisationOS()
        result = os.escalate_lock_level("Passport copy attached for 100 points ID check")
        assert result == "L4_VAULT"

    def test_escalate_lock_sensitive(self):
        os = PMEmailCategorisationOS()
        result = os.escalate_lock_level("VCAT tribunal hearing for breach notice")
        assert result == "L3_SENSITIVE"

    def test_escalate_lock_normal(self):
        os = PMEmailCategorisationOS()
        result = os.escalate_lock_level("Routine inspection scheduled for Tuesday")
        assert result == "L1_INTERNAL"

    def test_cover_scan_residential_renter(self):
        os = PMEmailCategorisationOS()
        result = os.cover_scan(
            subject="Renter maintenance request - leaking tap",
            body="The renter reported a leaking tap in the kitchen."
        )
        assert result.portfolio_guess == "RESIDENTIAL"
        assert result.stakeholder_primary == "RESIDENTIAL.RENTERS"
        assert "PMOS/RESIDENTIAL" in result.labels
        assert "PMOS/RES-RENTERS" in result.labels

    def test_cover_scan_commercial_outgoings(self):
        os = PMEmailCategorisationOS()
        result = os.cover_scan(
            subject="CPI rent review and outgoings reconciliation",
            body="The lessee outgoings require review per lease terms."
        )
        assert result.portfolio_guess == "COMMERCIAL"
        assert result.stakeholder_primary == "COMMERCIAL.TENANTS"
        assert "PMOS/COMMERCIAL" in result.labels

    def test_cover_scan_vault_escalation(self):
        os = PMEmailCategorisationOS()
        result = os.cover_scan(
            subject="Rental application - 100 points ID check",
            body="Please find attached passport and driver licence",
            attachment_names=["passport_scan.pdf", "driver_licence.jpg"]
        )
        assert result.lock_level_guess == "L4_VAULT"
        assert result.needs_deep_extraction is True
        assert "PMOS/LOCK-L4-VAULT" in result.labels
        assert "VAULT/" in result.routing_folder

    def test_cover_scan_sensitive_escalation(self):
        os = PMEmailCategorisationOS()
        result = os.cover_scan(
            subject="VCAT hearing for rent arrears - Unit 5",
            body="Notice to vacate issued after breach notice"
        )
        assert result.lock_level_guess == "L3_SENSITIVE"
        assert result.needs_deep_extraction is True
        assert "PMOS/LOCK-L3" in result.labels

    def test_cover_scan_default_labels(self):
        os = PMEmailCategorisationOS()
        result = os.cover_scan(subject="Hello, just checking in")
        assert "PMOS/PROFESSIONAL" in result.labels
        assert result.portfolio_guess == "UNKNOWN"
        assert result.stakeholder_primary == "UNKNOWN"

    def test_cover_scan_secondary_stakeholder(self):
        os = PMEmailCategorisationOS()
        result = os.cover_scan(
            subject="Bond refund for renter",
            body="I have forwarded to owner for approval"
        )
        assert result.stakeholder_secondary == "PRESENT"
        assert any("counterparties" in r for r in result.rationale)

    def test_stakeholder_enum_values(self):
        assert Stakeholder.RES_RENTERS.value == "RESIDENTIAL.RENTERS"
        assert Stakeholder.COM_CLIENTS.value == "COMMERCIAL.CLIENTS"
        assert Stakeholder.UNKNOWN.value == "UNKNOWN"

    def test_get_stakeholder_folder(self):
        os = PMEmailCategorisationOS()
        folder = os.get_stakeholder_folder("RESIDENTIAL.RENTERS")
        assert folder == "RES/20_Stakeholders/Renters/"

    def test_get_vault_folder(self):
        os = PMEmailCategorisationOS()
        vault = os.get_vault_folder("COMMERCIAL.TENANTS")
        assert vault == "VAULT/Commercial/Tenants_Confidential/"


# --- GOV Domain Registry ---
from src.unimelb.gov_registry.domain_registry import (
    GovDomainRegistry,
    DomainClassification,
    SearchMode,
    TrafficSignal,
    DOMAIN_REGISTER,
    VIC_GOV_CATEGORIES,
)


class TestGovDomainRegistry:
    """Tests for GOV Domain Registry and validation framework."""

    def test_domain_register_populated(self):
        assert len(DOMAIN_REGISTER) >= 30

    def test_vic_gov_categories_complete(self):
        assert len(VIC_GOV_CATEGORIES) == 8
        assert "Infrastructure & Major Projects" in VIC_GOV_CATEGORIES
        assert "Health" in VIC_GOV_CATEGORIES
        assert "Transport" in VIC_GOV_CATEGORIES

    def test_classify_vic_gov_domain(self):
        reg = GovDomainRegistry()
        assert reg.classify_domain("bigbuild.vic.gov.au") == DomainClassification.VIC_GOV

    def test_classify_au_gov_domain(self):
        reg = GovDomainRegistry()
        assert reg.classify_domain("rba.gov.au") == DomainClassification.AU_GOV

    def test_classify_edu_domain(self):
        reg = GovDomainRegistry()
        assert reg.classify_domain("unimelb.edu.au") == DomainClassification.AU_EDU

    def test_classify_commercial_domain(self):
        reg = GovDomainRegistry()
        assert reg.classify_domain("google.com") == DomainClassification.COMMERCIAL

    def test_traffic_signal_green_vic_gov(self):
        reg = GovDomainRegistry()
        assert reg.get_traffic_signal("health.vic.gov.au") == TrafficSignal.GREEN

    def test_traffic_signal_green_edu(self):
        reg = GovDomainRegistry()
        assert reg.get_traffic_signal("unimelb.edu.au") == TrafficSignal.GREEN

    def test_traffic_signal_yellow_commercial(self):
        reg = GovDomainRegistry()
        assert reg.get_traffic_signal("example.com") == TrafficSignal.YELLOW

    def test_traffic_signal_red_no_https(self):
        reg = GovDomainRegistry()
        assert reg.get_traffic_signal("health.vic.gov.au", has_https=False) == TrafficSignal.RED

    def test_strict_mode_vic_only(self):
        reg = GovDomainRegistry(search_mode=SearchMode.STRICT)
        assert reg.is_domain_allowed("health.vic.gov.au") is True
        assert reg.is_domain_allowed("rba.gov.au") is False

    def test_merged_mode_allows_gov_au(self):
        reg = GovDomainRegistry(search_mode=SearchMode.MERGED)
        assert reg.is_domain_allowed("health.vic.gov.au") is True
        assert reg.is_domain_allowed("rba.gov.au") is True
        assert reg.is_domain_allowed("google.com") is False

    def test_boundary_mode_allows_all(self):
        reg = GovDomainRegistry(search_mode=SearchMode.BOUNDARY)
        assert reg.is_domain_allowed("google.com") is True

    def test_source_label_vic_gov(self):
        reg = GovDomainRegistry()
        assert reg.get_source_label("ptv.vic.gov.au") == "VIC Gov Primary"

    def test_source_label_au_gov(self):
        reg = GovDomainRegistry()
        assert reg.get_source_label("rba.gov.au") == "Other AU Gov"

    def test_source_label_commercial(self):
        reg = GovDomainRegistry()
        assert reg.get_source_label("example.com") == "Non-gov Context"

    def test_category_for_domain(self):
        reg = GovDomainRegistry()
        assert reg.get_category_for_domain("bigbuild.vic.gov.au") == "Infrastructure & Major Projects"
        assert reg.get_category_for_domain("health.vic.gov.au") == "Health"
        assert reg.get_category_for_domain("ptv.vic.gov.au") == "Transport"

    def test_domain_frequency(self):
        reg = GovDomainRegistry()
        assert reg.get_domain_frequency("bigbuild.vic.gov.au") == 26
        assert reg.get_domain_frequency("health.vic.gov.au") == 24

    def test_top_domains(self):
        reg = GovDomainRegistry()
        top5 = reg.get_top_domains(5)
        assert len(top5) == 5
        assert top5[0].count >= top5[1].count  # sorted descending

    def test_vic_gov_domains_list(self):
        reg = GovDomainRegistry()
        vic = reg.get_vic_gov_domains()
        assert len(vic) >= 25
        for entry in vic:
            assert entry.registrable_domain == "vic.gov.au"

    def test_total_research_hits(self):
        reg = GovDomainRegistry()
        total = reg.get_total_research_hits()
        assert total > 150  # sum of all counts

    def test_verify_domain_step1(self):
        reg = GovDomainRegistry()
        result = reg.verify_domain_step1("health.vic.gov.au")
        assert result["classification"] == "vic.gov.au"
        assert result["allowed"] is True
        assert result["traffic_signal"] == "GREEN"
        assert result["source_label"] == "VIC Gov Primary"
        assert result["category"] == "Health"

    def test_registry_summary(self):
        reg = GovDomainRegistry()
        summary = reg.get_registry_summary()
        assert summary["total_domains"] >= 30
        assert summary["total_hits"] > 0
        assert summary["vic_gov_domains"] >= 25
        assert len(summary["categories"]) == 8
        assert len(summary["top_5"]) == 5

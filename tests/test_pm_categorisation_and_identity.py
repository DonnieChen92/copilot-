"""
Tests for PM-Email-Categorisation.os and 1:1:1 Equivalence Register.
=====================================================================
"""

import pytest

# --- PM-Email-Categorisation.os ---
from src.unimelb.property_management.categorisation_os.pm_email_categorisation import (
    FolderCategory,
    IDFormat,
    LockLevel,
    PMEmailCategorisationOS,
    PropertyDomain,
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

"""
Tests for Legal AI Evidence Mapping Module
===========================================
Tests cover:
- LegalKnowledgeBase data integrity
- SimilarityMatcher scoring algorithms
- EvidenceMapper clause and case mapping
- LegalSearchPipeline end-to-end flow
"""

import pytest

from src.legal.legal_knowledge_base import (
    LegalKnowledgeBase,
    LegislationType,
    TopicArea,
)
from src.legal.similarity_matcher import SimilarityMatcher
from src.legal.evidence_mapper import (
    EvidenceItem,
    EvidenceMapper,
)
from src.legal.legal_search_pipeline import LegalSearchPipeline


# ============================================================
# LegalKnowledgeBase Tests
# ============================================================

class TestLegalKnowledgeBase:
    """Tests for the legal knowledge base."""

    def setup_method(self):
        self.kb = LegalKnowledgeBase()

    def test_knowledge_base_loads_legislation(self):
        """Knowledge base should load core legislation on init."""
        stats = self.kb.get_stats()
        assert stats["total_legislation"] >= 10
        assert stats["total_clauses"] >= 20
        assert stats["total_cases"] >= 25

    def test_all_legislation_has_clauses(self):
        """Every legislation should have at least one clause."""
        for leg_id, leg in self.kb.legislation.items():
            assert len(leg.clauses) > 0, f"{leg_id} has no clauses"

    def test_all_legislation_in_force(self):
        """All core legislation should be currently in force."""
        for leg_id, leg in self.kb.legislation.items():
            assert leg.in_force is True, f"{leg_id} is not in force"

    def test_udhr_present(self):
        """UDHR should be in the knowledge base."""
        udhr = self.kb.get_legislation("UDHR")
        assert udhr is not None
        assert udhr.title == "Universal Declaration of Human Rights"
        assert udhr.in_force is True

    def test_iccpr_present(self):
        """ICCPR should be in the knowledge base."""
        iccpr = self.kb.get_legislation("ICCPR")
        assert iccpr is not None
        assert "Civil and Political Rights" in iccpr.title

    def test_get_legislation_by_topic(self):
        """Should return legislation for each major topic."""
        for topic in [
            TopicArea.FREEDOM_OF_INFORMATION,
            TopicArea.RESIDENCE_RIGHTS,
            TopicArea.AGENT_DUTY,
            TopicArea.LGBTI_RIGHTS,
            TopicArea.AI_GOVERNANCE,
        ]:
            results = self.kb.get_legislation_by_topic(topic)
            assert len(results) > 0, f"No legislation for topic {topic.value}"

    def test_get_clauses_by_topic(self):
        """Should return clauses for each major topic."""
        for topic in [
            TopicArea.FREEDOM_OF_INFORMATION,
            TopicArea.RESIDENCE_RIGHTS,
            TopicArea.AGENT_DUTY,
            TopicArea.LGBTI_RIGHTS,
        ]:
            results = self.kb.get_clauses_by_topic(topic)
            assert len(results) > 0, f"No clauses for topic {topic.value}"

    def test_get_cases_by_topic(self):
        """Should return at least 5 cases per topic area."""
        for topic in [
            TopicArea.FREEDOM_OF_INFORMATION,
            TopicArea.RESIDENCE_RIGHTS,
            TopicArea.AGENT_DUTY,
            TopicArea.LGBTI_RIGHTS,
            TopicArea.AI_GOVERNANCE,
        ]:
            results = self.kb.get_cases_by_topic(topic)
            assert len(results) >= 5, (
                f"Topic {topic.value} has only {len(results)} cases (need ≥5)"
            )

    def test_cases_have_required_fields(self):
        """All cases should have required fields populated."""
        for case_id, case in self.kb.cases.items():
            assert case.case_name, f"{case_id} missing case_name"
            assert case.court, f"{case_id} missing court"
            assert case.date, f"{case_id} missing date"
            assert case.citation, f"{case_id} missing citation"
            assert len(case.key_principles) > 0, f"{case_id} missing key_principles"
            assert case.summary, f"{case_id} missing summary"

    def test_get_cases_for_clause(self):
        """Should find cases referencing specific clauses."""
        # ECHR Art.8 should have multiple cases
        cases = self.kb.get_cases_for_clause("ECHR-Art8")
        assert len(cases) > 0

    def test_search_clauses_by_keywords(self):
        """Keyword search should return relevant clauses."""
        results = self.kb.search_clauses(["freedom", "information", "expression"])
        assert len(results) > 0
        # Top result should be about freedom of information/expression
        assert any(
            "freedom" in r.title.lower() or "expression" in r.title.lower()
            for r in results[:3]
        )

    def test_supporting_acts_referenced(self):
        """All legislation should reference supporting acts."""
        for leg_id, leg in self.kb.legislation.items():
            if leg.legislation_type != LegislationType.TREATY or leg_id == "UDHR":
                continue
            assert leg.supporting_act, f"{leg_id} missing supporting_act"


# ============================================================
# SimilarityMatcher Tests
# ============================================================

class TestSimilarityMatcher:
    """Tests for the similarity matching engine."""

    def setup_method(self):
        self.matcher = SimilarityMatcher()

    def test_identical_texts_high_similarity(self):
        """Identical texts should have similarity score of 1.0."""
        text = "freedom of expression and information rights"
        score = self.matcher.tfidf_cosine_similarity(text, text)
        assert score == pytest.approx(1.0, abs=0.01)

    def test_empty_text_zero_similarity(self):
        """Empty texts should return 0.0 similarity."""
        assert self.matcher.tfidf_cosine_similarity("", "") == 0.0
        assert self.matcher.tfidf_cosine_similarity("hello", "") == 0.0

    def test_related_texts_moderate_similarity(self):
        """Related texts should have moderate to high similarity."""
        text_a = "freedom of information access to public records"
        text_b = "right to access information from public authorities"
        score = self.matcher.tfidf_cosine_similarity(text_a, text_b)
        assert score > 0.3

    def test_unrelated_texts_low_similarity(self):
        """Unrelated texts should have low similarity."""
        text_a = "freedom of information access to public records"
        text_b = "quantum computing algorithms and machine learning"
        score = self.matcher.tfidf_cosine_similarity(text_a, text_b)
        assert score < 0.3

    def test_keyword_overlap_identical(self):
        """Identical keyword sets should return 1.0."""
        keywords = ["freedom", "information", "rights"]
        score = self.matcher.keyword_overlap_score(keywords, keywords)
        assert score == pytest.approx(1.0, abs=0.01)

    def test_keyword_overlap_partial(self):
        """Partial keyword overlap should return intermediate score."""
        kw_a = ["freedom", "information", "rights"]
        kw_b = ["freedom", "expression", "media"]
        score = self.matcher.keyword_overlap_score(kw_a, kw_b)
        assert 0.0 < score < 1.0

    def test_keyword_overlap_empty(self):
        """Empty keyword lists should return 0.0."""
        assert self.matcher.keyword_overlap_score([], []) == 0.0

    def test_ngram_similarity(self):
        """N-gram similarity should work for similar strings."""
        score = self.matcher.ngram_similarity(
            "freedom of expression",
            "freedom of information",
        )
        assert score > 0.5

    def test_hybrid_similarity(self):
        """Hybrid similarity should combine methods."""
        score = self.matcher.hybrid_similarity(
            "freedom of information rights",
            "right to access public information",
            keywords_a=["freedom", "information"],
            keywords_b=["access", "information"],
        )
        assert 0.0 <= score <= 1.0

    def test_batch_similarity_returns_sorted(self):
        """Batch similarity should return results sorted by score descending."""
        query = "freedom of expression"
        candidates = [
            "quantum physics theory",
            "freedom of opinion and expression rights",
            "housing regulations for residents",
        ]
        results = self.matcher.batch_similarity(query, candidates)
        assert len(results) == 3
        # Should be sorted descending
        assert results[0][1] >= results[1][1] >= results[2][1]
        # Most similar should be the expression rights candidate
        assert results[0][0] == 1  # index of expression rights

    def test_tokenize_removes_stop_words(self):
        """Tokenizer should remove stop words."""
        tokens = self.matcher.tokenize("the right to freedom of expression")
        assert "the" not in tokens
        assert "to" not in tokens
        assert "of" not in tokens
        assert "right" in tokens
        assert "freedom" in tokens
        assert "expression" in tokens


# ============================================================
# EvidenceMapper Tests
# ============================================================

class TestEvidenceMapper:
    """Tests for the evidence mapping engine."""

    def setup_method(self):
        self.mapper = EvidenceMapper()

    def _make_evidence(
        self, evidence_id: str, description: str, content: str,
        keywords: list[str], topics: list[TopicArea] | None = None,
    ) -> EvidenceItem:
        return EvidenceItem(
            evidence_id=evidence_id,
            description=description,
            content=content,
            source="Test",
            date_collected="2025-01-01",
            topics=topics or [],
            keywords=keywords,
        )

    def test_map_foi_evidence(self):
        """FOI evidence should map to freedom of information clauses."""
        evidence = self._make_evidence(
            "TEST-FOI",
            "Government refused to disclose information to public",
            "A public authority denied access to information requested by "
            "an NGO. The authority refused to provide documents related to "
            "freedom of expression and public interest disclosure.",
            ["freedom", "information", "disclosure", "public authority"],
            [TopicArea.FREEDOM_OF_INFORMATION],
        )
        result = self.mapper.map_evidence(evidence)
        assert len(result.clause_mappings) > 0
        assert len(result.case_mappings) > 0
        assert TopicArea.FREEDOM_OF_INFORMATION in result.topics_covered

    def test_map_residence_evidence(self):
        """Residence evidence should map to residence rights clauses."""
        evidence = self._make_evidence(
            "TEST-RES",
            "Residents evicted without legal process",
            "Multiple residents were evicted from their homes without "
            "proper legal process. The right to housing and residence "
            "was violated. State agents failed to follow due process.",
            ["residence", "housing", "eviction", "home", "movement"],
            [TopicArea.RESIDENCE_RIGHTS],
        )
        result = self.mapper.map_evidence(evidence)
        assert len(result.clause_mappings) > 0
        assert len(result.case_mappings) > 0

    def test_map_lgbti_evidence(self):
        """LGBTI evidence should map to LGBTI rights clauses."""
        evidence = self._make_evidence(
            "TEST-LGBTI",
            "LGBTI individuals face housing discrimination",
            "LGBTI persons were denied housing based on their sexual "
            "orientation and gender identity. This constitutes discrimination "
            "and violates the principle of equality and non-discrimination.",
            ["LGBTI", "sexual orientation", "gender identity",
             "discrimination", "housing", "equality"],
            [TopicArea.LGBTI_RIGHTS],
        )
        result = self.mapper.map_evidence(evidence)
        assert len(result.clause_mappings) > 0
        assert len(result.case_mappings) > 0

    def test_cases_per_point_default(self):
        """Should return up to 5 cases per evidence point by default."""
        evidence = self._make_evidence(
            "TEST-CASES",
            "Agent failed to protect community safety",
            "State agents failed to take preventive measures to protect "
            "community safety despite warnings. The duty of agents to "
            "investigate and prevent harm was breached.",
            ["agent", "duty", "safety", "community", "protection"],
            [TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY],
        )
        result = self.mapper.map_evidence(evidence)
        assert len(result.case_mappings) <= 5

    def test_similarity_threshold_configurable(self):
        """Mapper should accept custom similarity thresholds."""
        strict_mapper = EvidenceMapper(similarity_threshold=0.95)
        assert strict_mapper.similarity_threshold == 0.95
        lenient_mapper = EvidenceMapper(similarity_threshold=0.10)
        assert lenient_mapper.similarity_threshold == 0.10

    def test_compliance_notes_generated(self):
        """Mapping results should include compliance notes."""
        evidence = self._make_evidence(
            "TEST-COMP",
            "Freedom of information request denied",
            "Public authority denied freedom of information access "
            "to expression-related documents.",
            ["freedom", "information", "expression"],
            [TopicArea.FREEDOM_OF_INFORMATION],
        )
        result = self.mapper.map_evidence(evidence)
        assert len(result.compliance_notes) > 0
        # Should mention in-force status
        assert any("in-force" in note.lower() or "in force" in note.lower()
                    for note in result.compliance_notes)

    def test_audit_log_populated(self):
        """Mapping should populate the audit log."""
        evidence = self._make_evidence(
            "TEST-AUDIT",
            "Test evidence for audit log",
            "Freedom of information and expression rights.",
            ["freedom", "information"],
            [TopicArea.FREEDOM_OF_INFORMATION],
        )
        self.mapper.map_evidence(evidence)
        log = self.mapper.get_audit_log()
        assert len(log) >= 1
        assert log[-1]["evidence_id"] == "TEST-AUDIT"

    def test_to_excel_data_format(self):
        """Excel export data should have required structure."""
        evidence = self._make_evidence(
            "TEST-EXCEL",
            "Freedom of expression test",
            "Right to freedom of expression and information.",
            ["freedom", "expression", "information"],
            [TopicArea.FREEDOM_OF_INFORMATION],
        )
        result = self.mapper.map_evidence(evidence)
        excel_data = self.mapper.to_excel_data(result)
        assert "evidence" in excel_data
        assert "clause_mappings" in excel_data
        assert "case_mappings" in excel_data
        assert "compliance" in excel_data

    def test_to_knowledge_graph_triples(self):
        """KG triples should be generated from mapping results."""
        evidence = self._make_evidence(
            "TEST-KG",
            "Agent duty to protect community safety",
            "State agents have a duty to protect community safety "
            "and investigate threats. Due diligence obligation.",
            ["agent", "duty", "safety", "community"],
            [TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY],
        )
        result = self.mapper.map_evidence(evidence)
        triples = self.mapper.to_knowledge_graph_triples(result)
        assert len(triples) > 0
        for triple in triples:
            assert "subject" in triple
            assert "predicate" in triple
            assert "object" in triple

    def test_auto_topic_detection(self):
        """Topics should be auto-detected from evidence content."""
        evidence = self._make_evidence(
            "TEST-AUTO",
            "AI surveillance and privacy violation",
            "An artificial intelligence surveillance system was deployed "
            "without privacy safeguards. The algorithm showed bias and "
            "discrimination against minorities.",
            ["AI", "surveillance", "privacy", "discrimination"],
            # No explicit topics - should auto-detect
        )
        result = self.mapper.map_evidence(evidence)
        assert len(result.topics_covered) > 0


# ============================================================
# LegalSearchPipeline Tests
# ============================================================

class TestLegalSearchPipeline:
    """Tests for the end-to-end legal search pipeline."""

    def setup_method(self):
        self.pipeline = LegalSearchPipeline()

    def test_pipeline_initialization(self):
        """Pipeline should initialize with all components."""
        stats = self.pipeline.get_stats()
        assert stats["knowledge_base"]["total_legislation"] >= 10
        assert stats["evidence_processed"] == 0

    def test_ingest_single_evidence(self):
        """Pipeline should process single evidence item."""
        evidence = EvidenceItem(
            evidence_id="PIPE-001",
            description="Freedom of information denial",
            content="Public authority denied access to information "
                    "and documents related to public interest.",
            source="Test",
            date_collected="2025-01-01",
            keywords=["freedom", "information", "disclosure"],
            topics=[TopicArea.FREEDOM_OF_INFORMATION],
        )
        result = self.pipeline.ingest_evidence(evidence)
        assert result is not None
        assert result.evidence.evidence_id == "PIPE-001"

    def test_search_by_topic(self):
        """Topic search should return structured results."""
        result = self.pipeline.search_by_topic(TopicArea.FREEDOM_OF_INFORMATION)
        assert result["topic"] == "freedom_of_information"
        assert len(result["legislation"]) > 0
        assert len(result["clauses"]) > 0
        assert len(result["cases"]) > 0

    def test_comprehensive_search(self):
        """Comprehensive search should return complete report."""
        evidence_items = [
            EvidenceItem(
                evidence_id="COMP-001",
                description="FOI test",
                content="Freedom of information and expression rights "
                        "access to public authority documents.",
                source="Test",
                date_collected="2025-01-01",
                keywords=["freedom", "information", "expression"],
                topics=[TopicArea.FREEDOM_OF_INFORMATION],
            ),
        ]
        report = self.pipeline.run_comprehensive_search(evidence_items)

        assert "search_metadata" in report
        assert "evidence_mappings" in report
        assert "topic_analysis" in report
        assert "aggregate_statistics" in report
        assert "compliance_summary" in report
        assert "knowledge_graph_stats" in report
        assert "framework_references" in report

        # Check framework references include required URLs
        refs = report["framework_references"]
        assert "ohchr" in refs
        assert "un_ai" in refs
        assert "un_hr" in refs

    def test_knowledge_graph_populated(self):
        """Knowledge graph should be populated after ingestion."""
        evidence = EvidenceItem(
            evidence_id="KG-001",
            description="Agent duty failure",
            content="State agents failed duty to protect community "
                    "safety and investigate threats.",
            source="Test",
            date_collected="2025-01-01",
            keywords=["agent", "duty", "safety"],
            topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY],
        )
        self.pipeline.ingest_evidence(evidence)
        kg = self.pipeline.get_knowledge_graph()
        stats = kg.get_stats()
        assert stats["node_count"] > 0
        assert stats["edge_count"] > 0

    def test_pipeline_stats_increment(self):
        """Pipeline stats should increment after processing."""
        evidence = EvidenceItem(
            evidence_id="STAT-001",
            description="Test",
            content="Freedom of information expression rights.",
            source="Test",
            date_collected="2025-01-01",
            keywords=["freedom", "information"],
            topics=[TopicArea.FREEDOM_OF_INFORMATION],
        )
        self.pipeline.ingest_evidence(evidence)
        stats = self.pipeline.get_stats()
        assert stats["evidence_processed"] == 1

"""
Legal Search Pipeline / 法律搜索管線 / 法律搜索管线
====================================================
End-to-end orchestration pipeline for legal evidence mapping.
Integrates with the existing DocumentPipeline, KnowledgeGraphBuilder,
and NLU system.

Pipeline Flow / 管線流程 / 管线流程:
1. Ingest evidence → NLU extraction
2. Topic classification → Knowledge Base query
3. Evidence-to-clause mapping with similarity scoring
4. Case law matching (5 cases per point, ≥90% similarity)
5. Compliance validation against OHCHR/UN frameworks
6. Export to Excel/PPTX/Knowledge Graph

References / 參考資料 / 参考资料:
- OHCHR: https://www.ohchr.org/en/ohchr_homepage
- OHCHR LGBTI: https://www.ohchr.org/en/sexual-orientation-and-gender-identity/
- UN AI: https://www.un.org/zh/global-issues/artificial-intelligence
- UN HR: https://www.un.org/zh/our-work/protect-human-rights
- PMC Reference: https://pmc.ncbi.nlm.nih.gov/articles/PMC10601905/
"""

from datetime import datetime
from typing import Any

from ..knowledge_graph.kg_builder import KnowledgeGraphBuilder
from .evidence_mapper import (
    CaseMapping,
    ClauseMapping,
    EvidenceItem,
    EvidenceMapper,
    EvidenceMappingResult,
)
from .legal_knowledge_base import (
    LegalKnowledgeBase,
    TopicArea,
)
from .similarity_matcher import SimilarityMatcher


class LegalSearchPipeline:
    """
    End-to-end legal search and evidence mapping pipeline.

    端到端法律搜索和證據映射管線。
    端到端法律搜索和证据映射管线。

    Integrates with:
    - KnowledgeGraphBuilder for entity/relation storage
    - EvidenceMapper for clause and case mapping
    - LegalKnowledgeBase for legislation and case law
    - SimilarityMatcher for confidence scoring

    Compliance / 合規 / 合规:
    - Maps only to in-force legislation
    - Enforces ≥90% average similarity threshold
    - Cross-references original supporting acts
    - 5 recent cases per evidence point
    - Full audit trail
    """

    def __init__(
        self,
        output_dir: str = "./output/legal",
        similarity_threshold: float = 0.90,
        cases_per_point: int = 5,
    ):
        self.output_dir = output_dir
        self.kb = LegalKnowledgeBase()
        self.mapper = EvidenceMapper(
            knowledge_base=self.kb,
            similarity_threshold=similarity_threshold,
            cases_per_point=cases_per_point,
        )
        self.kg = KnowledgeGraphBuilder()
        self.matcher = SimilarityMatcher()
        self._results: list[EvidenceMappingResult] = []

    def ingest_evidence(self, evidence: EvidenceItem) -> EvidenceMappingResult:
        """
        Process a single evidence item through the full legal search pipeline.

        透過完整法律搜索管線處理單個證據項目。
        通过完整法律搜索管线处理单个证据项目。

        Steps:
        1. Map evidence to clauses and cases
        2. Store mappings in knowledge graph
        3. Validate compliance
        4. Return comprehensive result
        """
        # Step 1: Map evidence
        result = self.mapper.map_evidence(evidence)

        # Step 2: Store in knowledge graph
        self._store_in_kg(result)

        # Step 3: Accumulate results
        self._results.append(result)

        return result

    def ingest_evidence_batch(
        self, evidence_items: list[EvidenceItem]
    ) -> list[EvidenceMappingResult]:
        """Process multiple evidence items through the pipeline."""
        return [self.ingest_evidence(ev) for ev in evidence_items]

    def _store_in_kg(self, result: EvidenceMappingResult) -> None:
        """Store mapping results in the knowledge graph."""
        ev_id = f"Evidence:{result.evidence.evidence_id}"
        self.kg.add_entity(ev_id, entity_type="EVIDENCE")

        for m in result.clause_mappings:
            clause_node = f"Clause:{m.clause_id}"
            self.kg.add_entity(clause_node, entity_type="CLAUSE")
            self.kg.add_relation(
                ev_id,
                f"mapped_to (score={m.similarity_score:.2f})",
                clause_node,
                confidence=m.similarity_score,
            )

            leg_node = f"Legislation:{m.legislation_title[:50]}"
            self.kg.add_entity(leg_node, entity_type="LEGISLATION")
            self.kg.add_relation(clause_node, "part_of", leg_node)

        for m in result.case_mappings:
            case_node = f"Case:{m.case_id}"
            self.kg.add_entity(case_node, entity_type="CASE_LAW")
            self.kg.add_relation(
                ev_id,
                f"supported_by (score={m.similarity_score:.2f})",
                case_node,
                confidence=m.similarity_score,
            )

    def search_by_topic(
        self,
        topic: TopicArea,
        evidence_text: str = "",
    ) -> dict[str, Any]:
        """
        Search the knowledge base by topic area.

        按主題領域搜索知識庫。
        按主题领域搜索知识库。

        Returns legislation, clauses, and cases for the given topic.
        """
        legislation = self.kb.get_legislation_by_topic(topic)
        clauses = self.kb.get_clauses_by_topic(topic)
        cases = self.kb.get_cases_by_topic(topic)

        result = {
            "topic": topic.value,
            "legislation": [
                {
                    "id": leg.legislation_id,
                    "title": leg.title,
                    "type": leg.legislation_type.value,
                    "in_force": leg.in_force,
                    "supporting_act": leg.supporting_act,
                }
                for leg in legislation
            ],
            "clauses": [
                {
                    "id": cl.clause_id,
                    "article": cl.article_number,
                    "title": cl.title,
                    "text": cl.text[:200] + "..." if len(cl.text) > 200 else cl.text,
                }
                for cl in clauses
            ],
            "cases": [
                {
                    "id": c.case_id,
                    "name": c.case_name,
                    "court": c.court,
                    "date": c.date,
                    "citation": c.citation,
                    "summary": c.summary[:200] + "..." if len(c.summary) > 200 else c.summary,
                }
                for c in cases
            ],
            "counts": {
                "legislation": len(legislation),
                "clauses": len(clauses),
                "cases": len(cases),
            },
        }

        # If evidence text provided, score relevance
        if evidence_text:
            clause_scores = []
            for cl in clauses:
                score = self.matcher.tfidf_cosine_similarity(
                    evidence_text, f"{cl.title} {cl.text}"
                )
                clause_scores.append({"clause_id": cl.clause_id, "relevance": round(score, 4)})
            clause_scores.sort(key=lambda x: x["relevance"], reverse=True)
            result["clause_relevance_scores"] = clause_scores

        return result

    def run_comprehensive_search(
        self,
        evidence_items: list[EvidenceItem],
        topics: list[TopicArea] | None = None,
    ) -> dict[str, Any]:
        """
        Run a comprehensive legal search across all topics and evidence.

        執行跨所有主題和證據的全面法律搜索。
        执行跨所有主题和证据的全面法律搜索。

        This is the primary entry point for the legal AI search system.

        Returns a comprehensive report including:
        - All evidence mappings
        - Topic-level analysis
        - Compliance summary
        - Knowledge graph statistics
        """
        # Default topics if not specified
        if topics is None:
            topics = [
                TopicArea.FREEDOM_OF_INFORMATION,
                TopicArea.RESIDENCE_RIGHTS,
                TopicArea.AGENT_DUTY,
                TopicArea.COMMUNITY_SAFETY,
                TopicArea.LGBTI_RIGHTS,
                TopicArea.AI_GOVERNANCE,
            ]

        # Map all evidence
        results = self.ingest_evidence_batch(evidence_items)

        # Topic-level analysis
        topic_analysis = {}
        for topic in topics:
            topic_data = self.search_by_topic(topic)
            topic_analysis[topic.value] = topic_data

        # Aggregate compliance
        all_compliance_notes = []
        all_clause_mappings: list[ClauseMapping] = []
        all_case_mappings: list[CaseMapping] = []

        for r in results:
            all_compliance_notes.extend(r.compliance_notes)
            all_clause_mappings.extend(r.clause_mappings)
            all_case_mappings.extend(r.case_mappings)

        # Calculate aggregate similarity
        clause_scores = [m.similarity_score for m in all_clause_mappings]
        case_scores = [m.similarity_score for m in all_case_mappings]
        all_scores = clause_scores + case_scores

        avg_similarity = sum(all_scores) / len(all_scores) if all_scores else 0.0

        return {
            "search_metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "evidence_count": len(evidence_items),
                "topics_searched": [t.value for t in topics],
                "similarity_threshold": self.mapper.similarity_threshold,
                "cases_per_point": self.mapper.cases_per_point,
            },
            "evidence_mappings": [
                self.mapper.to_excel_data(r) for r in results
            ],
            "topic_analysis": topic_analysis,
            "aggregate_statistics": {
                "total_clause_mappings": len(all_clause_mappings),
                "total_case_mappings": len(all_case_mappings),
                "average_similarity": round(avg_similarity, 4),
                "meets_threshold": avg_similarity >= self.mapper.similarity_threshold,
                "unique_legislation": len({m.legislation_title for m in all_clause_mappings}),
                "unique_cases": len({m.case_id for m in all_case_mappings}),
            },
            "compliance_summary": list(set(all_compliance_notes)),
            "knowledge_graph_stats": self.kg.get_stats(),
            "audit_log": self.mapper.get_audit_log(),
            "framework_references": {
                "ohchr": "https://www.ohchr.org/en/ohchr_homepage",
                "ohchr_lgbti": "https://www.ohchr.org/en/sexual-orientation-and-gender-identity/",
                "un_ai": "https://www.un.org/zh/global-issues/artificial-intelligence",
                "un_hr": "https://www.un.org/zh/our-work/protect-human-rights",
                "pmc_reference": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10601905/",
            },
        }

    def get_all_results(self) -> list[EvidenceMappingResult]:
        """Return all accumulated mapping results."""
        return self._results.copy()

    def get_knowledge_graph(self) -> KnowledgeGraphBuilder:
        """Return the knowledge graph for visualization or export."""
        return self.kg

    def get_stats(self) -> dict[str, Any]:
        """
        Get pipeline statistics.
        取得管線統計資料。
        获取管线统计数据。
        """
        return {
            "evidence_processed": len(self._results),
            "knowledge_base": self.kb.get_stats(),
            "knowledge_graph": self.kg.get_stats(),
            "audit_entries": len(self.mapper.get_audit_log()),
        }


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    pipeline = LegalSearchPipeline()

    # Demo evidence items covering all topic areas
    demo_evidence = [
        EvidenceItem(
            evidence_id="EV-001",
            description="Government agency refused to disclose environmental impact data "
                        "despite public interest request under freedom of information.",
            content="A public authority denied access to environmental monitoring data "
                    "requested by an NGO acting as a public watchdog. The information "
                    "relates to community health and safety impacts. The authority cited "
                    "national security without providing specific justification.",
            source="FOI Request Denial Case File",
            date_collected="2025-01-15",
            keywords=["freedom of information", "disclosure", "public authority",
                      "environmental data", "NGO", "transparency"],
        ),
        EvidenceItem(
            evidence_id="EV-002",
            description="LGBTI residents faced housing discrimination and eviction "
                        "threats based on sexual orientation in a Council of Europe member state.",
            content="Multiple LGBTI individuals reported being denied housing or threatened "
                    "with eviction by landlords upon discovery of their sexual orientation "
                    "or gender identity. State agents failed to investigate complaints "
                    "or take protective action despite documented patterns of discrimination.",
            source="LGBTI Housing Rights Complaint",
            date_collected="2025-02-01",
            keywords=["LGBTI", "housing", "discrimination", "eviction",
                      "sexual orientation", "residence", "agent duty"],
        ),
        EvidenceItem(
            evidence_id="EV-003",
            description="AI-powered surveillance system deployed without human rights "
                        "impact assessment, disproportionately affecting minority communities.",
            content="An automated facial recognition system was deployed in public spaces "
                    "without conducting a human rights impact assessment. The system showed "
                    "demonstrable bias against racial minorities and LGBTI individuals. "
                    "No legal framework was established prior to deployment.",
            source="AI Surveillance Investigation Report",
            date_collected="2025-01-20",
            keywords=["AI", "surveillance", "facial recognition", "bias",
                      "discrimination", "privacy", "human rights"],
        ),
    ]

    # Run comprehensive search
    report = pipeline.run_comprehensive_search(demo_evidence)

    print("=" * 70)
    print("LEGAL AI EVIDENCE MAPPING REPORT")
    print("=" * 70)

    meta = report["search_metadata"]
    print(f"\nTimestamp: {meta['timestamp']}")
    print(f"Evidence Items: {meta['evidence_count']}")
    print(f"Topics: {', '.join(meta['topics_searched'])}")
    print(f"Similarity Threshold: {meta['similarity_threshold']:.0%}")

    stats = report["aggregate_statistics"]
    print(f"\n--- Aggregate Statistics ---")
    print(f"Clause Mappings: {stats['total_clause_mappings']}")
    print(f"Case Mappings: {stats['total_case_mappings']}")
    print(f"Average Similarity: {stats['average_similarity']:.2%}")
    print(f"Meets Threshold: {stats['meets_threshold']}")
    print(f"Unique Legislation: {stats['unique_legislation']}")
    print(f"Unique Cases: {stats['unique_cases']}")

    print(f"\n--- Compliance Summary ---")
    for note in report["compliance_summary"]:
        print(f"  - {note}")

    print(f"\n--- Evidence Mappings ---")
    for mapping in report["evidence_mappings"]:
        ev = mapping["evidence"]
        print(f"\n  Evidence: {ev['id']} - {ev['description'][:60]}...")
        print(f"  Topics: {', '.join(ev['topics'])}")
        print(f"  Clause Mappings ({len(mapping['clause_mappings'])}):")
        for cm in mapping["clause_mappings"][:3]:
            print(f"    [{cm['similarity']:.2%}] {cm['article']} - {cm['title']}")
            print(f"           from: {cm['legislation'][:60]}")
        print(f"  Case Mappings ({len(mapping['case_mappings'])}):")
        for csm in mapping["case_mappings"][:3]:
            print(f"    [{csm['similarity']:.2%}] {csm['name']}")
            print(f"           {csm['court']} ({csm['date']})")

    print(f"\n--- Knowledge Graph ---")
    kg_stats = report["knowledge_graph_stats"]
    print(f"  Nodes: {kg_stats['node_count']}")
    print(f"  Edges: {kg_stats['edge_count']}")

    print(f"\n--- Framework References ---")
    for name, url in report["framework_references"].items():
        print(f"  {name}: {url}")

    print("\nLegal search pipeline demo complete.")

"""
Legal AI Evidence Mapping Module / 法律 AI 證據映射模組 / 法律 AI 证据映射模块
=============================================================================
AI-powered legal search and evidence-to-clause mapping engine with
legislation tracking, case law similarity matching, and human rights
framework compliance.

Core Components / 核心組件 / 核心组件:
- LegalKnowledgeBase: Legislation, treaties, and case law database
- EvidenceMapper: Maps evidence to legislative clauses
- SimilarityMatcher: Cosine/semantic similarity for case law matching
- LegalSearchPipeline: End-to-end legal search orchestration
"""

from .evidence_mapper import EvidenceMapper
from .legal_knowledge_base import LegalKnowledgeBase
from .legal_search_pipeline import LegalSearchPipeline
from .similarity_matcher import SimilarityMatcher

__all__ = [
    "LegalKnowledgeBase",
    "EvidenceMapper",
    "SimilarityMatcher",
    "LegalSearchPipeline",
]

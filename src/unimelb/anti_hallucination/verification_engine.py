"""
Anti-Hallucination Verification Engine
=======================================
Zero-Assumption, Zero-Faking-Answer-Rate verification framework.

Design: Jiadong Chen (Student ID: 723912)

Pipeline:
  1. Multi-Model Query (3+ frontier models)
  2. Cross-Verification (consensus analysis)
  3. Source Citation (evidence extraction)
  4. Confidence Scoring (0.0 → 1.0)
  5. Manual Verification Queue (human-in-the-loop)
  6. Azure Monitor Audit Log (immutable trail)

Principle: "I don't know" is a valid and preferred response over hallucination.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class VerificationStatus(Enum):
    """Verification outcome for an AI-generated response."""

    HIGH_CONFIDENCE = "high_confidence"                # score > 0.8
    PARTIALLY_VERIFIED = "partially_verified"          # 0.6 ≤ score ≤ 0.8
    UNVERIFIED = "unverified"                          # score < 0.6
    MANUAL_REVIEW_REQUIRED = "manual_review_required"  # flagged for human review
    LEGISLATION_CHECK = "legislation_check"            # requires legal source check
    ELIBRARY_CHECK = "elibrary_check"                  # requires e-library verification
    REJECTED = "rejected"                              # hallucination detected
    CONFIRMED_ACCURATE = "confirmed_accurate"          # human-verified


class SourceType(Enum):
    """Types of evidence sources for citation."""

    ACADEMIC_PAPER = "academic_paper"       # DOI-referenced
    LEGISLATION = "legislation"             # Act, section, clause
    ELIBRARY = "elibrary"                   # UniMelb e-library resource
    OFFICIAL_DOC = "official_documentation" # University or government docs
    WEB_SOURCE = "web_source"               # Verified web URL
    DATASET = "dataset"                     # Research dataset
    COURT_CASE = "court_case"               # Legal case citation
    TEXTBOOK = "textbook"                   # Published textbook


@dataclass
class SourceCitation:
    """A single source citation for evidence backing."""

    source_type: SourceType
    title: str
    reference: str  # DOI, URL, legislation reference, etc.
    relevance_score: float = 0.0
    verified: bool = False
    verification_method: str = ""  # "auto" | "manual" | "austlii" | "elibrary"
    accessed_at: datetime = field(default_factory=datetime.now)


@dataclass
class VerificationResult:
    """Complete verification result for an AI response."""

    query: str
    response: str
    confidence_score: float
    status: VerificationStatus
    sources: list[SourceCitation] = field(default_factory=list)
    models_queried: list[str] = field(default_factory=list)
    consensus_details: dict[str, Any] = field(default_factory=dict)
    manual_review_notes: str = ""
    audit_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: str = ""
    session_id: str = ""


@dataclass
class ManualReviewTask:
    """A task in the manual verification queue."""

    task_id: str
    verification_result: VerificationResult
    assigned_to: str = ""  # staff email or "unassigned"
    priority: str = "medium"
    review_type: str = ""  # "legislation" | "elibrary" | "expert"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    reviewer_notes: str = ""
    final_status: VerificationStatus | None = None


class AntiHallucinationEngine:
    """
    Zero-Assumption Verification Engine for UniMelb AI Platform.

    Every AI response passes through this engine before being delivered
    to the user. Responses are scored, cited, and potentially queued
    for manual verification.

    Key principle: It is ALWAYS better to say "I don't know — please verify
    manually" than to present an unverified answer as fact.
    """

    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.8
    PARTIAL_CONFIDENCE_THRESHOLD = 0.6
    REJECTION_THRESHOLD = 0.2

    # Query patterns that ALWAYS require manual verification
    MANDATORY_MANUAL_CHECK_PATTERNS = [
        "legislation",
        "legal",
        "law",
        "regulation",
        "act ",
        "section ",
        "clause",
        "court",
        "precedent",
        "statute",
        "compliance",
        "medical",
        "diagnosis",
        "treatment",
        "financial advice",
        "tax",
    ]

    def __init__(self) -> None:
        self._review_queue: list[ManualReviewTask] = []
        self._verification_log: list[VerificationResult] = []

    def verify_response(
        self,
        query: str,
        response: str,
        model_responses: list[dict[str, Any]] | None = None,
        sources: list[SourceCitation] | None = None,
        user_id: str = "",
        session_id: str = "",
    ) -> VerificationResult:
        """
        Run the full verification pipeline on an AI response.

        Steps:
        1. Check if query requires mandatory manual review
        2. Analyse multi-model consensus (if available)
        3. Validate source citations
        4. Calculate confidence score
        5. Determine verification status
        6. Queue for manual review if needed
        7. Log to audit trail
        """
        # Step 1: Check mandatory manual review patterns
        requires_manual = self._check_mandatory_review(query)

        # Step 2: Multi-model consensus
        consensus_score = 0.0
        consensus_details: dict[str, Any] = {}
        models_used: list[str] = []

        if model_responses:
            consensus_score, consensus_details = self._analyse_model_consensus(
                model_responses
            )
            models_used = [r.get("model", "unknown") for r in model_responses]

        # Step 3: Source citation validation
        source_score = 0.0
        validated_sources = sources or []
        if validated_sources:
            source_score = self._validate_sources(validated_sources)

        # Step 4: Calculate composite confidence score
        confidence = self._calculate_confidence(
            consensus_score=consensus_score,
            source_score=source_score,
            has_sources=len(validated_sources) > 0,
            model_count=len(models_used),
        )

        # Step 5: Determine status
        if confidence >= self.HIGH_CONFIDENCE_THRESHOLD and not requires_manual:
            status = VerificationStatus.HIGH_CONFIDENCE
        elif confidence >= self.PARTIAL_CONFIDENCE_THRESHOLD:
            status = VerificationStatus.PARTIALLY_VERIFIED
        elif requires_manual:
            status = VerificationStatus.MANUAL_REVIEW_REQUIRED
        elif confidence <= self.REJECTION_THRESHOLD:
            status = VerificationStatus.REJECTED
        else:
            status = VerificationStatus.UNVERIFIED

        # Override: legal/legislation queries always require check
        if requires_manual and any(
            p in query.lower()
            for p in ["legislation", "law", "act ", "regulation", "statute"]
        ):
            status = VerificationStatus.LEGISLATION_CHECK

        result = VerificationResult(
            query=query,
            response=response,
            confidence_score=confidence,
            status=status,
            sources=validated_sources,
            models_queried=models_used,
            consensus_details=consensus_details,
            user_id=user_id,
            session_id=session_id,
        )

        # Step 6: Queue for manual review if needed
        if status in (
            VerificationStatus.MANUAL_REVIEW_REQUIRED,
            VerificationStatus.LEGISLATION_CHECK,
            VerificationStatus.ELIBRARY_CHECK,
            VerificationStatus.UNVERIFIED,
        ):
            self._queue_for_review(result)

        # Step 7: Log
        self._verification_log.append(result)

        return result

    def format_response_with_verification(
        self, result: VerificationResult
    ) -> str:
        """
        Format an AI response with verification metadata for the user.

        Adds confidence badge, source citations, and verification warnings.
        """
        confidence_badge = self._get_confidence_badge(result.confidence_score)
        lines = [
            result.response,
            "",
            f"--- Verification: {confidence_badge} ---",
            f"Confidence: {result.confidence_score:.0%}",
            f"Status: {result.status.value}",
        ]

        if result.sources:
            lines.append("Sources:")
            for src in result.sources:
                verified_mark = "[verified]" if src.verified else "[unverified]"
                lines.append(
                    f"  {verified_mark} [{src.source_type.value}] "
                    f"{src.title} — {src.reference}"
                )

        if result.status in (
            VerificationStatus.UNVERIFIED,
            VerificationStatus.MANUAL_REVIEW_REQUIRED,
            VerificationStatus.LEGISLATION_CHECK,
        ):
            lines.extend([
                "",
                "WARNING: This response has not been fully verified.",
                "Please check against official sources before relying on this information.",
            ])

        if result.status == VerificationStatus.LEGISLATION_CHECK:
            lines.append(
                "LEGAL NOTE: Please verify against AustLII (www.austlii.edu.au) "
                "or relevant legislation databases."
            )

        if result.status == VerificationStatus.REJECTED:
            lines.extend([
                "",
                "This response was flagged as potentially inaccurate and has been rejected.",
                "Please consult a human expert or search the UniMelb e-library directly.",
            ])

        return "\n".join(lines)

    def get_review_queue(
        self, review_type: str | None = None
    ) -> list[ManualReviewTask]:
        """Get pending manual review tasks."""
        tasks = self._review_queue
        if review_type:
            tasks = [t for t in tasks if t.review_type == review_type]
        return [t for t in tasks if t.completed_at is None]

    def complete_review(
        self,
        task_id: str,
        reviewer: str,
        notes: str,
        final_status: VerificationStatus,
    ) -> ManualReviewTask | None:
        """Complete a manual review task."""
        for task in self._review_queue:
            if task.task_id == task_id:
                task.completed_at = datetime.now()
                task.assigned_to = reviewer
                task.reviewer_notes = notes
                task.final_status = final_status
                return task
        return None

    def get_audit_log(
        self,
        user_id: str | None = None,
        session_id: str | None = None,
        limit: int = 100,
    ) -> list[VerificationResult]:
        """Get verification audit log entries."""
        results = self._verification_log
        if user_id:
            results = [r for r in results if r.user_id == user_id]
        if session_id:
            results = [r for r in results if r.session_id == session_id]
        return results[-limit:]

    def get_accuracy_metrics(self) -> dict[str, Any]:
        """Calculate platform-wide accuracy and verification metrics."""
        total = len(self._verification_log)
        if total == 0:
            return {"total_queries": 0, "message": "No data yet"}

        high_conf = sum(
            1
            for r in self._verification_log
            if r.status == VerificationStatus.HIGH_CONFIDENCE
        )
        partial = sum(
            1
            for r in self._verification_log
            if r.status == VerificationStatus.PARTIALLY_VERIFIED
        )
        unverified = sum(
            1
            for r in self._verification_log
            if r.status == VerificationStatus.UNVERIFIED
        )
        rejected = sum(
            1
            for r in self._verification_log
            if r.status == VerificationStatus.REJECTED
        )
        manual_pending = len(self.get_review_queue())

        avg_confidence = (
            sum(r.confidence_score for r in self._verification_log) / total
        )

        return {
            "total_queries": total,
            "high_confidence_rate": high_conf / total,
            "partial_verification_rate": partial / total,
            "unverified_rate": unverified / total,
            "rejection_rate": rejected / total,
            "average_confidence": avg_confidence,
            "manual_reviews_pending": manual_pending,
            "manual_reviews_completed": len(self._review_queue) - manual_pending,
        }

    # ── Private Methods ──────────────────────────────────────────────

    def _check_mandatory_review(self, query: str) -> bool:
        """Check if query matches patterns requiring mandatory manual review."""
        query_lower = query.lower()
        return any(
            pattern in query_lower
            for pattern in self.MANDATORY_MANUAL_CHECK_PATTERNS
        )

    def _analyse_model_consensus(
        self, responses: list[dict[str, Any]]
    ) -> tuple[float, dict[str, Any]]:
        """Analyse consensus across multiple model responses."""
        if len(responses) < 2:
            return 0.5, {"method": "single_model", "models": len(responses)}

        # Alpha: simple text-based comparison
        # Production: embedding-based semantic similarity
        contents = [r.get("content", "") for r in responses]
        n = len(contents)

        # Pairwise similarity (placeholder for semantic similarity)
        agreement_count = 0
        total_pairs = 0
        for i in range(n):
            for j in range(i + 1, n):
                total_pairs += 1
                # Alpha: check if responses are non-empty and similar length
                if contents[i] and contents[j]:
                    len_ratio = min(len(contents[i]), len(contents[j])) / max(
                        len(contents[i]), len(contents[j])
                    )
                    if len_ratio > 0.5:
                        agreement_count += 1

        score = agreement_count / total_pairs if total_pairs > 0 else 0.0
        return score, {
            "method": "pairwise_comparison",
            "models": n,
            "agreement_pairs": agreement_count,
            "total_pairs": total_pairs,
        }

    def _validate_sources(self, sources: list[SourceCitation]) -> float:
        """Validate source citations and return a source quality score."""
        if not sources:
            return 0.0

        verified_count = sum(1 for s in sources if s.verified)
        high_quality_types = {
            SourceType.ACADEMIC_PAPER,
            SourceType.LEGISLATION,
            SourceType.COURT_CASE,
            SourceType.TEXTBOOK,
        }
        high_quality_count = sum(
            1 for s in sources if s.source_type in high_quality_types
        )

        # Weighted score: verified sources count more
        verified_weight = 0.6
        quality_weight = 0.4

        verified_score = verified_count / len(sources)
        quality_score = high_quality_count / len(sources)

        return verified_weight * verified_score + quality_weight * quality_score

    def _calculate_confidence(
        self,
        consensus_score: float,
        source_score: float,
        has_sources: bool,
        model_count: int,
    ) -> float:
        """Calculate composite confidence score (0.0 → 1.0)."""
        # Weights
        consensus_weight = 0.4
        source_weight = 0.35
        model_diversity_weight = 0.25

        # Model diversity bonus (more models = higher confidence)
        diversity_score = min(model_count / 3.0, 1.0)

        # No sources penalty
        if not has_sources:
            source_score = 0.0
            source_weight = 0.0
            consensus_weight = 0.6
            model_diversity_weight = 0.4

        total_weight = consensus_weight + source_weight + model_diversity_weight
        confidence = (
            consensus_weight * consensus_score
            + source_weight * source_score
            + model_diversity_weight * diversity_score
        ) / total_weight

        return round(min(max(confidence, 0.0), 1.0), 3)

    def _get_confidence_badge(self, score: float) -> str:
        """Return a text badge for the confidence level."""
        if score >= self.HIGH_CONFIDENCE_THRESHOLD:
            return "HIGH CONFIDENCE"
        elif score >= self.PARTIAL_CONFIDENCE_THRESHOLD:
            return "PARTIALLY VERIFIED"
        elif score > self.REJECTION_THRESHOLD:
            return "UNVERIFIED — MANUAL CHECK RECOMMENDED"
        else:
            return "REJECTED — DO NOT RELY ON THIS RESPONSE"

    def _queue_for_review(self, result: VerificationResult) -> None:
        """Add a verification result to the manual review queue."""
        review_type = "general"
        if result.status == VerificationStatus.LEGISLATION_CHECK:
            review_type = "legislation"
        elif result.status == VerificationStatus.ELIBRARY_CHECK:
            review_type = "elibrary"

        task = ManualReviewTask(
            task_id=f"MR-{len(self._review_queue) + 1:06d}",
            verification_result=result,
            review_type=review_type,
            priority="high" if review_type == "legislation" else "medium",
        )
        self._review_queue.append(task)

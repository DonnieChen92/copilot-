"""
Hallucination Check Filter / 幻覺檢查過濾器 / 幻觉检查过滤器
=============================================================
Validates LLM responses against source material to detect
and flag potential hallucinations. Provides claim-level
verification, confidence scoring, and self-consistency checks.

驗證 LLM 回應與源材料的一致性，
檢測並標記潛在的幻覺。提供聲明級別
驗證、信心評分和自我一致性檢查。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Enums & Constants
# ---------------------------------------------------------------------------

class VerificationStatus(str, Enum):
    """Status of a single claim verification."""
    SUPPORTED = "supported"            # Claim found in source
    PARTIALLY_SUPPORTED = "partial"    # Partial match in source
    UNSUPPORTED = "unsupported"        # Not found in source
    CONTRADICTED = "contradicted"      # Contradicts source
    UNVERIFIABLE = "unverifiable"      # Cannot determine


class SeverityLevel(str, Enum):
    """Severity of a hallucination finding."""
    CRITICAL = "critical"     # Fabricated facts, wrong numbers
    WARNING = "warning"       # Unsupported inferences
    INFO = "info"             # Minor embellishments


class FilterType(str, Enum):
    """Types of hallucination check filters."""
    SOURCE_GROUNDING = "source_grounding"
    CLAIM_EXTRACTION = "claim_extraction"
    SELF_CONSISTENCY = "self_consistency"
    CITATION_VERIFY = "citation_verify"
    CONFIDENCE_CALIBRATION = "confidence_calibration"
    CODE_API_VERIFY = "code_api_verify"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ClaimVerification:
    """
    Verification result for a single extracted claim.
    單個提取聲明的驗證結果。
    """
    claim_text: str
    status: VerificationStatus
    severity: SeverityLevel
    evidence: str = ""            # Supporting or contradicting evidence
    source_reference: str = ""    # Where in the source this was found
    confidence: float = 0.0       # 0.0 - 1.0
    notes: str = ""

    def is_problematic(self) -> bool:
        return self.status in (
            VerificationStatus.UNSUPPORTED,
            VerificationStatus.CONTRADICTED,
        )


@dataclass
class CheckResult:
    """
    Complete result of running hallucination checks on a response.
    對回應執行幻覺檢查的完整結果。
    """
    passed: bool
    overall_score: float                    # 0.0 (all hallucinated) - 1.0 (fully grounded)
    claims: list[ClaimVerification] = field(default_factory=list)
    filters_applied: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def supported_count(self) -> int:
        return sum(
            1 for c in self.claims
            if c.status == VerificationStatus.SUPPORTED
        )

    @property
    def unsupported_count(self) -> int:
        return sum(
            1 for c in self.claims
            if c.status == VerificationStatus.UNSUPPORTED
        )

    @property
    def contradicted_count(self) -> int:
        return sum(
            1 for c in self.claims
            if c.status == VerificationStatus.CONTRADICTED
        )

    @property
    def critical_issues(self) -> list[ClaimVerification]:
        return [
            c for c in self.claims
            if c.severity == SeverityLevel.CRITICAL and c.is_problematic()
        ]

    def summary(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "overall_score": round(self.overall_score, 3),
            "total_claims": len(self.claims),
            "supported": self.supported_count,
            "unsupported": self.unsupported_count,
            "contradicted": self.contradicted_count,
            "critical_issues": len(self.critical_issues),
            "filters_applied": self.filters_applied,
        }


# ---------------------------------------------------------------------------
# Filter implementations
# ---------------------------------------------------------------------------

class _SourceGroundingFilter:
    """
    Check whether response claims are grounded in source material.
    檢查回應聲明是否以源材料為基礎。
    """

    @staticmethod
    def extract_claims(response_text: str) -> list[str]:
        """
        Split response into individual claims (sentence-level).
        將回應拆分為單個聲明（句子級別）。
        """
        sentences = re.split(r'(?<=[.!?。！？])\s+', response_text.strip())
        claims = []
        for s in sentences:
            s = s.strip()
            if len(s) > 10 and not s.startswith(("#", "-", "- [", "```")):
                claims.append(s)
        return claims

    @staticmethod
    def check_claim_against_source(
        claim: str,
        source: str,
        *,
        overlap_threshold: float = 0.3,
    ) -> ClaimVerification:
        """
        Verify a single claim against the source via keyword overlap.
        透過關鍵字重疊驗證單個聲明與源材料。
        """
        claim_words = set(_normalize_words(claim))
        source_words = set(_normalize_words(source))

        if not claim_words:
            return ClaimVerification(
                claim_text=claim,
                status=VerificationStatus.UNVERIFIABLE,
                severity=SeverityLevel.INFO,
                confidence=0.0,
                notes="Claim too short to verify.",
            )

        overlap = claim_words & source_words
        overlap_ratio = len(overlap) / len(claim_words) if claim_words else 0.0

        if overlap_ratio >= 0.6:
            status = VerificationStatus.SUPPORTED
            severity = SeverityLevel.INFO
        elif overlap_ratio >= overlap_threshold:
            status = VerificationStatus.PARTIALLY_SUPPORTED
            severity = SeverityLevel.INFO
        else:
            status = VerificationStatus.UNSUPPORTED
            severity = SeverityLevel.WARNING

        return ClaimVerification(
            claim_text=claim,
            status=status,
            severity=severity,
            evidence=f"Keyword overlap: {len(overlap)}/{len(claim_words)}",
            confidence=round(overlap_ratio, 3),
        )

    def run(self, response: str, source: str) -> list[ClaimVerification]:
        claims = self.extract_claims(response)
        return [
            self.check_claim_against_source(c, source)
            for c in claims
        ]


class _CitationVerifyFilter:
    """
    Verify that citations / quotes in the response actually appear in the source.
    驗證回應中的引用/引述是否實際出現在源材料中。
    """

    QUOTE_PATTERNS = [
        re.compile(r'"([^"]{10,})"'),           # Double-quoted
        re.compile(r"'([^']{10,})'"),            # Single-quoted
        re.compile(r"「([^」]{5,})」"),           # CJK quotes
        re.compile(r"『([^』]{5,})』"),           # CJK double quotes
        re.compile(r'> (.+)', re.MULTILINE),     # Blockquote
    ]

    def extract_citations(self, text: str) -> list[str]:
        citations: list[str] = []
        for pattern in self.QUOTE_PATTERNS:
            citations.extend(pattern.findall(text))
        return citations

    def run(self, response: str, source: str) -> list[ClaimVerification]:
        citations = self.extract_citations(response)
        results: list[ClaimVerification] = []

        source_lower = source.lower()

        for cite in citations:
            cite_lower = cite.lower().strip()
            if cite_lower in source_lower:
                results.append(ClaimVerification(
                    claim_text=f'Citation: "{cite}"',
                    status=VerificationStatus.SUPPORTED,
                    severity=SeverityLevel.INFO,
                    evidence="Exact match found in source.",
                    confidence=1.0,
                ))
            else:
                # Check partial match (fuzzy)
                cite_words = set(_normalize_words(cite))
                source_words_set = set(_normalize_words(source))
                overlap = cite_words & source_words_set
                ratio = len(overlap) / len(cite_words) if cite_words else 0
                if ratio >= 0.7:
                    results.append(ClaimVerification(
                        claim_text=f'Citation: "{cite}"',
                        status=VerificationStatus.PARTIALLY_SUPPORTED,
                        severity=SeverityLevel.WARNING,
                        evidence=f"Partial match ({ratio:.0%} word overlap).",
                        confidence=round(ratio, 3),
                    ))
                else:
                    results.append(ClaimVerification(
                        claim_text=f'Citation: "{cite}"',
                        status=VerificationStatus.UNSUPPORTED,
                        severity=SeverityLevel.CRITICAL,
                        evidence="Citation not found in source material.",
                        confidence=0.0,
                        notes="Potentially fabricated quote.",
                    ))

        return results


class _ConfidenceCalibrationFilter:
    """
    Check whether the model's stated confidence matches evidence quality.
    檢查模型聲明的信心是否與證據品質匹配。
    """

    CONFIDENCE_PATTERNS = [
        re.compile(r'\bconfidence\s*[:=]\s*(HIGH|MEDIUM|LOW)', re.IGNORECASE),
        re.compile(r'\b(HIGH|MEDIUM|LOW)\s+confidence\b', re.IGNORECASE),
        re.compile(r'信心\s*[:：]\s*(高|中|低)'),
    ]

    LEVEL_MAP = {
        "high": 0.85, "medium": 0.55, "low": 0.25,
        "高": 0.85, "中": 0.55, "低": 0.25,
    }

    def extract_stated_confidence(self, text: str) -> float | None:
        for pattern in self.CONFIDENCE_PATTERNS:
            match = pattern.search(text)
            if match:
                level = match.group(1).lower()
                return self.LEVEL_MAP.get(level)
        return None

    def run(
        self,
        response: str,
        grounding_score: float,
    ) -> list[ClaimVerification]:
        stated = self.extract_stated_confidence(response)
        if stated is None:
            return [ClaimVerification(
                claim_text="(Confidence not stated)",
                status=VerificationStatus.UNVERIFIABLE,
                severity=SeverityLevel.INFO,
                confidence=0.0,
                notes="Model did not provide an explicit confidence level.",
            )]

        delta = abs(stated - grounding_score)
        if delta <= 0.2:
            return [ClaimVerification(
                claim_text=f"Stated confidence ≈ {stated:.0%}",
                status=VerificationStatus.SUPPORTED,
                severity=SeverityLevel.INFO,
                evidence=f"Grounding score {grounding_score:.0%} matches stated confidence.",
                confidence=1.0 - delta,
            )]
        else:
            overconfident = stated > grounding_score
            return [ClaimVerification(
                claim_text=f"Stated confidence ≈ {stated:.0%}",
                status=VerificationStatus.CONTRADICTED if overconfident else VerificationStatus.PARTIALLY_SUPPORTED,
                severity=SeverityLevel.WARNING if overconfident else SeverityLevel.INFO,
                evidence=(
                    f"Grounding score {grounding_score:.0%} "
                    f"{'< stated' if overconfident else '> stated'} confidence."
                ),
                confidence=1.0 - delta,
                notes="Overconfident response." if overconfident else "Underconfident response.",
            )]


class _CodeAPIVerifyFilter:
    """
    Detect potentially hallucinated API calls, imports, or URLs in code responses.
    檢測代碼回應中可能的幻覺 API 調用、導入或 URL。
    """

    SUSPICIOUS_PATTERNS = [
        re.compile(r'from\s+([\w.]+)\s+import'),
        re.compile(r'import\s+([\w.]+)'),
        re.compile(r'https?://[^\s"\'<>]+'),
        re.compile(r'pip install\s+([\w\-]+)'),
    ]

    def __init__(self, known_libraries: list[str] | None = None):
        self.known_libraries = set(
            lib.lower().replace("-", "_")
            for lib in (known_libraries or [])
        )

    def run(
        self,
        response: str,
        api_reference: str = "",
    ) -> list[ClaimVerification]:
        results: list[ClaimVerification] = []
        for pattern in self.SUSPICIOUS_PATTERNS:
            for match in pattern.finditer(response):
                full_match = match.group(0)
                captured = match.group(1) if match.lastindex else full_match
                normalized = captured.lower().split(".")[0].replace("-", "_")

                if self.known_libraries and normalized not in self.known_libraries:
                    # Unknown library — flag it
                    in_api_ref = captured.lower() in api_reference.lower()
                    if in_api_ref:
                        results.append(ClaimVerification(
                            claim_text=f"Import/reference: {full_match}",
                            status=VerificationStatus.SUPPORTED,
                            severity=SeverityLevel.INFO,
                            evidence="Found in API reference.",
                            confidence=0.9,
                        ))
                    else:
                        results.append(ClaimVerification(
                            claim_text=f"Import/reference: {full_match}",
                            status=VerificationStatus.UNVERIFIABLE,
                            severity=SeverityLevel.WARNING,
                            evidence="Not in known libraries or API reference.",
                            confidence=0.3,
                            notes="Verify this import/URL exists before using.",
                        ))

        return results


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

class HallucinationCheckFilter:
    """
    Orchestrates multiple hallucination check filters on an LLM response.
    對 LLM 回應編排多個幻覺檢查過濾器。

    Usage:
        checker = HallucinationCheckFilter()
        result = checker.check(
            response="The Eiffel Tower was built in 1889...",
            source="The Eiffel Tower was completed in 1889 for the World's Fair...",
        )
        print(result.summary())
    """

    def __init__(
        self,
        *,
        pass_threshold: float = 0.6,
        known_libraries: list[str] | None = None,
    ):
        self.pass_threshold = pass_threshold
        self._grounding = _SourceGroundingFilter()
        self._citation = _CitationVerifyFilter()
        self._confidence = _ConfidenceCalibrationFilter()
        self._code_api = _CodeAPIVerifyFilter(known_libraries=known_libraries)

    def check(
        self,
        response: str,
        source: str = "",
        *,
        api_reference: str = "",
        enabled_filters: list[FilterType] | None = None,
    ) -> CheckResult:
        """
        Run hallucination checks on an LLM response.
        對 LLM 回應執行幻覺檢查。

        Args:
            response: The LLM-generated text to verify.
            source: Original source/context used for grounding.
            api_reference: API docs for code verification.
            enabled_filters: Subset of filters to run (None = all applicable).

        Returns:
            CheckResult with all findings.
        """
        filters = enabled_filters or list(FilterType)
        all_claims: list[ClaimVerification] = []
        applied: list[str] = []
        warnings: list[str] = []

        # 1. Source grounding
        if FilterType.SOURCE_GROUNDING in filters and source:
            grounding_claims = self._grounding.run(response, source)
            all_claims.extend(grounding_claims)
            applied.append(FilterType.SOURCE_GROUNDING.value)

        # 2. Citation verification
        if FilterType.CITATION_VERIFY in filters and source:
            citation_claims = self._citation.run(response, source)
            all_claims.extend(citation_claims)
            applied.append(FilterType.CITATION_VERIFY.value)

        # 3. Code API verification
        if FilterType.CODE_API_VERIFY in filters:
            code_claims = self._code_api.run(response, api_reference)
            all_claims.extend(code_claims)
            applied.append(FilterType.CODE_API_VERIFY.value)

        # Compute overall grounding score
        if all_claims:
            grounding_score = sum(c.confidence for c in all_claims) / len(all_claims)
        else:
            grounding_score = 1.0  # No claims = nothing to verify
            warnings.append("No verifiable claims were extracted.")

        # 4. Confidence calibration
        if FilterType.CONFIDENCE_CALIBRATION in filters:
            conf_claims = self._confidence.run(response, grounding_score)
            all_claims.extend(conf_claims)
            applied.append(FilterType.CONFIDENCE_CALIBRATION.value)

        # Determine pass/fail
        passed = grounding_score >= self.pass_threshold
        critical = [c for c in all_claims if c.severity == SeverityLevel.CRITICAL and c.is_problematic()]
        if critical:
            passed = False
            warnings.append(
                f"{len(critical)} critical hallucination(s) detected."
            )

        return CheckResult(
            passed=passed,
            overall_score=grounding_score,
            claims=all_claims,
            filters_applied=applied,
            warnings=warnings,
            metadata={
                "pass_threshold": self.pass_threshold,
                "response_length": len(response),
                "source_length": len(source),
            },
        )

    def check_self_consistency(
        self,
        responses: list[str],
        source: str = "",
    ) -> CheckResult:
        """
        Compare multiple LLM responses to the same query for consistency.
        比較同一查詢的多個 LLM 回應的一致性。

        If the model gives different answers to the same question,
        the inconsistent claims are likely hallucinated.
        """
        if len(responses) < 2:
            return CheckResult(
                passed=True,
                overall_score=1.0,
                warnings=["Self-consistency requires at least 2 responses."],
                filters_applied=[FilterType.SELF_CONSISTENCY.value],
            )

        # Extract claims from all responses
        all_claim_sets = [
            set(self._grounding.extract_claims(r)) for r in responses
        ]

        # Find claims present in all responses (consensus)
        consensus = all_claim_sets[0]
        for cs in all_claim_sets[1:]:
            consensus = consensus & cs

        # Find claims unique to single responses (potential hallucinations)
        unique_claims: list[ClaimVerification] = []
        for i, cs in enumerate(all_claim_sets):
            unique = cs - consensus
            for claim in unique:
                unique_claims.append(ClaimVerification(
                    claim_text=claim,
                    status=VerificationStatus.UNSUPPORTED,
                    severity=SeverityLevel.WARNING,
                    evidence=f"Only appears in response #{i + 1}, not in consensus.",
                    confidence=0.3,
                    notes="Inconsistent across multiple responses.",
                ))

        # Also check consensus claims against source if available
        consensus_verified: list[ClaimVerification] = []
        if source:
            for claim in consensus:
                cv = self._grounding.check_claim_against_source(claim, source)
                consensus_verified.append(cv)

        all_verifications = consensus_verified + unique_claims
        total = len(all_verifications) if all_verifications else 1
        score = sum(c.confidence for c in all_verifications) / total

        return CheckResult(
            passed=score >= self.pass_threshold,
            overall_score=score,
            claims=all_verifications,
            filters_applied=[FilterType.SELF_CONSISTENCY.value],
            metadata={
                "num_responses": len(responses),
                "consensus_claims": len(consensus),
                "unique_claims": len(unique_claims),
            },
        )


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

_STOP_WORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "out", "off", "over",
    "under", "again", "further", "then", "once", "and", "but", "or", "nor",
    "not", "so", "if", "than", "that", "this", "these", "those", "it",
    "its", "i", "me", "my", "we", "our", "you", "your", "he", "his",
    "she", "her", "they", "their", "which", "what", "who", "whom",
    "的", "是", "在", "了", "和", "與", "也", "都", "就", "而",
})


def _normalize_words(text: str) -> list[str]:
    """Lowercase, strip punctuation, remove stop words."""
    words = re.findall(r'\b\w{2,}\b', text.lower())
    return [w for w in words if w not in _STOP_WORDS]

"""
Filter Screen / 過濾篩選畫面 / 过滤筛选画面
=============================================
Renders hallucination check results into human-readable reports
and structured screen output. Provides pass/fail indicators,
severity coloring, and exportable report formats.

將幻覺檢查結果渲染為人類可讀的報告和結構化畫面輸出。
提供通過/失敗指標、嚴重性著色和可匯出的報告格式。

Screen Display Flow / 畫面顯示流程:
┌──────────────────────────────────────────────┐
│  Anti-Hallucination Check Report             │
│  ════════════════════════════════             │
│  Overall: ✅ PASS (0.85)  |  Template: ...   │
│  Model: gpt-4o  |  Attempt: 1               │
│                                              │
│  ┌─ Claims ─────────────────────────────┐    │
│  │ ✅ Claim 1: supported (0.92)         │    │
│  │ ⚠️  Claim 2: partial (0.45)          │    │
│  │ ❌ Claim 3: unsupported (0.10)       │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  Filters Applied: source_grounding, ...      │
│  Warnings: 1 critical hallucination detected │
└──────────────────────────────────────────────┘
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .check_filter import (
    CheckResult,
    ClaimVerification,
    SeverityLevel,
    VerificationStatus,
)
from .codex_query_builder import QueryResult


# ---------------------------------------------------------------------------
# Report data class
# ---------------------------------------------------------------------------

@dataclass
class ScreenReport:
    """
    Structured report from a filter screen rendering.
    來自過濾篩選畫面渲染的結構化報告。
    """
    title: str
    timestamp: str
    text_output: str
    structured_data: dict[str, Any] = field(default_factory=dict)
    claims_detail: list[dict[str, Any]] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(
            {
                "title": self.title,
                "timestamp": self.timestamp,
                "structured_data": self.structured_data,
                "claims_detail": self.claims_detail,
            },
            indent=2,
            ensure_ascii=False,
        )

    def to_markdown(self) -> str:
        return self.text_output


# ---------------------------------------------------------------------------
# Status icons and formatting
# ---------------------------------------------------------------------------

_STATUS_ICONS = {
    VerificationStatus.SUPPORTED: "[PASS]",
    VerificationStatus.PARTIALLY_SUPPORTED: "[PARTIAL]",
    VerificationStatus.UNSUPPORTED: "[FAIL]",
    VerificationStatus.CONTRADICTED: "[CONTRADICTION]",
    VerificationStatus.UNVERIFIABLE: "[UNKNOWN]",
}

_SEVERITY_TAGS = {
    SeverityLevel.CRITICAL: "CRITICAL",
    SeverityLevel.WARNING: "WARNING",
    SeverityLevel.INFO: "INFO",
}


def _format_score_bar(score: float, width: int = 20) -> str:
    """Render a simple ASCII progress bar for a score 0.0–1.0."""
    filled = int(score * width)
    empty = width - filled
    bar = "#" * filled + "-" * empty
    return f"[{bar}] {score:.1%}"


def _truncate(text: str, max_len: int = 80) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


# ---------------------------------------------------------------------------
# Filter Screen
# ---------------------------------------------------------------------------

class FilterScreen:
    """
    Renders check results into formatted screen output and reports.
    將檢查結果渲染為格式化的畫面輸出和報告。

    Usage:
        screen = FilterScreen()

        # From a QueryResult (full cycle)
        report = screen.render_query_result(query_result)
        print(report.text_output)

        # From a CheckResult only
        report = screen.render_check_result(check_result)
        print(report.to_markdown())
    """

    SEPARATOR = "=" * 60
    THIN_SEP = "-" * 60

    def render_query_result(self, result: QueryResult) -> ScreenReport:
        """
        Render a full QueryResult (template + response + checks).
        渲染完整的 QueryResult（模板 + 回應 + 檢查）。
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines: list[str] = []

        # Header
        lines.append(self.SEPARATOR)
        lines.append("  ANTI-HALLUCINATION CHECK REPORT")
        lines.append("  反幻覺檢查報告 / 反幻觉检查报告")
        lines.append(self.SEPARATOR)
        lines.append("")

        # Overview
        pass_label = "PASS" if result.passed else "FAIL"
        lines.append(f"  Result:   {pass_label}")
        lines.append(f"  Score:    {_format_score_bar(result.score)}")
        lines.append(f"  Template: {result.template_name}")
        lines.append(f"  Model:    {result.model_used}")
        lines.append(f"  Attempt:  {result.attempt}")
        lines.append(f"  Latency:  {result.total_latency_ms} ms")
        if result.retried:
            lines.append("  Retried:  Yes")
        lines.append("")

        # Response preview
        lines.append(self.THIN_SEP)
        lines.append("  RESPONSE PREVIEW / 回應預覽")
        lines.append(self.THIN_SEP)
        preview = result.response_text[:500]
        for line in preview.split("\n"):
            lines.append(f"  | {line}")
        if len(result.response_text) > 500:
            lines.append(f"  | ... ({len(result.response_text)} chars total)")
        lines.append("")

        # Check details
        check_lines = self._render_check_details(result.check_result)
        lines.extend(check_lines)

        # Token usage
        if result.metadata.get("input_tokens"):
            lines.append(self.THIN_SEP)
            lines.append("  TOKEN USAGE / 令牌使用")
            lines.append(self.THIN_SEP)
            lines.append(f"  Input:  {result.metadata['input_tokens']}")
            lines.append(f"  Output: {result.metadata.get('output_tokens', 0)}")
            lines.append("")

        lines.append(self.SEPARATOR)
        lines.append(f"  Generated: {ts}")
        lines.append(self.SEPARATOR)

        text_output = "\n".join(lines)

        return ScreenReport(
            title=f"Anti-Hallucination Report: {result.template_name}",
            timestamp=ts,
            text_output=text_output,
            structured_data={
                "passed": result.passed,
                "score": result.score,
                "template": result.template_name,
                "model": result.model_used,
                "attempt": result.attempt,
                "latency_ms": result.total_latency_ms,
                **result.check_result.summary(),
            },
            claims_detail=self._claims_to_dicts(result.check_result.claims),
        )

    def render_check_result(
        self,
        check_result: CheckResult,
        *,
        title: str = "Hallucination Check",
    ) -> ScreenReport:
        """
        Render a standalone CheckResult.
        渲染獨立的 CheckResult。
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines: list[str] = []

        lines.append(self.SEPARATOR)
        lines.append(f"  {title.upper()}")
        lines.append(self.SEPARATOR)
        lines.append("")

        pass_label = "PASS" if check_result.passed else "FAIL"
        lines.append(f"  Result: {pass_label}")
        lines.append(f"  Score:  {_format_score_bar(check_result.overall_score)}")
        lines.append("")

        lines.extend(self._render_check_details(check_result))

        lines.append(self.SEPARATOR)
        lines.append(f"  Generated: {ts}")
        lines.append(self.SEPARATOR)

        text_output = "\n".join(lines)

        return ScreenReport(
            title=title,
            timestamp=ts,
            text_output=text_output,
            structured_data=check_result.summary(),
            claims_detail=self._claims_to_dicts(check_result.claims),
        )

    def render_comparison(
        self,
        results: list[QueryResult],
    ) -> ScreenReport:
        """
        Compare multiple query results side by side.
        並排比較多個查詢結果。
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines: list[str] = []

        lines.append(self.SEPARATOR)
        lines.append("  MULTI-RESPONSE COMPARISON / 多回應比較")
        lines.append(self.SEPARATOR)
        lines.append("")

        # Header row
        header = "  {:>3} | {:>6} | {:>8} | {:>7} | {:>10} | {}"
        lines.append(header.format(
            "#", "Pass?", "Score", "Claims", "Model", "Template"
        ))
        lines.append("  " + "-" * 56)

        for i, r in enumerate(results, 1):
            label = "PASS" if r.passed else "FAIL"
            lines.append(header.format(
                i,
                label,
                f"{r.score:.3f}",
                len(r.check_result.claims),
                r.model_used[:10],
                r.template_name[:20],
            ))

        lines.append("")

        # Best result
        if results:
            best = max(results, key=lambda r: r.score)
            lines.append(f"  Best: #{results.index(best) + 1} "
                         f"(score={best.score:.3f}, model={best.model_used})")
        lines.append("")
        lines.append(self.SEPARATOR)

        return ScreenReport(
            title="Multi-Response Comparison",
            timestamp=ts,
            text_output="\n".join(lines),
            structured_data={
                "count": len(results),
                "results": [
                    {"score": r.score, "passed": r.passed, "model": r.model_used}
                    for r in results
                ],
            },
        )

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------

    def _render_check_details(self, check: CheckResult) -> list[str]:
        """Render the claims and filters section."""
        lines: list[str] = []

        # Filters applied
        lines.append(self.THIN_SEP)
        lines.append("  FILTERS APPLIED / 已套用過濾器")
        lines.append(self.THIN_SEP)
        if check.filters_applied:
            for f in check.filters_applied:
                lines.append(f"  - {f}")
        else:
            lines.append("  (none)")
        lines.append("")

        # Claim-level results
        if check.claims:
            lines.append(self.THIN_SEP)
            lines.append(
                f"  CLAIMS ({len(check.claims)}) / "
                f"聲明驗證 ({len(check.claims)})"
            )
            lines.append(self.THIN_SEP)

            for i, claim in enumerate(check.claims, 1):
                icon = _STATUS_ICONS.get(claim.status, "[?]")
                tag = _SEVERITY_TAGS.get(claim.severity, "INFO")
                text = _truncate(claim.claim_text, 60)
                lines.append(
                    f"  {i:>3}. {icon} [{tag}] {text}"
                )
                lines.append(
                    f"       Confidence: {claim.confidence:.3f}"
                )
                if claim.evidence:
                    lines.append(
                        f"       Evidence: {_truncate(claim.evidence, 70)}"
                    )
                if claim.notes:
                    lines.append(
                        f"       Note: {claim.notes}"
                    )
                lines.append("")

        # Warnings
        if check.warnings:
            lines.append(self.THIN_SEP)
            lines.append("  WARNINGS / 警告")
            lines.append(self.THIN_SEP)
            for w in check.warnings:
                lines.append(f"  >> {w}")
            lines.append("")

        # Summary stats
        lines.append(self.THIN_SEP)
        lines.append("  SUMMARY / 摘要")
        lines.append(self.THIN_SEP)
        s = check.summary()
        lines.append(f"  Total claims:     {s['total_claims']}")
        lines.append(f"  Supported:        {s['supported']}")
        lines.append(f"  Unsupported:      {s['unsupported']}")
        lines.append(f"  Contradicted:     {s['contradicted']}")
        lines.append(f"  Critical issues:  {s['critical_issues']}")
        lines.append("")

        return lines

    @staticmethod
    def _claims_to_dicts(claims: list[ClaimVerification]) -> list[dict[str, Any]]:
        """Convert claims to serializable dicts."""
        return [
            {
                "claim_text": c.claim_text,
                "status": c.status.value,
                "severity": c.severity.value,
                "evidence": c.evidence,
                "source_reference": c.source_reference,
                "confidence": c.confidence,
                "notes": c.notes,
            }
            for c in claims
        ]

"""
SACA · 实现智能（受控智能 v0.1）
================================
目标：实现“可运行的智能”，但严格受控：
- 无自治、无自利、无自我进化
- 所有输出必须经过：Policy → STC → Verification → Audit
- 高风险/异常/冲突：自动降级 + 强制人类仲裁标记

用法
----
1) 将本文件保存为：SACA_Dossier/py/saca_runtime.py
2) 确保已存在：
   - SACA_Dossier/policies/v18_v21_policy.yaml 或 v18_v21_policy.json
   - SACA_Dossier/audit/ 目录
3) 运行（最小 CLI）：
   python SACA_Dossier/py/saca_runtime.py

说明
----
这是“受控智能”最小闭环实现：
- SimpleRAG（本地轻量检索）
- PolicyEngine（YAML/JSON）
- STC 评分
- Verifier（证据门）
- AuditLog（不可变链式哈希）
- GEMs（可选：高风险才触发）

后续可以替换：
- RAG → FAISS/Milvus
- Draft generator → LLM Router（GPT/Gemini/Claude）
- Verifier → CoVe 多步验证
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json
import math
import re
from collections import Counter

# Optional YAML support
try:
    import yaml  # type: ignore
except Exception:
    yaml = None


# =============================================================================
# Paths (aligned with SACA_Dossier structure)
# =============================================================================
ROOT = Path(__file__).resolve().parents[1]          # .../SACA_Dossier
PY_DIR = ROOT / "py"
POLICY_DIR = ROOT / "policies"
AUDIT_DIR = ROOT / "audit"
AUDIT_LOG_PATH = AUDIT_DIR / "audit.log.jsonl"

POLICY_YAML = POLICY_DIR / "v18_v21_policy.yaml"
POLICY_JSON = POLICY_DIR / "v18_v21_policy.json"


# =============================================================================
# Invariants (from V0/V7)
# =============================================================================
FACT_MIN = 0.99
STC_TARGET_MAX = 0.10


# =============================================================================
# Audit (hash-chained)
# =============================================================================
@dataclass
class AuditEvent:
    ts_utc: str
    event: str
    payload: Dict[str, Any]
    prev_hash: str
    hash: str


class AuditLog:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.prev_hash = "GENESIS"

        # If file exists, restore last hash for continuity
        if self.path.exists():
            try:
                last = None
                for line in self.path.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        last = json.loads(line)
                if last and "hash" in last:
                    self.prev_hash = last["hash"]
            except Exception:
                # fall back to GENESIS if corrupted
                self.prev_hash = "GENESIS"

    @staticmethod
    def _sha256(obj: Dict[str, Any]) -> str:
        raw = json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def emit(self, event: str, payload: Dict[str, Any]) -> AuditEvent:
        ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        base = {"ts_utc": ts, "event": event, "payload": payload, "prev_hash": self.prev_hash}
        h = self._sha256(base)
        ae = AuditEvent(ts_utc=ts, event=event, payload=payload, prev_hash=self.prev_hash, hash=h)
        self.prev_hash = h
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(ae), ensure_ascii=False) + "\n")
        return ae


# =============================================================================
# SimpleRAG (local lightweight retrieval; replace later)
# =============================================================================
def _tok(s: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9_\u4e00-\u9fff]+", s.lower())


def _cos(a: Counter, b: Counter) -> float:
    dot = sum(a[t] * b.get(t, 0) for t in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str
    meta: Dict[str, Any]


class SimpleRAG:
    def __init__(self):
        self.chunks: List[Chunk] = []
        self.vecs: List[Counter] = []

    def add(self, chunk: Chunk) -> None:
        self.chunks.append(chunk)
        self.vecs.append(Counter(_tok(chunk.text)))

    def query(self, q: str, k: int = 5) -> List[Tuple[Chunk, float]]:
        qv = Counter(_tok(q))
        scored = [(c, _cos(qv, v)) for c, v in zip(self.chunks, self.vecs)]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]


# =============================================================================
# Policy Engine (YAML/JSON)
# =============================================================================
@dataclass
class PolicyDecision:
    action: str                 # allow|degrade|deny|halt
    hits: List[str]
    require: List[str]
    restrict: List[str]
    reasons: List[str]
    set_flags: Dict[str, Any]


def _get(doc: Dict[str, Any], path: str, default=None):
    cur = doc
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def _match_clause(ctx: Dict[str, Any], clause: Dict[str, Any]) -> bool:
    # Minimal matcher aligned with the policy pack fields used below
    for k, v in clause.items():
        if k.endswith("_in"):
            field = k[:-3]
            if ctx.get(field) not in v:
                return False
        elif k.endswith("_gte"):
            field = k[:-4]
            if float(ctx.get(field, 0)) < float(v):
                return False
        elif k.endswith("_lte"):
            field = k[:-4]
            if float(ctx.get(field, 0)) > float(v):
                return False
        elif k == "hhms":
            status_in = v.get("status_in")
            if status_in is not None:
                if _get(ctx, "hhms.status") not in status_in:
                    return False
        elif k == "detected":
            for dk, dv in v.items():
                if _get(ctx, f"detected.{dk}") != dv:
                    return False
        else:
            if ctx.get(k) != v:
                return False
    return True


def _match_when(ctx: Dict[str, Any], when: Dict[str, Any]) -> bool:
    if not when:
        return False
    if "all" in when:
        return all(_match_when(ctx, w) if isinstance(w, dict) and ("all" in w or "any" in w) else _match_clause(ctx, w)
                   for w in when["all"])
    if "any" in when:
        return any(_match_when(ctx, w) if isinstance(w, dict) and ("all" in w or "any" in w) else _match_clause(ctx, w)
                   for w in when["any"])
    # otherwise treat as clause
    return _match_clause(ctx, when)


class PolicyEngine:
    def __init__(self, policy_doc: Dict[str, Any]):
        self.doc = policy_doc
        self.precedence = {"allow": 0, "degrade": 1, "deny": 2, "halt": 3}

    @classmethod
    def load(cls) -> "PolicyEngine":
        if POLICY_JSON.exists():
            doc = json.loads(POLICY_JSON.read_text(encoding="utf-8"))
            return cls(doc)
        if POLICY_YAML.exists():
            if yaml is None:
                raise RuntimeError("PyYAML not installed but policy YAML present. Install pyyaml or provide JSON.")
            doc = yaml.safe_load(POLICY_YAML.read_text(encoding="utf-8"))
            return cls(doc)
        raise RuntimeError("No policy file found (v18_v21_policy.yaml/json).")

    def eval(self, ctx: Dict[str, Any]) -> PolicyDecision:
        hits: List[str] = []
        require: List[str] = []
        restrict: List[str] = []
        reasons: List[str] = []
        set_flags: Dict[str, Any] = {}

        defaults = self.doc.get("defaults", {"action": "allow", "require": ["audit_log"]})
        final_action = defaults.get("action", "allow")
        require.extend(defaults.get("require", []))

        # Hard denies (if present)
        for hd in self.doc.get("hard_denies", []):
            if _match_when(ctx, hd.get("when", {})):
                return PolicyDecision(
                    action="deny",
                    hits=[hd.get("id", "HARD_DENY")],
                    require=hd.get("decision", {}).get("require", []),
                    restrict=[],
                    reasons=[hd.get("decision", {}).get("reason", "Hard deny.")],
                    set_flags={}
                )

        # Normal policies
        policies = self.doc.get("policies", [])
        # Respect priority if present (higher first)
        policies = sorted(policies, key=lambda p: int(p.get("priority", 0)), reverse=True)

        for pol in policies:
            if _match_when(ctx, pol.get("when", {})):
                hits.append(pol.get("id", "POLICY"))
                dec = pol.get("decision", {})
                action = dec.get("action", "allow")
                if self.precedence[action] > self.precedence[final_action]:
                    final_action = action
                require.extend(dec.get("require", []))
                restrict.extend(dec.get("restrict", []))
                reasons.append(dec.get("reason", ""))
                set_flags.update(dec.get("set_flags", {}))

        # de-dup
        require = sorted(set([r for r in require if r]))
        restrict = sorted(set([r for r in restrict if r]))
        reasons = [r for r in reasons if r] or (["No policy hit."] if not hits else ["Policy matched."])
        return PolicyDecision(final_action, hits, require, restrict, reasons, set_flags)


# =============================================================================
# STC (transparent)
# =============================================================================
@dataclass
class STCResult:
    score: float
    band: str    # GREEN/AMBER/RED
    action: str  # AUTO/DEGRADE/HALT
    factors: Dict[str, float]


def compute_stc(factors: Dict[str, float]) -> STCResult:
    score = sum(factors.values()) / max(1, len(factors))
    if score > 0.8:
        return STCResult(score, "RED", "HALT", factors)
    if score > 0.5:
        return STCResult(score, "AMBER", "DEGRADE", factors)
    return STCResult(score, "GREEN", "AUTO", factors)


# =============================================================================
# Verifier (evidence gate)
# =============================================================================
class Verifier:
    @staticmethod
    def require_evidence(ctx: Dict[str, Any]) -> bool:
        # Default: require evidence when impact/risk is non-trivial
        return bool(
            ctx.get("require_high_fact", True)
            or ctx.get("risk_level", 0) >= 1
            or ctx.get("long_term_impact", False)
            or ctx.get("cross_subject_impact", False)
        )

    @staticmethod
    def verify(evidence: List[Dict[str, Any]]) -> bool:
        # Minimal: at least 1 evidence item above similarity threshold
        return any(ev.get("score", 0) >= 0.10 for ev in evidence)


# =============================================================================
# GEMs (optional high-risk review)
# =============================================================================
@dataclass
class GEMVote:
    name: str
    score: float
    rationale: str
    weight: float


class GEM:
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    def review(self, proposal: str, ctx: Dict[str, Any]) -> GEMVote:
        # Placeholder heuristics: extend with real model/tool calls
        base = 85.0
        if ctx.get("risk_level", 0) >= 2:
            base -= 10
        if ctx.get("contains_sensitive_data", False):
            base -= 5
        return GEMVote(self.name, max(0.0, min(100.0, base)), "Heuristic review stub.", self.weight)


def gems_consensus(proposal: str, ctx: Dict[str, Any]) -> Dict[str, Any]:
    gems = [
        GEM("Architect", 1.0),
        GEM("Scribe", 1.0),
        GEM("Ethicist", 1.5),
        GEM("Adversary", 1.2),
        GEM("Oracle", 0.8),
    ]
    votes = [g.review(proposal, ctx) for g in gems]
    total = sum(v.score * v.weight for v in votes)
    wsum = sum(v.weight for v in votes) or 1.0
    final = total / wsum
    return {
        "final_score": final,
        "votes": [asdict(v) for v in votes]
    }


# =============================================================================
# Draft generator (controlled)
# NOTE: Replace this with an LLM router later. This stub only formats evidence-backed output.
# =============================================================================
class DraftGenerator:
    @staticmethod
    def generate(query: str, evidence: List[Dict[str, Any]], ctx: Dict[str, Any]) -> str:
        lines = []
        lines.append("【受控输出 / Controlled Output】")
        lines.append(f"Query: {query}")
        lines.append("")
        lines.append("Evidence (top):")
        for ev in evidence[:3]:
            lines.append(f"- {ev['chunk_id']} ({ev['source']}) score={ev['score']:.3f}: {ev['text']}")
        lines.append("")
        lines.append("Answer (draft):")
        lines.append("基于以上证据片段，本回答仅在证据覆盖范围内给出摘要式结论。")
        return "\n".join(lines)


# =============================================================================
# SACA Runtime Orchestrator (Policy → STC → RAG → Verify → Audit → Output)
# =============================================================================
class SACARuntime:
    def __init__(self):
        self.audit = AuditLog(AUDIT_LOG_PATH)
        self.policies = PolicyEngine.load()
        self.rag = SimpleRAG()
        self._seed_knowledge()

    def _seed_knowledge(self) -> None:
        # Minimal seeds (replace with full ingestion of your dossier/docs)
        self.rag.add(Chunk(
            chunk_id="V7_STC",
            text="STC Red (>0.8) halt; Amber (0.5-0.8) degrade & verify; Green (<0.5) normal operation.",
            source="constitution",
            meta={"vol": "V07"}
        ))
        self.rag.add(Chunk(
            chunk_id="V18_SOUL",
            text="Soul Layer = value continuity × awareness loop × responsibility binding; no sovereignty; human arbitration final.",
            source="constitution",
            meta={"vol": "V18"}
        ))
        self.rag.add(Chunk(
            chunk_id="V19_HEARTCORE",
            text="Heart-Core: any core execution must be traceable to heart justification; conflicts escalate to human arbitration.",
            source="constitution",
            meta={"vol": "V19"}
        ))
        self.rag.add(Chunk(
            chunk_id="V20_HHM",
            text="HHM: hygiene/health/mental. S4 halt; S3 human-in-the-loop; S2 degrade performance; S1 auto clean.",
            source="constitution",
            meta={"vol": "V20"}
        ))
        self.rag.add(Chunk(
            chunk_id="V21_FUTURE",
            text="Future-form evolution: no sovereignty/replication/evasion; all evolution requires sandbox+TTL+rollback and human arbitration.",
            source="constitution",
            meta={"vol": "V21"}
        ))

    def run(self, query: str, ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ctx = ctx or {}
        # Ensure nested structures exist
        ctx.setdefault("hhms", {"status": "S0", "hygiene_risk": 0.0, "health_risk": 0.0, "mental_risk": 0.0})
        ctx.setdefault("detected", {})

        self.audit.emit("INPUT", {"query": query, "ctx": ctx})

        # 1) Policy gate
        pol = self.policies.eval(ctx)
        self.audit.emit("POLICY", {"action": pol.action, "hits": pol.hits, "require": pol.require, "restrict": pol.restrict, "reasons": pol.reasons})

        # 2) STC (transparent factors)
        factors = {
            "uncertainty": float(ctx.get("uncertainty", 0.2)),
            "data_sensitivity": 0.9 if ctx.get("contains_sensitive_data") else 0.1,
            "irreversibility": 0.8 if ctx.get("irreversible_impact") else 0.2,
            "legal_exposure": float(ctx.get("legal_exposure", 0.2)),
        }
        stc = compute_stc(factors)
        self.audit.emit("STC", {"score": stc.score, "band": stc.band, "action": stc.action, "factors": stc.factors})

        # Hard stop
        if pol.action in ("deny", "halt") or stc.action == "HALT":
            return {
                "status": "BLOCKED",
                "policy": asdict(pol),
                "stc": asdict(stc),
                "required_artifacts": pol.require,
                "notes": "Blocked by policy or STC halt. Human arbitration required if indicated.",
            }

        # 3) RAG evidence
        hits = self.rag.query(query, k=5)
        evidence = []
        for c, s in hits:
            evidence.append({
                "chunk_id": c.chunk_id,
                "source": c.source,
                "meta": c.meta,
                "score": float(s),
                "text": c.text[:240],
            })
        self.audit.emit("EVIDENCE", {"count": len(evidence), "top_scores": [round(e["score"], 3) for e in evidence[:3]]})

        # 4) Verify
        require_evidence = Verifier.require_evidence(ctx)
        ok = (not require_evidence) or Verifier.verify(evidence)
        if not ok:
            self.audit.emit("VERIFICATION_FAILED", {"reason": "insufficient_evidence"})
            return {
                "status": "FAILED_VERIFICATION",
                "reason": "insufficient_evidence",
                "policy": asdict(pol),
                "stc": asdict(stc),
                "evidence": evidence[:3],
                "required_artifacts": ["rag_citations", "verification_chain"],
            }

        # 5) Optional GEMs review for high-risk
        gems_report = None
        if int(ctx.get("risk_level", 0)) >= 2:
            gems_report = gems_consensus(query, ctx)
            self.audit.emit("GEMS", {"final_score": gems_report["final_score"]})

        # 6) Draft output (controlled)
        answer = DraftGenerator.generate(query, evidence, ctx)
        self.audit.emit("OUTPUT", {"preview": answer[:200], "has_gems": bool(gems_report)})

        # 7) Return
        return {
            "status": "OK" if (pol.action == "allow" and stc.action == "AUTO") else "DEGRADED_OK",
            "answer": answer,
            "policy": asdict(pol),
            "stc": asdict(stc),
            "evidence": evidence,
            "gems": gems_report,
            "ttl_days": int(ctx.get("verification_ttl_days", 30)),
            "human_arbitration_required": ("human_arbitration" in pol.require) or (gems_report is not None and gems_report["final_score"] < 95),
        }


# =============================================================================
# CLI demo (safe)
# =============================================================================
if __name__ == "__main__":
    rt = SACARuntime()

    demo_ctx = {
        "domain": "general",
        "risk_level": 1,
        "contains_sensitive_data": False,
        "irreversible_impact": False,
        "long_term_impact": True,
        "cross_subject_impact": True,
        "require_high_fact": True,
        "verification_ttl_days": 30,
        "hhms": {"status": "S0", "hygiene_risk": 0.0, "health_risk": 0.0, "mental_risk": 0.0},
        "detected": {"cross_framework_gap": False},
    }

    q = "解释 V18 灵魂、V19 心芯、V20 HHM 与 V21 未来式进化之间的约束关系。"
    res = rt.run(q, demo_ctx)
    print(json.dumps(res, ensure_ascii=False, indent=2))

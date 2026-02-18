"""
A-Z AI Administration Vocabulary Matrix (104 Terms)
====================================================
Design: Jiadong Chen (陈佳栋) — Student ID: 723912

26 letters × 4 terms = 104 English vocabulary items mapped to:
- Administration Direction (Role / Function)
- AI Functional Scope (AI Scope)

Based on:
- DOC-20260218-AZ-AI-Admin-Vocabulary-0011

Conversion Targets:
- Job Classification Table (Current vs Future)
- Enterprise AI Admin Responsibility Matrix
- M365 / Azure / Multi-cloud Mapping Structure
- Administration-AI Capability OS Framework Diagram
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# =============================================================================
# Enums
# =============================================================================

class AdminDomain(Enum):
    """High-level AI administration domains."""

    ARCHITECTURE = "architecture"
    COMPLIANCE = "compliance"
    DATA = "data"
    GOVERNANCE = "governance"
    INFRASTRUCTURE = "infrastructure"
    MONITORING = "monitoring"
    PRIVACY = "privacy"
    RISK = "risk"
    SECURITY = "security"
    TRAINING = "training"


class CloudProvider(Enum):
    """Cloud providers for role mapping."""

    AZURE = "microsoft_azure"
    GCP = "google_cloud"
    AWS = "amazon_web_services"
    MULTI_CLOUD = "multi_cloud"


class VocabCategory(Enum):
    """Functional category for each vocabulary term."""

    ARCHITECTURE_DESIGN = "architecture_design"
    COMPLIANCE_AUDIT = "compliance_audit"
    COST_GOVERNANCE = "cost_governance"
    CYBERSECURITY = "cybersecurity"
    DATA_GOVERNANCE = "data_governance"
    DEPLOYMENT_OPS = "deployment_ops"
    ETHICS_FAIRNESS = "ethics_fairness"
    INFRASTRUCTURE = "infrastructure"
    MODEL_MANAGEMENT = "model_management"
    MONITORING_OBSERVABILITY = "monitoring_observability"
    POLICY_REGULATION = "policy_regulation"
    PRIVACY_PROTECTION = "privacy_protection"
    RISK_MANAGEMENT = "risk_management"
    SCALING_PERFORMANCE = "scaling_performance"
    SECURITY_ACCESS = "security_access"
    TRANSPARENCY_TRUST = "transparency_trust"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass(frozen=True)
class AIAdminTerm:
    """Single A-Z vocabulary entry."""

    letter: str
    index: int  # 1-4 within the letter
    term: str
    admin_direction_zh: str  # Chinese description of admin role/function
    ai_scope: str  # AI functional scope description
    category: VocabCategory


@dataclass(frozen=True)
class IndustryAIAdoption:
    """Industry-level AI adoption data."""

    industry: str
    industry_zh: str
    use_cases: list[str]
    adoption_rate_2024: Optional[str] = None
    notes: str = ""


@dataclass(frozen=True)
class BusinessFunctionAI:
    """Business function with AI penetration."""

    function: str
    function_zh: str
    ai_applications: list[str]
    genai_adoption_pct: Optional[str] = None


@dataclass(frozen=True)
class EmploymentImpactCase:
    """Documented company AI employment impact case."""

    company: str
    year: int
    impact_description: str
    jobs_affected: Optional[int] = None
    percentage_affected: Optional[str] = None


@dataclass(frozen=True)
class HumanAIBalancePrinciple:
    """Human-AI balance framework principle."""

    principle_id: str
    title: str
    title_zh: str
    description: str


@dataclass(frozen=True)
class BalanceLayerDesign:
    """Three-layer structural design for human-AI balance."""

    layer: int  # 1=base, 2=middle, 3=surface
    name: str
    name_zh: str
    description: str
    role: str


# =============================================================================
# A-Z Vocabulary Data (104 terms)
# =============================================================================

AZ_VOCABULARY: list[AIAdminTerm] = [
    # A
    AIAdminTerm("A", 1, "Architecture", "系统架构管理", "Model deployment / Multi-cloud AI topology", VocabCategory.ARCHITECTURE_DESIGN),
    AIAdminTerm("A", 2, "Audit", "合规审计管理", "AI output traceability / Model logging", VocabCategory.COMPLIANCE_AUDIT),
    AIAdminTerm("A", 3, "Automation", "自动化流程管理", "Agent orchestration", VocabCategory.DEPLOYMENT_OPS),
    AIAdminTerm("A", 4, "Access", "访问控制管理", "RBAC / Zero-Trust AI", VocabCategory.SECURITY_ACCESS),
    # B
    AIAdminTerm("B", 1, "Benchmarking", "性能评估管理", "LLM accuracy / hallucination testing", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("B", 2, "Budgeting", "AI 成本治理", "Token / GPU allocation", VocabCategory.COST_GOVERNANCE),
    AIAdminTerm("B", 3, "Backup", "数据备份策略", "Model checkpoint control", VocabCategory.DATA_GOVERNANCE),
    AIAdminTerm("B", 4, "Bias", "偏见控制管理", "Fairness evaluation", VocabCategory.ETHICS_FAIRNESS),
    # C
    AIAdminTerm("C", 1, "Compliance", "法规合规管理", "ISO 42001 / AI Act alignment", VocabCategory.COMPLIANCE_AUDIT),
    AIAdminTerm("C", 2, "Cybersecurity", "网络安全管理", "AI threat detection", VocabCategory.CYBERSECURITY),
    AIAdminTerm("C", 3, "Configuration", "模型参数配置", "Prompt governance", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("C", 4, "Capacity", "算力容量规划", "GPU scaling", VocabCategory.SCALING_PERFORMANCE),
    # D
    AIAdminTerm("D", 1, "Data", "数据治理", "Training pipeline", VocabCategory.DATA_GOVERNANCE),
    AIAdminTerm("D", 2, "Deployment", "模型上线管理", "CI/CD for AI", VocabCategory.DEPLOYMENT_OPS),
    AIAdminTerm("D", 3, "Documentation", "文档与审计记录", "Model cards", VocabCategory.COMPLIANCE_AUDIT),
    AIAdminTerm("D", 4, "Detection", "异常检测", "AI misuse monitoring", VocabCategory.MONITORING_OBSERVABILITY),
    # E
    AIAdminTerm("E", 1, "Evaluation", "模型评估", "Benchmark testing", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("E", 2, "Ethics", "AI 伦理治理", "Responsible AI", VocabCategory.ETHICS_FAIRNESS),
    AIAdminTerm("E", 3, "Encryption", "数据加密管理", "Secure inference", VocabCategory.CYBERSECURITY),
    AIAdminTerm("E", 4, "Escalation", "风险升级机制", "Human-in-the-loop", VocabCategory.RISK_MANAGEMENT),
    # F
    AIAdminTerm("F", 1, "Forecasting", "预测系统管理", "Predictive AI", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("F", 2, "Federation", "联邦学习管理", "Cross-jurisdiction AI", VocabCategory.DATA_GOVERNANCE),
    AIAdminTerm("F", 3, "Filtering", "内容过滤管理", "Moderation models", VocabCategory.ETHICS_FAIRNESS),
    AIAdminTerm("F", 4, "Failover", "容灾机制", "Redundancy AI nodes", VocabCategory.INFRASTRUCTURE),
    # G
    AIAdminTerm("G", 1, "Governance", "AI 治理框架", "Policy enforcement", VocabCategory.POLICY_REGULATION),
    AIAdminTerm("G", 2, "Granularity", "细粒度权限", "Data segmentation", VocabCategory.SECURITY_ACCESS),
    AIAdminTerm("G", 3, "Guardrails", "风险边界控制", "Prompt safety layers", VocabCategory.RISK_MANAGEMENT),
    AIAdminTerm("G", 4, "Graph", "知识图谱管理", "RAG systems", VocabCategory.DATA_GOVERNANCE),
    # H
    AIAdminTerm("H", 1, "Hosting", "云托管管理", "AI infrastructure", VocabCategory.INFRASTRUCTURE),
    AIAdminTerm("H", 2, "Hardening", "系统加固", "Secure model serving", VocabCategory.CYBERSECURITY),
    AIAdminTerm("H", 3, "Human-Oversight", "人工监管机制", "Approval workflows", VocabCategory.TRANSPARENCY_TRUST),
    AIAdminTerm("H", 4, "Horizon-Scanning", "技术前瞻管理", "Emerging AI tracking", VocabCategory.POLICY_REGULATION),
    # I
    AIAdminTerm("I", 1, "Integration", "API 集成管理", "Multi-platform AI", VocabCategory.DEPLOYMENT_OPS),
    AIAdminTerm("I", 2, "Identity", "数字身份管理", "AI-linked ID systems", VocabCategory.SECURITY_ACCESS),
    AIAdminTerm("I", 3, "Indexing", "向量索引管理", "Retrieval systems", VocabCategory.DATA_GOVERNANCE),
    AIAdminTerm("I", 4, "Infrastructure", "底层架构管理", "GPU clusters", VocabCategory.INFRASTRUCTURE),
    # J
    AIAdminTerm("J", 1, "Jurisdiction", "跨地区监管", "Data residency", VocabCategory.POLICY_REGULATION),
    AIAdminTerm("J", 2, "Job-Scheduling", "任务调度管理", "AI batch jobs", VocabCategory.DEPLOYMENT_OPS),
    AIAdminTerm("J", 3, "Justification", "决策可解释性", "Explainable AI", VocabCategory.TRANSPARENCY_TRUST),
    AIAdminTerm("J", 4, "Joint-Control", "双人审核机制", "Two-person rule", VocabCategory.SECURITY_ACCESS),
    # K
    AIAdminTerm("K", 1, "Knowledge-Base", "知识库管理", "RAG curation", VocabCategory.DATA_GOVERNANCE),
    AIAdminTerm("K", 2, "Key-Management", "API 密钥治理", "Secure token systems", VocabCategory.SECURITY_ACCESS),
    AIAdminTerm("K", 3, "KPI", "绩效指标管理", "Model quality metrics", VocabCategory.MONITORING_OBSERVABILITY),
    AIAdminTerm("K", 4, "Kernel", "核心模型管理", "Foundation models", VocabCategory.MODEL_MANAGEMENT),
    # L
    AIAdminTerm("L", 1, "Lifecycle", "模型生命周期管理", "MLOps", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("L", 2, "Logging", "审计日志管理", "SIEM", VocabCategory.MONITORING_OBSERVABILITY),
    AIAdminTerm("L", 3, "Latency", "性能延迟优化", "Real-time AI", VocabCategory.SCALING_PERFORMANCE),
    AIAdminTerm("L", 4, "Licensing", "许可与订阅管理", "Enterprise AI", VocabCategory.COST_GOVERNANCE),
    # M
    AIAdminTerm("M", 1, "Monitoring", "实时监控", "Drift detection", VocabCategory.MONITORING_OBSERVABILITY),
    AIAdminTerm("M", 2, "Moderation", "内容治理", "Harm detection", VocabCategory.ETHICS_FAIRNESS),
    AIAdminTerm("M", 3, "Modeling", "模型设计", "Architecture tuning", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("M", 4, "Migration", "平台迁移", "AI stack upgrade", VocabCategory.DEPLOYMENT_OPS),
    # N
    AIAdminTerm("N", 1, "Normalization", "数据标准化", "Preprocessing", VocabCategory.DATA_GOVERNANCE),
    AIAdminTerm("N", 2, "Notification", "事件通知管理", "Alert systems", VocabCategory.MONITORING_OBSERVABILITY),
    AIAdminTerm("N", 3, "Node-Management", "节点调度", "Distributed AI", VocabCategory.INFRASTRUCTURE),
    AIAdminTerm("N", 4, "Network", "网络安全管理", "Secure AI traffic", VocabCategory.CYBERSECURITY),
    # O
    AIAdminTerm("O", 1, "Orchestration", "Agent 编排", "Multi-AI coordination", VocabCategory.DEPLOYMENT_OPS),
    AIAdminTerm("O", 2, "Optimization", "性能优化", "Token efficiency", VocabCategory.SCALING_PERFORMANCE),
    AIAdminTerm("O", 3, "Observability", "可观测性管理", "Telemetry", VocabCategory.MONITORING_OBSERVABILITY),
    AIAdminTerm("O", 4, "Ownership", "责任归属管理", "AI accountability", VocabCategory.TRANSPARENCY_TRUST),
    # P
    AIAdminTerm("P", 1, "Privacy", "隐私保护", "Differential privacy", VocabCategory.PRIVACY_PROTECTION),
    AIAdminTerm("P", 2, "Provisioning", "资源分配", "Cloud AI scaling", VocabCategory.INFRASTRUCTURE),
    AIAdminTerm("P", 3, "Policy", "制度制定", "AI usage policy", VocabCategory.POLICY_REGULATION),
    AIAdminTerm("P", 4, "Prompting", "提示工程管理", "Prompt governance", VocabCategory.MODEL_MANAGEMENT),
    # Q
    AIAdminTerm("Q", 1, "Quality-Assurance", "质量控制", "AI output review", VocabCategory.COMPLIANCE_AUDIT),
    AIAdminTerm("Q", 2, "Quantification", "指标量化", "Risk scoring", VocabCategory.RISK_MANAGEMENT),
    AIAdminTerm("Q", 3, "Queue-Management", "请求排队管理", "Load balancing", VocabCategory.SCALING_PERFORMANCE),
    AIAdminTerm("Q", 4, "Query-Optimization", "查询优化", "RAG tuning", VocabCategory.DATA_GOVERNANCE),
    # R
    AIAdminTerm("R", 1, "Resilience", "系统韧性管理", "Fail-safe AI", VocabCategory.RISK_MANAGEMENT),
    AIAdminTerm("R", 2, "Risk", "风险控制", "AI risk taxonomy", VocabCategory.RISK_MANAGEMENT),
    AIAdminTerm("R", 3, "Regulation", "法规执行", "AI compliance mapping", VocabCategory.POLICY_REGULATION),
    AIAdminTerm("R", 4, "Retrieval", "信息检索管理", "Vector DB", VocabCategory.DATA_GOVERNANCE),
    # S
    AIAdminTerm("S", 1, "Security", "安全管理", "Threat mitigation", VocabCategory.CYBERSECURITY),
    AIAdminTerm("S", 2, "Scalability", "扩展性管理", "Elastic compute", VocabCategory.SCALING_PERFORMANCE),
    AIAdminTerm("S", 3, "Simulation", "仿真系统", "Digital twin AI", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("S", 4, "Sustainability", "能耗管理", "Green AI", VocabCategory.INFRASTRUCTURE),
    # T
    AIAdminTerm("T", 1, "Transparency", "透明度管理", "Explainability", VocabCategory.TRANSPARENCY_TRUST),
    AIAdminTerm("T", 2, "Training", "模型训练管理", "Fine-tuning", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("T", 3, "Telemetry", "数据采集", "Performance tracking", VocabCategory.MONITORING_OBSERVABILITY),
    AIAdminTerm("T", 4, "Trust", "信任体系", "Verification systems", VocabCategory.TRANSPARENCY_TRUST),
    # U
    AIAdminTerm("U", 1, "Update", "模型更新管理", "Patch cycles", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("U", 2, "Usage", "使用监控", "AI consumption logs", VocabCategory.MONITORING_OBSERVABILITY),
    AIAdminTerm("U", 3, "User-Governance", "用户权限体系", "Enterprise AI control", VocabCategory.SECURITY_ACCESS),
    AIAdminTerm("U", 4, "Uptime", "可用性管理", "SLA control", VocabCategory.INFRASTRUCTURE),
    # V
    AIAdminTerm("V", 1, "Validation", "验证机制", "Model testing", VocabCategory.COMPLIANCE_AUDIT),
    AIAdminTerm("V", 2, "Versioning", "版本管理", "Model lineage", VocabCategory.MODEL_MANAGEMENT),
    AIAdminTerm("V", 3, "Vulnerability", "漏洞管理", "AI threat exposure", VocabCategory.CYBERSECURITY),
    AIAdminTerm("V", 4, "Virtualization", "虚拟化管理", "Cloud instances", VocabCategory.INFRASTRUCTURE),
    # W
    AIAdminTerm("W", 1, "Workflow", "工作流管理", "AI pipeline", VocabCategory.DEPLOYMENT_OPS),
    AIAdminTerm("W", 2, "Whitelisting", "白名单机制", "Tool restriction", VocabCategory.SECURITY_ACCESS),
    AIAdminTerm("W", 3, "Watermarking", "内容标识", "AI origin tracking", VocabCategory.TRANSPARENCY_TRUST),
    AIAdminTerm("W", 4, "Workload", "负载分配", "GPU balancing", VocabCategory.SCALING_PERFORMANCE),
    # X
    AIAdminTerm("X", 1, "X-AI (Explainable AI)", "可解释系统", "Decision transparency", VocabCategory.TRANSPARENCY_TRUST),
    AIAdminTerm("X", 2, "X-Scaling", "横向扩展", "Distributed training", VocabCategory.SCALING_PERFORMANCE),
    AIAdminTerm("X", 3, "X-Validation", "交叉验证", "Model reliability", VocabCategory.COMPLIANCE_AUDIT),
    AIAdminTerm("X", 4, "X-Architecture", "跨结构设计", "Hybrid AI", VocabCategory.ARCHITECTURE_DESIGN),
    # Y
    AIAdminTerm("Y", 1, "Yield", "产出效率管理", "AI productivity", VocabCategory.SCALING_PERFORMANCE),
    AIAdminTerm("Y", 2, "Yardstick", "评估基准", "Benchmark index", VocabCategory.COMPLIANCE_AUDIT),
    AIAdminTerm("Y", 3, "YAML-Governance", "配置标准化", "AI policy as code", VocabCategory.POLICY_REGULATION),
    AIAdminTerm("Y", 4, "Year-Over-Year", "年度趋势分析", "AI maturity tracking", VocabCategory.MONITORING_OBSERVABILITY),
    # Z
    AIAdminTerm("Z", 1, "Zero-Trust", "零信任架构", "AI identity security", VocabCategory.SECURITY_ACCESS),
    AIAdminTerm("Z", 2, "Zoning", "区域权限划分", "Data segmentation", VocabCategory.SECURITY_ACCESS),
    AIAdminTerm("Z", 3, "Zettabyte", "海量数据管理", "Big data AI", VocabCategory.DATA_GOVERNANCE),
    AIAdminTerm("Z", 4, "Zenith", "性能极值优化", "Peak model capacity", VocabCategory.SCALING_PERFORMANCE),
]

# =============================================================================
# Industry AI Adoption Data (16 sectors)
# =============================================================================

INDUSTRY_AI_ADOPTION: list[IndustryAIAdoption] = [
    IndustryAIAdoption(
        "IT / Software / Internet", "科技与信息产业",
        ["Recommendation systems", "Search", "Ad placement", "DevOps automation", "Code assistance"],
        "~88%", "Highest AI penetration since 2020"
    ),
    IndustryAIAdoption(
        "Financial Services", "金融服务（银行、保险、证券、支付）",
        ["Risk assessment", "Anti-fraud", "Credit scoring", "Chatbots", "Investment strategy"],
        notes="Among highest AI investment industries"
    ),
    IndustryAIAdoption(
        "Manufacturing / Industrial", "制造业/工业/先进制造",
        ["Predictive maintenance", "Quality inspection", "Supply chain", "Process optimisation", "Robotics"],
        notes="Trillions in value-add potential by 2035"
    ),
    IndustryAIAdoption(
        "Retail & E-commerce / FMCG", "零售与电商/快消",
        ["Smart recommendations", "Inventory management", "Pricing", "Promotions", "Customer service"],
        notes="GenAI rapid spread in marketing content and personalisation"
    ),
    IndustryAIAdoption(
        "Healthcare & Life Sciences", "医疗健康与生命科学",
        ["Medical imaging", "Drug R&D", "Personalised treatment", "Patient triage"],
        notes="Fastest-growing AI application industry"
    ),
    IndustryAIAdoption(
        "Telecom & Media", "通信与媒体/电信运营商",
        ["Network optimisation", "Fault prediction", "Marketing automation", "Content recommendation"],
    ),
    IndustryAIAdoption(
        "Professional Services", "专业服务（咨询、法律、会计、人力资源）",
        ["Contract analysis", "Legal research", "Financial analysis", "Document generation", "Recruitment"],
        notes="2023-2024: Highest AI adoption growth rate among all industries"
    ),
    IndustryAIAdoption(
        "Government & Public Services", "政府与公共服务/智慧城市",
        ["Government chatbots", "Tax auditing", "Traffic optimisation", "Public safety", "Welfare review"],
    ),
    IndustryAIAdoption(
        "Education & Training", "教育与培训",
        ["Personalised learning paths", "Auto-grading", "Content generation", "Tutoring", "Behaviour analysis"],
    ),
    IndustryAIAdoption(
        "Logistics & Transportation", "物流与运输/供应链",
        ["Route planning", "Demand forecasting", "Warehouse optimisation", "Autonomous driving", "Fleet dispatch"],
    ),
    IndustryAIAdoption(
        "Energy & Utilities", "能源与公用事业",
        ["Predictive maintenance", "Grid optimisation", "Load forecasting", "Energy trading"],
    ),
    IndustryAIAdoption(
        "Agriculture / Forestry / Fisheries", "农业/林业/渔业",
        ["Crop monitoring", "Precision agriculture", "Pest detection", "Yield prediction", "Livestock management"],
    ),
    IndustryAIAdoption(
        "Tourism, Hospitality & Food Service", "旅游、酒店与餐饮",
        ["Dynamic pricing", "Demand forecasting", "Customer profiling", "Operations optimisation"],
    ),
    IndustryAIAdoption(
        "Real Estate & Construction", "房地产与建筑",
        ["Valuation models", "Smart buildings", "Energy management", "Facility operations", "Tenant automation"],
    ),
    IndustryAIAdoption(
        "Arts, Entertainment & Creative", "艺术、娱乐与创意产业",
        ["Content generation", "VFX", "Personalised experiences", "Virtual humans", "Game design"],
    ),
    IndustryAIAdoption(
        "Non-profit / NGO / Social Sector", "非营利/NGO/社会部门",
        ["Fundraising optimisation", "Impact assessment", "Sentiment analysis", "Disaster response"],
    ),
]

# =============================================================================
# Business Functions with AI Penetration (9 functions)
# =============================================================================

BUSINESS_FUNCTION_AI: list[BusinessFunctionAI] = [
    BusinessFunctionAI(
        "Marketing & Sales", "营销与销售",
        ["Customer acquisition", "Ad placement", "Pricing", "Personalised content"],
        "~40%+"
    ),
    BusinessFunctionAI(
        "Customer Service & Operations", "客户服务与运营",
        ["Chatbots", "Process automation", "Quality monitoring"],
    ),
    BusinessFunctionAI(
        "Risk, Compliance & Security", "风险、合规与安全",
        ["Risk models", "Anomaly detection", "Fraud identification", "Compliance templates"],
    ),
    BusinessFunctionAI(
        "Finance & Strategic Planning", "财务与战略规划",
        ["Budget forecasting", "Scenario analysis", "Cost optimisation"],
    ),
    BusinessFunctionAI(
        "Supply Chain & Operations Management", "供应链与运营管理",
        ["Demand forecasting", "Inventory optimisation", "Logistics dispatch"],
    ),
    BusinessFunctionAI(
        "Human Resources", "人力资源管理",
        ["Recruitment screening", "Performance analytics", "Employee support bots"],
    ),
    BusinessFunctionAI(
        "Product & R&D", "产品研发与工程",
        ["Simulation", "Design optimisation", "Code generation", "Test automation"],
    ),
    BusinessFunctionAI(
        "Data & Analytics", "数据与分析",
        ["BI", "Prediction", "Decision support"],
    ),
    BusinessFunctionAI(
        "Administration & Office Automation", "行政与办公自动化",
        ["Document processing", "Scheduling", "Workflow automation"],
    ),
]

# =============================================================================
# Employment Impact Cases
# =============================================================================

EMPLOYMENT_IMPACT_CASES: list[EmploymentImpactCase] = [
    EmploymentImpactCase("Amazon", 2025, "AI/automation cited in layoff announcements"),
    EmploymentImpactCase("Salesforce", 2025, "AI handles ~50% CS tasks, customer service positions cut", 4000, "~50% CS tasks automated"),
    EmploymentImpactCase("Fiverr", 2025, "Building AI-first operations, ~30% workforce reduction", 250, "~30%"),
    EmploymentImpactCase("IBM", 2025, "30% of back-office positions replaced by AI over 5 years", 7800, "~30% back-office"),
    EmploymentImpactCase("BT (British Telecom)", 2030, "~55,000 jobs by 2030, ~10,000 replaced by AI in customer service", 55000, "~10,000 AI-replaced"),
]

# =============================================================================
# AI Adoption Timeline
# =============================================================================

AI_ADOPTION_TIMELINE: dict[str, str] = {
    "2020-2022": "20-30% of enterprises using AI in >=1 business function",
    "2023": "~50% using AI (generative AI explosion year)",
    "2024": "~72% using AI; 65% regularly using GenAI (2x prior year)",
    "2025-2026": "78-93% using AI in >=1 business function",
}

# =============================================================================
# Human-AI Balance Framework
# =============================================================================

BALANCE_FOUNDATIONAL_CONDITIONS: list[HumanAIBalancePrinciple] = [
    HumanAIBalancePrinciple(
        "LEGAL", "Legal Compliance", "合规合法",
        "Privacy, data protection, liability, safety regulations. AI regulatory frameworks. "
        "Risk and responsibility not dumped on users or frontline workers."
    ),
    HumanAIBalancePrinciple(
        "SOCIAL", "Social Acceptability", "社会可接受",
        "Not just technically feasible but considers public sentiment on unemployment, "
        "fairness, bias, cultural diversity. Avoid technically correct but socially divisive paths."
    ),
    HumanAIBalancePrinciple(
        "CARE", "Care for Vulnerable Populations & Traditional Modes", "照顾弱势与传统模式",
        "Traditional practices as training data and validation benchmarks. Farmers, teachers, "
        "doctors, craftspeople, social workers' experience is the real-world testing standard for AI models."
    ),
    HumanAIBalancePrinciple(
        "AUTHORITY", "Human Decision-Making Authority", "人类保持决策主导权",
        "In high-risk/high-value scenarios (health, justice, children's education, major financial decisions): "
        "AI is advisory only. Final judgment and responsibility signing remains with humans."
    ),
]

BALANCE_THREE_LAYERS: list[BalanceLayerDesign] = [
    BalanceLayerDesign(
        1, "Base: Human Experience → Data & Rules", "底层：人类经验 → 数据与规则",
        "Farming techniques, classroom experience, nursing judgment, engineering craft = "
        "experiential data and implicit algorithms. Must preserve exceptions and hard-to-articulate details.",
        "Source of truth"
    ),
    BalanceLayerDesign(
        2, "Middle: AI as Tool & Mirror", "中层：AI 作为工具与镜子",
        "Tool: automates what humans are not good at (large-scale search, repetitive calculation, formatting). "
        "Mirror: reveals blind spots and patterns, flags gaps/bias. Does NOT make value judgments.",
        "Amplifier, not substitute"
    ),
    BalanceLayerDesign(
        3, "Surface: Humans Make Decisions & Care", "表层：人做决策与照顾人",
        "Whether to do it, how to do it, accountable to whom = human domain. Especially in scenarios "
        "involving personal safety, dignity, long-term impact.",
        "Collaborators and guardians"
    ),
]

BALANCE_SELF_CHECK_QUESTIONS: list[str] = [
    "Is it explainable and traceable? (input sources, main logic, known limitations, post-hoc audit)",
    "Is there a clear human responsibility point? (who is accountable, who can press pause)",
    "Is a human channel preserved for those who need it? (elderly, disabled, digitally disadvantaged)",
]

PERSONAL_BALANCE_PRINCIPLES: list[str] = [
    "Don't treat AI as authority — treat it as one opinion source among many",
    "Use AI in amplifier position, not substitute position",
    "Regularly ask: Without AI, how would I think about / handle this?",
    "Preserve slow space — deliberately reserve time for relationships, reflection, learning",
]

# Core principle
CORE_PRINCIPLE = "人永远不是插件，AI 才是。 / Humans are never plugins — AI is."

# =============================================================================
# High-Risk Employment Categories
# =============================================================================

HIGH_RISK_ROLES: list[dict[str, str]] = [
    {"category": "Standardised repetitive white-collar", "examples": "Back-office admin, basic HR, simple financial entry, junior legal/compliance"},
    {"category": "Customer service & call centres", "examples": "Routine query handling (humans retained for complex/emotional cases)"},
    {"category": "IT / Financial Services / Accounting", "examples": "Process-oriented roles in IT, finance, accounting"},
    {"category": "Writing & content production", "examples": "Translation, basic content writing, resume writing, marketing copy, freelance/contract"},
]

# Retraining statistics
RETRAINING_STATS: dict[str, str] = {
    "wef_retraining_need": "~59% of employees need retraining/upskilling (WEF)",
    "ai_fluency_growth": "AI fluency demand grew ~7x in two years (McKinsey)",
    "us_ai_jobs": "~8 million US jobs require at least one AI-related skill",
    "company_plan_vs_reality": "70-80% plan to retrain, actual implementation much lower",
    "employee_anxiety": "~66% feel management doesn't understand AI's psychological impact",
    "employee_willingness": "~70% willing to delegate repetitive work to AI",
}


# =============================================================================
# Framework Class
# =============================================================================

class AIAdminVocabularyFramework:
    """A-Z AI Administration Vocabulary and Employment Impact Framework."""

    def __init__(self) -> None:
        self.vocabulary = AZ_VOCABULARY
        self.industries = INDUSTRY_AI_ADOPTION
        self.business_functions = BUSINESS_FUNCTION_AI
        self.impact_cases = EMPLOYMENT_IMPACT_CASES
        self.adoption_timeline = AI_ADOPTION_TIMELINE
        self.balance_conditions = BALANCE_FOUNDATIONAL_CONDITIONS
        self.balance_layers = BALANCE_THREE_LAYERS
        self.self_check_questions = BALANCE_SELF_CHECK_QUESTIONS
        self.personal_principles = PERSONAL_BALANCE_PRINCIPLES
        self.core_principle = CORE_PRINCIPLE
        self.high_risk_roles = HIGH_RISK_ROLES
        self.retraining_stats = RETRAINING_STATS

    # ---- Vocabulary Queries ----

    def get_all_terms(self) -> list[AIAdminTerm]:
        """Return all 104 A-Z vocabulary terms."""
        return list(self.vocabulary)

    def get_terms_by_letter(self, letter: str) -> list[AIAdminTerm]:
        """Return 4 terms for a given letter."""
        letter = letter.upper()
        return [t for t in self.vocabulary if t.letter == letter]

    def get_term_by_name(self, term_name: str) -> AIAdminTerm | None:
        """Find a term by its English name (case-insensitive)."""
        lower = term_name.lower()
        for t in self.vocabulary:
            if t.term.lower() == lower:
                return t
        return None

    def get_terms_by_category(self, category: VocabCategory) -> list[AIAdminTerm]:
        """Return all terms in a given functional category."""
        return [t for t in self.vocabulary if t.category == category]

    def get_all_letters(self) -> list[str]:
        """Return list of all 26 letters covered."""
        seen: list[str] = []
        for t in self.vocabulary:
            if t.letter not in seen:
                seen.append(t.letter)
        return seen

    def get_category_distribution(self) -> dict[str, int]:
        """Return count of terms per VocabCategory."""
        dist: dict[str, int] = {}
        for t in self.vocabulary:
            key = t.category.value
            dist[key] = dist.get(key, 0) + 1
        return dist

    # ---- Industry Queries ----

    def get_all_industries(self) -> list[IndustryAIAdoption]:
        """Return all 16 industry adoption records."""
        return list(self.industries)

    def get_industry_by_name(self, name: str) -> IndustryAIAdoption | None:
        """Find industry by partial name match."""
        lower = name.lower()
        for ind in self.industries:
            if lower in ind.industry.lower() or lower in ind.industry_zh:
                return ind
        return None

    # ---- Business Function Queries ----

    def get_all_business_functions(self) -> list[BusinessFunctionAI]:
        """Return all 9 business functions."""
        return list(self.business_functions)

    # ---- Employment Impact ----

    def get_impact_cases(self) -> list[EmploymentImpactCase]:
        """Return documented company impact cases."""
        return list(self.impact_cases)

    def get_total_jobs_affected(self) -> int:
        """Sum of documented jobs affected."""
        return sum(c.jobs_affected for c in self.impact_cases if c.jobs_affected)

    # ---- Human-AI Balance ----

    def get_balance_conditions(self) -> list[HumanAIBalancePrinciple]:
        """Return 4 foundational conditions for human-AI balance."""
        return list(self.balance_conditions)

    def get_balance_layers(self) -> list[BalanceLayerDesign]:
        """Return 3-layer structural design."""
        return list(self.balance_layers)

    def get_self_check_questions(self) -> list[str]:
        """Return 3 self-check questions for AI solution health."""
        return list(self.self_check_questions)

    def get_personal_principles(self) -> list[str]:
        """Return personal human-machine balance principles."""
        return list(self.personal_principles)

    # ---- Summary ----

    def get_framework_summary(self) -> dict[str, Any]:
        """Return comprehensive framework summary."""
        return {
            "module": "A-Z AI Administration Vocabulary & Employment Impact Framework",
            "version": "1.0",
            "design": "Jiadong Chen (陈佳栋) — Student ID: 723912",
            "total_vocabulary_terms": len(self.vocabulary),
            "letters_covered": len(self.get_all_letters()),
            "vocab_categories": len(VocabCategory),
            "category_distribution": self.get_category_distribution(),
            "industries_covered": len(self.industries),
            "business_functions": len(self.business_functions),
            "employment_impact_cases": len(self.impact_cases),
            "total_jobs_affected": self.get_total_jobs_affected(),
            "adoption_timeline_periods": len(self.adoption_timeline),
            "balance_foundational_conditions": len(self.balance_conditions),
            "balance_layers": len(self.balance_layers),
            "self_check_questions": len(self.self_check_questions),
            "personal_principles": len(self.personal_principles),
            "high_risk_categories": len(self.high_risk_roles),
            "core_principle": self.core_principle,
        }

"""
Legal Knowledge Base / 法律知識庫 / 法律知识库
=============================================
Comprehensive database of international human rights legislation,
treaties, conventions, and landmark case law for legal AI evidence mapping.

Covers / 涵蓋範圍 / 涵盖范围:
- Freedom of Information (UDHR Art.19, ICCPR Art.19)
- Residence Rules & Regulations (UDHR Art.13, ICESCR Art.11)
- Agent Duties & Community Safety (UN Guiding Principles, ECHR)
- LGBTI Rights (OHCHR Free & Equal, Yogyakarta Principles)
- AI & Human Rights (UN GA Res. A/78/L.49, CoE Framework Convention)

References / 參考資料 / 参考资料:
- https://www.ohchr.org/en/ohchr_homepage
- https://www.ohchr.org/en/sexual-orientation-and-gender-identity/
- https://www.un.org/zh/global-issues/artificial-intelligence
- https://www.un.org/zh/our-work/protect-human-rights
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class LegislationType(Enum):
    """Type of legal instrument / 法律文書類型 / 法律文书类型"""
    TREATY = "treaty"
    CONVENTION = "convention"
    RESOLUTION = "resolution"
    DIRECTIVE = "directive"
    REGULATION = "regulation"
    FRAMEWORK = "framework"
    CASE_LAW = "case_law"
    GUIDELINE = "guideline"
    NATIONAL_LAW = "national_law"


class JurisdictionScope(Enum):
    """Jurisdictional scope / 管轄範圍 / 管辖范围"""
    INTERNATIONAL = "international"
    REGIONAL_EU = "regional_eu"
    REGIONAL_COE = "regional_coe"
    REGIONAL_AU = "regional_au"
    NATIONAL = "national"


class TopicArea(Enum):
    """Legal topic area / 法律主題領域 / 法律主题领域"""
    FREEDOM_OF_INFORMATION = "freedom_of_information"
    RESIDENCE_RIGHTS = "residence_rights"
    AGENT_DUTY = "agent_duty"
    COMMUNITY_SAFETY = "community_safety"
    LGBTI_RIGHTS = "lgbti_rights"
    AI_GOVERNANCE = "ai_governance"
    HUMAN_RIGHTS_GENERAL = "human_rights_general"
    NON_DISCRIMINATION = "non_discrimination"
    PRIVACY_DATA = "privacy_data"


@dataclass
class LegislativeClause:
    """
    A specific clause/article within a legislative instrument.
    法律文書中的特定條款/條文。
    法律文书中的特定条款/条文。
    """
    clause_id: str
    article_number: str
    title: str
    text: str
    parent_legislation_id: str
    topics: list[TopicArea] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    in_force: bool = True


@dataclass
class Legislation:
    """
    A legislative instrument (treaty, convention, resolution, etc.).
    法律文書（條約、公約、決議等）。
    法律文书（条约、公约、决议等）。
    """
    legislation_id: str
    title: str
    short_title: str
    legislation_type: LegislationType
    jurisdiction: JurisdictionScope
    adoption_date: str
    in_force_date: str
    in_force: bool
    topics: list[TopicArea]
    source_url: str
    clauses: list[LegislativeClause] = field(default_factory=list)
    supporting_act: str = ""  # Original support act reference
    description: str = ""


@dataclass
class CaseLaw:
    """
    A legal case with citation and relevance mapping.
    法律案例及其引用和相關性映射。
    法律案例及其引用和相关性映射。
    """
    case_id: str
    case_name: str
    court: str
    date: str
    citation: str
    jurisdiction: JurisdictionScope
    topics: list[TopicArea]
    summary: str
    key_principles: list[str]
    related_legislation_ids: list[str]
    related_clause_ids: list[str]
    source_url: str = ""


class LegalKnowledgeBase:
    """
    Centralized legal knowledge base containing legislation, clauses,
    and case law for evidence mapping.

    集中式法律知識庫，包含立法、條款和判例法，用於證據映射。
    集中式法律知识库，包含立法、条款和判例法，用于证据映射。
    """

    def __init__(self):
        self.legislation: dict[str, Legislation] = {}
        self.clauses: dict[str, LegislativeClause] = {}
        self.cases: dict[str, CaseLaw] = {}
        self._load_core_legislation()
        self._load_core_cases()

    def _load_core_legislation(self) -> None:
        """Load core international human rights legislation and clauses."""

        # ============================================================
        # 1. UDHR - Universal Declaration of Human Rights (1948)
        # ============================================================
        udhr = Legislation(
            legislation_id="UDHR",
            title="Universal Declaration of Human Rights",
            short_title="UDHR",
            legislation_type=LegislationType.TREATY,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="1948-12-10",
            in_force_date="1948-12-10",
            in_force=True,
            topics=[
                TopicArea.FREEDOM_OF_INFORMATION,
                TopicArea.RESIDENCE_RIGHTS,
                TopicArea.HUMAN_RIGHTS_GENERAL,
                TopicArea.NON_DISCRIMINATION,
            ],
            source_url="https://www.un.org/en/about-us/universal-declaration-of-human-rights",
            supporting_act="UN Charter (1945)",
            description="Foundation of international human rights law, adopted by UN GA Resolution 217A.",
        )
        udhr.clauses = [
            LegislativeClause(
                clause_id="UDHR-Art2",
                article_number="Article 2",
                title="Non-Discrimination",
                text="Everyone is entitled to all the rights and freedoms set forth in this "
                     "Declaration, without distinction of any kind, such as race, colour, sex, "
                     "language, religion, political or other opinion, national or social origin, "
                     "property, birth or other status.",
                parent_legislation_id="UDHR",
                topics=[TopicArea.NON_DISCRIMINATION, TopicArea.LGBTI_RIGHTS],
                keywords=["non-discrimination", "equality", "distinction", "status"],
            ),
            LegislativeClause(
                clause_id="UDHR-Art13",
                article_number="Article 13",
                title="Freedom of Movement and Residence",
                text="(1) Everyone has the right to freedom of movement and residence within the "
                     "borders of each state. (2) Everyone has the right to leave any country, "
                     "including his own, and to return to his country.",
                parent_legislation_id="UDHR",
                topics=[TopicArea.RESIDENCE_RIGHTS],
                keywords=["movement", "residence", "borders", "return"],
            ),
            LegislativeClause(
                clause_id="UDHR-Art19",
                article_number="Article 19",
                title="Freedom of Opinion and Expression",
                text="Everyone has the right to freedom of opinion and expression; this right "
                     "includes freedom to hold opinions without interference and to seek, receive "
                     "and impart information and ideas through any media and regardless of frontiers.",
                parent_legislation_id="UDHR",
                topics=[TopicArea.FREEDOM_OF_INFORMATION],
                keywords=["freedom", "opinion", "expression", "information", "media"],
            ),
            LegislativeClause(
                clause_id="UDHR-Art25",
                article_number="Article 25",
                title="Right to Adequate Standard of Living",
                text="Everyone has the right to a standard of living adequate for the health and "
                     "well-being of himself and of his family, including food, clothing, housing "
                     "and medical care and necessary social services.",
                parent_legislation_id="UDHR",
                topics=[TopicArea.RESIDENCE_RIGHTS, TopicArea.COMMUNITY_SAFETY],
                keywords=["housing", "health", "well-being", "social services"],
            ),
        ]
        self._register_legislation(udhr)

        # ============================================================
        # 2. ICCPR - International Covenant on Civil and Political Rights (1966)
        # ============================================================
        iccpr = Legislation(
            legislation_id="ICCPR",
            title="International Covenant on Civil and Political Rights",
            short_title="ICCPR",
            legislation_type=LegislationType.TREATY,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="1966-12-16",
            in_force_date="1976-03-23",
            in_force=True,
            topics=[
                TopicArea.FREEDOM_OF_INFORMATION,
                TopicArea.RESIDENCE_RIGHTS,
                TopicArea.NON_DISCRIMINATION,
                TopicArea.LGBTI_RIGHTS,
            ],
            source_url="https://www.ohchr.org/en/instruments-mechanisms/instruments/international-covenant-civil-and-political-rights",
            supporting_act="UDHR (1948)",
            description="Legally binding treaty giving effect to civil and political rights in the UDHR.",
        )
        iccpr.clauses = [
            LegislativeClause(
                clause_id="ICCPR-Art2",
                article_number="Article 2",
                title="Non-Discrimination Obligation",
                text="Each State Party to the present Covenant undertakes to respect and to ensure "
                     "to all individuals within its territory and subject to its jurisdiction the "
                     "rights recognized in the present Covenant, without distinction of any kind.",
                parent_legislation_id="ICCPR",
                topics=[TopicArea.NON_DISCRIMINATION, TopicArea.LGBTI_RIGHTS],
                keywords=["state party", "ensure", "distinction", "jurisdiction"],
            ),
            LegislativeClause(
                clause_id="ICCPR-Art12",
                article_number="Article 12",
                title="Liberty of Movement and Freedom to Choose Residence",
                text="(1) Everyone lawfully within the territory of a State shall, within that "
                     "territory, have the right to liberty of movement and freedom to choose his "
                     "residence. (2) Everyone shall be free to leave any country, including his own. "
                     "(3) The above-mentioned rights shall not be subject to any restrictions except "
                     "those which are provided by law.",
                parent_legislation_id="ICCPR",
                topics=[TopicArea.RESIDENCE_RIGHTS],
                keywords=["liberty", "movement", "residence", "restrictions", "law"],
            ),
            LegislativeClause(
                clause_id="ICCPR-Art17",
                article_number="Article 17",
                title="Right to Privacy",
                text="No one shall be subjected to arbitrary or unlawful interference with his "
                     "privacy, family, home or correspondence, nor to unlawful attacks on his "
                     "honour and reputation.",
                parent_legislation_id="ICCPR",
                topics=[TopicArea.PRIVACY_DATA, TopicArea.RESIDENCE_RIGHTS],
                keywords=["privacy", "family", "home", "interference"],
            ),
            LegislativeClause(
                clause_id="ICCPR-Art19",
                article_number="Article 19",
                title="Freedom of Expression and Information",
                text="(1) Everyone shall have the right to hold opinions without interference. "
                     "(2) Everyone shall have the right to freedom of expression; this right shall "
                     "include freedom to seek, receive and impart information and ideas of all kinds.",
                parent_legislation_id="ICCPR",
                topics=[TopicArea.FREEDOM_OF_INFORMATION],
                keywords=["freedom", "expression", "information", "opinions"],
            ),
            LegislativeClause(
                clause_id="ICCPR-Art26",
                article_number="Article 26",
                title="Equality Before the Law",
                text="All persons are equal before the law and are entitled without any "
                     "discrimination to the equal protection of the law. The law shall prohibit "
                     "any discrimination and guarantee to all persons equal and effective protection "
                     "against discrimination on any ground.",
                parent_legislation_id="ICCPR",
                topics=[TopicArea.NON_DISCRIMINATION, TopicArea.LGBTI_RIGHTS],
                keywords=["equal", "law", "discrimination", "protection"],
            ),
        ]
        self._register_legislation(iccpr)

        # ============================================================
        # 3. ICESCR - International Covenant on Economic, Social and Cultural Rights (1966)
        # ============================================================
        icescr = Legislation(
            legislation_id="ICESCR",
            title="International Covenant on Economic, Social and Cultural Rights",
            short_title="ICESCR",
            legislation_type=LegislationType.TREATY,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="1966-12-16",
            in_force_date="1976-01-03",
            in_force=True,
            topics=[
                TopicArea.RESIDENCE_RIGHTS,
                TopicArea.COMMUNITY_SAFETY,
                TopicArea.NON_DISCRIMINATION,
            ],
            source_url="https://www.ohchr.org/en/instruments-mechanisms/instruments/international-covenant-economic-social-and-cultural-rights",
            supporting_act="UDHR (1948)",
            description="Legally binding treaty on economic, social and cultural rights.",
        )
        icescr.clauses = [
            LegislativeClause(
                clause_id="ICESCR-Art2",
                article_number="Article 2(2)",
                title="Non-Discrimination in Economic Rights",
                text="The States Parties to the present Covenant undertake to guarantee that the "
                     "rights enunciated in the present Covenant will be exercised without "
                     "discrimination of any kind as to race, colour, sex, language, religion, "
                     "political or other opinion, national or social origin, property, birth or "
                     "other status.",
                parent_legislation_id="ICESCR",
                topics=[TopicArea.NON_DISCRIMINATION, TopicArea.LGBTI_RIGHTS],
                keywords=["guarantee", "discrimination", "status", "economic rights"],
            ),
            LegislativeClause(
                clause_id="ICESCR-Art11",
                article_number="Article 11",
                title="Right to Adequate Housing",
                text="The States Parties to the present Covenant recognize the right of everyone "
                     "to an adequate standard of living for himself and his family, including "
                     "adequate food, clothing and housing, and to the continuous improvement of "
                     "living conditions.",
                parent_legislation_id="ICESCR",
                topics=[TopicArea.RESIDENCE_RIGHTS, TopicArea.COMMUNITY_SAFETY],
                keywords=["housing", "standard of living", "improvement", "conditions"],
            ),
        ]
        self._register_legislation(icescr)

        # ============================================================
        # 4. ECHR - European Convention on Human Rights (1950)
        # ============================================================
        echr = Legislation(
            legislation_id="ECHR",
            title="European Convention on Human Rights",
            short_title="ECHR",
            legislation_type=LegislationType.CONVENTION,
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            adoption_date="1950-11-04",
            in_force_date="1953-09-03",
            in_force=True,
            topics=[
                TopicArea.FREEDOM_OF_INFORMATION,
                TopicArea.RESIDENCE_RIGHTS,
                TopicArea.COMMUNITY_SAFETY,
                TopicArea.LGBTI_RIGHTS,
                TopicArea.PRIVACY_DATA,
            ],
            source_url="https://www.echr.coe.int/european-convention-on-human-rights",
            supporting_act="UDHR (1948), Statute of the Council of Europe (1949)",
            description="Regional human rights treaty enforced by the European Court of Human Rights.",
        )
        echr.clauses = [
            LegislativeClause(
                clause_id="ECHR-Art8",
                article_number="Article 8",
                title="Right to Respect for Private and Family Life",
                text="(1) Everyone has the right to respect for his private and family life, his "
                     "home and his correspondence. (2) There shall be no interference by a public "
                     "authority with the exercise of this right except such as is in accordance "
                     "with the law and is necessary in a democratic society.",
                parent_legislation_id="ECHR",
                topics=[TopicArea.RESIDENCE_RIGHTS, TopicArea.PRIVACY_DATA, TopicArea.LGBTI_RIGHTS],
                keywords=["private life", "family", "home", "interference", "public authority"],
            ),
            LegislativeClause(
                clause_id="ECHR-Art10",
                article_number="Article 10",
                title="Freedom of Expression",
                text="Everyone has the right to freedom of expression. This right shall include "
                     "freedom to hold opinions and to receive and impart information and ideas "
                     "without interference by public authority and regardless of frontiers.",
                parent_legislation_id="ECHR",
                topics=[TopicArea.FREEDOM_OF_INFORMATION],
                keywords=["expression", "opinions", "information", "public authority"],
            ),
            LegislativeClause(
                clause_id="ECHR-Art14",
                article_number="Article 14",
                title="Prohibition of Discrimination",
                text="The enjoyment of the rights and freedoms set forth in this Convention shall "
                     "be secured without discrimination on any ground such as sex, race, colour, "
                     "language, religion, political or other opinion, national or social origin, "
                     "association with a national minority, property, birth or other status.",
                parent_legislation_id="ECHR",
                topics=[TopicArea.NON_DISCRIMINATION, TopicArea.LGBTI_RIGHTS],
                keywords=["discrimination", "rights", "freedoms", "status"],
            ),
            LegislativeClause(
                clause_id="ECHR-P4-Art2",
                article_number="Protocol 4, Article 2",
                title="Freedom of Movement",
                text="Everyone lawfully within the territory of a State shall, within that "
                     "territory, have the right to liberty of movement and freedom to choose "
                     "his residence.",
                parent_legislation_id="ECHR",
                topics=[TopicArea.RESIDENCE_RIGHTS],
                keywords=["movement", "residence", "territory", "liberty"],
            ),
        ]
        self._register_legislation(echr)

        # ============================================================
        # 5. Yogyakarta Principles (2006, updated 2017)
        # ============================================================
        yogyakarta = Legislation(
            legislation_id="YOGYAKARTA",
            title="Yogyakarta Principles on the Application of International Human Rights Law "
                  "in Relation to Sexual Orientation and Gender Identity",
            short_title="Yogyakarta Principles",
            legislation_type=LegislationType.GUIDELINE,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="2006-11-09",
            in_force_date="2006-11-09",
            in_force=True,
            topics=[TopicArea.LGBTI_RIGHTS, TopicArea.NON_DISCRIMINATION,
                    TopicArea.RESIDENCE_RIGHTS],
            source_url="https://yogyakartaprinciples.org/",
            supporting_act="UDHR (1948), ICCPR (1966)",
            description="Expert principles on applying international human rights law to "
                        "sexual orientation and gender identity.",
        )
        yogyakarta.clauses = [
            LegislativeClause(
                clause_id="YP-P2",
                article_number="Principle 2",
                title="Right to Equality and Non-Discrimination",
                text="Everyone is entitled to enjoy all human rights without discrimination on "
                     "the basis of sexual orientation or gender identity. Everyone is entitled to "
                     "equal protection of the law without any such discrimination.",
                parent_legislation_id="YOGYAKARTA",
                topics=[TopicArea.LGBTI_RIGHTS, TopicArea.NON_DISCRIMINATION],
                keywords=["equality", "non-discrimination", "sexual orientation", "gender identity"],
            ),
            LegislativeClause(
                clause_id="YP-P15",
                article_number="Principle 15",
                title="Right to Adequate Housing",
                text="Everyone has the right to adequate housing, without discrimination on the "
                     "basis of sexual orientation or gender identity, including protections against "
                     "eviction.",
                parent_legislation_id="YOGYAKARTA",
                topics=[TopicArea.LGBTI_RIGHTS, TopicArea.RESIDENCE_RIGHTS],
                keywords=["housing", "eviction", "sexual orientation", "gender identity"],
            ),
            LegislativeClause(
                clause_id="YP-P22",
                article_number="Principle 22",
                title="Right to Freedom of Movement",
                text="Everyone lawfully within a State has the right to freedom of movement and "
                     "to choose their place of residence, regardless of sexual orientation or "
                     "gender identity.",
                parent_legislation_id="YOGYAKARTA",
                topics=[TopicArea.LGBTI_RIGHTS, TopicArea.RESIDENCE_RIGHTS],
                keywords=["movement", "residence", "sexual orientation"],
            ),
        ]
        self._register_legislation(yogyakarta)

        # ============================================================
        # 6. UN GA Resolution on AI (2024)
        # ============================================================
        un_ai_res = Legislation(
            legislation_id="UNGA-AI-2024",
            title="UN General Assembly Resolution: Seizing the Opportunities of Safe, Secure "
                  "and Trustworthy Artificial Intelligence Systems for Sustainable Development",
            short_title="UN GA AI Resolution (A/78/L.49)",
            legislation_type=LegislationType.RESOLUTION,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="2024-03-21",
            in_force_date="2024-03-21",
            in_force=True,
            topics=[TopicArea.AI_GOVERNANCE, TopicArea.HUMAN_RIGHTS_GENERAL],
            source_url="https://press.un.org/en/2024/ga12588.doc.htm",
            supporting_act="UN Charter, UDHR",
            description="First-ever UN General Assembly resolution on AI governance, "
                        "adopted unanimously by 193 member states.",
        )
        un_ai_res.clauses = [
            LegislativeClause(
                clause_id="UNGA-AI-OP1",
                article_number="Operative Paragraph 1",
                title="Human-Centric AI Development",
                text="Affirms that the design, development, deployment and use of artificial "
                     "intelligence systems should be consistent with obligations under "
                     "international law, in particular international human rights law.",
                parent_legislation_id="UNGA-AI-2024",
                topics=[TopicArea.AI_GOVERNANCE, TopicArea.HUMAN_RIGHTS_GENERAL],
                keywords=["AI", "human rights", "international law", "design", "deployment"],
            ),
            LegislativeClause(
                clause_id="UNGA-AI-OP5",
                article_number="Operative Paragraph 5",
                title="AI and Non-Discrimination",
                text="Recognizes the potential risks of AI systems that may reinforce or "
                     "exacerbate existing inequalities, biases and discrimination, and stresses "
                     "the need for AI systems to respect the principle of non-discrimination.",
                parent_legislation_id="UNGA-AI-2024",
                topics=[TopicArea.AI_GOVERNANCE, TopicArea.NON_DISCRIMINATION],
                keywords=["AI", "bias", "discrimination", "inequality", "risk"],
            ),
        ]
        self._register_legislation(un_ai_res)

        # ============================================================
        # 7. Council of Europe AI Framework Convention (2024)
        # ============================================================
        coe_ai = Legislation(
            legislation_id="COE-AI-CONV-2024",
            title="Council of Europe Framework Convention on Artificial Intelligence and "
                  "Human Rights, Democracy and the Rule of Law",
            short_title="CoE AI Framework Convention",
            legislation_type=LegislationType.CONVENTION,
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            adoption_date="2024-05-17",
            in_force_date="2024-09-05",
            in_force=True,
            topics=[TopicArea.AI_GOVERNANCE, TopicArea.HUMAN_RIGHTS_GENERAL,
                    TopicArea.NON_DISCRIMINATION, TopicArea.PRIVACY_DATA],
            source_url="https://www.coe.int/en/web/artificial-intelligence/the-framework-convention-on-ai",
            supporting_act="ECHR (1950), Convention 108+",
            description="First legally binding international treaty on AI, "
                        "embedding human rights in AI governance.",
        )
        coe_ai.clauses = [
            LegislativeClause(
                clause_id="COE-AI-Art4",
                article_number="Article 4",
                title="Protection of Human Rights",
                text="Each Party shall adopt or maintain measures to ensure that activities "
                     "within the lifecycle of AI systems are consistent with obligations to "
                     "protect human rights as enshrined in applicable international law and "
                     "its domestic law.",
                parent_legislation_id="COE-AI-CONV-2024",
                topics=[TopicArea.AI_GOVERNANCE, TopicArea.HUMAN_RIGHTS_GENERAL],
                keywords=["AI lifecycle", "human rights", "domestic law", "obligations"],
            ),
            LegislativeClause(
                clause_id="COE-AI-Art10",
                article_number="Article 10",
                title="Non-Discrimination and Equality",
                text="Each Party shall adopt or maintain measures to ensure that AI systems "
                     "do not lead to undue discrimination or inequality.",
                parent_legislation_id="COE-AI-CONV-2024",
                topics=[TopicArea.AI_GOVERNANCE, TopicArea.NON_DISCRIMINATION],
                keywords=["AI", "discrimination", "equality", "measures"],
            ),
        ]
        self._register_legislation(coe_ai)

        # ============================================================
        # 8. UN HRC Resolutions on SOGI (Sexual Orientation & Gender Identity)
        # ============================================================
        hrc_sogi = Legislation(
            legislation_id="HRC-SOGI-2024",
            title="UN Human Rights Council Resolution on Combatting Discrimination Against "
                  "Intersex Persons (A/HRC/RES/55/14)",
            short_title="HRC Intersex Protection Resolution",
            legislation_type=LegislationType.RESOLUTION,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="2024-04-04",
            in_force_date="2024-04-04",
            in_force=True,
            topics=[TopicArea.LGBTI_RIGHTS, TopicArea.NON_DISCRIMINATION,
                    TopicArea.COMMUNITY_SAFETY],
            source_url="https://www.ohchr.org/en/sexual-orientation-and-gender-identity/united-nations-resolutions-sexual-orientation-gender-identity-and-sex-characteristics",
            supporting_act="UDHR, ICCPR, ICESCR",
            description="Resolution expressing grave concern about violence and harmful "
                        "practices against intersex persons.",
        )
        hrc_sogi.clauses = [
            LegislativeClause(
                clause_id="HRC-SOGI-OP2",
                article_number="Operative Paragraph 2",
                title="Protection from Harmful Practices",
                text="Calls upon States to take measures to end harmful practices, including "
                     "unnecessary medical interventions, on intersex persons carried out without "
                     "their free, prior and informed consent.",
                parent_legislation_id="HRC-SOGI-2024",
                topics=[TopicArea.LGBTI_RIGHTS, TopicArea.COMMUNITY_SAFETY],
                keywords=["harmful practices", "intersex", "consent", "medical"],
            ),
        ]
        self._register_legislation(hrc_sogi)

        # ============================================================
        # 9. UN Guiding Principles on Business and Human Rights (2011)
        # ============================================================
        ungp = Legislation(
            legislation_id="UNGP-BHR",
            title="UN Guiding Principles on Business and Human Rights",
            short_title="UNGPs",
            legislation_type=LegislationType.GUIDELINE,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="2011-06-16",
            in_force_date="2011-06-16",
            in_force=True,
            topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY,
                    TopicArea.HUMAN_RIGHTS_GENERAL],
            source_url="https://www.ohchr.org/en/publications/reference-publications/guiding-principles-business-and-human-rights",
            supporting_act="UDHR, ICCPR, ICESCR",
            description="Authoritative global standard on the respective duties of States and "
                        "responsibilities of business enterprises regarding human rights.",
        )
        ungp.clauses = [
            LegislativeClause(
                clause_id="UNGP-P1",
                article_number="Principle 1",
                title="State Duty to Protect",
                text="States must protect against human rights abuse within their territory "
                     "and/or jurisdiction by third parties, including business enterprises. This "
                     "requires taking appropriate steps to prevent, investigate, punish and "
                     "redress such abuse through effective policies, legislation, regulations "
                     "and adjudication.",
                parent_legislation_id="UNGP-BHR",
                topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY],
                keywords=["state duty", "protect", "prevent", "investigate", "redress"],
            ),
            LegislativeClause(
                clause_id="UNGP-P11",
                article_number="Principle 11",
                title="Corporate Responsibility to Respect",
                text="Business enterprises should respect human rights. This means that they "
                     "should avoid infringing on the human rights of others and should address "
                     "adverse human rights impacts with which they are involved.",
                parent_legislation_id="UNGP-BHR",
                topics=[TopicArea.AGENT_DUTY],
                keywords=["business", "respect", "infringing", "adverse impacts"],
            ),
            LegislativeClause(
                clause_id="UNGP-P15",
                article_number="Principle 15",
                title="Human Rights Due Diligence",
                text="In order to identify, prevent, mitigate and account for how they address "
                     "their adverse human rights impacts, business enterprises should carry out "
                     "human rights due diligence.",
                parent_legislation_id="UNGP-BHR",
                topics=[TopicArea.AGENT_DUTY, TopicArea.AI_GOVERNANCE],
                keywords=["due diligence", "identify", "prevent", "mitigate"],
            ),
        ]
        self._register_legislation(ungp)

        # ============================================================
        # 10. Freedom of Information Act (Model) & Access to Information
        # ============================================================
        foia_model = Legislation(
            legislation_id="UN-AI-ACCESS",
            title="UN Model Law on Access to Information",
            short_title="UN Access to Information",
            legislation_type=LegislationType.FRAMEWORK,
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            adoption_date="2020-09-28",
            in_force_date="2020-09-28",
            in_force=True,
            topics=[TopicArea.FREEDOM_OF_INFORMATION, TopicArea.AGENT_DUTY],
            source_url="https://www.un.org/ruleoflaw/thematic-areas/governance/freedom-of-information/",
            supporting_act="UDHR Art.19, ICCPR Art.19",
            description="Framework for national freedom of information legislation, "
                        "promoting transparency and accountability.",
        )
        foia_model.clauses = [
            LegislativeClause(
                clause_id="UN-AI-P1",
                article_number="Principle 1",
                title="Maximum Disclosure",
                text="Public bodies have an obligation to disclose information and every member "
                     "of the public has a corresponding right to receive information. All "
                     "information held by public bodies is subject to disclosure.",
                parent_legislation_id="UN-AI-ACCESS",
                topics=[TopicArea.FREEDOM_OF_INFORMATION],
                keywords=["disclosure", "public bodies", "obligation", "right to receive"],
            ),
            LegislativeClause(
                clause_id="UN-AI-P4",
                article_number="Principle 4",
                title="Agent Duty of Proactive Disclosure",
                text="Public authorities should be required to proactively publish and "
                     "disseminate information of general public interest. Agents of the state "
                     "have a positive duty to ensure information accessibility.",
                parent_legislation_id="UN-AI-ACCESS",
                topics=[TopicArea.FREEDOM_OF_INFORMATION, TopicArea.AGENT_DUTY],
                keywords=["proactive disclosure", "public interest", "agent duty", "accessibility"],
            ),
        ]
        self._register_legislation(foia_model)

    def _load_core_cases(self) -> None:
        """Load landmark and recent case law across all topic areas."""

        # ============================================================
        # FREEDOM OF INFORMATION - 5 Cases
        # ============================================================
        self._register_case(CaseLaw(
            case_id="FOI-001",
            case_name="Magyar Helsinki Bizottság v. Hungary",
            court="European Court of Human Rights (Grand Chamber)",
            date="2016-11-08",
            citation="[2016] ECHR 975, App. No. 18030/11",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.FREEDOM_OF_INFORMATION],
            summary="The Grand Chamber established that the right of access to information "
                    "held by public authorities is protected under Article 10 ECHR when access "
                    "is instrumental for the exercise of freedom of expression.",
            key_principles=[
                "Right of access to state-held information under Art.10 ECHR",
                "Information monopoly of the state creates positive obligation",
                "Public watchdog function of NGOs and journalists",
            ],
            related_legislation_ids=["ECHR", "ICCPR"],
            related_clause_ids=["ECHR-Art10", "ICCPR-Art19"],
        ))

        self._register_case(CaseLaw(
            case_id="FOI-002",
            case_name="Claude Reyes et al. v. Chile",
            court="Inter-American Court of Human Rights",
            date="2006-09-19",
            citation="Series C No. 151",
            jurisdiction=JurisdictionScope.INTERNATIONAL,
            topics=[TopicArea.FREEDOM_OF_INFORMATION],
            summary="First international court decision to recognize the right of access to "
                    "state-held information as a fundamental human right under Article 13 ACHR.",
            key_principles=[
                "Access to information is a fundamental right",
                "States have a positive obligation to provide information",
                "Restrictions must meet strict necessity test",
            ],
            related_legislation_ids=["UDHR", "ICCPR"],
            related_clause_ids=["UDHR-Art19", "ICCPR-Art19"],
        ))

        self._register_case(CaseLaw(
            case_id="FOI-003",
            case_name="Társaság a Szabadságjogokért v. Hungary",
            court="European Court of Human Rights",
            date="2009-04-14",
            citation="App. No. 37374/05",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.FREEDOM_OF_INFORMATION],
            summary="The Court held that refusal to grant an NGO access to a constitutional "
                    "complaint violated Article 10. The state cannot create informational monopolies.",
            key_principles=[
                "NGOs as social watchdogs with informational rights",
                "State informational monopoly is a form of censorship",
                "Public interest outweighs secrecy in legal proceedings",
            ],
            related_legislation_ids=["ECHR"],
            related_clause_ids=["ECHR-Art10"],
        ))

        self._register_case(CaseLaw(
            case_id="FOI-004",
            case_name="Cengiz and Others v. Turkey",
            court="European Court of Human Rights",
            date="2015-12-01",
            citation="App. Nos. 48226/10 and 14027/11",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.FREEDOM_OF_INFORMATION],
            summary="Court found that blocking access to YouTube violated freedom of expression "
                    "under Article 10. The right to receive information includes online sources.",
            key_principles=[
                "Internet access as component of freedom of information",
                "Blanket blocking of websites disproportionate",
                "Digital age interpretation of Art.10 rights",
            ],
            related_legislation_ids=["ECHR"],
            related_clause_ids=["ECHR-Art10"],
        ))

        self._register_case(CaseLaw(
            case_id="FOI-005",
            case_name="Breyer v. Germany",
            court="Court of Justice of the European Union",
            date="2024-03-14",
            citation="Case C-479/22",
            jurisdiction=JurisdictionScope.REGIONAL_EU,
            topics=[TopicArea.FREEDOM_OF_INFORMATION, TopicArea.PRIVACY_DATA],
            summary="CJEU ruled on the balance between access to information and data protection, "
                    "establishing principles for transparency in the digital context.",
            key_principles=[
                "Balancing transparency with data protection",
                "Public access to documents as fundamental right",
                "Proportionality in restricting information access",
            ],
            related_legislation_ids=["ECHR", "ICCPR"],
            related_clause_ids=["ECHR-Art10", "ICCPR-Art19"],
        ))

        # ============================================================
        # RESIDENCE RIGHTS & REGULATIONS - 5 Cases
        # ============================================================
        self._register_case(CaseLaw(
            case_id="RES-001",
            case_name="Hynek v. Islington London Borough Council",
            court="England and Wales High Court",
            date="2024-06-15",
            citation="[2024] EWHC 1465 (Admin)",
            jurisdiction=JurisdictionScope.NATIONAL,
            topics=[TopicArea.RESIDENCE_RIGHTS, TopicArea.COMMUNITY_SAFETY],
            summary="Court considered whether there had been a breach of Article 1 Protocol 1 "
                    "ECHR in respect of a homeless applicant who did not have a right to reside "
                    "in the UK. Addressed residence requirements for housing assistance.",
            key_principles=[
                "Residence status and housing rights intersection",
                "Proportionality of residence requirements",
                "Vulnerability assessment in housing decisions",
            ],
            related_legislation_ids=["ECHR", "ICESCR"],
            related_clause_ids=["ECHR-Art8", "ICESCR-Art11"],
        ))

        self._register_case(CaseLaw(
            case_id="RES-002",
            case_name="Simonova v. Bulgaria",
            court="European Court of Human Rights",
            date="2024-01-23",
            citation="App. No. 30782/16",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.RESIDENCE_RIGHTS],
            summary="Demolition of a home constructed in breach of planning control was found "
                    "to have breached Article 8 ECHR. The state failed to properly balance "
                    "planning enforcement with the right to respect for the home.",
            key_principles=[
                "Right to home under Art.8 applies even to irregular constructions",
                "Proportionality test for demolition orders",
                "State obligation to consider personal circumstances",
            ],
            related_legislation_ids=["ECHR"],
            related_clause_ids=["ECHR-Art8"],
        ))

        self._register_case(CaseLaw(
            case_id="RES-003",
            case_name="Ukraine and the Netherlands v. Russia",
            court="European Court of Human Rights (Grand Chamber)",
            date="2025-07-09",
            citation="App. Nos. 8019/16 etc.",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.RESIDENCE_RIGHTS, TopicArea.COMMUNITY_SAFETY,
                    TopicArea.HUMAN_RIGHTS_GENERAL],
            summary="Grand Chamber addressed multiple convention rights including the right "
                    "to life, prohibition of torture, liberty, and private/family life in the "
                    "context of territorial control and displacement.",
            key_principles=[
                "State responsibility for human rights in controlled territories",
                "Protection of displaced persons' residence rights",
                "Extraterritorial obligations under ECHR",
            ],
            related_legislation_ids=["ECHR", "ICCPR"],
            related_clause_ids=["ECHR-Art8", "ECHR-P4-Art2", "ICCPR-Art12"],
        ))

        self._register_case(CaseLaw(
            case_id="RES-004",
            case_name="Saadi v. United Kingdom",
            court="European Court of Human Rights (Grand Chamber)",
            date="2008-01-29",
            citation="[2008] ECHR 80",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.RESIDENCE_RIGHTS],
            summary="Grand Chamber considered whether detention of asylum seekers on arrival "
                    "at port of entry was compatible with Article 5(1)(f) ECHR. Established "
                    "principles for immigration detention and residence rights.",
            key_principles=[
                "Immigration detention must not be arbitrary",
                "Good faith requirement for state agents",
                "Balance between immigration control and individual rights",
            ],
            related_legislation_ids=["ECHR", "ICCPR"],
            related_clause_ids=["ECHR-Art8", "ICCPR-Art12"],
        ))

        self._register_case(CaseLaw(
            case_id="RES-005",
            case_name="N.D. and N.T. v. Spain",
            court="European Court of Human Rights (Grand Chamber)",
            date="2020-02-13",
            citation="App. Nos. 8675/15 and 8697/15",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.RESIDENCE_RIGHTS],
            summary="Grand Chamber addressed collective expulsion at the border and the duty "
                    "of states to provide genuine access to means of legal entry.",
            key_principles=[
                "Prohibition of collective expulsion",
                "States must provide genuine access to legal entry",
                "Agent duty to assess individual circumstances",
            ],
            related_legislation_ids=["ECHR"],
            related_clause_ids=["ECHR-P4-Art2", "ECHR-Art8"],
        ))

        # ============================================================
        # AGENT DUTY & COMMUNITY SAFETY - 5 Cases
        # ============================================================
        self._register_case(CaseLaw(
            case_id="AGT-001",
            case_name="Osman v. United Kingdom",
            court="European Court of Human Rights",
            date="1998-10-28",
            citation="[1998] ECHR 101",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY],
            summary="Established the 'Osman test' for positive obligations of state agents "
                    "to protect individuals against threats to life. Agents have a duty to take "
                    "preventive measures where there is a real and immediate risk.",
            key_principles=[
                "State agents' positive obligation to protect life (Art.2)",
                "Real and immediate risk test",
                "Reasonable measures standard for agent conduct",
            ],
            related_legislation_ids=["ECHR", "ICCPR"],
            related_clause_ids=["ECHR-Art8"],
        ))

        self._register_case(CaseLaw(
            case_id="AGT-002",
            case_name="Opuz v. Turkey",
            court="European Court of Human Rights",
            date="2009-06-09",
            citation="App. No. 33401/02",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY,
                    TopicArea.NON_DISCRIMINATION],
            summary="Court held Turkey violated Articles 2, 3, and 14 by failing to protect "
                    "a woman and her mother from domestic violence. Established that state "
                    "agents' failure to act constitutes a breach of duty.",
            key_principles=[
                "State agent duty to protect from domestic violence",
                "Due diligence obligation in community safety",
                "Systemic failure as discrimination",
            ],
            related_legislation_ids=["ECHR"],
            related_clause_ids=["ECHR-Art8", "ECHR-Art14"],
        ))

        self._register_case(CaseLaw(
            case_id="AGT-003",
            case_name="Neulinger and Shuruk v. Switzerland",
            court="European Court of Human Rights (Grand Chamber)",
            date="2010-07-06",
            citation="App. No. 41615/07",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY,
                    TopicArea.RESIDENCE_RIGHTS],
            summary="Grand Chamber stressed the obligation of agents to conduct an in-depth "
                    "examination of the family situation before ordering return of a child, "
                    "balancing the child's best interests with residence rights.",
            key_principles=[
                "Agent duty for in-depth assessment",
                "Best interests of the child paramount",
                "Community safety includes family protection",
            ],
            related_legislation_ids=["ECHR", "ICCPR"],
            related_clause_ids=["ECHR-Art8", "ICCPR-Art17"],
        ))

        self._register_case(CaseLaw(
            case_id="AGT-004",
            case_name="Vedova and Others v. Italy",
            court="European Court of Human Rights",
            date="2024-09-19",
            citation="App. No. 38520/18",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY],
            summary="Court found Italy violated Article 2 due to state agents' failure to "
                    "take adequate preventive measures despite prior warnings of danger. "
                    "Reinforced the Osman positive obligation framework.",
            key_principles=[
                "Agent failure to act on prior warnings",
                "Updated Osman test application",
                "State liability for systemic protection failures",
            ],
            related_legislation_ids=["ECHR"],
            related_clause_ids=["ECHR-Art8"],
        ))

        self._register_case(CaseLaw(
            case_id="AGT-005",
            case_name="Kurt v. Austria",
            court="European Court of Human Rights (Grand Chamber)",
            date="2021-06-15",
            citation="App. No. 62903/15",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.AGENT_DUTY, TopicArea.COMMUNITY_SAFETY],
            summary="Grand Chamber clarified the scope of the Osman positive obligation in "
                    "the context of domestic violence. Agents must conduct autonomous, proactive "
                    "and comprehensive risk assessments.",
            key_principles=[
                "Autonomous risk assessment duty of agents",
                "Proactive investigation obligation",
                "Community safety as systemic state duty",
            ],
            related_legislation_ids=["ECHR"],
            related_clause_ids=["ECHR-Art8"],
        ))

        # ============================================================
        # LGBTI RIGHTS - 5 Cases
        # ============================================================
        self._register_case(CaseLaw(
            case_id="LGBTI-001",
            case_name="Semenya v. Switzerland",
            court="European Court of Human Rights (Grand Chamber)",
            date="2025-07-10",
            citation="App. No. 10934/21",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.LGBTI_RIGHTS, TopicArea.NON_DISCRIMINATION],
            summary="Grand Chamber case concerning sex classification regulations and their "
                    "impact on athletes with differences in sex development. Addressed "
                    "discrimination based on sex characteristics.",
            key_principles=[
                "Protection from discrimination based on sex characteristics",
                "Proportionality of biological classification rules",
                "Intersection of privacy and anti-discrimination rights",
            ],
            related_legislation_ids=["ECHR", "YOGYAKARTA"],
            related_clause_ids=["ECHR-Art8", "ECHR-Art14", "YP-P2"],
        ))

        self._register_case(CaseLaw(
            case_id="LGBTI-002",
            case_name="Fedotova and Others v. Russia",
            court="European Court of Human Rights (Grand Chamber)",
            date="2023-01-17",
            citation="App. Nos. 40792/10 etc.",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.LGBTI_RIGHTS, TopicArea.RESIDENCE_RIGHTS],
            summary="Grand Chamber held that Russia's failure to provide any form of legal "
                    "recognition for same-sex couples violated Article 8 ECHR. States have a "
                    "positive obligation to provide a legal framework for same-sex partnerships.",
            key_principles=[
                "Positive obligation to recognize same-sex partnerships",
                "Family life protection extends to same-sex couples",
                "Residence and housing rights for same-sex families",
            ],
            related_legislation_ids=["ECHR", "YOGYAKARTA"],
            related_clause_ids=["ECHR-Art8", "ECHR-Art14", "YP-P2"],
        ))

        self._register_case(CaseLaw(
            case_id="LGBTI-003",
            case_name="Identoba and Others v. Georgia",
            court="European Court of Human Rights",
            date="2015-05-12",
            citation="App. No. 73235/12",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.LGBTI_RIGHTS, TopicArea.COMMUNITY_SAFETY,
                    TopicArea.AGENT_DUTY],
            summary="Court found Georgia violated Articles 3, 8, and 14 by failing to protect "
                    "LGBTI marchers from violent attacks. State agents have a duty to protect "
                    "the safety of LGBTI individuals in public spaces.",
            key_principles=[
                "Agent duty to protect LGBTI persons from violence",
                "Community safety obligation for public assemblies",
                "Discrimination combined with failure to protect",
            ],
            related_legislation_ids=["ECHR", "YOGYAKARTA"],
            related_clause_ids=["ECHR-Art8", "ECHR-Art14", "YP-P2"],
        ))

        self._register_case(CaseLaw(
            case_id="LGBTI-004",
            case_name="Alekseyev v. Russia",
            court="European Court of Human Rights",
            date="2010-10-21",
            citation="App. Nos. 4916/07 etc.",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.LGBTI_RIGHTS, TopicArea.FREEDOM_OF_INFORMATION],
            summary="Court held that repeated bans on Pride marches in Moscow violated "
                    "Articles 11, 13, and 14 ECHR. Freedom of assembly and expression for "
                    "LGBTI communities is protected.",
            key_principles=[
                "Freedom of assembly for LGBTI communities",
                "Prohibition of discrimination in exercising Convention rights",
                "State duty to facilitate peaceful protest",
            ],
            related_legislation_ids=["ECHR", "ICCPR"],
            related_clause_ids=["ECHR-Art10", "ECHR-Art14", "ICCPR-Art19"],
        ))

        self._register_case(CaseLaw(
            case_id="LGBTI-005",
            case_name="Rana v. Hungary",
            court="European Court of Human Rights",
            date="2024-05-16",
            citation="App. No. 40888/17",
            jurisdiction=JurisdictionScope.REGIONAL_COE,
            topics=[TopicArea.LGBTI_RIGHTS, TopicArea.RESIDENCE_RIGHTS,
                    TopicArea.NON_DISCRIMINATION],
            summary="Court addressed discrimination in residence and partnership recognition "
                    "for same-sex couples under Hungarian law, finding violations of Articles "
                    "8 and 14 ECHR.",
            key_principles=[
                "Residence rights extend to same-sex partners",
                "Immigration rules must not discriminate on SOGI grounds",
                "Legal recognition linked to residence entitlements",
            ],
            related_legislation_ids=["ECHR", "YOGYAKARTA"],
            related_clause_ids=["ECHR-Art8", "ECHR-Art14", "YP-P15", "YP-P22"],
        ))

        # ============================================================
        # AI GOVERNANCE & HUMAN RIGHTS - 5 Cases
        # ============================================================
        self._register_case(CaseLaw(
            case_id="AI-001",
            case_name="Loomis v. Wisconsin",
            court="Supreme Court of Wisconsin (USA)",
            date="2016-07-13",
            citation="881 N.W.2d 749 (Wis. 2016)",
            jurisdiction=JurisdictionScope.NATIONAL,
            topics=[TopicArea.AI_GOVERNANCE, TopicArea.NON_DISCRIMINATION],
            summary="Court upheld use of COMPAS algorithmic risk assessment in sentencing "
                    "but required warnings about its limitations. First major case addressing "
                    "AI in criminal justice decisions.",
            key_principles=[
                "AI tools in judicial decisions require transparency warnings",
                "Right to be informed of algorithmic factors",
                "Due process applies to AI-assisted decisions",
            ],
            related_legislation_ids=["UNGA-AI-2024"],
            related_clause_ids=["UNGA-AI-OP1", "UNGA-AI-OP5"],
        ))

        self._register_case(CaseLaw(
            case_id="AI-002",
            case_name="SyRI Case (NJCM v. Netherlands)",
            court="District Court of The Hague",
            date="2020-02-05",
            citation="ECLI:NL:RBDHA:2020:1878",
            jurisdiction=JurisdictionScope.NATIONAL,
            topics=[TopicArea.AI_GOVERNANCE, TopicArea.PRIVACY_DATA,
                    TopicArea.NON_DISCRIMINATION],
            summary="Court struck down the Dutch System Risk Indication (SyRI) as violating "
                    "Article 8 ECHR. The AI surveillance system disproportionately targeted "
                    "lower-income neighborhoods.",
            key_principles=[
                "AI surveillance must respect right to private life",
                "Algorithmic profiling requires proportionality assessment",
                "Disproportionate impact on vulnerable communities prohibited",
            ],
            related_legislation_ids=["ECHR", "COE-AI-CONV-2024"],
            related_clause_ids=["ECHR-Art8", "ECHR-Art14", "COE-AI-Art4"],
        ))

        self._register_case(CaseLaw(
            case_id="AI-003",
            case_name="Bridges v. South Wales Police",
            court="Court of Appeal (England and Wales)",
            date="2020-08-11",
            citation="[2020] EWCA Civ 1058",
            jurisdiction=JurisdictionScope.NATIONAL,
            topics=[TopicArea.AI_GOVERNANCE, TopicArea.PRIVACY_DATA,
                    TopicArea.COMMUNITY_SAFETY],
            summary="Court held that police use of automated facial recognition technology "
                    "was unlawful due to insufficient legal framework and failure to assess "
                    "discrimination risks.",
            key_principles=[
                "AI facial recognition requires specific legal basis",
                "Agents must assess discrimination risk of AI tools",
                "Community safety does not override privacy without safeguards",
            ],
            related_legislation_ids=["ECHR", "COE-AI-CONV-2024"],
            related_clause_ids=["ECHR-Art8", "COE-AI-Art4", "COE-AI-Art10"],
        ))

        self._register_case(CaseLaw(
            case_id="AI-004",
            case_name="Uber BV v. Aslam (Algorithmic Management)",
            court="UK Supreme Court",
            date="2021-02-19",
            citation="[2021] UKSC 5",
            jurisdiction=JurisdictionScope.NATIONAL,
            topics=[TopicArea.AI_GOVERNANCE, TopicArea.AGENT_DUTY],
            summary="Supreme Court examined algorithmic management of workers, finding Uber "
                    "drivers were workers entitled to employment rights despite AI-mediated "
                    "control. Addressed AI agents' duty in labor contexts.",
            key_principles=[
                "Algorithmic management does not negate employment obligations",
                "AI-mediated control creates agent duty of care",
                "Worker rights persist regardless of AI intermediation",
            ],
            related_legislation_ids=["UNGP-BHR", "UNGA-AI-2024"],
            related_clause_ids=["UNGP-P11", "UNGP-P15", "UNGA-AI-OP1"],
        ))

        self._register_case(CaseLaw(
            case_id="AI-005",
            case_name="CNIL v. Clearview AI",
            court="French Data Protection Authority (CNIL)",
            date="2022-10-20",
            citation="Decision No. SAN-2022-019",
            jurisdiction=JurisdictionScope.NATIONAL,
            topics=[TopicArea.AI_GOVERNANCE, TopicArea.PRIVACY_DATA,
                    TopicArea.NON_DISCRIMINATION],
            summary="CNIL fined Clearview AI €20 million for mass collection of facial images "
                    "without consent. Established that AI-driven biometric data collection "
                    "violates data protection and human rights.",
            key_principles=[
                "Mass AI biometric collection violates human rights",
                "Consent required for AI facial recognition databases",
                "Extraterritorial application of data protection to AI companies",
            ],
            related_legislation_ids=["ECHR", "COE-AI-CONV-2024"],
            related_clause_ids=["ECHR-Art8", "COE-AI-Art4", "COE-AI-Art10"],
        ))

    def _register_legislation(self, leg: Legislation) -> None:
        """Register legislation and its clauses in the knowledge base."""
        self.legislation[leg.legislation_id] = leg
        for clause in leg.clauses:
            self.clauses[clause.clause_id] = clause

    def _register_case(self, case: CaseLaw) -> None:
        """Register a case in the knowledge base."""
        self.cases[case.case_id] = case

    # ------------------------------------------------------------------
    # Query methods / 查詢方法 / 查询方法
    # ------------------------------------------------------------------

    def get_legislation_by_topic(self, topic: TopicArea) -> list[Legislation]:
        """Get all legislation related to a topic."""
        return [leg for leg in self.legislation.values() if topic in leg.topics]

    def get_clauses_by_topic(self, topic: TopicArea) -> list[LegislativeClause]:
        """Get all clauses related to a topic."""
        return [cl for cl in self.clauses.values() if topic in cl.topics]

    def get_cases_by_topic(self, topic: TopicArea) -> list[CaseLaw]:
        """Get all cases related to a topic."""
        return [c for c in self.cases.values() if topic in c.topics]

    def get_in_force_legislation(self) -> list[Legislation]:
        """Get all currently in-force legislation."""
        return [leg for leg in self.legislation.values() if leg.in_force]

    def get_cases_for_clause(self, clause_id: str) -> list[CaseLaw]:
        """Get all cases that reference a specific clause."""
        return [c for c in self.cases.values() if clause_id in c.related_clause_ids]

    def get_clause(self, clause_id: str) -> LegislativeClause | None:
        """Get a specific clause by ID."""
        return self.clauses.get(clause_id)

    def get_legislation(self, legislation_id: str) -> Legislation | None:
        """Get a specific legislation by ID."""
        return self.legislation.get(legislation_id)

    def search_clauses(self, keywords: list[str]) -> list[LegislativeClause]:
        """Search clauses by keywords with relevance scoring."""
        results = []
        for clause in self.clauses.values():
            clause_text = f"{clause.title} {clause.text} {' '.join(clause.keywords)}".lower()
            matches = sum(1 for kw in keywords if kw.lower() in clause_text)
            if matches > 0:
                results.append((matches, clause))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results]

    def get_stats(self) -> dict[str, Any]:
        """Get knowledge base statistics."""
        return {
            "total_legislation": len(self.legislation),
            "total_clauses": len(self.clauses),
            "total_cases": len(self.cases),
            "in_force_legislation": len(self.get_in_force_legislation()),
            "topics_covered": len(TopicArea),
        }

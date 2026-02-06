"""
NLU Pipeline / NLU 管線 / NLU 管线
===================================
Natural Language Understanding pipeline using spaCy and jieba.
使用 spaCy 和 jieba 的自然語言理解管線。
使用 spaCy 和 jieba 的自然语言理解管线。

Integration Points / 接入點 / 接入点:
- Entity extraction → entity_memory table
  實體提取 → entity_memory 表 / 实体提取 → entity_memory 表
- Sentence embeddings → embedding_store
  句子嵌入 → embedding_store / 句子嵌入 → embedding_store
- Named entities → knowledge graph triples
  命名實體 → 知識圖譜三元組 / 命名实体 → 知识图谱三元组
"""

from dataclasses import dataclass
from typing import Any

import spacy


@dataclass
class ExtractedEntity:
    """Extracted NER entity / 提取的 NER 實體 / 提取的 NER 实体"""
    text: str
    label: str          # PERSON, ORG, GPE, DATE, MONEY, etc.
    start: int
    end: int
    confidence: float = 1.0


@dataclass
class NLUResult:
    """NLU processing result / NLU 處理結果 / NLU 处理结果"""
    entities: list[ExtractedEntity]
    tokens: list[str]
    sentences: list[str]
    noun_chunks: list[str]
    language: str = "en"


class NLUPipeline:
    """
    NLU processing pipeline.
    NLU 處理管線。
    NLU 处理管线。

    Extracts entities, tokens, sentences for downstream memory/KG use.
    提取實體、令牌、句子供下游記憶/知識圖譜使用。
    提取实体、令牌、句子供下游记忆/知识图谱使用。
    """

    def __init__(self, model: str = "en_core_web_sm", use_jieba: bool = False):
        """
        Args:
            model: spaCy model name / spaCy 模型名稱
            use_jieba: Enable Chinese segmentation / 啟用中文分詞
        """
        self.nlp = spacy.load(model)
        self.use_jieba = use_jieba
        self._jieba = None
        if use_jieba:
            import jieba as _jieba
            self._jieba = _jieba

    def process(self, text: str) -> NLUResult:
        """
        Process text through NLU pipeline.
        透過 NLU 管線處理文本。
        通过 NLU 管线处理文本。

        Args:
            text: Input text / 輸入文本 / 输入文本

        Returns:
            NLUResult with entities, tokens, sentences
        """
        doc = self.nlp(text)

        # Extract entities / 提取實體 / 提取实体
        entities = [
            ExtractedEntity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char,
            )
            for ent in doc.ents
        ]

        # Extract tokens / 提取令牌 / 提取令牌
        tokens = [token.text for token in doc if not token.is_space]

        # Chinese segmentation if enabled / 如啟用則進行中文分詞
        if self.use_jieba and self._jieba:
            zh_tokens = list(self._jieba.cut(text))
            tokens = zh_tokens + tokens

        # Extract sentences / 提取句子 / 提取句子
        sentences = [sent.text.strip() for sent in doc.sents]

        # Noun chunks / 名詞短語 / 名词短语
        noun_chunks = [chunk.text for chunk in doc.noun_chunks]

        return NLUResult(
            entities=entities,
            tokens=tokens,
            sentences=sentences,
            noun_chunks=noun_chunks,
        )

    def extract_relations(self, text: str) -> list[dict[str, str]]:
        """
        Extract subject-verb-object relations for knowledge graph.
        提取主語-動詞-賓語關係供知識圖譜使用。
        提取主语-动词-宾语关系供知识图谱使用。

        Returns:
            List of {"subject": str, "predicate": str, "object": str}
        """
        doc = self.nlp(text)
        relations = []

        for token in doc:
            if token.dep_ in ("nsubj", "nsubjpass"):
                subject = token.text
                verb = token.head.text
                # Find direct object / 找直接賓語
                for child in token.head.children:
                    if child.dep_ in ("dobj", "attr", "prep"):
                        obj = child.text
                        if child.dep_ == "prep":
                            # Get the object of the preposition
                            for pobj in child.children:
                                if pobj.dep_ == "pobj":
                                    obj = f"{child.text} {pobj.text}"
                        relations.append({
                            "subject": subject,
                            "predicate": verb,
                            "object": obj,
                        })

        return relations

    def to_memory_entities(self, result: NLUResult) -> list[dict[str, Any]]:
        """
        Convert NLU entities to memory manager format.
        將 NLU 實體轉換為記憶管理器格式。
        将 NLU 实体转换为记忆管理器格式。
        """
        return [
            {
                "name": e.text,
                "entity_type": e.label,
                "description": f"Extracted via NLU ({e.label})",
                "confidence": e.confidence,
            }
            for e in result.entities
        ]


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    pipeline = NLUPipeline()
    text = "OpenAI released GPT-4 in March 2023. Google launched Gemini in December."
    result = pipeline.process(text)

    print("Entities / 實體:")
    for e in result.entities:
        print(f"  {e.text} ({e.label})")

    print(f"\nTokens: {len(result.tokens)}")
    print(f"Sentences: {len(result.sentences)}")

    relations = pipeline.extract_relations(text)
    print(f"\nRelations / 關係:")
    for r in relations:
        print(f"  {r['subject']} -> {r['predicate']} -> {r['object']}")

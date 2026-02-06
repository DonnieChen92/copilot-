"""
LLM Memory Manager / LLM 記憶管理器 / LLM 记忆管理器
====================================================
Unified memory management integrating buffer, summary, entity, and embedding memory
with document export capabilities (Excel, PPTX).

統一記憶管理，整合緩衝、摘要、實體和嵌入記憶，具備文件匯出功能。
统一记忆管理，整合缓冲、摘要、实体和嵌入记忆，具备文档导出功能。

Memory Types / 記憶類型 / 记忆类型:
- Buffer Memory: Short-term conversation context / 短期對話上下文 / 短期对话上下文
- Summary Memory: Compressed conversation summaries / 壓縮對話摘要 / 压缩对话摘要
- Entity Memory: Extracted named entities / 提取的命名實體 / 提取的命名实体
- Embedding Memory: Vector representations for RAG / RAG 向量表示 / RAG 向量表示
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Message:
    """Single conversation message / 單條對話訊息 / 单条对话消息"""
    role: str           # 'user' | 'assistant' | 'system'
    content: str        # Message text / 訊息文本 / 消息文本
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    token_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Entity:
    """Extracted entity / 提取的實體 / 提取的实体"""
    name: str
    entity_type: str    # PERSON | ORG | LOCATION | CONCEPT | PRODUCT
    description: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)
    mention_count: int = 1
    first_seen: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Summary:
    """Conversation summary / 對話摘要 / 对话摘要"""
    text: str
    summary_type: str = "progressive"  # progressive | map_reduce | refine
    source_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class MemoryManager:
    """
    Unified LLM Memory Manager.
    統一 LLM 記憶管理器。
    统一 LLM 记忆管理器。

    Manages all memory layers and provides export interfaces.
    管理所有記憶層並提供匯出介面。
    管理所有记忆层并提供导出接口。
    """

    def __init__(
        self,
        session_id: str | None = None,
        max_buffer_messages: int = 50,
        max_buffer_tokens: int = 4096,
    ):
        # Session ID / 會話 ID / 会话 ID
        self.session_id = session_id or str(uuid.uuid4())
        self.max_buffer_messages = max_buffer_messages
        self.max_buffer_tokens = max_buffer_tokens

        # Memory stores / 記憶儲存 / 记忆存储
        self._buffer: list[Message] = []
        self._entities: dict[str, Entity] = {}
        self._summaries: list[Summary] = []
        self._embeddings: list[dict[str, Any]] = []

    # =========================================================================
    # Buffer Memory / 緩衝記憶 / 缓冲记忆
    # =========================================================================

    def add_message(self, role: str, content: str, **kwargs: Any) -> Message:
        """
        Add message to buffer memory.
        將訊息加入緩衝記憶。
        将消息加入缓冲记忆。
        """
        msg = Message(role=role, content=content, **kwargs)
        self._buffer.append(msg)

        # Evict old messages if buffer exceeds limit
        # 如果緩衝超過限制則驅逐舊訊息
        while len(self._buffer) > self.max_buffer_messages:
            self._buffer.pop(0)

        return msg

    def get_buffer(self) -> list[Message]:
        """Get current buffer / 取得當前緩衝 / 获取当前缓冲"""
        return list(self._buffer)

    def get_context_window(self, max_messages: int = 10) -> list[dict[str, str]]:
        """
        Get recent messages for LLM context.
        取得近期訊息供 LLM 上下文使用。
        获取近期消息供 LLM 上下文使用。
        """
        recent = self._buffer[-max_messages:]
        return [{"role": m.role, "content": m.content} for m in recent]

    # =========================================================================
    # Entity Memory / 實體記憶 / 实体记忆
    # =========================================================================

    def add_entity(
        self,
        name: str,
        entity_type: str,
        description: str = "",
        **attributes: Any,
    ) -> Entity:
        """
        Add or update entity in memory.
        在記憶中新增或更新實體。
        在记忆中添加或更新实体。
        """
        key = f"{name}:{entity_type}"
        if key in self._entities:
            existing = self._entities[key]
            existing.mention_count += 1
            existing.last_updated = datetime.now().isoformat()
            if description:
                existing.description = description
            existing.attributes.update(attributes)
            return existing

        entity = Entity(
            name=name,
            entity_type=entity_type,
            description=description,
            attributes=attributes,
        )
        self._entities[key] = entity
        return entity

    def get_entities(self, entity_type: str | None = None) -> list[Entity]:
        """
        Get entities, optionally filtered by type.
        取得實體，可選按類型篩選。
        获取实体，可选按类型筛选。
        """
        entities = list(self._entities.values())
        if entity_type:
            entities = [e for e in entities if e.entity_type == entity_type]
        return entities

    # =========================================================================
    # Summary Memory / 摘要記憶 / 摘要记忆
    # =========================================================================

    def add_summary(self, text: str, summary_type: str = "progressive") -> Summary:
        """
        Add conversation summary.
        新增對話摘要。
        添加对话摘要。
        """
        summary = Summary(
            text=text,
            summary_type=summary_type,
            source_count=len(self._buffer),
        )
        self._summaries.append(summary)
        return summary

    def get_summaries(self) -> list[Summary]:
        """Get all summaries / 取得所有摘要 / 获取所有摘要"""
        return list(self._summaries)

    # =========================================================================
    # Embedding Memory / 嵌入記憶 / 嵌入记忆
    # =========================================================================

    def add_embedding(
        self,
        text: str,
        vector: list[float],
        model: str = "text-embedding-ada-002",
    ) -> dict[str, Any]:
        """
        Store embedding vector.
        儲存嵌入向量。
        存储嵌入向量。
        """
        entry = {
            "text": text,
            "vector": vector,
            "model": model,
            "created_at": datetime.now().isoformat(),
        }
        self._embeddings.append(entry)
        return entry

    def get_embeddings(self) -> list[dict[str, Any]]:
        """Get all embeddings / 取得所有嵌入 / 获取所有嵌入"""
        return list(self._embeddings)

    # =========================================================================
    # Export Interfaces / 匯出介面 / 导出接口
    # =========================================================================

    def to_excel_data(self) -> dict[str, list[dict[str, Any]]]:
        """
        Prepare all memory data for Excel export.
        準備所有記憶資料供 Excel 匯出。
        准备所有记忆数据供 Excel 导出。

        Returns dict with keys: 'messages', 'entities', 'summaries', 'embeddings'
        """
        return {
            "messages": [
                {"role": m.role, "content": m.content, "timestamp": m.timestamp}
                for m in self._buffer
            ],
            "entities": [
                {
                    "name": e.name,
                    "type": e.entity_type,
                    "description": e.description,
                    "count": e.mention_count,
                }
                for e in self._entities.values()
            ],
            "summaries": [
                {"text": s.text, "type": s.summary_type, "created_at": s.created_at}
                for s in self._summaries
            ],
            "embeddings": self._embeddings,
        }

    def to_pptx_data(self) -> dict[str, Any]:
        """
        Prepare memory data for PPTX slide generation.
        準備記憶資料供 PPTX 幻燈片生成。
        准备记忆数据供 PPTX 幻灯片生成。
        """
        return {
            "title": f"Session {self.session_id[:8]}",
            "summary": self._summaries[-1].text if self._summaries else "No summary available",
            "entity_count": len(self._entities),
            "message_count": len(self._buffer),
            "entities": [
                {"name": e.name, "type": e.entity_type, "description": e.description}
                for e in self._entities.values()
            ],
            "key_points": [s.text for s in self._summaries[-3:]],
        }

    def export_state(self) -> str:
        """
        Export full memory state as JSON.
        將完整記憶狀態匯出為 JSON。
        将完整记忆状态导出为 JSON。
        """
        state = {
            "session_id": self.session_id,
            "exported_at": datetime.now().isoformat(),
            "buffer_size": len(self._buffer),
            "entity_count": len(self._entities),
            "summary_count": len(self._summaries),
            "embedding_count": len(self._embeddings),
            "data": self.to_excel_data(),
        }
        return json.dumps(state, ensure_ascii=False, indent=2)


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    mm = MemoryManager()

    # Add conversation / 新增對話 / 添加对话
    mm.add_message("user", "What is knowledge graph?")
    mm.add_message(
        "assistant",
        "A knowledge graph is a structured representation of facts using entities and relationships.",
    )
    mm.add_message("user", "How does it relate to NLU?")
    mm.add_message(
        "assistant",
        "NLU extracts entities and intents from text, which can populate a knowledge graph.",
    )

    # Add entities / 新增實體 / 添加实体
    mm.add_entity("Knowledge Graph", "CONCEPT", "Structured fact representation")
    mm.add_entity("NLU", "CONCEPT", "Natural Language Understanding")
    mm.add_entity("spaCy", "PRODUCT", "Industrial NLP library")

    # Add summary / 新增摘要 / 添加摘要
    mm.add_summary(
        "Discussion covered knowledge graphs and their relationship to NLU. "
        "Key tools include spaCy for entity extraction."
    )

    # Export for Excel / 匯出供 Excel 使用
    excel_data = mm.to_excel_data()
    print(f"Messages: {len(excel_data['messages'])}")
    print(f"Entities: {len(excel_data['entities'])}")
    print(f"Summaries: {len(excel_data['summaries'])}")

    # Export full state / 匯出完整狀態
    print(mm.export_state())

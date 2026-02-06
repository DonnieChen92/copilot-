"""
Document Pipeline / 文件管線 / 文档管线
=======================================
End-to-end pipeline: LLM conversation → NLU → Memory → Document Export.
端到端管線：LLM 對話 → NLU → 記憶 → 文件匯出。
端到端管线：LLM 对话 → NLU → 记忆 → 文档导出。

This pipeline orchestrates all components:
此管線編排所有組件：
此管线编排所有组件：

1. Receive conversation messages / 接收對話訊息
2. Process through NLU / 透過 NLU 處理
3. Store in memory layers / 存入記憶層
4. Build knowledge graph / 構建知識圖譜
5. Export to Excel/PPTX / 匯出至 Excel/PPTX
"""

from datetime import datetime
from typing import Any

from ..excel.excel_engine import ExcelEngine
from ..knowledge_graph.kg_builder import KnowledgeGraphBuilder
from ..llm_memory.memory_manager import MemoryManager
from ..nlu.nlu_pipeline import NLUPipeline
from ..pptx.pptx_engine import PPTXEngine


class DocumentPipeline:
    """
    End-to-end document automation pipeline.
    端到端文件自動化管線。
    端到端文档自动化管线。
    """

    def __init__(
        self,
        session_id: str | None = None,
        output_dir: str = "./output",
    ):
        self.output_dir = output_dir
        # Initialize components / 初始化組件 / 初始化组件
        self.memory = MemoryManager(session_id=session_id)
        self.nlu = NLUPipeline()
        self.kg = KnowledgeGraphBuilder()

    def ingest_message(self, role: str, content: str) -> dict[str, Any]:
        """
        Ingest a single message through the full pipeline.
        透過完整管線攝入單條訊息。
        通过完整管线摄入单条消息。

        Steps / 步驟 / 步骤:
        1. Add to buffer memory / 加入緩衝記憶
        2. Run NLU extraction / 執行 NLU 提取
        3. Store entities in memory / 將實體存入記憶
        4. Add relations to knowledge graph / 將關係加入知識圖譜
        """
        # Step 1: Buffer memory / 步驟1：緩衝記憶
        self.memory.add_message(role, content)

        # Step 2: NLU processing / 步驟2：NLU 處理
        nlu_result = self.nlu.process(content)

        # Step 3: Entity memory / 步驟3：實體記憶
        for entity_data in self.nlu.to_memory_entities(nlu_result):
            self.memory.add_entity(
                name=entity_data["name"],
                entity_type=entity_data["entity_type"],
                description=entity_data["description"],
            )
            self.kg.add_entity(
                entity_data["name"],
                entity_type=entity_data["entity_type"],
            )

        # Step 4: Knowledge graph relations / 步驟4：知識圖譜關係
        relations = self.nlu.extract_relations(content)
        self.kg.add_triples(relations)

        return {
            "entities_found": len(nlu_result.entities),
            "relations_found": len(relations),
            "buffer_size": len(self.memory.get_buffer()),
        }

    def ingest_conversation(
        self,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        """
        Ingest a full conversation.
        攝入完整對話。
        摄入完整对话。
        """
        total_entities = 0
        total_relations = 0

        for msg in messages:
            result = self.ingest_message(msg["role"], msg["content"])
            total_entities += result["entities_found"]
            total_relations += result["relations_found"]

        return {
            "messages_processed": len(messages),
            "total_entities": total_entities,
            "total_relations": total_relations,
            "kg_stats": self.kg.get_stats(),
        }

    def generate_summary(self, llm_client: Any = None) -> str:
        """
        Generate conversation summary (via LLM or simple extraction).
        生成對話摘要（透過 LLM 或簡單提取）。
        生成对话摘要（通过 LLM 或简单提取）。
        """
        buffer = self.memory.get_buffer()
        if not buffer:
            return "No conversation data available."

        if llm_client:
            # Use LLM for summary / 使用 LLM 生成摘要
            context = self.memory.get_context_window(max_messages=20)
            context.append({
                "role": "user",
                "content": "Please provide a concise summary of the above conversation.",
            })
            response = llm_client.chat(context)
            summary_text = response.content
        else:
            # Simple extraction / 簡單提取
            messages = [f"[{m.role}] {m.content}" for m in buffer[-10:]]
            summary_text = "Conversation summary:\n" + "\n".join(messages)

        self.memory.add_summary(summary_text)
        return summary_text

    def export_excel(self, filename: str | None = None) -> str:
        """
        Export all memory data to Excel.
        將所有記憶資料匯出至 Excel。
        将所有记忆数据导出至 Excel。
        """
        filename = filename or f"{self.output_dir}/report_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
        engine = ExcelEngine(filename)

        data = self.memory.to_excel_data()
        engine.export_conversation_memory(data["messages"])
        engine.export_entity_memory(data["entities"])
        engine.export_summary_memory(data["summaries"])

        if data["embeddings"]:
            engine.export_embeddings(data["embeddings"])

        return filename

    def export_pptx(self, filename: str | None = None) -> str:
        """
        Export summary and entities to PowerPoint.
        將摘要和實體匯出至 PowerPoint。
        将摘要和实体导出至 PowerPoint。
        """
        filename = filename or f"{self.output_dir}/report_{datetime.now():%Y%m%d_%H%M%S}.pptx"
        engine = PPTXEngine()

        pptx_data = self.memory.to_pptx_data()
        kg_data = self.kg.to_pptx_data()

        # Title slide / 標題幻燈片
        engine.add_title_slide(
            "AI Document Report",
            f"Session: {self.memory.session_id[:8]} | {datetime.now():%Y-%m-%d}",
        )

        # Summary slide / 摘要幻燈片
        engine.add_summary_slide(
            "Conversation Summary / 對話摘要",
            pptx_data["summary"],
            pptx_data.get("key_points", []),
        )

        # Entity table slide / 實體表幻燈片
        if pptx_data["entities"]:
            engine.add_entity_table_slide(
                "Extracted Entities / 提取的實體",
                pptx_data["entities"],
            )

        # Knowledge graph stats slide / 知識圖譜統計幻燈片
        stats = kg_data["stats"]
        engine.add_summary_slide(
            "Knowledge Graph / 知識圖譜",
            f"Nodes: {stats['node_count']} | Edges: {stats['edge_count']}",
            [f"{t['subject']} → {t['predicate']} → {t['object']}" for t in kg_data["triples"][:8]],
        )

        return engine.save(filename)

    def export_all(self) -> dict[str, str]:
        """
        Export to all formats.
        匯出至所有格式。
        导出至所有格式。
        """
        return {
            "excel": self.export_excel(),
            "pptx": self.export_pptx(),
        }


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    pipeline = DocumentPipeline(output_dir=".")

    # Simulate conversation / 模擬對話 / 模拟对话
    demo_conversation = [
        {"role": "user", "content": "Tell me about OpenAI and their GPT-4 model."},
        {
            "role": "assistant",
            "content": "OpenAI released GPT-4 in March 2023. It is a large language model "
            "that demonstrates human-level performance on various benchmarks.",
        },
        {"role": "user", "content": "How does Google Gemini compare?"},
        {
            "role": "assistant",
            "content": "Google launched Gemini in December 2023. Gemini supports multimodal "
            "inputs and competes with GPT-4 on reasoning tasks.",
        },
    ]

    # Run pipeline / 執行管線 / 运行管线
    result = pipeline.ingest_conversation(demo_conversation)
    print(f"Pipeline result: {result}")

    # Generate summary / 生成摘要
    summary = pipeline.generate_summary()
    print(f"\nSummary: {summary[:200]}...")

    print("\nPipeline demo complete. Use export_excel() / export_pptx() to generate documents.")
    # 管線示範完成。使用 export_excel() / export_pptx() 生成文件。

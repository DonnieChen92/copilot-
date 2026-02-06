"""
Excel Engine / Excel 引擎
========================
openpyxl-based Excel document generation with LLM memory integration.
基於 openpyxl 的 Excel 文件生成，整合 LLM 記憶系統。
基于 openpyxl 的 Excel 文档生成，整合 LLM 记忆系统。

Integration Points / 接入點 / 接入点:
- Export conversation memory to Excel worksheets
  將對話記憶匯出至 Excel 工作表 / 将对话记忆导出至 Excel 工作表
- Store embedding vectors in Excel for analysis
  將嵌入向量存入 Excel 供分析 / 将嵌入向量存入 Excel 供分析
- Export entity memory as structured tables
  將實體記憶匯出為結構化表格 / 将实体记忆导出为结构化表格
"""

from datetime import datetime
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


class ExcelEngine:
    """
    Excel document engine powered by openpyxl.
    Excel 文件引擎，由 openpyxl 驅動。
    Excel 文档引擎，由 openpyxl 驱动。
    """

    def __init__(self, output_path: str = "output.xlsx"):
        # Output file path / 輸出檔案路徑 / 输出文件路径
        self.output_path = output_path
        self.wb = Workbook()
        # Remove default sheet / 移除預設工作表 / 移除默认工作表
        self.wb.remove(self.wb.active)

    def _create_header_style(self) -> dict[str, Any]:
        """Header cell style / 標題儲存格樣式 / 标题单元格样式"""
        return {
            "font": Font(bold=True, color="FFFFFF", size=11),
            "fill": PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid"),
            "alignment": Alignment(horizontal="center", vertical="center"),
        }

    def export_conversation_memory(
        self,
        messages: list[dict[str, str]],
        sheet_name: str = "Conversation Memory",
    ) -> str:
        """
        Export conversation history to an Excel worksheet.
        將對話歷史匯出至 Excel 工作表。
        将对话历史导出至 Excel 工作表。

        Args:
            messages: List of {"role": str, "content": str, "timestamp": str}
                     訊息列表 / 消息列表
            sheet_name: Worksheet name / 工作表名稱 / 工作表名称

        Returns:
            Output file path / 輸出檔案路徑 / 输出文件路径
        """
        ws = self.wb.create_sheet(title=sheet_name)
        headers = ["#", "Role / 角色", "Content / 內容", "Timestamp / 時間戳"]
        style = self._create_header_style()

        # Write headers / 寫入標題 / 写入标题
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = style["font"]
            cell.fill = style["fill"]
            cell.alignment = style["alignment"]

        # Write data rows / 寫入資料列 / 写入数据行
        for idx, msg in enumerate(messages, 1):
            ws.cell(row=idx + 1, column=1, value=idx)
            ws.cell(row=idx + 1, column=2, value=msg.get("role", ""))
            ws.cell(row=idx + 1, column=3, value=msg.get("content", ""))
            ws.cell(row=idx + 1, column=4, value=msg.get("timestamp", ""))

        # Auto-adjust column widths / 自動調整欄寬 / 自动调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[get_column_letter(col)].width = 25

        self.wb.save(self.output_path)
        return self.output_path

    def export_entity_memory(
        self,
        entities: list[dict[str, Any]],
        sheet_name: str = "Entity Memory",
    ) -> str:
        """
        Export extracted entities to Excel.
        將提取的實體匯出至 Excel。
        将提取的实体导出至 Excel。

        Args:
            entities: List of {"name": str, "type": str, "description": str, "count": int}
                     實體列表 / 实体列表
        """
        ws = self.wb.create_sheet(title=sheet_name)
        headers = [
            "Entity Name / 實體名稱",
            "Type / 類型",
            "Description / 描述",
            "Mention Count / 提及次數",
        ]
        style = self._create_header_style()

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = style["font"]
            cell.fill = style["fill"]
            cell.alignment = style["alignment"]

        for idx, entity in enumerate(entities, 1):
            ws.cell(row=idx + 1, column=1, value=entity.get("name", ""))
            ws.cell(row=idx + 1, column=2, value=entity.get("type", ""))
            ws.cell(row=idx + 1, column=3, value=entity.get("description", ""))
            ws.cell(row=idx + 1, column=4, value=entity.get("count", 0))

        for col in range(1, len(headers) + 1):
            ws.column_dimensions[get_column_letter(col)].width = 30

        self.wb.save(self.output_path)
        return self.output_path

    def export_embeddings(
        self,
        embeddings: list[dict[str, Any]],
        sheet_name: str = "Embeddings",
    ) -> str:
        """
        Export embedding vectors to Excel for analysis.
        將嵌入向量匯出至 Excel 供分析。
        将嵌入向量导出至 Excel 供分析。

        Args:
            embeddings: List of {"text": str, "vector": list[float], "model": str}
        """
        ws = self.wb.create_sheet(title=sheet_name)
        headers = ["Text / 文本", "Model / 模型", "Dimensions / 維度", "Vector Preview / 向量預覽"]
        style = self._create_header_style()

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = style["font"]
            cell.fill = style["fill"]

        for idx, emb in enumerate(embeddings, 1):
            vector = emb.get("vector", [])
            ws.cell(row=idx + 1, column=1, value=emb.get("text", ""))
            ws.cell(row=idx + 1, column=2, value=emb.get("model", ""))
            ws.cell(row=idx + 1, column=3, value=len(vector))
            # Show first 5 dimensions as preview / 顯示前5個維度作為預覽
            preview = str(vector[:5]) + "..." if len(vector) > 5 else str(vector)
            ws.cell(row=idx + 1, column=4, value=preview)

        self.wb.save(self.output_path)
        return self.output_path

    def export_summary_memory(
        self,
        summaries: list[dict[str, str]],
        sheet_name: str = "Summary Memory",
    ) -> str:
        """
        Export conversation summaries to Excel.
        將對話摘要匯出至 Excel。
        将对话摘要导出至 Excel。
        """
        ws = self.wb.create_sheet(title=sheet_name)
        headers = ["#", "Summary / 摘要", "Type / 類型", "Created / 建立時間"]
        style = self._create_header_style()

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = style["font"]
            cell.fill = style["fill"]

        for idx, summary in enumerate(summaries, 1):
            ws.cell(row=idx + 1, column=1, value=idx)
            ws.cell(row=idx + 1, column=2, value=summary.get("text", ""))
            ws.cell(row=idx + 1, column=3, value=summary.get("type", "progressive"))
            ws.cell(row=idx + 1, column=4, value=summary.get("created_at", ""))

        self.wb.save(self.output_path)
        return self.output_path


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    engine = ExcelEngine("demo_output.xlsx")

    # Demo: Export conversation / 示範：匯出對話 / 示范：导出对话
    demo_messages = [
        {"role": "user", "content": "What is RAG?", "timestamp": str(datetime.now())},
        {
            "role": "assistant",
            "content": "RAG (Retrieval-Augmented Generation) combines retrieval with LLM generation.",
            "timestamp": str(datetime.now()),
        },
    ]
    engine.export_conversation_memory(demo_messages)

    # Demo: Export entities / 示範：匯出實體 / 示范：导出实体
    demo_entities = [
        {"name": "RAG", "type": "CONCEPT", "description": "Retrieval-Augmented Generation", "count": 5},
        {"name": "OpenAI", "type": "ORG", "description": "AI research company", "count": 12},
    ]
    engine.export_entity_memory(demo_entities)

    print(f"Demo Excel exported to: {engine.output_path}")
    # 示範 Excel 已匯出至：demo_output.xlsx

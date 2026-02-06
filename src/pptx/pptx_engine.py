"""
PPTX Engine / PPTX 引擎
=======================
python-pptx-based PowerPoint generation with LLM memory integration.
基於 python-pptx 的 PowerPoint 生成，整合 LLM 記憶系統。
基于 python-pptx 的 PowerPoint 生成，整合 LLM 记忆系统。

Integration Points / 接入點 / 接入点:
- Auto-generate summary slides from conversation memory
  從對話記憶自動生成摘要幻燈片 / 从对话记忆自动生成摘要幻灯片
- Display entity relationships on slides
  在幻燈片上顯示實體關係 / 在幻灯片上显示实体关系
- Visualize knowledge graph on presentation slides
  在簡報幻燈片上視覺化知識圖譜 / 在演示文稿幻灯片上可视化知识图谱
"""

from datetime import datetime
from typing import Any

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


class PPTXEngine:
    """
    PowerPoint presentation engine powered by python-pptx.
    PowerPoint 簡報引擎，由 python-pptx 驅動。
    PowerPoint 演示文稿引擎，由 python-pptx 驱动。
    """

    def __init__(self, template_path: str | None = None):
        # Load template or create blank / 載入模板或建立空白 / 加载模板或创建空白
        if template_path:
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()

    def add_title_slide(self, title: str, subtitle: str = "") -> None:
        """
        Add a title slide / 新增標題幻燈片 / 添加标题幻灯片

        Args:
            title: Slide title / 幻燈片標題 / 幻灯片标题
            subtitle: Slide subtitle / 副標題 / 副标题
        """
        slide_layout = self.prs.slide_layouts[0]  # Title Slide layout
        slide = self.prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = title
        if subtitle and slide.placeholders[1]:
            slide.placeholders[1].text = subtitle

    def add_summary_slide(
        self,
        title: str,
        summary_text: str,
        bullet_points: list[str] | None = None,
    ) -> None:
        """
        Add a conversation summary slide.
        新增對話摘要幻燈片。
        添加对话摘要幻灯片。

        Args:
            title: Slide title / 標題
            summary_text: Summary paragraph / 摘要段落
            bullet_points: Key points / 重點列表 / 重点列表
        """
        slide_layout = self.prs.slide_layouts[1]  # Title and Content layout
        slide = self.prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = title

        body = slide.placeholders[1]
        tf = body.text_frame
        tf.text = summary_text

        if bullet_points:
            for point in bullet_points:
                p = tf.add_paragraph()
                p.text = point
                p.level = 1
                p.font.size = Pt(14)

    def add_entity_table_slide(
        self,
        title: str,
        entities: list[dict[str, Any]],
    ) -> None:
        """
        Add a slide with entity memory table.
        新增包含實體記憶表的幻燈片。
        添加包含实体记忆表的幻灯片。

        Args:
            entities: List of {"name": str, "type": str, "description": str}
        """
        slide_layout = self.prs.slide_layouts[5]  # Blank layout
        slide = self.prs.slides.add_slide(slide_layout)

        # Add title text box / 新增標題文字框
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(24)
        p.font.bold = True

        # Create table / 建立表格 / 创建表格
        rows = min(len(entities) + 1, 15)  # Limit rows per slide / 每頁限制列數
        cols = 3
        table_shape = slide.shapes.add_table(
            rows, cols, Inches(0.5), Inches(1.2), Inches(9), Inches(5)
        )
        table = table_shape.table

        # Headers / 標題 / 标题
        headers = ["Entity / 實體", "Type / 類型", "Description / 描述"]
        for i, header in enumerate(headers):
            cell = table.cell(0, i)
            cell.text = header
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.bold = True
                paragraph.font.size = Pt(11)
                paragraph.alignment = PP_ALIGN.CENTER

        # Data rows / 資料列 / 数据行
        for row_idx, entity in enumerate(entities[: rows - 1], 1):
            table.cell(row_idx, 0).text = entity.get("name", "")
            table.cell(row_idx, 1).text = entity.get("type", "")
            table.cell(row_idx, 2).text = entity.get("description", "")

    def add_conversation_slides(
        self,
        messages: list[dict[str, str]],
        title: str = "Conversation Log / 對話記錄",
    ) -> None:
        """
        Add slides displaying conversation history.
        新增顯示對話歷史的幻燈片。
        添加显示对话历史的幻灯片。
        """
        # Group messages into chunks of 4 per slide
        # 每張幻燈片分組4條訊息
        chunk_size = 4
        for i in range(0, len(messages), chunk_size):
            chunk = messages[i : i + chunk_size]
            slide_layout = self.prs.slide_layouts[1]
            slide = self.prs.slides.add_slide(slide_layout)
            slide.shapes.title.text = f"{title} ({i + 1}-{i + len(chunk)})"

            body = slide.placeholders[1]
            tf = body.text_frame
            tf.clear()

            for msg in chunk:
                p = tf.add_paragraph()
                role = msg.get("role", "unknown").upper()
                content = msg.get("content", "")
                p.text = f"[{role}] {content}"
                p.font.size = Pt(12)
                p.space_after = Pt(6)

    def save(self, output_path: str = "output.pptx") -> str:
        """
        Save presentation / 儲存簡報 / 保存演示文稿

        Returns:
            Output file path / 輸出檔案路徑 / 输出文件路径
        """
        self.prs.save(output_path)
        return output_path


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    engine = PPTXEngine()

    # Title slide / 標題幻燈片
    engine.add_title_slide(
        "AI Document Automation Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d')}",
    )

    # Summary slide / 摘要幻燈片
    engine.add_summary_slide(
        "Conversation Summary / 對話摘要",
        "This report summarizes the key findings from the AI analysis session.",
        [
            "Identified 15 entities across 3 categories",
            "Generated 5 knowledge graph triples",
            "Exported embeddings for 50 text chunks",
        ],
    )

    # Entity table slide / 實體表幻燈片
    demo_entities = [
        {"name": "OpenAI", "type": "ORG", "description": "AI research organization"},
        {"name": "GPT-4", "type": "PRODUCT", "description": "Large language model"},
        {"name": "RAG", "type": "CONCEPT", "description": "Retrieval-Augmented Generation"},
    ]
    engine.add_entity_table_slide("Entity Memory / 實體記憶", demo_entities)

    output = engine.save("demo_presentation.pptx")
    print(f"Demo PPTX exported to: {output}")

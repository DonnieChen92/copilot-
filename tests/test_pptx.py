"""
Tests for PPTX Engine / PPTX 引擎測試 / PPTX 引擎测试
"""

import os
import tempfile

from src.pptx.pptx_engine import PPTXEngine


class TestPPTXEngine:
    """Test PPTXEngine functionality / 測試 PPTXEngine 功能"""

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.engine = PPTXEngine()

    def test_add_title_slide(self):
        """Test title slide creation / 測試標題幻燈片建立"""
        self.engine.add_title_slide("Test Title", "Test Subtitle")
        assert len(self.engine.prs.slides) == 1

    def test_add_summary_slide(self):
        """Test summary slide creation / 測試摘要幻燈片建立"""
        self.engine.add_summary_slide(
            "Summary",
            "Test summary text",
            ["Point 1", "Point 2"],
        )
        assert len(self.engine.prs.slides) == 1

    def test_add_entity_table_slide(self):
        """Test entity table slide / 測試實體表幻燈片"""
        entities = [
            {"name": "OpenAI", "type": "ORG", "description": "AI company"},
            {"name": "GPT-4", "type": "PRODUCT", "description": "LLM"},
        ]
        self.engine.add_entity_table_slide("Entities", entities)
        assert len(self.engine.prs.slides) == 1

    def test_add_conversation_slides(self):
        """Test conversation slides / 測試對話幻燈片"""
        messages = [
            {"role": "user", "content": f"Message {i}"}
            for i in range(6)
        ]
        self.engine.add_conversation_slides(messages)
        # 6 messages / 4 per slide = 2 slides
        assert len(self.engine.prs.slides) == 2

    def test_save(self):
        """Test save to file / 測試儲存至檔案"""
        self.engine.add_title_slide("Test")
        output = os.path.join(self.tmpdir, "test.pptx")
        result = self.engine.save(output)
        assert os.path.exists(result)

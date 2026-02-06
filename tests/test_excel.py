"""
Tests for Excel Engine / Excel 引擎測試 / Excel 引擎测试
"""

import os
import tempfile

from src.excel.excel_engine import ExcelEngine


class TestExcelEngine:
    """Test ExcelEngine functionality / 測試 ExcelEngine 功能"""

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.output = os.path.join(self.tmpdir, "test.xlsx")
        self.engine = ExcelEngine(self.output)

    def test_export_conversation_memory(self):
        """Test conversation export / 測試對話匯出"""
        messages = [
            {"role": "user", "content": "Hello", "timestamp": "2024-01-01"},
            {"role": "assistant", "content": "Hi", "timestamp": "2024-01-01"},
        ]
        result = self.engine.export_conversation_memory(messages)
        assert os.path.exists(result)

    def test_export_entity_memory(self):
        """Test entity export / 測試實體匯出"""
        entities = [
            {"name": "OpenAI", "type": "ORG", "description": "AI company", "count": 5},
        ]
        result = self.engine.export_entity_memory(entities)
        assert os.path.exists(result)

    def test_export_embeddings(self):
        """Test embedding export / 測試嵌入匯出"""
        embeddings = [
            {"text": "hello world", "vector": [0.1, 0.2, 0.3], "model": "ada-002"},
        ]
        result = self.engine.export_embeddings(embeddings)
        assert os.path.exists(result)

    def test_export_summary_memory(self):
        """Test summary export / 測試摘要匯出"""
        summaries = [
            {"text": "A test summary", "type": "progressive", "created_at": "2024-01-01"},
        ]
        result = self.engine.export_summary_memory(summaries)
        assert os.path.exists(result)

    def test_multiple_sheets(self):
        """Test multiple worksheets / 測試多個工作表"""
        self.engine.export_conversation_memory([{"role": "user", "content": "test", "timestamp": ""}])
        self.engine.export_entity_memory([{"name": "X", "type": "CONCEPT", "description": "", "count": 1}])
        assert len(self.engine.wb.sheetnames) == 2

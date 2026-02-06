"""
Tests for LLM Memory Manager / LLM 記憶管理器測試 / LLM 记忆管理器测试
"""

from src.llm_memory.memory_manager import MemoryManager


class TestMemoryManager:
    """Test MemoryManager functionality / 測試 MemoryManager 功能"""

    def setup_method(self):
        self.mm = MemoryManager(session_id="test-session-001")

    def test_add_message(self):
        """Test adding messages to buffer / 測試新增訊息至緩衝"""
        msg = self.mm.add_message("user", "Hello, world!")
        assert msg.role == "user"
        assert msg.content == "Hello, world!"
        assert len(self.mm.get_buffer()) == 1

    def test_buffer_eviction(self):
        """Test buffer eviction when exceeding max / 測試超過上限時的緩衝驅逐"""
        mm = MemoryManager(max_buffer_messages=3)
        mm.add_message("user", "msg1")
        mm.add_message("assistant", "msg2")
        mm.add_message("user", "msg3")
        mm.add_message("assistant", "msg4")
        assert len(mm.get_buffer()) == 3
        assert mm.get_buffer()[0].content == "msg2"

    def test_add_entity(self):
        """Test entity creation / 測試實體建立"""
        entity = self.mm.add_entity("OpenAI", "ORG", "AI research company")
        assert entity.name == "OpenAI"
        assert entity.entity_type == "ORG"
        assert entity.mention_count == 1

    def test_entity_update(self):
        """Test entity mention count update / 測試實體提及次數更新"""
        self.mm.add_entity("OpenAI", "ORG")
        self.mm.add_entity("OpenAI", "ORG")
        entities = self.mm.get_entities(entity_type="ORG")
        assert len(entities) == 1
        assert entities[0].mention_count == 2

    def test_add_summary(self):
        """Test adding summary / 測試新增摘要"""
        summary = self.mm.add_summary("Test summary text", "progressive")
        assert summary.text == "Test summary text"
        assert summary.summary_type == "progressive"

    def test_add_embedding(self):
        """Test adding embedding / 測試新增嵌入"""
        emb = self.mm.add_embedding("test text", [0.1, 0.2, 0.3], "test-model")
        assert emb["text"] == "test text"
        assert len(emb["vector"]) == 3

    def test_context_window(self):
        """Test context window retrieval / 測試上下文窗口檢索"""
        for i in range(10):
            self.mm.add_message("user", f"message {i}")
        context = self.mm.get_context_window(max_messages=3)
        assert len(context) == 3
        assert context[0]["content"] == "message 7"

    def test_to_excel_data(self):
        """Test Excel export data / 測試 Excel 匯出資料"""
        self.mm.add_message("user", "test")
        self.mm.add_entity("Test", "CONCEPT")
        data = self.mm.to_excel_data()
        assert "messages" in data
        assert "entities" in data
        assert len(data["messages"]) == 1
        assert len(data["entities"]) == 1

    def test_to_pptx_data(self):
        """Test PPTX export data / 測試 PPTX 匯出資料"""
        self.mm.add_entity("Test", "CONCEPT")
        data = self.mm.to_pptx_data()
        assert "title" in data
        assert data["entity_count"] == 1

    def test_export_state_json(self):
        """Test JSON state export / 測試 JSON 狀態匯出"""
        self.mm.add_message("user", "hello")
        state = self.mm.export_state()
        assert "session_id" in state
        assert "test-session-001" in state

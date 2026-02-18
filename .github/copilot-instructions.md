# =============================================================================
# GitHub Copilot Instructions / GitHub Copilot 指示 / GitHub Copilot 指示
# Real-Time AI Coding Assistant Configuration
# =============================================================================
# This file helps GitHub Copilot provide better, context-aware suggestions
# for the Document-AI Open Source Blueprint codebase.
# =============================================================================

# Project Context
You are working on the **Document-AI Open Source Blueprint**, a unified AI Matrix 
platform for document generation, LLM memory management, and knowledge graph construction.

## Key Technologies
- **Language**: Python 3.10+
- **Document Generation**: openpyxl (Excel), python-pptx (PowerPoint), python-docx (Word), reportlab (PDF)
- **LLM Integration**: OpenAI, Google Gemini, Anthropic Claude, Azure, DeepSeek, X.AI, Perplexity, Tencent, Hugging Face
- **NLP**: spaCy, transformers, sentence-transformers, jieba (Chinese)
- **Knowledge Graphs**: NetworkX, Neo4j, PyVis
- **Vector Stores**: FAISS, ChromaDB, Qdrant
- **Frameworks**: LangChain, LlamaIndex

## Code Style Guidelines

### Trilingual Documentation
ALL user-facing strings, docstrings, and comments should be in three languages:
1. English (primary)
2. Traditional Chinese (繁體中文)
3. Simplified Chinese (简体中文)

Example:
```python
def export_data(data: dict) -> str:
    """
    Export data to Excel format.
    將資料匯出至 Excel 格式。
    将数据导出至 Excel 格式。
    
    Args:
        data: Input data dictionary / 輸入資料字典 / 输入数据字典
        
    Returns:
        Output file path / 輸出檔案路徑 / 输出文件路径
    """
```

### Type Hints
Always use type hints for parameters and return values:
```python
from typing import Any

def process_message(role: str, content: str) -> dict[str, Any]:
    ...
```

### Import Organization
Group imports in this order:
1. Standard library
2. Third-party packages
3. Local application modules

```python
# Standard library
from datetime import datetime
from typing import Any

# Third-party
from openpyxl import Workbook
from pptx import Presentation

# Local
from ..excel.excel_engine import ExcelEngine
from ..llm_memory.memory_manager import MemoryManager
```

## Module Patterns

### LLM Client Pattern
When creating a new LLM provider client:
```python
from .base_client import BaseLLMClient, LLMResponse

class NewProviderClient(BaseLLMClient):
    """
    Client for NewProvider LLM API.
    NewProvider LLM API 客戶端。
    NewProvider LLM API 客户端。
    """
    
    def __init__(self, api_key: str, model: str = "default-model"):
        super().__init__(api_key)
        self.model = model
        # Initialize provider-specific client
        
    def chat(self, messages: list[dict]) -> LLMResponse:
        """
        Send chat messages and get response.
        發送聊天訊息並獲取回應。
        发送聊天消息并获取响应。
        """
        # Implement chat logic
        ...
        
    def stream_chat(self, messages: list[dict]):
        """
        Stream chat responses.
        串流聊天回應。
        流式聊天响应。
        """
        # Implement streaming logic
        ...
```

### Document Export Pattern
When adding export methods to engines:
```python
def export_new_data_type(
    self,
    data: list[dict[str, Any]],
    sheet_name: str = "Data Sheet",
) -> str:
    """
    Export new data type to Excel/PPTX.
    將新資料類型匯出至 Excel/PPTX。
    将新数据类型导出至 Excel/PPTX。
    
    Args:
        data: List of data dictionaries / 資料字典列表 / 数据字典列表
        sheet_name: Sheet/slide name / 工作表/幻燈片名稱 / 工作表/幻灯片名称
        
    Returns:
        Output file path / 輸出檔案路徑 / 输出文件路径
    """
    # Implementation
    ...
```

### Memory Management Pattern
When working with memory layers:
```python
# Add to buffer memory / 加入緩衝記憶 / 加入缓冲记忆
self.memory.add_message(role, content)

# Add entity / 加入實體 / 加入实体
self.memory.add_entity(
    name="EntityName",
    entity_type="TYPE",
    description="Description of entity"
)

# Generate summary / 生成摘要 / 生成摘要
summary = self.memory.generate_summary(llm_client)

# Get data for export / 獲取匯出資料 / 获取导出数据
excel_data = self.memory.to_excel_data()
pptx_data = self.memory.to_pptx_data()
```

## Project Structure Quick Reference

```
src/
├── excel/excel_engine.py          # Excel generation (openpyxl)
├── pptx/pptx_engine.py            # PowerPoint generation (python-pptx)
├── llm_api/                       # Multi-LLM client implementations
│   ├── base_client.py            # Base interface
│   ├── openai_client.py          # OpenAI GPT-4, o1, DALL-E
│   ├── google_client.py          # Google Gemini, Imagen
│   ├── anthropic_client.py       # Claude Opus, Sonnet, Haiku
│   └── ...                       # Other providers
├── llm_memory/memory_manager.py   # Memory layers (buffer, summary, entity)
├── nlu/nlu_pipeline.py           # NER, relation extraction
├── knowledge_graph/kg_builder.py  # Knowledge graph construction
└── pipelines/document_pipeline.py # End-to-end orchestration
```

## Common Tasks

### Adding a New LLM Provider
1. Create `src/llm_api/{provider}_client.py`
2. Inherit from `BaseLLMClient`
3. Implement `chat()` and `stream_chat()`
4. Add to README.md AI Platform table
5. Add tests in `tests/test_llm_api.py`
6. Update `config/settings.yaml`

### Adding Document Export Feature
1. Add method to `ExcelEngine` or `PPTXEngine`
2. Follow naming: `export_{type}_memory()`
3. Add trilingual docstrings
4. Add to `DocumentPipeline`
5. Write tests

### Working with Memory Layers
- **Buffer**: Recent conversation (FIFO, max 50 messages)
- **Summary**: Progressive summarization
- **Entity**: Extracted entities (PERSON, ORG, LOCATION, etc.)
- **Embedding**: Vector representations for semantic search

## Testing Expectations
- Use `pytest` for all tests
- Mock external API calls
- Test both success and error cases
- Aim for 80%+ coverage
- Follow pattern: `tests/test_{module}.py`

Example test:
```python
def test_export_conversation_memory():
    """Test conversation memory export / 測試對話記憶匯出 / 测试对话记忆导出"""
    engine = ExcelEngine("test_output.xlsx")
    messages = [
        {"role": "user", "content": "Hello", "timestamp": "2024-01-01"},
        {"role": "assistant", "content": "Hi there", "timestamp": "2024-01-01"},
    ]
    result = engine.export_conversation_memory(messages)
    assert os.path.exists(result)
```

## Error Handling
Always handle LLM API errors gracefully:
```python
try:
    response = llm_client.chat(messages)
    return response.content
except APIError as e:
    logger.error(f"LLM API error: {e}")
    return "Error processing request. Please try again."
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return "An unexpected error occurred."
```

## Integration Points

### LLM → Memory → Document Flow
```python
# 1. Get LLM response / 獲取 LLM 回應 / 获取 LLM 响应
response = llm_client.chat(messages)

# 2. Add to memory / 加入記憶 / 加入记忆
memory.add_message("assistant", response.content)

# 3. Extract entities / 提取實體 / 提取实体
nlu_result = nlu.process(response.content)
for entity in nlu_result.entities:
    memory.add_entity(entity.name, entity.type, entity.description)

# 4. Export to document / 匯出至文件 / 导出至文档
pipeline.export_excel()
pipeline.export_pptx()
```

## Multilingual Support
When generating text content:
- Use placeholders for multilingual strings
- Store translations in config/settings.yaml or dedicated i18n files
- Support EN, ZH-TW, ZH-CN at minimum

## Performance Considerations
- Use generators for large data processing
- Implement pagination for memory retrieval
- Cache embedding results
- Use async/await for concurrent LLM calls

## Security Best Practices
- Never hardcode API keys
- Use environment variables or secure config
- Validate all user inputs
- Sanitize data before document export
- Log security-relevant events

## Configuration Files
- `config/settings.yaml`: Main configuration
- `schemas/memory_schema.sql`: Database schema
- `schemas/memory_layout.yaml`: Memory layer config
- `schemas/project_scenarios.yaml`: Use case definitions

## Quick Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run demo pipeline
python src/pipelines/document_pipeline.py

# Run specific module
python src/excel/excel_engine.py
```

## When Suggesting Code
1. **Always include type hints**
2. **Write trilingual docstrings**
3. **Follow existing patterns in similar modules**
4. **Consider error handling**
5. **Think about testability**
6. **Maintain separation of concerns**

## Architecture Principles
- **Separation of Concerns**: Engines handle file I/O, memory handles data, pipeline orchestrates
- **Dependency Injection**: Pass dependencies rather than creating them
- **Interface Segregation**: Keep base classes focused
- **DRY**: Extract common patterns to base classes or utilities
- **SOLID**: Follow SOLID principles for maintainable code

## Remember
- This is a **multilingual project** (EN, ZH-TW, ZH-CN)
- This is an **open-source project** (MIT License)
- This integrates with **9 major LLM providers**
- The goal is **LLM conversation → structured documents**
- Code should be **production-ready and well-tested**

# Open-Source Component Registry & LLM Integration Blueprint
# 開源組件全覽與 LLM 整合藍圖
# 开源组件全览与 LLM 整合蓝图

---

## 1. Document Generation / 文件生成 / 文档生成

### python-pptx
- **PyPI**: `pip install python-pptx`
- **Use**: Create PowerPoint presentations programmatically
- **用途 (繁)**: 以程式方式建立 PowerPoint 簡報
- **用途 (简)**: 以程序方式创建 PowerPoint 演示文稿
- **LLM Integration / LLM 接入點 / LLM 接入点**:
  - Store LLM conversation summaries as slides / 將 LLM 對話摘要存為幻燈片
  - Auto-generate presentation from entity memory / 從實體記憶自動生成簡報
  - Visualize knowledge graph on slides / 在幻燈片上視覺化知識圖譜
- **Code**: `src/pptx/pptx_engine.py`

### openpyxl
- **PyPI**: `pip install openpyxl`
- **Use**: Read/write Excel .xlsx files
- **用途 (繁)**: 讀寫 Excel .xlsx 檔案
- **用途 (简)**: 读写 Excel .xlsx 文件
- **LLM Integration / LLM 接入點 / LLM 接入点**:
  - Export embedding vectors to Excel for analysis / 將嵌入向量匯出至 Excel 分析
  - Store conversation memory as structured worksheets / 將對話記憶存為結構化工作表
  - Training data curation and export / 訓練資料策展與匯出
- **Code**: `src/excel/excel_engine.py`

### python-docx
- **PyPI**: `pip install python-docx`
- **Use**: Create/modify Word documents
- **用途 (繁)**: 建立/修改 Word 文件
- **用途 (简)**: 创建/修改 Word 文档
- **LLM Integration**: Generate meeting minutes, reports from LLM output

### reportlab
- **PyPI**: `pip install reportlab`
- **Use**: Generate PDF documents
- **用途 (繁)**: 生成 PDF 文件
- **用途 (简)**: 生成 PDF 文档
- **LLM Integration**: Export LLM analysis results as formatted PDFs

---

## 2. NLU Pipeline / NLU 管線 / NLU 管线

### spaCy
- **Integration**: Named Entity Recognition (NER) feeds entity_memory table
- **接入 (繁)**: 命名實體辨識 (NER) 供給 entity_memory 表
- **接入 (简)**: 命名实体识别 (NER) 供给 entity_memory 表
- **Flow**: `text → spaCy NER → entity_memory → Neo4j KG → openpyxl export`

### sentence-transformers
- **Integration**: Generate embeddings for semantic search
- **接入 (繁)**: 生成語義搜尋的嵌入向量
- **接入 (简)**: 生成语义搜索的嵌入向量
- **Flow**: `text → sentence-transformers → embedding_store → FAISS index`

### jieba
- **Integration**: Chinese text segmentation for NLU pipeline
- **接入 (繁)**: NLU 管線的中文分詞
- **接入 (简)**: NLU 管线的中文分词
- **Flow**: `中文文本 → jieba → spaCy → entity extraction`

---

## 3. Knowledge Graph / 知識圖譜 / 知识图谱

### Neo4j + NetworkX
- **Integration**: Store and query entity relationships
- **接入 (繁)**: 儲存和查詢實體關係
- **接入 (简)**: 储存和查询实体关系
- **Flow**: `entities → kg_triples table → Neo4j → PyVis visualization → PPTX slides`

---

## 4. Vector Store / 向量儲存 / 向量存储

### FAISS / ChromaDB / Qdrant
- **Integration**: Index embeddings for RAG retrieval
- **接入 (繁)**: 索引嵌入向量供 RAG 檢索
- **接入 (简)**: 索引嵌入向量供 RAG 检索
- **Flow**: `embedding → vector_store → similarity_search → LLM context → response`

---

## 5. LLM Memory / LLM 記憶 / LLM 记忆

### LangChain Memory
- **Types**: ConversationBufferMemory, ConversationSummaryMemory, EntityMemory
- **類型 (繁)**: 對話緩衝記憶、對話摘要記憶、實體記憶
- **类型 (简)**: 对话缓冲记忆、对话摘要记忆、实体记忆
- **Integration**: All memory types export to Excel/PPTX via document engine

### Mem0 / Zep
- **Integration**: Long-term persistent memory across sessions
- **接入 (繁)**: 跨會話的長期持久記憶
- **接入 (简)**: 跨会话的长期持久记忆

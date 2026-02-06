# SACA Office Intelligence Blueprint & Architecture
# SACA 办公智能蓝图与架构
# SACA 辦公智能藍圖與架構

## 1. Open Source Technology Stack / 开源技术栈 / 開源技術棧

This module leverages the following open-source libraries to bridge the gap between traditional office formats and modern AI capabilities.
本模块利用以下开源库将传统办公格式与现代 AI 能力连接起来。
本模組利用以下開源庫將傳統辦公格式與現代 AI 能力連接起來。

### 1.1 Core Libraries / 核心库 / 核心庫

| Library / 库 / 庫 | Language | Function / 功能 / 功能 | AI Role / AI 角色 / AI 角色 |
| :--- | :--- | :--- | :--- |
| **openpyxl** | Python | Read/Write Excel (.xlsx) files.<br>读写 Excel 文件。<br>讀寫 Excel 文件。 | **Long-term Memory Storage (长期记忆存储 / 長期記憶存儲)**:<br>Stores vectors/embeddings in hidden sheets.<br>Encodes Knowledge Graph nodes as rows. |
| **python-pptx** | Python | Create/Modify PowerPoint (.pptx) files.<br>创建/修改 PowerPoint 文件。<br>創建/修改 PowerPoint 文件。 | **Presentation Agent (演示代理 / 演示代理)**:<br>Visualizes dialog summaries.<br>Generates reports from AI reasoning chains. |
| **pptxgenjs** | JavaScript | Client-side PPT generation.<br>客户端 PPT 生成。<br>客戶端 PPT 生成。 | **Frontend Visualization (前端可视化 / 前端可視化)**:<br>Browser-based dashboard export.<br>Real-time slide creation from UI. |
| **LangChain** | Python/JS | LLM orchestration.<br>LLM 编排。<br>LLM 編排。 | **Cognitive Controller (认知控制器 / 認知控制器)**:<br>Manages prompt flows between Excel data and LLMs. |

---

## 2. Artificial Intelligence Integration / 人工智能集成 / 人工智能集成

### 2.1 NLU & Intent Recognition / NLU 与意图识别 / NLU 與意圖識別

*   **English**: Extracts intent from Excel cell comments or PPT speaker notes to trigger workflows.
*   **Simplified Chinese**: 从 Excel 单元格注释或 PPT 演讲者备注中提取意图以触发工作流。
*   **Traditional Chinese**: 從 Excel 儲存格註釋或 PPT 演講者備註中提取意圖以觸發工作流。

### 2.2 Knowledge Graph (KG) / 知识图谱 / 知識圖譜

*   **Concept**: Use Excel worksheets as adjacency matrices or node lists.
*   **Implementation**:
    *   Sheet `Nodes`: Defines entities (ID, Name, Type, Embedding).
    *   Sheet `Edges`: Defines relationships (SourceID, TargetID, RelationType).
*   **Access**: The `excel_memory.py` module parses these sheets into a graph structure for RAG.

### 2.3 LLM Memory System / LLM 记忆系统 / LLM 記憶系統

*   **Embedding Storage / Embedding 存储 / Embedding 存儲**:
    *   Embeddings (e.g., from OpenAI `text-embedding-3-small`) are serialized as Base64 strings or JSON arrays and stored in a specific column in Excel.
    *   **Retrieval**: Python script reads rows, computes cosine similarity, and retrieves relevant context.
*   **Automatic Summarization / 自动摘要 / 自動摘要**:
    *   Conversation history is periodically summarized by the LLM and appended to a "Daily Log" Excel sheet.
    *   `ppt_agent.py` can visualize these summaries into a daily briefing slide.

---

## 3. User Scenario Definition / 用户场景定义 / 用戶場景定義

**Identity**: `donniechen92@gmail.com`
**Providers**: OpenAI, Google AI, Microsoft AI, X.AI, Claude AI, Perplexity AI, DeepSeek, Tencent AI.

### Data Table Schema Strategy / 数据表 Schema 策略 / 數據表 Schema 策略

| Field / 字段 / 欄位 | Description / 描述 / 描述 |
| :--- | :--- |
| `scenario_id` | Unique identifier (e.g., `SCN-001`). |
| `provider` | AI Provider (e.g., `openai`, `deepseek`). |
| `stage` | Current stage (e.g., `Ideation`, `Development`, `Audit`). |
| `memory_context` | JSON blob containing relevant memory phrases. |
| `last_updated` | Timestamp. |

---

## 4. Repository Structure / 仓库结构 / 倉庫結構

The executable template structure for this module:

```
saca/
├── applications/
│   └── office_intelligence/
│       ├── schemas/                # YAML/JSON configs (Schema definitions)
│       │   └── user_scenarios.yaml
│       ├── src/                    # Source Code
│       │   ├── llm_bridge.py       # Multi-provider LLM adapter
│       │   ├── excel_memory.py     # openpyxl wrapper for Memory/KG
│       │   └── ppt_agent.py        # python-pptx wrapper for Visualization
│       ├── BLUEPRINT.md            # This document
│       └── README.md
├── .github/
│   └── workflows/
│       └── office_intelligence_ci.yml # CI Automation
```

---

## 5. Automation Pipeline / 自动化流水线 / 自動化流水線

**Tool**: GitHub Actions

### Workflow Steps / 流程步骤 / 流程步驟

1.  **Checkout Code**: Pull the repository.
2.  **Setup Python**: Install Python 3.11.
3.  **Install Dependencies**: `pip install openpyxl python-pptx openai anthropic`.
4.  **Linting**: Check code style (flake8).
5.  **Test**: Run unit tests (pytest) to verify Excel reading/writing and PPT generation.

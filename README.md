# Document-AI Open Source Blueprint / 文件AI開源藍圖 / 文档AI开源蓝图

> **Owner / 負責人 / 负责人**: donniechen92@gmail.com
> **License**: MIT

---

## Table of Contents / 目錄 / 目录

1. [Open-Source Component Registry / 開源組件全覽 / 开源组件全览](#1-open-source-component-registry)
2. [AI Platform Integration / AI平台整合 / AI平台整合](#2-ai-platform-integration)
3. [Architecture Overview / 架構總覽 / 架构总览](#3-architecture-overview)
4. [Data Schema & Memory Layout / 資料表結構與記憶體佈局 / 数据表结构与内存布局](#4-data-schema--memory-layout)
5. [Repository Structure / 倉庫結構 / 仓库结构](#5-repository-structure)
6. [Quick Start / 快速開始 / 快速开始](#6-quick-start)
7. [CI/CD Pipeline / 持續整合流程 / 持续集成流程](#7-cicd-pipeline)
8. [AI Coding Assistant Integration / AI編碼助手整合 / AI编码助手整合](#8-ai-coding-assistant-integration)

---

## 1. Open-Source Component Registry

### 1.1 Document Generation Libraries / 文件生成函式庫 / 文档生成函数库

| Component / 組件 / 组件 | PyPI Package | Description (EN) | 說明 (繁體) | 说明 (简体) | License |
|---|---|---|---|---|---|
| **python-pptx** | `python-pptx` | Create/update PowerPoint (.pptx) files | 建立/更新 PowerPoint (.pptx) 檔案 | 创建/更新 PowerPoint (.pptx) 文件 | MIT |
| **openpyxl** | `openpyxl` | Read/write Excel 2010+ (.xlsx) files | 讀寫 Excel 2010+ (.xlsx) 檔案 | 读写 Excel 2010+ (.xlsx) 文件 | MIT |
| **python-docx** | `python-docx` | Create/update Word (.docx) documents | 建立/更新 Word (.docx) 文件 | 创建/更新 Word (.docx) 文档 | MIT |
| **xlsxwriter** | `XlsxWriter` | Write Excel .xlsx files with charts/images | 寫入含圖表的 Excel .xlsx 檔案 | 写入含图表的 Excel .xlsx 文件 | BSD |
| **reportlab** | `reportlab` | PDF generation library | PDF 生成函式庫 | PDF 生成函数库 | BSD |
| **pdfplumber** | `pdfplumber` | Extract text/tables from PDF | 從 PDF 提取文字/表格 | 从 PDF 提取文字/表格 | MIT |
| **camelot-py** | `camelot-py` | PDF table extraction | PDF 表格提取 | PDF 表格提取 | MIT |
| **tabula-py** | `tabula-py` | PDF table extraction (Java-based) | PDF 表格提取（基於 Java） | PDF 表格提取（基于 Java） | MIT |

### 1.2 NLU & NLP Libraries / 自然語言理解函式庫 / 自然语言理解函数库

| Component / 組件 / 组件 | Package | Description (EN) | 說明 (繁體) | 说明 (简体) | License |
|---|---|---|---|---|---|
| **spaCy** | `spacy` | Industrial NLP pipeline (tokenization, NER, POS) | 工業級 NLP 管線（分詞、命名實體、詞性標注） | 工业级 NLP 管线（分词、命名实体、词性标注） | MIT |
| **NLTK** | `nltk` | Classic NLP toolkit (corpora, tokenizers) | 經典 NLP 工具包（語料庫、分詞器） | 经典 NLP 工具包（语料库、分词器） | Apache 2.0 |
| **Transformers** | `transformers` | HuggingFace model hub (BERT, GPT, T5, etc.) | HuggingFace 模型中心（BERT、GPT、T5 等） | HuggingFace 模型中心（BERT、GPT、T5 等） | Apache 2.0 |
| **sentence-transformers** | `sentence-transformers` | Sentence/text embeddings | 句子/文本嵌入向量 | 句子/文本嵌入向量 | Apache 2.0 |
| **jieba** | `jieba` | Chinese text segmentation | 中文分詞 | 中文分词 | MIT |
| **LangChain** | `langchain` | LLM application framework (chains, agents, memory) | LLM 應用框架（鏈、代理、記憶） | LLM 应用框架（链、代理、记忆） | MIT |
| **LlamaIndex** | `llama-index` | Data framework for LLM (RAG, indexing) | LLM 資料框架（RAG、索引） | LLM 数据框架（RAG、索引） | MIT |

### 1.3 Knowledge Graph Libraries / 知識圖譜函式庫 / 知识图谱函数库

| Component / 組件 / 组件 | Package | Description (EN) | 說明 (繁體) | 说明 (简体) | License |
|---|---|---|---|---|---|
| **NetworkX** | `networkx` | Graph creation & analysis | 圖形建立與分析 | 图形创建与分析 | BSD |
| **Neo4j Python** | `neo4j` | Neo4j graph DB driver | Neo4j 圖資料庫驅動 | Neo4j 图数据库驱动 | Apache 2.0 |
| **rdflib** | `rdflib` | RDF graph parsing & serialization | RDF 圖形解析與序列化 | RDF 图形解析与序列化 | BSD |
| **PyVis** | `pyvis` | Interactive graph visualization | 互動式圖形視覺化 | 交互式图形可视化 | BSD |

### 1.4 Embedding & Vector Store / 嵌入向量與向量儲存 / 嵌入向量与向量存储

| Component / 組件 / 组件 | Package | Description (EN) | 說明 (繁體) | 说明 (简体) | License |
|---|---|---|---|---|---|
| **FAISS** | `faiss-cpu` | Facebook AI Similarity Search | Facebook AI 相似度搜尋 | Facebook AI 相似度搜索 | MIT |
| **ChromaDB** | `chromadb` | Open-source embedding database | 開源嵌入向量資料庫 | 开源嵌入向量数据库 | Apache 2.0 |
| **Pinecone Client** | `pinecone-client` | Managed vector database client | 託管向量資料庫客戶端 | 托管向量数据库客户端 | Apache 2.0 |
| **Weaviate** | `weaviate-client` | AI-native vector database | AI 原生向量資料庫 | AI 原生向量数据库 | BSD |
| **Qdrant** | `qdrant-client` | High-perf vector similarity search | 高效能向量相似度搜尋 | 高性能向量相似度搜索 | Apache 2.0 |

### 1.5 LLM Memory Systems / LLM 記憶系統 / LLM 记忆系统

| Component / 組件 / 组件 | Package | Description (EN) | 說明 (繁體) | 说明 (简体) | License |
|---|---|---|---|---|---|
| **LangChain Memory** | `langchain` | Conversation buffer/summary/entity memory | 對話緩衝/摘要/實體記憶 | 对话缓冲/摘要/实体记忆 | MIT |
| **Mem0** | `mem0ai` | Self-improving memory layer for LLMs | LLM 自我改善記憶層 | LLM 自我改善记忆层 | Apache 2.0 |
| **Zep** | `zep-python` | Long-term memory for AI assistants | AI 助手長期記憶 | AI 助手长期记忆 | Apache 2.0 |
| **Motorhead** | `motorhead` | Memory & context management server | 記憶與上下文管理伺服器 | 记忆与上下文管理服务器 | Apache 2.0 |

---

## 2. AI Platform Integration

### All Registered Platforms / 所有註冊平台 / 所有注册平台

> Account: **donniechen92@gmail.com**

| Platform / 平台 | API Provider | Models / 模型 | Integration Point / 接入點 / 接入点 |
|---|---|---|---|
| **OpenAI** | `openai` | GPT-4o, GPT-4-turbo, o1, o3, DALL-E 3 | `src/llm_api/openai_client.py` |
| **Google AI (Gemini)** | `google-generativeai` | Gemini 2.0 Flash, Gemini Pro, Imagen 3 | `src/llm_api/google_client.py` |
| **Microsoft Azure AI** | `openai` (Azure endpoint) | GPT-4, Phi-3, Azure Copilot | `src/llm_api/azure_client.py` |
| **Anthropic (Claude)** | `anthropic` | Claude Opus 4, Sonnet 4, Haiku | `src/llm_api/anthropic_client.py` |
| **X.AI (Grok)** | `openai`-compatible | Grok-2, Grok-3 | `src/llm_api/xai_client.py` |
| **Perplexity AI** | `openai`-compatible | pplx-70b-online, sonar | `src/llm_api/perplexity_client.py` |
| **DeepSeek** | `openai`-compatible | DeepSeek-V3, DeepSeek-R1 | `src/llm_api/deepseek_client.py` |
| **Tencent AI (Hunyuan)** | `tencentcloud-sdk` | Hunyuan-Large, Hunyuan-Pro | `src/llm_api/tencent_client.py` |
| **Hugging Face** | `huggingface_hub` | Any open model (Llama, Mistral, etc.) | `src/llm_api/huggingface_client.py` |

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Document-AI Open Source Blueprint             │
│                    文件AI開源藍圖 / 文档AI开源蓝图                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Excel    │  │ PPTX     │  │ PDF      │  │ Word         │   │
│  │ openpyxl │  │ pptx     │  │ reportlab│  │ python-docx  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘   │
│       └──────────────┼──────────────┼───────────────┘           │
│                      ▼                                          │
│            ┌─────────────────┐                                  │
│            │  Document Engine │  文件引擎 / 文档引擎             │
│            └────────┬────────┘                                  │
│                     ▼                                           │
│  ┌──────────────────────────────────────┐                       │
│  │        LLM Memory Layer              │                       │
│  │        LLM 記憶層 / LLM 记忆层       │                       │
│  │  ┌────────┐ ┌────────┐ ┌──────────┐  │                       │
│  │  │Buffer  │ │Summary │ │Entity    │  │                       │
│  │  │Memory  │ │Memory  │ │Memory    │  │                       │
│  │  │緩衝記憶│ │摘要記憶│ │實體記憶  │  │                       │
│  │  └────────┘ └────────┘ └──────────┘  │                       │
│  └──────────────────┬───────────────────┘                       │
│                     ▼                                           │
│  ┌──────────────────────────────────────┐                       │
│  │    NLU + Knowledge Graph Layer       │                       │
│  │    NLU + 知識圖譜層 / 知识图谱层     │                       │
│  │  ┌────────┐ ┌────────┐ ┌──────────┐  │                       │
│  │  │spaCy   │ │Neo4j   │ │Embedding │  │                       │
│  │  │NER/POS │ │Graph   │ │FAISS/    │  │                       │
│  │  │        │ │Store   │ │Chroma    │  │                       │
│  │  └────────┘ └────────┘ └──────────┘  │                       │
│  └──────────────────┬───────────────────┘                       │
│                     ▼                                           │
│  ┌──────────────────────────────────────┐                       │
│  │       Multi-LLM API Gateway          │                       │
│  │       多LLM API 閘道 / 网关          │                       │
│  │  OpenAI│Google│Azure│Claude│DeepSeek  │                       │
│  │  X.AI  │Perplexity│Tencent│HuggingFace│                      │
│  └──────────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Schema & Memory Layout

See full definitions: [`schemas/`](./schemas/)

- `schemas/memory_schema.sql` — Memory table DDL / 記憶表 DDL / 记忆表 DDL
- `schemas/memory_layout.yaml` — Memory layout config / 記憶體佈局 / 内存布局
- `schemas/project_scenarios.yaml` — All project scenarios / 全專案場景 / 全项目场景

---

## 5. Repository Structure

```
copilot-/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # CI pipeline / 持續整合 / 持续集成
│       └── release.yml               # Release pipeline / 發佈流程 / 发布流程
├── config/
│   └── settings.yaml                 # Global config / 全域設定 / 全局设置
├── docs/
│   └── COMPONENT_REGISTRY.md         # Full component list / 組件全覽 / 组件全览
├── schemas/
│   ├── memory_schema.sql             # DB schema / 資料表結構 / 数据表结构
│   ├── memory_layout.yaml            # Memory layout / 記憶體佈局 / 内存布局
│   └── project_scenarios.yaml        # Scenario defs / 場景定義 / 场景定义
├── src/
│   ├── excel/
│   │   └── excel_engine.py           # openpyxl operations / Excel操作
│   ├── pptx/
│   │   └── pptx_engine.py            # python-pptx operations / PPT操作
│   ├── llm_memory/
│   │   └── memory_manager.py         # LLM memory integration / 記憶管理
│   ├── llm_api/
│   │   ├── base_client.py            # Abstract LLM client / 抽象LLM客戶端
│   │   ├── openai_client.py          # OpenAI
│   │   ├── google_client.py          # Google Gemini
│   │   ├── azure_client.py           # Azure OpenAI
│   │   ├── anthropic_client.py       # Anthropic Claude
│   │   ├── xai_client.py             # X.AI Grok
│   │   ├── perplexity_client.py      # Perplexity
│   │   ├── deepseek_client.py        # DeepSeek
│   │   ├── tencent_client.py         # Tencent Hunyuan
│   │   └── huggingface_client.py     # Hugging Face
│   ├── nlu/
│   │   └── nlu_pipeline.py           # NLU processing / NLU處理
│   ├── knowledge_graph/
│   │   └── kg_builder.py             # Knowledge graph / 知識圖譜
│   └── pipelines/
│       └── document_pipeline.py      # End-to-end pipeline / 端到端管線
├── templates/
│   ├── report_template.pptx          # PPTX template
│   └── data_template.xlsx            # Excel template
├── tests/
│   ├── test_excel.py
│   ├── test_pptx.py
│   ├── test_memory.py
│   └── test_llm_api.py
├── requirements.txt
├── pyproject.toml
├── AI_generation_NextGen_plan.md
└── README.md
```

---

## 6. Quick Start

```bash
# Clone / 克隆
git clone https://github.com/JiadongCHENDonnie/copilot-.git
cd copilot-

# Install / 安裝 / 安装
pip install -r requirements.txt

# Configure API keys / 設定 API 金鑰 / 设置 API 密钥
cp config/settings.yaml.example config/settings.yaml
# Edit config/settings.yaml with your API keys
# 編輯 config/settings.yaml 填入您的 API 金鑰

# Run demo pipeline / 執行示範管線 / 运行示范管线
python src/pipelines/document_pipeline.py
```

---

## 7. CI/CD Pipeline

Automated via GitHub Actions:
- **Lint**: `flake8` + `mypy` type checking
- **Test**: `pytest` with coverage
- **Build**: Package validation
- **Release**: Tag-based PyPI publish

See [`.github/workflows/ci.yml`](./.github/workflows/ci.yml)

---

## 8. AI Coding Assistant Integration

This project is optimized for use with **Google Jules** and **GitHub Copilot** AI coding assistants.

### 🤖 Google Jules (Asynchronous AI Agent)
**Jules** is ideal for large, autonomous coding tasks:
- Add new LLM provider integrations
- Implement new document export formats
- Large-scale refactoring
- Comprehensive test suite generation

Configuration: [`.ai/jules-config.yaml`](./.ai/jules-config.yaml)

### 🚀 GitHub Copilot (Real-Time AI Assistant)
**Copilot** is perfect for interactive development:
- Inline code suggestions
- Quick bug fixes
- Learning the codebase
- Writing individual functions

Configuration: [`.github/copilot-instructions.md`](./.github/copilot-instructions.md)

### 📖 Full Integration Guide
For detailed instructions on using both assistants with this Digital Engine, see:
**[AI Assistant Integration Guide](./docs/AI_ASSISTANT_INTEGRATION.md)**

---

*Built with open-source tools for the AI-driven document automation community.*
*以開源工具為 AI 驅動的文件自動化社群打造。*
*以开源工具为 AI 驱动的文档自动化社区打造。*

# AI Coding Assistant Integration Guide
# AI 編碼助手整合指南 / AI 编码助手整合指南

## Overview / 概述 / 概述

This guide explains how to use the **Document-AI Open Source Blueprint** (Digital Engine) with **Google Jules** and **GitHub Copilot** AI coding assistants to maximize productivity and code quality.

本指南說明如何使用 **Document-AI 開源藍圖**（數位引擎）配合 **Google Jules** 和 **GitHub Copilot** AI 編碼助手，以最大化生產力和程式碼品質。

本指南说明如何使用 **Document-AI 开源蓝图**（数字引擎）配合 **Google Jules** 和 **GitHub Copilot** AI 编码助手，以最大化生产力和代码质量。

---

## Table of Contents / 目錄 / 目录

1. [What is the Digital Engine?](#what-is-the-digital-engine)
2. [Google Jules Integration](#google-jules-integration)
3. [GitHub Copilot Integration](#github-copilot-integration)
4. [Comparison & When to Use Each](#comparison--when-to-use-each)
5. [Best Practices](#best-practices)
6. [Example Workflows](#example-workflows)

---

## What is the Digital Engine?

The **Document-AI Open Source Blueprint** (referred to as "Digital Engine") is a comprehensive AI platform that:

- Integrates with 9+ major LLM providers (OpenAI, Google, Anthropic, etc.)
- Converts LLM conversations into structured documents (Excel, PowerPoint, PDF, Word)
- Manages multi-layered memory systems (buffer, summary, entity, embedding)
- Builds knowledge graphs from conversation data
- Provides NLU pipelines for entity and relation extraction
- Supports multilingual operations (English, Traditional Chinese, Simplified Chinese)

**數位引擎**是一個全面的 AI 平台，可以：
- 整合 9+ 主要 LLM 提供者
- 將 LLM 對話轉換為結構化文件
- 管理多層記憶系統
- 從對話資料構建知識圖譜
- 提供 NLU 管線
- 支援多語言操作

**数字引擎**是一个全面的 AI 平台，可以：
- 整合 9+ 主要 LLM 提供者
- 将 LLM 对话转换为结构化文档
- 管理多层记忆系统
- 从对话数据构建知识图谱
- 提供 NLU 管线
- 支持多语言操作

---

## Google Jules Integration

### What is Jules?

**Jules** is Google's asynchronous AI coding assistant that:
- Runs autonomously in secure cloud VMs
- Handles entire coding tasks from start to finish
- Understands full codebase context
- Generates detailed change reports with audio changelogs
- Works across CLI, API, web, and IDE interfaces

**Jules** 是 Google 的非同步 AI 編碼助手：
- 在安全的雲端 VM 中自主運行
- 從頭到尾處理整個編碼任務
- 理解完整程式碼庫上下文
- 生成詳細的變更報告
- 跨 CLI、API、網頁和 IDE 介面工作

### Setting Up Jules with Digital Engine

1. **Install Jules CLI** (when available):
   ```bash
   # Jules is currently in preview - check Google AI for access
   # Jules 目前處於預覽階段 - 查看 Google AI 獲取訪問權限
   # Jules 目前处于预览阶段 - 查看 Google AI 获取访问权限
   ```

2. **Configuration File**:
   Jules automatically reads `.ai/jules-config.yaml` for project-specific instructions.
   
3. **Assign Tasks to Jules**:
   ```bash
   # Example: Add a new LLM provider
   jules assign "Add support for Anthropic Claude 3.7 Opus model to the LLM API clients"
   
   # Example: Implement new export format
   jules assign "Add PDF export functionality to the document pipeline using reportlab"
   
   # Example: Fix bug
   jules assign "Fix issue #123: Memory manager entity deduplication not working"
   ```

4. **Review Jules' Work**:
   Jules will:
   - Clone the repository
   - Analyze the codebase
   - Present a plan for approval
   - Implement the changes
   - Run tests
   - Submit a pull request

### Best Use Cases for Jules

✅ **Use Jules for:**
- Adding new LLM provider integrations
- Implementing new document export formats
- Large refactoring tasks (e.g., reorganizing module structure)
- Updating dependencies across multiple files
- Writing comprehensive test suites
- Documentation updates across multiple files
- Feature implementations requiring 5+ file changes

❌ **Don't use Jules for:**
- Quick single-line fixes
- Interactive debugging sessions
- Exploratory coding where you need real-time feedback
- Learning the codebase (use GitHub Copilot instead)

---

## GitHub Copilot Integration

### What is GitHub Copilot?

**GitHub Copilot** is Microsoft's real-time AI coding assistant that:
- Provides inline code suggestions as you type
- Acts as a pair programmer in your IDE
- Answers coding questions in real-time
- Can handle agentic tasks (issue triage, PR creation)
- Tightly integrated with GitHub ecosystem

**GitHub Copilot** 是 Microsoft 的即時 AI 編碼助手：
- 在您輸入時提供行內程式碼建議
- 在 IDE 中充當配對程式設計師
- 即時回答編碼問題
- 可處理代理任務
- 與 GitHub 生態系統緊密整合

### Setting Up GitHub Copilot with Digital Engine

1. **Install GitHub Copilot**:
   - Install Copilot extension in VS Code, Visual Studio, JetBrains IDEs, or Neovim
   - Sign in with your GitHub account
   - Ensure Copilot subscription is active

2. **Configuration File**:
   Copilot reads `.github/copilot-instructions.md` for project-specific guidelines.

3. **Using Copilot**:
   
   **Interactive Coding:**
   ```python
   # Start typing and Copilot suggests completions
   # 開始輸入，Copilot 會建議完成內容
   # 开始输入，Copilot 会建议完成内容
   
   def export_knowledge_graph_data(
       # Copilot will suggest the full function signature and implementation
   ```
   
   **Ask Questions:**
   ```
   # In Copilot Chat:
   "How do I add a new LLM provider to this project?"
   "Explain how the memory management system works"
   "Generate tests for the ExcelEngine class"
   ```
   
   **Code Explanation:**
   ```
   # Select code and ask Copilot:
   "Explain this function"
   "What are the potential issues with this code?"
   "How can I optimize this?"
   ```

### Best Use Cases for GitHub Copilot

✅ **Use Copilot for:**
- Writing individual functions and methods
- Quick bug fixes (1-3 file changes)
- Understanding existing code
- Writing unit tests for specific functions
- Implementing small features
- Code documentation
- Learning project patterns interactively

❌ **Don't use Copilot for:**
- Large multi-file refactorings
- Batch updates across many files
- Long-running tasks that block your workflow
- Tasks requiring extended autonomous execution

---

## Comparison & When to Use Each

| Aspect | Google Jules | GitHub Copilot |
|--------|-------------|----------------|
| **Execution Model** | Asynchronous, autonomous | Synchronous, interactive |
| **Best For** | Large tasks, features, refactors | Small edits, learning, quick fixes |
| **Context Window** | Full codebase via cloud VM | Limited to current file + context |
| **Task Granularity** | Coarse (entire features) | Fine (individual functions/lines) |
| **Workflow Integration** | Assign and forget | Active pair programming |
| **Resource Usage** | Cloud-based (no local impact) | Local IDE integration |
| **Approval Process** | Review plan before execution | Accept/reject suggestions inline |
| **Multi-file Changes** | Excellent | Good (but manual navigation) |
| **Learning Curve** | Moderate (task assignment) | Low (works as you code) |

### Recommended Workflow

**For New Features:**
1. Use **Jules** to implement the core feature (5+ files)
2. Use **Copilot** to refine and polish individual functions
3. Use **Copilot** to write additional edge case tests

**For Bug Fixes:**
1. Use **Copilot** for simple bugs (1-2 files)
2. Use **Jules** for complex bugs requiring multi-file changes

**For Learning:**
1. Use **Copilot** to understand existing code
2. Ask questions and get real-time explanations
3. Use Jules to see how a complete feature would be implemented

**For Maintenance:**
1. Use **Jules** for dependency updates, license updates, batch refactorings
2. Use **Copilot** for documentation touchups and comment improvements

---

## Best Practices

### General Guidelines

1. **Trilingual Support**:
   - Always maintain English, Traditional Chinese, and Simplified Chinese in docstrings
   - Both Jules and Copilot understand this project's multilingual convention

2. **Type Hints**:
   - Use type hints for all functions
   - Both assistants will generate better suggestions with proper types

3. **Testing**:
   - Write tests for all new features
   - Use Copilot to quickly generate test templates
   - Use Jules to write comprehensive test suites

4. **Documentation**:
   - Keep README.md updated when adding major features
   - Use Copilot for inline documentation
   - Use Jules for large documentation overhauls

### Digital Engine Specific Tips

1. **Adding LLM Providers**:
   ```bash
   # Use Jules for new provider integration
   jules assign "Add support for [Provider Name] LLM with models [Model List]"
   
   # Use Copilot for quick tweaks to existing providers
   # Open the provider file and let Copilot suggest modifications
   ```

2. **Document Export Features**:
   ```python
   # Use Copilot to start the function structure
   def export_new_format(self, data: list[dict[str, Any]]) -> str:
       """
       Export data to new format.
       # Copilot will suggest the trilingual version
   ```

3. **Memory Management**:
   ```bash
   # Use Jules for new memory layer types
   jules assign "Add temporal memory layer for time-based event storage"
   
   # Use Copilot for tweaking existing memory methods
   ```

---

## Example Workflows

### Workflow 1: Adding a New LLM Provider (Cohere)

**Using Jules** (Recommended for this task):
```bash
# Assign the task
jules assign "Add Cohere LLM provider support with Command-R and Command-R+ models to src/llm_api/"

# Jules will:
# 1. Analyze base_client.py pattern
# 2. Create cohere_client.py
# 3. Add tests to test_llm_api.py
# 4. Update README.md integration table
# 5. Update requirements.txt
# 6. Submit PR with detailed changelog
```

**Using Copilot** (Requires more manual steps):
```python
# 1. Create new file: src/llm_api/cohere_client.py
# 2. Start typing:

from .base_client import BaseLLMClient

class CohereClient(BaseLLMClient):
    """
    # Copilot suggests trilingual docstring
    
# 3. Let Copilot complete the class
# 4. Manually add tests
# 5. Manually update README
```

### Workflow 2: Quick Bug Fix

**Using Copilot** (Recommended for this task):
```python
# Bug: Entity deduplication not working in memory_manager.py

# 1. Open src/llm_memory/memory_manager.py
# 2. Navigate to add_entity method
# 3. Ask Copilot: "Why isn't entity deduplication working?"
# 4. Apply suggested fix
# 5. Ask Copilot: "Generate a test for entity deduplication"
# 6. Commit changes
```

### Workflow 3: Large Refactoring

**Using Jules** (Recommended for this task):
```bash
# Refactor: Separate concerns in document_pipeline.py

jules assign "Refactor document_pipeline.py: Extract export logic into separate ExportManager class, extract NLU processing into ProcessingManager class, maintain backward compatibility"

# Jules handles:
# - Creating new classes
# - Moving methods
# - Updating imports
# - Updating tests
# - Maintaining API compatibility
```

### Workflow 4: Interactive Development

**Using Both**:
```bash
# Phase 1: Feature skeleton with Jules
jules assign "Create initial structure for PDF export feature using reportlab, include basic PDFEngine class and integration points"

# Phase 2: Implementation details with Copilot
# After Jules creates the structure:
# - Open PDFEngine class
# - Use Copilot to implement individual export methods
# - Use Copilot chat to ask about reportlab best practices
# - Use Copilot to write unit tests for each method

# Phase 3: Polish with Copilot
# - Add edge case handling
# - Improve error messages
# - Add missing docstrings
```

---

## Troubleshooting

### Jules Issues

**Problem**: Jules doesn't understand project structure
- **Solution**: Check `.ai/jules-config.yaml` is properly formatted
- **Solution**: Provide more context in task description

**Problem**: Jules makes changes in wrong direction
- **Solution**: Review and decline the plan before execution
- **Solution**: Provide more specific requirements in task assignment

### Copilot Issues

**Problem**: Copilot suggestions don't follow project conventions
- **Solution**: Ensure `.github/copilot-instructions.md` is present
- **Solution**: Manually correct first suggestion, Copilot will learn

**Problem**: Copilot doesn't suggest trilingual docstrings
- **Solution**: Start typing all three languages, Copilot will complete
- **Solution**: Ask in Copilot chat: "Convert this to trilingual format"

---

## Additional Resources

### Digital Engine Documentation
- [README.md](../README.md) - Project overview
- [AI_generation_NextGen_plan.md](../AI_generation_NextGen_plan.md) - Vision and roadmap
- [docs/COMPONENT_REGISTRY.md](../docs/COMPONENT_REGISTRY.md) - Component details

### Jules Resources
- [Google Jules Official Site](https://ai.google.dev/jules) (when available)
- [Jules vs Copilot Comparison](https://markaicode.com/jules-vs-github-copilot-asynchronous-coding-comparison/)

### Copilot Resources
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Copilot Best Practices](https://github.blog/ai-and-ml/github-copilot/)

---

## Contributing

When contributing to this project:

1. **Use the AI assistants** - They're configured to understand our codebase
2. **Follow trilingual convention** - Use English, Traditional Chinese, Simplified Chinese
3. **Write tests** - For all new features and bug fixes
4. **Document changes** - Update relevant documentation files
5. **Follow patterns** - Maintain consistency with existing code

Both Jules and Copilot are powerful tools. Use them wisely, and they'll significantly boost your productivity on the Document-AI Open Source Blueprint!

---

*Last Updated: 2026-02-18*  
*最後更新：2026-02-18*  
*最后更新：2026-02-18*

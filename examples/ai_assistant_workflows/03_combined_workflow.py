"""
Example 3: Combined Jules + Copilot Workflow
組合式 Jules + Copilot 工作流程範例
组合式 Jules + Copilot 工作流程示例

This example demonstrates how to leverage both Google Jules and GitHub Copilot
together for maximum productivity in the Document-AI platform.

此範例展示如何同時利用 Google Jules 和 GitHub Copilot
在 Document-AI 平台中實現最大生產力。

此示例展示如何同时利用 Google Jules 和 GitHub Copilot
在 Document-AI 平台中实现最大生产力。
"""

# ==============================================================================
# Scenario: Building a Complete RAG Feature
# 場景：構建完整的 RAG 功能
# 场景：构建完整的 RAG 功能
# ==============================================================================

# Goal: Implement a Retrieval-Augmented Generation system that:
# 目標：實作檢索增強生成系統，具備以下功能：
# 目标：实现检索增强生成系统，具备以下功能：
# 1. Embeds conversation history
# 2. Stores embeddings in vector database (ChromaDB)
# 3. Retrieves relevant context for queries
# 4. Generates responses using LLM with retrieved context

# ==============================================================================
# Phase 1: Architecture Design with Jules
# 階段 1：使用 Jules 進行架構設計
# 阶段 1：使用 Jules 进行架构设计
# ==============================================================================

# Use Jules to create the foundational structure:
# 使用 Jules 建立基礎結構：
# 使用 Jules 创建基础结构：

"""
Jules Command:
---
jules assign "Create RAG (Retrieval-Augmented Generation) module for Document-AI platform.

Structure:
1. Create src/rag/ directory with:
   - __init__.py
   - rag_engine.py (main RAG orchestrator)
   - embedder.py (text embedding functionality)
   - retriever.py (vector search functionality)
   - context_builder.py (context window management)

2. RAGEngine class should:
   - Initialize with LLM client and vector store
   - Provide embed_documents() method
   - Provide query_with_context() method
   - Support ChromaDB and FAISS backends
   
3. Integration points:
   - Connect with existing MemoryManager
   - Use existing LLM clients from src/llm_api/
   - Export RAG results via document_pipeline.py
   
4. Include:
   - Trilingual docstrings (EN/ZH-TW/ZH-CN)
   - Type hints
   - Comprehensive tests in tests/test_rag.py
   - Update README.md with RAG section
   - Add to docs/COMPONENT_REGISTRY.md

Follow patterns from existing modules (excel_engine.py, memory_manager.py).
Add chromadb and sentence-transformers to requirements.txt.
"""

# Jules will:
# - Analyze existing codebase patterns
# - Create comprehensive module structure
# - Implement all base functionality
# - Generate test suite
# - Update documentation

# Expected timeline: 20-30 minutes autonomous execution
# 預期時間：20-30 分鐘自主執行
# 预期时间：20-30 分钟自主执行

# ==============================================================================
# Phase 2: Detailed Implementation with Copilot
# 階段 2：使用 Copilot 進行詳細實作
# 阶段 2：使用 Copilot 进行详细实现
# ==============================================================================

# After Jules creates the structure, use Copilot to add specific features:
# Jules 建立結構後，使用 Copilot 新增特定功能：
# Jules 创建结构后，使用 Copilot 添加特定功能：

# 1. Open src/rag/rag_engine.py
# 2. Add a method for semantic chunking:

from typing import Any


class RAGEngine:
    # ... Jules-generated base code ...
    
    def semantic_chunk_text(
        self,
        text: str,
        chunk_size: int = 512,
        overlap: int = 50
    ) -> list[dict[str, Any]]:
        """
        Split text into semantic chunks with overlap.
        將文本分割為語義區塊並設定重疊。
        将文本分割为语义块并设置重叠。
        
        Args:
            text: Input text to chunk / 要分塊的輸入文本 / 要分块的输入文本
            chunk_size: Target chunk size in tokens / 目標區塊大小（標記數）/ 目标块大小（标记数）
            overlap: Overlap between chunks / 區塊間重疊 / 块间重叠
            
        Returns:
            List of chunks with metadata / 帶有元資料的區塊列表 / 带有元数据的块列表
        """
        # Copilot suggests implementation:
        chunks = []
        # Let Copilot complete the logic
        # ... Copilot will suggest tokenization and chunking ...
        return chunks


# 3. Add hybrid search combining semantic and keyword:

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        semantic_weight: float = 0.7
    ) -> list[dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword matching.
        # Copilot completes trilingual docstring
        """
        # Copilot suggests combining vector search with BM25
        # ... implementation ...


# ==============================================================================
# Phase 3: Optimization with Both
# 階段 3：使用兩者進行優化
# 阶段 3：使用两者进行优化
# ==============================================================================

# Use Jules for batch optimizations:
# 使用 Jules 進行批次優化：
# 使用 Jules 进行批量优化：

"""
Jules Command:
---
jules assign "Optimize RAG module performance:
1. Add caching layer for embeddings (use functools.lru_cache)
2. Implement batch embedding for multiple documents
3. Add async support for concurrent LLM calls
4. Profile and optimize slow operations
5. Update tests to verify performance improvements
6. Document performance characteristics in docstrings"
"""

# Use Copilot for specific optimizations:
# 使用 Copilot 進行特定優化：
# 使用 Copilot 进行特定优化：

# Ask Copilot Chat:
"""
Copilot Chat Query:
---
How can I optimize this embedding function to handle 10,000 documents efficiently?
Suggest batching strategy, parallel processing, and caching approaches.
"""

# ==============================================================================
# Phase 4: Testing with Both
# 階段 4：使用兩者進行測試
# 阶段 4：使用两者进行测试
# ==============================================================================

# Jules generates comprehensive test suite:
# Jules 生成全面的測試套件：
# Jules 生成全面的测试套件：

"""
Jules Command:
---
jules assign "Create comprehensive test suite for RAG module:
1. Unit tests for each component (embedder, retriever, context_builder)
2. Integration tests for full RAG pipeline
3. Performance tests for large document sets
4. Edge case tests (empty queries, long documents, special characters)
5. Mock external dependencies (LLM APIs, vector stores)
6. Achieve 90%+ code coverage
Use pytest fixtures and parameterized tests."
"""

# Copilot adds specific test cases:
# Copilot 新增特定測試案例：
# Copilot 添加特定测试案例：

# Open tests/test_rag.py and ask Copilot:
"""
Copilot Chat Query:
---
Generate tests for edge cases:
1. Query with only stopwords
2. Document with mixed languages (EN/ZH)
3. Extremely long document (100k+ tokens)
4. Duplicate documents in corpus
5. Query with special characters and emojis
"""

# ==============================================================================
# Phase 5: Documentation with Both
# 階段 5：使用兩者進行文件化
# 阶段 5：使用两者进行文档化
# ==============================================================================

# Jules creates comprehensive documentation:
# Jules 建立全面的文件：
# Jules 创建全面的文档：

"""
Jules Command:
---
jules assign "Create complete documentation for RAG module:
1. Add detailed docstrings to all classes and methods
2. Create docs/RAG_GUIDE.md with:
   - Architecture overview
   - Usage examples
   - Configuration options
   - Performance tuning guide
   - Troubleshooting section
3. Add RAG section to README.md
4. Create example notebooks in examples/rag/
5. Add to docs/API_REFERENCE.md
All documentation should be trilingual (EN/ZH-TW/ZH-CN)."
"""

# Copilot refines documentation:
# Copilot 精煉文件：
# Copilot 精炼文档：

# Open docs/RAG_GUIDE.md and ask:
"""
Copilot Chat Query:
---
Improve this usage example by:
1. Adding error handling
2. Showing best practices
3. Including performance tips
4. Adding troubleshooting steps
"""

# ==============================================================================
# Real-World Example: Adding a Feature End-to-End
# 實際範例：端到端新增功能
# 实际示例：端到端添加功能
# ==============================================================================

# Feature: Multi-language RAG with automatic language detection
# 功能：具有自動語言檢測的多語言 RAG
# 功能：具有自动语言检测的多语言 RAG

# Step 1: Jules creates the structure
"""
jules assign "Add multi-language support to RAG module:
1. Create language_detector.py with auto-detection
2. Add language-specific embedders (EN, ZH-TW, ZH-CN)
3. Implement language-aware retrieval
4. Add language parameter to RAGEngine methods
5. Update tests and documentation"
"""

# Step 2: Copilot adds specific language handling
# Open src/rag/language_detector.py

# from langdetect import detect


def detect_language_example(text: str) -> str:
    """
    Detect language of input text.
    # Copilot suggests trilingual docstring
    """
    # Copilot suggests implementation with error handling
    try:
        lang_code = detect(text)
        # Map to supported languages
        if lang_code in ['zh-cn', 'zh-tw']:
            return 'zh'
        return lang_code
    except Exception:
        return 'en'  # Default fallback


# Step 3: Jules integrates everything
"""
jules assign "Integrate multi-language support into existing RAG pipeline:
1. Update RAGEngine to use language detector
2. Route to appropriate embedder based on language
3. Update all existing methods to support language parameter
4. Add language metadata to chunks
5. Update tests to cover multi-language scenarios
6. Update documentation with multi-language examples"
"""

# Step 4: Copilot adds edge cases and refinements
"""
Copilot Chat Query:
---
Add handling for:
1. Mixed-language documents
2. Code snippets in documentation
3. URLs and technical terms
4. User preference override for language
"""

# ==============================================================================
# Workflow Decision Matrix
# 工作流程決策矩陣
# 工作流程决策矩阵
# ==============================================================================

workflow_guide = {
    "Initial Structure": {
        "tool": "Jules",
        "reason": "Creates complete module structure efficiently",
        "example": "Creating new RAG module with all boilerplate"
    },
    "Specific Features": {
        "tool": "Copilot",
        "reason": "Interactive refinement with immediate feedback",
        "example": "Adding semantic_chunk_text method"
    },
    "Batch Updates": {
        "tool": "Jules",
        "reason": "Autonomous execution across many files",
        "example": "Adding type hints to entire module"
    },
    "Bug Fixes": {
        "tool": "Copilot (simple) or Jules (complex)",
        "reason": "Copilot for 1-2 file fixes, Jules for multi-file",
        "example": "Quick fix vs. refactoring bug"
    },
    "Test Generation": {
        "tool": "Jules (comprehensive) + Copilot (specific)",
        "reason": "Jules for full suite, Copilot for edge cases",
        "example": "Generate 100 tests with Jules, add 5 edge cases with Copilot"
    },
    "Documentation": {
        "tool": "Jules (initial) + Copilot (refinement)",
        "reason": "Jules creates structure, Copilot adds details",
        "example": "Create guide with Jules, improve examples with Copilot"
    },
    "Code Review": {
        "tool": "Copilot",
        "reason": "Real-time analysis and suggestions",
        "example": "Review PR with Copilot Chat"
    },
    "Learning": {
        "tool": "Copilot",
        "reason": "Interactive Q&A and exploration",
        "example": "Ask 'How does the memory system work?'"
    }
}

# ==============================================================================
# Tips for Combined Usage
# 組合使用技巧
# 组合使用技巧
# ==============================================================================

# 1. Start Big, Refine Small / 從大處著手，從小處精煉 / 从大处着手，从小处精炼
#    - Use Jules to create modules
#    - Use Copilot to polish methods

# 2. Parallel Workflows / 並行工作流程 / 并行工作流程
#    - Assign complex task to Jules
#    - Work on other features with Copilot while Jules runs

# 3. Context Switching / 上下文切換 / 上下文切换
#    - Jules for "assign and forget" tasks
#    - Copilot for "active development" tasks

# 4. Review Everything / 檢視所有內容 / 查看所有内容
#    - Always review Jules' PR before merging
#    - Always review Copilot suggestions before accepting

# 5. Maintain Standards / 維持標準 / 维持标准
#    - Both tools respect .ai/jules-config.yaml and .github/copilot-instructions.md
#    - Ensure trilingual documentation is maintained

# 6. Leverage Strengths / 利用優勢 / 利用优势
#    Jules: Large tasks, refactoring, batch operations
#    Copilot: Learning, debugging, quick edits, interactive development

print("Combined workflow examples loaded successfully!")
print("組合工作流程範例載入成功！")
print("组合工作流程示例加载成功！")

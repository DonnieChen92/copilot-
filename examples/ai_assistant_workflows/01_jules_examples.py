"""
Example 1: Using Digital Engine with Google Jules
使用 Google Jules 與數位引擎的範例
使用 Google Jules 与数字引擎的示例

This example demonstrates how to assign tasks to Jules for autonomous
completion of complex features in the Document-AI platform.

此範例展示如何將任務分配給 Jules，讓其自主完成 Document-AI 平台中的複雜功能。
此示例展示如何将任务分配给 Jules，让其自主完成 Document-AI 平台中的复杂功能。
"""

# ==============================================================================
# Example Task 1: Add a New LLM Provider (Cohere)
# 範例任務 1：新增 LLM 提供者 (Cohere)
# 示例任务 1：添加 LLM 提供者 (Cohere)
# ==============================================================================

# Jules Command / Jules 指令 / Jules 命令:
# jules assign "Add Cohere LLM provider integration to the Document-AI platform. \
#   Create src/llm_api/cohere_client.py implementing BaseLLMClient interface. \
#   Support Command-R and Command-R+ models. \
#   Include chat() and stream_chat() methods. \
#   Add trilingual docstrings (EN/ZH-TW/ZH-CN). \
#   Add tests to tests/test_llm_api.py. \
#   Update README.md AI Platform Integration table. \
#   Update requirements.txt with cohere dependency."

# Expected Jules Workflow / 預期 Jules 工作流程 / 预期 Jules 工作流程:
# 1. Jules clones repository and analyzes codebase
#    Jules 複製儲存庫並分析程式碼庫
#    Jules 克隆仓库并分析代码库
# 2. Jules reviews base_client.py to understand interface
#    Jules 檢視 base_client.py 以理解介面
#    Jules 查看 base_client.py 以理解接口
# 3. Jules presents implementation plan for approval
#    Jules 提出實施計劃以供批准
#    Jules 提出实施计划以供批准
# 4. After approval, Jules creates all necessary files
#    批准後，Jules 建立所有必要的檔案
#    批准后，Jules 创建所有必要的文件
# 5. Jules runs tests to verify implementation
#    Jules 執行測試以驗證實施
#    Jules 运行测试以验证实施
# 6. Jules submits PR with detailed changelog
#    Jules 提交 PR 並附上詳細的變更日誌
#    Jules 提交 PR 并附上详细的变更日志

# ==============================================================================
# Example Task 2: Implement PDF Export Feature
# 範例任務 2：實作 PDF 匯出功能
# 示例任务 2：实现 PDF 导出功能
# ==============================================================================

# Jules Command:
# jules assign "Implement PDF export functionality for the Document-AI platform. \
#   Create src/pdf/pdf_engine.py using reportlab library. \
#   Add class PDFEngine with methods: \
#   - export_conversation_memory(messages, filename) \
#   - export_entity_memory(entities, filename) \
#   - export_summary_memory(summaries, filename) \
#   Follow the pattern from excel_engine.py and pptx_engine.py. \
#   Include trilingual docstrings. \
#   Integrate with document_pipeline.py: add export_pdf() method. \
#   Write comprehensive tests in tests/test_pdf.py. \
#   Update README.md and docs/COMPONENT_REGISTRY.md."

# Expected Output Files / 預期輸出檔案 / 预期输出文件:
# - src/pdf/__init__.py
# - src/pdf/pdf_engine.py
# - tests/test_pdf.py
# - Updated: src/pipelines/document_pipeline.py
# - Updated: README.md
# - Updated: docs/COMPONENT_REGISTRY.md
# - Updated: requirements.txt (add reportlab)

# ==============================================================================
# Example Task 3: Large-Scale Refactoring
# 範例任務 3：大規模重構
# 示例任务 3：大规模重构
# ==============================================================================

# Jules Command:
# jules assign "Refactor the document_pipeline.py module to improve separation of concerns. \
#   Current issues: pipeline class handles too many responsibilities. \
#   Proposed structure: \
#   1. Create ExportManager class in src/pipelines/export_manager.py \
#      - Move all export_* methods to this class \
#   2. Create ProcessingManager class in src/pipelines/processing_manager.py \
#      - Move NLU and memory processing logic \
#   3. Update DocumentPipeline to use these managers \
#   4. Maintain backward compatibility - old API should still work \
#   5. Update all imports in test files \
#   6. Add tests for new classes \
#   7. Update documentation"

# This refactoring touches multiple files and requires careful planning
# Jules handles this autonomously while maintaining test coverage
# 這種重構涉及多個檔案並需要謹慎規劃
# Jules 自主處理這些工作，同時維持測試覆蓋率

# ==============================================================================
# Example Task 4: Batch Update Dependencies
# 範例任務 4：批次更新依賴項
# 示例任务 4：批量更新依赖项
# ==============================================================================

# Jules Command:
# jules assign "Update all dependencies in requirements.txt to their latest stable versions. \
#   For each dependency: \
#   1. Check for breaking changes in changelogs \
#   2. Update import statements if APIs changed \
#   3. Update code to use new APIs where beneficial \
#   4. Run full test suite after each update \
#   5. Document any breaking changes in CHANGELOG.md \
#   Focus on: openpyxl, python-pptx, langchain, transformers, spacy"

# Jules will systematically update each dependency and handle any compatibility issues
# Jules 會系統性地更新每個依賴項並處理任何相容性問題

# ==============================================================================
# Example Task 5: Generate Comprehensive Test Suite
# 範例任務 5：生成完整的測試套件
# 示例任务 5：生成完整的测试套件
# ==============================================================================

# Jules Command:
# jules assign "Create a comprehensive test suite for the llm_api module. \
#   Requirements: \
#   - Test each LLM client (OpenAI, Google, Anthropic, Azure, DeepSeek, X.AI, Perplexity, Tencent, HuggingFace) \
#   - Mock API calls to avoid actual API usage in tests \
#   - Test success cases and error handling \
#   - Test streaming functionality \
#   - Test API key validation \
#   - Achieve 90%+ code coverage for llm_api module \
#   - Use pytest fixtures for common test data \
#   - Follow existing test patterns in tests/test_excel.py"

# This generates a large, well-structured test suite autonomously
# 這會自主生成一個龐大且結構良好的測試套件

# ==============================================================================
# Example Task 6: Documentation Overhaul
# 範例任務 6：文件全面改寫
# 示例任务 6：文档全面改写
# ==============================================================================

# Jules Command:
# jules assign "Perform comprehensive documentation update across the codebase. \
#   Tasks: \
#   1. Audit all docstrings - ensure they are trilingual (EN/ZH-TW/ZH-CN) \
#   2. Add missing docstrings to any functions without them \
#   3. Update examples in docstrings to reflect current API \
#   4. Create API reference documentation in docs/API_REFERENCE.md \
#   5. Update type hints to latest Python 3.10+ syntax \
#   6. Add usage examples to each major module \
#   7. Create tutorial in docs/TUTORIAL.md for new users"

# Jules handles documentation across many files systematically
# Jules 系統性地處理多個檔案的文件

# ==============================================================================
# Monitoring Jules Progress
# 監控 Jules 進度
# 监控 Jules 进度
# ==============================================================================

# Check Jules task status / 檢查 Jules 任務狀態 / 检查 Jules 任务状态:
# jules status

# View detailed logs / 查看詳細日誌 / 查看详细日志:
# jules logs <task-id>

# Approve Jules' proposed plan / 批准 Jules 的提案計劃 / 批准 Jules 的提案计划:
# jules approve <task-id>

# Request changes to Jules' plan / 要求 Jules 修改計劃 / 要求 Jules 修改计划:
# jules revise <task-id> "Please also add integration with Azure OpenAI"

# Cancel a running task / 取消正在執行的任務 / 取消正在执行的任务:
# jules cancel <task-id>

# ==============================================================================
# Best Practices for Jules Usage
# Jules 使用最佳實踐
# Jules 使用最佳实践
# ==============================================================================

# 1. Be Specific / 具體明確 / 具体明确
#    - Provide clear requirements and acceptance criteria
#    - Reference specific files and patterns to follow
#    - Specify what should be updated (tests, docs, etc.)

# 2. Review Plans / 檢視計劃 / 查看计划
#    - Always review Jules' proposed plan before approval
#    - Check that it understands the architecture correctly
#    - Verify it's not making unnecessary changes

# 3. Use for Complex Tasks / 用於複雜任務 / 用于复杂任务
#    - Multi-file changes
#    - Large refactorings
#    - Comprehensive test generation
#    - Documentation updates

# 4. Provide Context / 提供上下文 / 提供上下文
#    - Reference the jules-config.yaml for project conventions
#    - Mention similar patterns in the codebase
#    - Link to relevant documentation

# 5. Trust but Verify / 信任但驗證 / 信任但验证
#    - Review the PR carefully
#    - Run tests locally
#    - Check that changes align with project goals

print("Jules examples loaded successfully!")
print("Jules 範例載入成功！")
print("Jules 示例加载成功！")

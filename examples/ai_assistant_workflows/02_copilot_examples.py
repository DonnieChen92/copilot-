"""
Example 2: Using Digital Engine with GitHub Copilot
使用 GitHub Copilot 與數位引擎的範例
使用 GitHub Copilot 与数字引擎的示例

This example demonstrates interactive development with GitHub Copilot
for the Document-AI platform.

此範例展示使用 GitHub Copilot 進行 Document-AI 平台的互動式開發。
此示例展示使用 GitHub Copilot 进行 Document-AI 平台的交互式开发。
"""

# ==============================================================================
# Example 1: Quick Bug Fix with Copilot
# 範例 1：使用 Copilot 快速修復錯誤
# 示例 1：使用 Copilot 快速修复错误
# ==============================================================================

# Scenario: Entity deduplication is not working in memory_manager.py
# 場景：memory_manager.py 中的實體去重不起作用
# 场景：memory_manager.py 中的实体去重不起作用

# Step 1: Open src/llm_memory/memory_manager.py in your IDE
# Step 2: Navigate to the add_entity method
# Step 3: Ask Copilot Chat:

"""
Copilot Chat Query:
---
@workspace Why isn't entity deduplication working in the add_entity method?
The same entities are being added multiple times even though we have a check.
"""

# Step 4: Copilot will analyze and suggest:
# - Check if entity comparison is case-sensitive
# - Verify entity_name normalization
# - Suggest adding entity.lower() or entity.strip()

# Step 5: Apply the suggested fix
# Step 6: Ask Copilot to generate a test:

"""
Copilot Chat Query:
---
Generate a pytest test that verifies entity deduplication in MemoryManager.
The test should add the same entity twice and verify only one is stored.
Include trilingual docstrings.
"""

# ==============================================================================
# Example 2: Implementing a New Function with Copilot
# 範例 2：使用 Copilot 實作新功能
# 示例 2：使用 Copilot 实现新功能
# ==============================================================================

# Task: Add a method to export knowledge graph to JSON format
# 任務：新增將知識圖譜匯出為 JSON 格式的方法
# 任务：添加将知识图谱导出为 JSON 格式的方法

# Open src/knowledge_graph/kg_builder.py and start typing:

from typing import Any
import json


class KnowledgeGraphBuilder:
    # ... existing code ...
    
    def export_to_json(self, filepath: str) -> dict[str, Any]:
        """
        Export knowledge graph to JSON format.
        將知識圖譜匯出為 JSON 格式。
        将知识图谱导出为 JSON 格式。
        
        Args:
            filepath: Output JSON file path / 輸出 JSON 檔案路徑 / 输出 JSON 文件路径
            
        Returns:
            Export statistics / 匯出統計資訊 / 导出统计信息
        """
        # As you type, Copilot will suggest:
        # 當您輸入時，Copilot 會建議：
        # 当您输入时，Copilot 会建议：
        
        # Copilot suggestion:
        graph_data = {
            "nodes": [
                {"id": node, "data": self.graph.nodes[node]}
                for node in self.graph.nodes()
            ],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "data": self.graph.edges[u, v]
                }
                for u, v in self.graph.edges()
            ],
            "metadata": {
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges(),
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        return graph_data["metadata"]


# ==============================================================================
# Example 3: Understanding Existing Code with Copilot
# 範例 3：使用 Copilot 理解現有程式碼
# 示例 3：使用 Copilot 理解现有代码
# ==============================================================================

# Scenario: You need to understand how the document pipeline works
# 場景：您需要了解文件管線如何運作
# 场景：您需要了解文档管线如何运作

# Open src/pipelines/document_pipeline.py
# Select the entire ingest_message method
# Ask Copilot Chat:

"""
Copilot Chat Query:
---
/explain

Follow-up questions:
- How does NLU processing integrate with memory storage?
- What happens if an entity is already in memory?
- Where are the knowledge graph triples actually stored?
"""

# Copilot will provide step-by-step explanation
# Copilot 會提供逐步說明
# Copilot 会提供逐步说明

# ==============================================================================
# Example 4: Writing Tests with Copilot
# 範例 4：使用 Copilot 編寫測試
# 示例 4：使用 Copilot 编写测试
# ==============================================================================

# Create a new test file or open existing: tests/test_excel.py
# Start typing a test function:

import pytest
from src.excel.excel_engine import ExcelEngine


def test_export_entity_memory_with_empty_list():
    """
    Test entity memory export with empty entity list.
    測試空實體列表的實體記憶匯出。
    测试空实体列表的实体记忆导出。
    """
    # Copilot will suggest:
    engine = ExcelEngine("test_empty.xlsx")
    result = engine.export_entity_memory([])
    
    # Verify file is created / 驗證檔案已建立 / 验证文件已创建
    assert result == "test_empty.xlsx"
    
    # Verify workbook has entity sheet / 驗證工作簿有實體工作表 / 验证工作簿有实体工作表
    # Copilot continues suggesting assertions...


# Then ask Copilot Chat:
"""
Copilot Chat Query:
---
Generate 5 more test cases for ExcelEngine.export_entity_memory():
1. Test with large entity list (100+ entities)
2. Test with special characters in entity names
3. Test with missing entity fields
4. Test with duplicate entities
5. Test with multilingual entity descriptions (EN/ZH-TW/ZH-CN)

Use pytest fixtures for common test data.
Include trilingual docstrings.
"""

# ==============================================================================
# Example 5: Refining Code with Copilot
# 範例 5：使用 Copilot 精煉程式碼
# 示例 5：使用 Copilot 精炼代码
# ==============================================================================

# Scenario: You have working code but want to improve it
# 場景：您有可運作的程式碼但想要改進它
# 场景：您有可运作的代码但想要改进它

# Original code in src/llm_api/openai_client.py:
def chat_original(self, messages):
    response = openai.ChatCompletion.create(
        model=self.model,
        messages=messages
    )
    return response.choices[0].message.content


# Ask Copilot Chat:
"""
Copilot Chat Query:
---
Improve this function:
1. Add proper error handling for API failures
2. Add retry logic with exponential backoff
3. Add type hints
4. Add trilingual docstring
5. Add logging
6. Handle rate limiting
"""

# Copilot suggests improved version:
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


def chat_improved(self, messages: list[dict[str, str]]) -> str:
    """
    Send chat messages to OpenAI and get response with retry logic.
    向 OpenAI 發送聊天訊息並透過重試邏輯獲取回應。
    向 OpenAI 发送聊天消息并通过重试逻辑获取响应。
    
    Args:
        messages: List of message dictionaries / 訊息字典列表 / 消息字典列表
        
    Returns:
        Response content / 回應內容 / 响应内容
        
    Raises:
        APIError: If API call fails after retries / 如果重試後 API 呼叫失敗
    """
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                timeout=30
            )
            return response.choices[0].message.content
            
        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Rate limit hit. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise
                
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            if attempt < max_retries - 1:
                time.sleep(base_delay)
            else:
                raise


# ==============================================================================
# Example 6: Interactive Feature Development
# 範例 6：互動式功能開發
# 示例 6：交互式功能开发
# ==============================================================================

# Task: Add support for exporting embeddings to CSV format
# 任務：新增支援將嵌入向量匯出為 CSV 格式
# 任务：添加支持将嵌入向量导出为 CSV 格式

# Step 1: Ask Copilot Chat for guidance
"""
Copilot Chat Query:
---
I want to add CSV export for embeddings in ExcelEngine.
What's the best approach given the existing export_embeddings method?
Should I create a separate CSVEngine or extend ExcelEngine?
"""

# Step 2: Based on Copilot's suggestion, start implementing
# Open src/excel/excel_engine.py and add:

import csv


def export_embeddings_to_csv(
    self,
    embeddings: list[dict[str, Any]],
    filepath: str = "embeddings.csv"
) -> str:
    """
    Export embedding vectors to CSV format.
    # Copilot completes the trilingual docstring
    """
    # Copilot suggests implementation:
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        if not embeddings:
            return filepath
            
        fieldnames = ['text', 'model', 'dimensions', 'vector']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for emb in embeddings:
            writer.writerow({
                'text': emb.get('text', ''),
                'model': emb.get('model', ''),
                'dimensions': len(emb.get('vector', [])),
                'vector': str(emb.get('vector', []))
            })
    
    return filepath


# Step 3: Ask Copilot to generate tests
"""
Copilot Chat Query:
---
Generate pytest tests for the export_embeddings_to_csv method.
Include edge cases like empty lists and large vectors.
"""

# ==============================================================================
# Example 7: Code Documentation with Copilot
# 範例 7：使用 Copilot 進行程式碼文件化
# 示例 7：使用 Copilot 进行代码文档化
# ==============================================================================

# Scenario: You have undocumented code that needs docstrings
# 場景：您有需要文件字串的未記錄程式碼
# 场景：您有需要文档字符串的未记录代码

# Select a function without docstring
# Ask Copilot Chat:
"""
Copilot Chat Query:
---
/doc

Add trilingual docstring (EN/ZH-TW/ZH-CN) following project conventions.
Include Args, Returns, and Raises sections if applicable.
"""

# ==============================================================================
# Example 8: Debugging with Copilot
# 範例 8：使用 Copilot 除錯
# 示例 8：使用 Copilot 调试
# ==============================================================================

# Scenario: You have a failing test
# 場景：您有一個失敗的測試
# 场景：您有一个失败的测试

# Select the failing test and the function it tests
# Ask Copilot Chat:
"""
Copilot Chat Query:
---
This test is failing with error: "AssertionError: Expected 3, got 2"
Analyze why the entity count is wrong.
"""

# Copilot analyzes both test and implementation and suggests fixes
# Copilot 分析測試和實作並建議修復
# Copilot 分析测试和实现并建议修复

# ==============================================================================
# Copilot Slash Commands Reference
# Copilot 斜線命令參考
# Copilot 斜线命令参考
# ==============================================================================

# /explain - Explain selected code / 解釋所選程式碼 / 解释所选代码
# /doc - Generate documentation / 生成文件 / 生成文档
# /fix - Suggest fix for issues / 建議問題修復 / 建议问题修复
# /tests - Generate tests / 生成測試 / 生成测试
# /optimize - Optimize performance / 優化效能 / 优化性能
# /simplify - Simplify code / 簡化程式碼 / 简化代码

# ==============================================================================
# Best Practices for Copilot Usage
# Copilot 使用最佳實踐
# Copilot 使用最佳实践
# ==============================================================================

# 1. Be Specific in Comments / 在註解中具體說明 / 在注释中具体说明
#    Write clear intent comments before coding
#    Copilot uses these to generate better suggestions

# 2. Review Suggestions / 檢視建議 / 查看建议
#    Don't blindly accept - always review and understand
#    Ensure suggestions follow project conventions

# 3. Use Context / 使用上下文 / 使用上下文
#    Keep related files open
#    Copilot learns from your current workspace

# 4. Iterate / 迭代 / 迭代
#    If first suggestion isn't right, modify and retry
#    Copilot learns from your corrections

# 5. Ask Questions / 提問 / 提问
#    Use Copilot Chat to understand codebase
#    Ask about patterns, architecture, best practices

# 6. Combine with IDE Features / 結合 IDE 功能 / 结合 IDE 功能
#    Use with IntelliSense, debugging, refactoring
#    Copilot complements, not replaces, IDE tools

print("GitHub Copilot examples loaded successfully!")
print("GitHub Copilot 範例載入成功！")
print("GitHub Copilot 示例加载成功！")

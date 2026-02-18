# AI Assistant Workflow Examples
# AI 助手工作流程範例
# AI 助手工作流程示例

This directory contains practical examples demonstrating how to use **Google Jules** and **GitHub Copilot** with the Document-AI Open Source Blueprint (Digital Engine).

此目錄包含實用範例，展示如何將 **Google Jules** 和 **GitHub Copilot** 與 Document-AI 開源藍圖（數位引擎）結合使用。

此目录包含实用示例，展示如何将 **Google Jules** 和 **GitHub Copilot** 与 Document-AI 开源蓝图（数字引擎）结合使用。

## Files / 檔案 / 文件

### [01_jules_examples.py](./01_jules_examples.py)
Examples of using Google Jules for autonomous, asynchronous coding tasks.

使用 Google Jules 進行自主、非同步編碼任務的範例。

使用 Google Jules 进行自主、异步编码任务的示例。

**Covered scenarios / 涵蓋場景 / 涵盖场景:**
- Adding new LLM providers
- Implementing document export features
- Large-scale refactoring
- Batch dependency updates
- Comprehensive test suite generation
- Documentation overhauls

### [02_copilot_examples.py](./02_copilot_examples.py)
Examples of using GitHub Copilot for interactive, real-time coding assistance.

使用 GitHub Copilot 進行互動式即時編碼協助的範例。

使用 GitHub Copilot 进行交互式实时编码协助的示例。

**Covered scenarios / 涵蓋場景 / 涵盖场景:**
- Quick bug fixes
- Implementing new functions
- Understanding existing code
- Writing tests
- Refining code quality
- Interactive feature development
- Code documentation
- Debugging

### [03_combined_workflow.py](./03_combined_workflow.py)
Examples of leveraging both Jules and Copilot together for maximum productivity.

同時利用 Jules 和 Copilot 以實現最大生產力的範例。

同时利用 Jules 和 Copilot 以实现最大生产力的示例。

**Covered scenarios / 涵蓋場景 / 涵盖场景:**
- Building complete features (RAG system example)
- Architecture design with Jules, implementation with Copilot
- Combined testing and optimization
- Documentation workflows
- Decision matrix for tool selection

## Quick Start / 快速開始 / 快速开始

### Prerequisites / 先決條件 / 先决条件

1. **For Google Jules:**
   - Access to Google Jules (currently in preview)
   - Jules CLI installed
   - Project cloned to Jules-accessible location

2. **For GitHub Copilot:**
   - GitHub Copilot subscription
   - Copilot extension installed in your IDE
   - Signed in to GitHub account

### Configuration Files / 配置檔案 / 配置文件

Both assistants use project-specific configuration files:

兩個助手都使用專案特定的配置檔案：

两个助手都使用项目特定的配置文件：

- **Jules Configuration:** [`.ai/jules-config.yaml`](../../.ai/jules-config.yaml)
- **Copilot Configuration:** [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md)

## Usage Examples / 使用範例 / 使用示例

### Running Jules Examples / 執行 Jules 範例 / 运行 Jules 示例

```bash
# View example commands
python examples/ai_assistant_workflows/01_jules_examples.py

# Assign a task to Jules (example)
jules assign "Add support for Claude 3.7 Opus model"

# Check Jules task status
jules status

# Approve Jules' plan
jules approve <task-id>
```

### Using Copilot Examples / 使用 Copilot 範例 / 使用 Copilot 示例

```bash
# View example patterns
python examples/ai_assistant_workflows/02_copilot_examples.py

# Then in your IDE:
# 1. Open any Python file in the project
# 2. Start typing - Copilot will suggest completions
# 3. Use Copilot Chat for questions and explanations
# 4. Use slash commands: /explain, /fix, /tests, /doc
```

### Combined Workflow / 組合工作流程 / 组合工作流程

```bash
# View combined workflow examples
python examples/ai_assistant_workflows/03_combined_workflow.py

# Typical workflow:
# 1. Use Jules for initial structure
jules assign "Create new RAG module structure"

# 2. While Jules runs, work on other features with Copilot
# 3. After Jules completes, refine with Copilot
# 4. Use Jules for batch updates, Copilot for specifics
```

## Key Concepts / 關鍵概念 / 关键概念

### When to Use Jules / 何時使用 Jules / 何时使用 Jules

✅ **Use Jules for:**
- Large, multi-file features
- Complex refactoring
- Batch updates across codebase
- Comprehensive test generation
- Documentation overhauls
- Dependency updates

### When to Use Copilot / 何時使用 Copilot / 何时使用 Copilot

✅ **Use Copilot for:**
- Interactive development
- Quick bug fixes
- Learning the codebase
- Writing individual functions
- Code refinement
- Debugging
- Documentation touchups

## Best Practices / 最佳實踐 / 最佳实践

1. **Be Specific / 具體明確 / 具体明确**
   - Provide clear requirements for Jules
   - Write descriptive comments for Copilot

2. **Review Everything / 檢視所有內容 / 查看所有内容**
   - Review Jules' PR before merging
   - Review Copilot suggestions before accepting

3. **Maintain Conventions / 維持慣例 / 维持惯例**
   - Both tools respect project conventions
   - Ensure trilingual documentation (EN/ZH-TW/ZH-CN)
   - Follow type hint requirements

4. **Leverage Strengths / 利用優勢 / 利用优势**
   - Use Jules for autonomy
   - Use Copilot for interactivity
   - Combine for maximum productivity

5. **Iterate and Learn / 迭代與學習 / 迭代与学习**
   - Refine your prompts based on results
   - Learn from both assistants' suggestions
   - Build your own workflow patterns

## Troubleshooting / 疑難排解 / 疑难排解

### Jules Issues

**Problem:** Jules doesn't follow project conventions
- **Solution:** Verify `.ai/jules-config.yaml` is properly configured
- **Solution:** Be more explicit in task description

**Problem:** Jules makes unexpected changes
- **Solution:** Review plan carefully before approval
- **Solution:** Use more specific requirements

### Copilot Issues

**Problem:** Suggestions don't match project style
- **Solution:** Ensure `.github/copilot-instructions.md` exists
- **Solution:** Manually correct first few suggestions

**Problem:** Trilingual docstrings not suggested
- **Solution:** Start typing all three languages
- **Solution:** Ask Copilot Chat to convert to trilingual

## Additional Resources / 其他資源 / 其他资源

### Project Documentation
- [Main README](../../README.md)
- [AI Assistant Integration Guide](../../docs/AI_ASSISTANT_INTEGRATION.md)
- [Component Registry](../../docs/COMPONENT_REGISTRY.md)
- [NextGen AI Plan](../../AI_generation_NextGen_plan.md)

### External Resources
- [Google Jules Documentation](https://ai.google.dev/jules) (when available)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Jules vs Copilot Comparison](https://markaicode.com/jules-vs-github-copilot-asynchronous-coding-comparison/)

## Contributing / 貢獻 / 贡献

If you develop new workflow patterns or examples:

如果您開發了新的工作流程模式或範例：

如果您开发了新的工作流程模式或示例：

1. Add them to this directory
2. Update this README
3. Follow trilingual documentation format
4. Include practical, runnable examples
5. Submit a PR

## License / 授權 / 授权

These examples are part of the Document-AI Open Source Blueprint and are licensed under MIT License.

這些範例是 Document-AI 開源藍圖的一部分，並在 MIT 授權下發布。

这些示例是 Document-AI 开源蓝图的一部分，并在 MIT 许可下发布。

---

*Happy coding with AI assistants!*  
*使用 AI 助手愉快編碼！*  
*使用 AI 助手愉快编码！*

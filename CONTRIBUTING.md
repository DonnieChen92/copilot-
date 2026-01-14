# Contributing Guide / 贡献指南

[English](#english) | [中文](#中文)

---

## English

### Welcome Contributors

Thank you for your interest in contributing to the TensorFlow Lite C Integration project! We welcome contributions from developers of all skill levels.

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### How to Contribute

#### 1. Fork the Repository

Fork the project on GitHub and clone your fork locally:

```bash
git clone https://github.com/your-username/copilot-.git
cd copilot-
```

#### 2. Create a Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
```

#### 3. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add bilingual comments (Chinese and English) where appropriate
- Update documentation as needed

#### 4. Test Your Changes

Run the test suite to ensure your changes don't break existing functionality:

```bash
make test
```

#### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of your changes"
```

#### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

#### 7. Submit a Pull Request

- Go to the original repository on GitHub
- Click "New Pull Request"
- Select your branch
- Provide a clear description of your changes
- Include relevant issue numbers if applicable

### Coding Standards

#### C Code Style

- Use consistent indentation (4 spaces)
- Follow K&R brace style
- Use meaningful variable and function names
- Keep functions focused and concise
- Maximum line length: 100 characters

#### Documentation

- Document all public functions with bilingual comments
- Include parameter descriptions
- Provide usage examples where appropriate
- Update README.md if adding new features

#### Comments

All comments should be bilingual (Chinese/English):

```c
// 初始化模型 / Initialize model
int model_init(Model* model) {
    // 验证参数 / Validate parameters
    if (!model) {
        return -1;
    }
    return 0;
}
```

### Reporting Issues

When reporting issues, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- System information (OS, compiler version, etc.)
- Code samples if applicable

### Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists or has been requested
- Clearly describe the feature and its benefits
- Provide use cases
- Consider contributing the implementation yourself

### Questions?

If you have questions, please:

- Check the documentation first
- Search existing issues
- Open a new issue with the "question" label

---

## 中文

### 欢迎贡献者

感谢您对TensorFlow Lite C集成项目的关注！我们欢迎所有技能水平的开发者贡献。

### 行为准则

- 尊重和包容
- 提供建设性反馈
- 关注对社区最有利的事情
- 对其他社区成员表现出同理心

### 如何贡献

#### 1. Fork仓库

在GitHub上Fork项目并在本地克隆您的fork：

```bash
git clone https://github.com/your-username/copilot-.git
cd copilot-
```

#### 2. 创建分支

为您的功能或错误修复创建新分支：

```bash
git checkout -b feature/your-feature-name
```

#### 3. 进行更改

- 编写清晰、可读的代码
- 遵循现有的代码风格
- 在适当的地方添加双语注释（中文和英文）
- 根据需要更新文档

#### 4. 测试您的更改

运行测试套件以确保您的更改不会破坏现有功能：

```bash
make test
```

#### 5. 提交您的更改

编写清晰、描述性的提交消息：

```bash
git add .
git commit -m "添加功能：您的更改描述"
```

#### 6. 推送到您的Fork

```bash
git push origin feature/your-feature-name
```

#### 7. 提交Pull Request

- 转到GitHub上的原始仓库
- 点击"New Pull Request"
- 选择您的分支
- 提供清晰的更改描述
- 如果适用，包含相关的issue编号

### 编码标准

#### C代码风格

- 使用一致的缩进（4个空格）
- 遵循K&R大括号风格
- 使用有意义的变量和函数名
- 保持函数专注和简洁
- 最大行长度：100个字符

#### 文档

- 使用双语注释记录所有公共函数
- 包含参数描述
- 在适当的地方提供使用示例
- 如果添加新功能，更新README.md

#### 注释

所有注释应该是双语的（中文/英文）：

```c
// 初始化模型 / Initialize model
int model_init(Model* model) {
    // 验证参数 / Validate parameters
    if (!model) {
        return -1;
    }
    return 0;
}
```

### 报告问题

报告问题时，请包含：

- 清晰、描述性的标题
- 重现问题的步骤
- 预期行为
- 实际行为
- 系统信息（操作系统、编译器版本等）
- 如果适用，提供代码示例

### 功能请求

我们欢迎功能请求！请：

- 检查该功能是否已存在或已被请求
- 清楚地描述功能及其好处
- 提供用例
- 考虑自己贡献实现

### 有疑问？

如果您有疑问，请：

- 首先检查文档
- 搜索现有的issues
- 使用"question"标签打开新issue

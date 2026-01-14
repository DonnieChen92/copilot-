# Testing Guide
# 测试指南

## Overview 概述

This document describes how to test the Google AI & Apple C Integration project.

本文档描述如何测试 Google AI 与 Apple C 语言集成项目。

## Quick Start Testing 快速开始测试

### Automated Quick Start 自动快速启动

Run the automated quick start script:

运行自动快速启动脚本：

```bash
./examples/quickstart.sh
```

This script will:
此脚本将：

1. Check prerequisites (gcc, make)
2. Build the project
3. Run both demonstration modules
4. Show next steps

1. 检查前提条件（gcc、make）
2. 构建项目
3. 运行两个演示模块
4. 显示下一步

## Manual Testing 手动测试

### Building the Project 构建项目

```bash
# Clean build
make clean

# Build without TensorFlow Lite
make

# Build with TensorFlow Lite support (requires TFLite library)
make USE_TENSORFLOW_LITE=1
```

### Testing TensorFlow Lite Inference Module 测试 TensorFlow Lite 推理模块

```bash
# Test with default model path
./build/tensorflow_lite_inference

# Test with custom model path
./build/tensorflow_lite_inference /path/to/your/model.tflite
```

**Expected Output (without TFLite library):**
**预期输出（无 TFLite 库）：**

```
=== TensorFlow Lite C API Integration ===
=== Google AI 与 Apple C 语言融合 ===

Using model path: my_model.tflite

TensorFlow Lite support not enabled. Build with USE_TENSORFLOW_LITE flag.
TensorFlow Lite 支持未启用。使用 USE_TENSORFLOW_LITE 标志构建。

✗ Failed. 失败。
```

**Expected Output (with TFLite library and valid model):**
**预期输出（有 TFLite 库和有效模型）：**

```
=== TensorFlow Lite C API Integration ===
=== Google AI 与 Apple C 语言融合 ===

Using model path: my_model.tflite

Model loaded successfully from: my_model.tflite
Interpreter created successfully
Tensors allocated successfully
Input tensor obtained, ready for data
Inference invoked successfully
Output tensor obtained
Resources cleaned up
Inference completed successfully.

✓ Success! 成功！
```

### Testing API Integration Module 测试 API 集成模块

```bash
./build/api_integration
```

**Expected Output:**
**预期输出：**

The module should display:
模块应显示：

1. API configurations for all providers
2. Model export operations
3. Packaging operations
4. Success confirmation

1. 所有提供商的 API 配置
2. 模型导出操作
3. 打包操作
4. 成功确认

## Validation Checklist 验证检查清单

### Build Validation 构建验证

- [ ] Project builds without errors
- [ ] No compilation warnings
- [ ] Build artifacts created in `build/` directory
- [ ] Both executables are created

- [ ] 项目无错误构建
- [ ] 无编译警告
- [ ] 在 `build/` 目录中创建构建产物
- [ ] 创建了两个可执行文件

### Functional Validation 功能验证

- [ ] TensorFlow Lite module runs without crashes
- [ ] API integration module runs without crashes
- [ ] Bilingual output is displayed correctly
- [ ] Error handling works properly

- [ ] TensorFlow Lite 模块运行无崩溃
- [ ] API 集成模块运行无崩溃
- [ ] 正确显示双语输出
- [ ] 错误处理正常工作

### Code Quality 代码质量

- [ ] No memory leaks (use valgrind if available)
- [ ] Proper resource cleanup
- [ ] Error messages are clear and helpful
- [ ] Code follows C11 standards

- [ ] 无内存泄漏（如可用，使用 valgrind）
- [ ] 正确的资源清理
- [ ] 错误消息清晰有用
- [ ] 代码遵循 C11 标准

## Advanced Testing 高级测试

### Memory Leak Testing 内存泄漏测试

If valgrind is available:
如果 valgrind 可用：

```bash
valgrind --leak-check=full --show-leak-kinds=all \
    ./build/tensorflow_lite_inference

valgrind --leak-check=full --show-leak-kinds=all \
    ./build/api_integration
```

### Performance Testing 性能测试

```bash
# Time the execution
time ./build/api_integration

# Profile with gprof (requires -pg compilation flag)
gcc -Wall -Wextra -std=c11 -O2 -pg -o build/api_integration src/api_integration.c
./build/api_integration
gprof build/api_integration gmon.out > analysis.txt
```

### Static Analysis 静态分析

```bash
# Using cppcheck (if available)
cppcheck --enable=all --std=c11 src/

# Using clang-tidy (if available)
clang-tidy src/*.c -- -std=c11
```

## Integration Testing 集成测试

### Swift Integration Testing Swift 集成测试

1. Create a new Xcode project
2. Add C source files
3. Create bridging header
4. Use the Swift example from `examples/SwiftIntegration.swift`
5. Build and run

1. 创建新的 Xcode 项目
2. 添加 C 源文件
3. 创建桥接头文件
4. 使用 `examples/SwiftIntegration.swift` 中的 Swift 示例
5. 构建并运行

### Model Conversion Testing 模型转换测试

```bash
# Test model conversion script
python3 examples/model_conversion.py --help

# Test with a sample model (requires TensorFlow)
# python3 examples/model_conversion.py sample_model.h5 tflite
```

## Continuous Integration 持续集成

### GitHub Actions Example GitHub Actions 示例

```yaml
name: Build and Test

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Install dependencies
      run: sudo apt-get update && sudo apt-get install -y gcc make
    
    - name: Build project
      run: make
    
    - name: Run tests
      run: |
        ./build/api_integration
        ./build/tensorflow_lite_inference || true
```

## Test Results Documentation 测试结果文档

### Recording Test Results 记录测试结果

Create a test results file:
创建测试结果文件：

```markdown
# Test Results 测试结果

Date: YYYY-MM-DD
Platform: [Linux/macOS/Windows]
Compiler: gcc version X.X.X

## Build Tests 构建测试
- [ ] Clean build: PASS/FAIL
- [ ] Warnings: NONE/LIST

## Functional Tests 功能测试
- [ ] TFLite module: PASS/FAIL
- [ ] API module: PASS/FAIL
- [ ] Bilingual output: PASS/FAIL

## Performance Tests 性能测试
- Build time: X.X seconds
- TFLite execution: X.X seconds
- API execution: X.X seconds

## Notes 备注
[Any additional observations]
```

## Troubleshooting Test Failures 故障排除测试失败

### Build Failures 构建失败

**Symptom:** Compilation errors
**症状：** 编译错误

**Solution:**
**解决方案：**
- Verify gcc is installed: `gcc --version`
- Verify make is installed: `make --version`
- Check for syntax errors in source files

### Runtime Failures 运行时失败

**Symptom:** Segmentation fault
**症状：** 段错误

**Solution:**
**解决方案：**
- Run with valgrind to identify memory issues
- Check for null pointer dereferences
- Verify proper resource initialization

### Missing Dependencies 缺少依赖

**Symptom:** Library not found errors
**症状：** 未找到库错误

**Solution:**
**解决方案：**
- For TensorFlow Lite: Build without USE_TENSORFLOW_LITE flag
- For Python dependencies: `pip install tensorflow tf2onnx coremltools`

## Best Practices 最佳实践

1. **Test Frequently** 经常测试
   - Test after each code change
   - Run full test suite before committing

2. **Document Results** 记录结果
   - Keep test logs
   - Document any failures and fixes

3. **Automate Testing** 自动化测试
   - Use CI/CD pipelines
   - Automate regression testing

4. **Follow Standards** 遵循标准
   - Truth, Fact, and Accuracy principles
   - No unsafe or toy code
   - Professional-grade quality

   - 真实、事实、准确性原则
   - 无不安全或玩具代码
   - 专业级质量

## Support 支持

For testing issues or questions:
对于测试问题或疑问：

- Review documentation: README.md, TECHNICAL_GUIDE.md
- Check examples: `examples/` directory
- Contact: donniechen92@gmail.com

---

**Remember 记住**: Always maintain Truth, Fact, and Accuracy in all testing procedures.

**记住**: 在所有测试程序中始终保持真实、事实和准确性。

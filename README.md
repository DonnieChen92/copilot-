# TensorFlow Lite C Integration / TensorFlow Lite C 集成

[English](#english) | [中文](#chinese)

---

## English

### Overview

This project provides a C language integration for TensorFlow Lite, enabling AI model inference on various platforms including iOS, macOS, and embedded systems. It features a clean API for model loading, inference execution, and integration with Google AI services.

### Features

- **TensorFlow Lite C API Wrapper**: Simplified interface for model loading and inference
- **Google AI Integration**: API wrapper for Google AI and Gemini services
- **Model Export Utilities**: Tools for packaging and deploying models
- **Cross-Platform Support**: Compatible with multiple platforms and architectures
- **Bilingual Documentation**: Full documentation in English and Chinese

### Project Structure

```
.
├── include/              # Header files
│   ├── tflite_wrapper.h     # TensorFlow Lite wrapper
│   ├── api_integration.h    # API integration
│   └── model_export.h       # Model export utilities
├── src/                  # Source files
│   ├── main.c               # Main application
│   ├── tflite_wrapper.c     # TensorFlow Lite implementation
│   ├── api_integration.c    # API integration implementation
│   └── model_export.c       # Model export implementation
├── tests/                # Test files
├── docs/                 # Documentation
├── examples/             # Example code
├── models/               # Model files
├── build/                # Build output directory
├── CMakeLists.txt        # CMake build configuration
└── Makefile              # Make build configuration
```

### Requirements

- **C Compiler**: GCC 7.0+ or Clang 6.0+
- **TensorFlow Lite C Library**: Version 2.0+
- **CMake**: Version 3.10+ (optional, for CMake builds)
- **Make**: Any recent version (optional, for Make builds)

### Building

#### Using CMake

```bash
mkdir build
cd build
cmake ..
make
```

#### Using Make

```bash
make
```

### Installation

```bash
make install
```

### Usage

#### Basic Example

```c
#include "tflite_wrapper.h"

int main() {
    TFLiteWrapper wrapper;
    
    // Initialize with model file
    if (tflite_wrapper_init(&wrapper, "model.tflite") != 0) {
        return 1;
    }
    
    // Get input tensor and fill with data
    TfLiteTensor* input = tflite_wrapper_get_input_tensor(&wrapper, 0);
    // ... fill input tensor ...
    
    // Run inference
    if (tflite_wrapper_invoke(&wrapper) != 0) {
        tflite_wrapper_cleanup(&wrapper);
        return 1;
    }
    
    // Get output tensor
    const TfLiteTensor* output = tflite_wrapper_get_output_tensor(&wrapper, 0);
    // ... process output ...
    
    // Cleanup
    tflite_wrapper_cleanup(&wrapper);
    return 0;
}
```

#### API Integration Example

```c
#include "api_integration.h"

int main() {
    APIConfig config;
    api_config_init(&config, "your-api-key", "https://api.google.com/gemini");
    
    APIResponse response;
    api_call_gemini(&config, "Hello, Gemini!", &response);
    
    if (response.status_code == 200) {
        printf("Response: %s\n", response.response_data);
    }
    
    api_response_free(&response);
    return 0;
}
```

### Testing

Run tests with:

```bash
make test
```

### License

This project is provided as-is for educational and research purposes.

### Contributing

Contributions are welcome! Please ensure all code follows the project's coding standards and includes appropriate bilingual comments.

---

## Chinese

### 概述

本项目提供了TensorFlow Lite的C语言集成，可在包括iOS、macOS和嵌入式系统在内的各种平台上实现AI模型推理。它提供了一个简洁的API用于模型加载、推理执行以及与Google AI服务的集成。

### 功能特性

- **TensorFlow Lite C API封装器**：简化的模型加载和推理接口
- **Google AI集成**：Google AI和Gemini服务的API封装器
- **模型导出工具**：用于打包和部署模型的工具
- **跨平台支持**：兼容多个平台和架构
- **双语文档**：完整的中英文文档

### 项目结构

```
.
├── include/              # 头文件
│   ├── tflite_wrapper.h     # TensorFlow Lite封装器
│   ├── api_integration.h    # API集成
│   └── model_export.h       # 模型导出工具
├── src/                  # 源文件
│   ├── main.c               # 主应用程序
│   ├── tflite_wrapper.c     # TensorFlow Lite实现
│   ├── api_integration.c    # API集成实现
│   └── model_export.c       # 模型导出实现
├── tests/                # 测试文件
├── docs/                 # 文档
├── examples/             # 示例代码
├── models/               # 模型文件
├── build/                # 构建输出目录
├── CMakeLists.txt        # CMake构建配置
└── Makefile              # Make构建配置
```

### 系统要求

- **C编译器**：GCC 7.0+ 或 Clang 6.0+
- **TensorFlow Lite C库**：版本2.0+
- **CMake**：版本3.10+（可选，用于CMake构建）
- **Make**：任何最新版本（可选，用于Make构建）

### 构建

#### 使用CMake

```bash
mkdir build
cd build
cmake ..
make
```

#### 使用Make

```bash
make
```

### 安装

```bash
make install
```

### 使用方法

#### 基本示例

```c
#include "tflite_wrapper.h"

int main() {
    TFLiteWrapper wrapper;
    
    // 使用模型文件初始化
    if (tflite_wrapper_init(&wrapper, "model.tflite") != 0) {
        return 1;
    }
    
    // 获取输入张量并填充数据
    TfLiteTensor* input = tflite_wrapper_get_input_tensor(&wrapper, 0);
    // ... 填充输入张量 ...
    
    // 运行推理
    if (tflite_wrapper_invoke(&wrapper) != 0) {
        tflite_wrapper_cleanup(&wrapper);
        return 1;
    }
    
    // 获取输出张量
    const TfLiteTensor* output = tflite_wrapper_get_output_tensor(&wrapper, 0);
    // ... 处理输出 ...
    
    // 清理资源
    tflite_wrapper_cleanup(&wrapper);
    return 0;
}
```

#### API集成示例

```c
#include "api_integration.h"

int main() {
    APIConfig config;
    api_config_init(&config, "your-api-key", "https://api.google.com/gemini");
    
    APIResponse response;
    api_call_gemini(&config, "你好，Gemini！", &response);
    
    if (response.status_code == 200) {
        printf("响应: %s\n", response.response_data);
    }
    
    api_response_free(&response);
    return 0;
}
```

### 测试

运行测试：

```bash
make test
```

### 许可证

本项目按原样提供，用于教育和研究目的。

### 贡献

欢迎贡献！请确保所有代码遵循项目的编码标准，并包含适当的双语注释。

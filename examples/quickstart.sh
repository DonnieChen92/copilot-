#!/bin/bash
# Quick Start Script for Google AI & Apple C Integration
# Google AI 与 Apple C 语言集成快速启动脚本

set -e

echo "=== Google AI & Apple C Integration Quick Start ==="
echo "=== Google AI 与 Apple C 语言集成快速启动 ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${YELLOW}Step 1: Checking prerequisites 检查前提条件${NC}"
if ! command -v gcc &> /dev/null; then
    echo -e "${RED}Error: gcc not found. Please install gcc first.${NC}"
    echo -e "${RED}错误：未找到 gcc。请先安装 gcc。${NC}"
    exit 1
fi

if ! command -v make &> /dev/null; then
    echo -e "${RED}Error: make not found. Please install make first.${NC}"
    echo -e "${RED}错误：未找到 make。请先安装 make。${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites check passed 前提条件检查通过${NC}"
echo ""

# Step 2: Build the project
echo -e "${YELLOW}Step 2: Building project 构建项目${NC}"
make clean
make

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build successful 构建成功${NC}"
else
    echo -e "${RED}✗ Build failed 构建失败${NC}"
    exit 1
fi
echo ""

# Step 3: Run demos
echo -e "${YELLOW}Step 3: Running demonstrations 运行演示${NC}"
echo ""

echo "--- API Integration Demo API 集成演示 ---"
./build/api_integration
echo ""

echo "--- TensorFlow Lite Inference Demo (without TFLite library) ---"
echo "--- TensorFlow Lite 推理演示（无 TFLite 库）---"
./build/tensorflow_lite_inference || true  # Expected to fail without TFLite library
echo ""

# Step 4: Show next steps
echo -e "${YELLOW}=== Next Steps 下一步 ===${NC}"
echo ""
echo "1. To enable TensorFlow Lite support:"
echo "   要启用 TensorFlow Lite 支持："
echo "   make USE_TENSORFLOW_LITE=1"
echo ""
echo "2. To use your own model:"
echo "   要使用您自己的模型："
echo "   ./build/tensorflow_lite_inference /path/to/your/model.tflite"
echo ""
echo "3. Read the documentation:"
echo "   阅读文档："
echo "   - README.md"
echo "   - TECHNICAL_GUIDE.md"
echo ""
echo -e "${GREEN}Setup complete! 设置完成！${NC}"

# Makefile for Google AI & Apple C Integration
# Google AI 与 Apple C 语言集成构建文件

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -O2
INCLUDES = 
LIBS = 

# TensorFlow Lite support (optional)
# Set USE_TENSORFLOW_LITE=1 to enable TensorFlow Lite support
# 设置 USE_TENSORFLOW_LITE=1 以启用 TensorFlow Lite 支持
ifdef USE_TENSORFLOW_LITE
	CFLAGS += -DUSE_TENSORFLOW_LITE
	INCLUDES += -I/usr/local/include/tensorflow
	LIBS += -ltensorflowlite_c
endif

# Source files
SRC_DIR = src
BUILD_DIR = build

# Targets
TARGETS = $(BUILD_DIR)/tensorflow_lite_inference $(BUILD_DIR)/api_integration

.PHONY: all clean directories help

all: directories $(TARGETS)

directories:
	@mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/tensorflow_lite_inference: $(SRC_DIR)/tensorflow_lite_inference.c
	@echo "Building TensorFlow Lite inference module..."
	@echo "构建 TensorFlow Lite 推理模块..."
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $< $(LIBS)
	@echo "✓ Built: $@"

$(BUILD_DIR)/api_integration: $(SRC_DIR)/api_integration.c
	@echo "Building API integration module..."
	@echo "构建 API 集成模块..."
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $< $(LIBS)
	@echo "✓ Built: $@"

clean:
	@echo "Cleaning build artifacts..."
	@echo "清理构建产物..."
	rm -rf $(BUILD_DIR)
	@echo "✓ Clean complete"

help:
	@echo "=== Google AI & Apple C Integration Build System ==="
	@echo "=== Google AI 与 Apple C 语言集成构建系统 ==="
	@echo ""
	@echo "Available targets 可用目标:"
	@echo "  all              - Build all modules (default) 构建所有模块（默认）"
	@echo "  clean            - Remove build artifacts 清理构建产物"
	@echo "  help             - Show this help message 显示此帮助信息"
	@echo ""
	@echo "Options 选项:"
	@echo "  USE_TENSORFLOW_LITE=1  - Enable TensorFlow Lite support 启用 TensorFlow Lite 支持"
	@echo ""
	@echo "Examples 示例:"
	@echo "  make                    - Build without TensorFlow Lite"
	@echo "  make USE_TENSORFLOW_LITE=1  - Build with TensorFlow Lite"
	@echo "  make clean              - Clean build directory"

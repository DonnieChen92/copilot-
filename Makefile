# Makefile for TensorFlow Lite C Integration
# TensorFlow Lite C集成的Makefile

# 编译器 / Compiler
CC = gcc

# 编译标志 / Compile flags
CFLAGS = -Wall -Wextra -pedantic -std=c11 -I./include

# TensorFlow Lite路径（需要根据实际安装位置调整）
# TensorFlow Lite paths (adjust according to actual installation location)
# TFLITE_INCLUDE = -I/path/to/tensorflow/lite/c
# TFLITE_LIB = -L/path/to/tensorflow/lite/lib -ltensorflowlite_c

# 链接标志 / Link flags
LDFLAGS = 

# 源文件 / Source files
SRCS = src/tflite_wrapper.c src/api_integration.c src/model_export.c src/main.c

# 目标文件 / Object files
OBJS = $(SRCS:.c=.o)

# 库源文件 / Library source files
LIB_SRCS = src/tflite_wrapper.c src/api_integration.c src/model_export.c
LIB_OBJS = $(LIB_SRCS:.c=.o)

# 可执行文件 / Executable
TARGET = tflite_app

# 静态库 / Static library
LIB = libtflite_integration.a

# 默认目标 / Default target
all: $(TARGET)

# 构建可执行文件 / Build executable
$(TARGET): $(OBJS)
	@echo "Linking $(TARGET) / 链接$(TARGET)"
	$(CC) $(OBJS) $(LDFLAGS) -o $(TARGET)
	@echo "Build complete / 构建完成"

# 构建静态库 / Build static library
$(LIB): $(LIB_OBJS)
	@echo "Creating static library $(LIB) / 创建静态库$(LIB)"
	ar rcs $(LIB) $(LIB_OBJS)

# 编译源文件 / Compile source files
%.o: %.c
	@echo "Compiling $< / 编译$<"
	$(CC) $(CFLAGS) -c $< -o $@

# 清理 / Clean
clean:
	@echo "Cleaning build files / 清理构建文件"
	rm -f $(OBJS) $(TARGET) $(LIB)

# 安装 / Install
install: $(TARGET)
	@echo "Installing $(TARGET) / 安装$(TARGET)"
	install -d $(DESTDIR)/usr/local/bin
	install -m 755 $(TARGET) $(DESTDIR)/usr/local/bin

# 卸载 / Uninstall
uninstall:
	@echo "Uninstalling $(TARGET) / 卸载$(TARGET)"
	rm -f $(DESTDIR)/usr/local/bin/$(TARGET)

# 帮助 / Help
help:
	@echo "Available targets / 可用目标:"
	@echo "  all       - Build the application / 构建应用程序"
	@echo "  clean     - Remove build files / 删除构建文件"
	@echo "  install   - Install the application / 安装应用程序"
	@echo "  uninstall - Uninstall the application / 卸载应用程序"
	@echo "  help      - Show this help message / 显示此帮助信息"

.PHONY: all clean install uninstall help

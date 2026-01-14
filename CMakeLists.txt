cmake_minimum_required(VERSION 3.10)

# 项目名称 / Project name
project(TensorFlowLiteIntegration VERSION 1.0.0 LANGUAGES C)

# C标准 / C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 编译选项 / Compile options
add_compile_options(-Wall -Wextra -pedantic)

# 包含目录 / Include directories
include_directories(${PROJECT_SOURCE_DIR}/include)

# TensorFlow Lite C API路径（需要根据实际安装位置调整）
# TensorFlow Lite C API path (adjust according to actual installation location)
# set(TFLITE_INCLUDE_DIR "/path/to/tensorflow/lite/c")
# set(TFLITE_LIB_DIR "/path/to/tensorflow/lite/lib")

# 如果已安装TensorFlow Lite，取消注释以下行
# Uncomment the following lines if TensorFlow Lite is installed
# include_directories(${TFLITE_INCLUDE_DIR})
# link_directories(${TFLITE_LIB_DIR})

# 源文件 / Source files
set(SOURCES
    src/tflite_wrapper.c
    src/api_integration.c
    src/model_export.c
)

# 创建静态库 / Create static library
add_library(tflite_integration STATIC ${SOURCES})

# 创建主可执行文件 / Create main executable
add_executable(tflite_app src/main.c)

# 链接库 / Link libraries
target_link_libraries(tflite_app tflite_integration)

# 如果已安装TensorFlow Lite，取消注释以下行
# Uncomment the following line if TensorFlow Lite is installed
# target_link_libraries(tflite_app tensorflowlite_c)

# 安装目标 / Install targets
install(TARGETS tflite_app tflite_integration
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# 安装头文件 / Install header files
install(DIRECTORY include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)

# 测试支持 / Test support
enable_testing()

# 添加测试（如果有）/ Add tests (if any)
# add_subdirectory(tests)

# 文档 / Documentation
# add_subdirectory(docs)

# 打印配置信息 / Print configuration information
message(STATUS "Project: ${PROJECT_NAME}")
message(STATUS "Version: ${PROJECT_VERSION}")
message(STATUS "C Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

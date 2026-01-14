#include <stdio.h>
#include <stdlib.h>
#include "../include/tflite_wrapper.h"
#include "../include/api_integration.h"
#include "../include/model_export.h"

/**
 * @brief 示例：使用TensorFlow Lite进行推理
 * Example: Using TensorFlow Lite for inference
 */
void example_tflite_inference() {
    printf("\n=== TensorFlow Lite Inference Example ===\n");
    printf("=== TensorFlow Lite 推理示例 ===\n\n");
    
    // 注意：这需要一个实际的.tflite模型文件
    // Note: This requires an actual .tflite model file
    const char* model_path = "example_model.tflite";
    
    TFLiteWrapper wrapper;
    
    printf("Initializing TFLite wrapper / 初始化TFLite封装器...\n");
    if (tflite_wrapper_init(&wrapper, model_path) != 0) {
        printf("Failed to initialize (model file may not exist) / 初始化失败（模型文件可能不存在）\n");
        printf("This is expected if you don't have a model file / 如果没有模型文件，这是正常的\n");
        return;
    }
    
    printf("Getting input tensor / 获取输入张量...\n");
    TfLiteTensor* input = tflite_wrapper_get_input_tensor(&wrapper, 0);
    if (!input) {
        printf("Failed to get input tensor / 获取输入张量失败\n");
        tflite_wrapper_cleanup(&wrapper);
        return;
    }
    
    // 在这里填充输入数据
    // Fill input data here
    printf("Filling input tensor with data / 填充输入张量数据...\n");
    
    printf("Running inference / 运行推理...\n");
    if (tflite_wrapper_invoke(&wrapper) != 0) {
        printf("Failed to run inference / 运行推理失败\n");
        tflite_wrapper_cleanup(&wrapper);
        return;
    }
    
    printf("Getting output tensor / 获取输出张量...\n");
    const TfLiteTensor* output = tflite_wrapper_get_output_tensor(&wrapper, 0);
    if (!output) {
        printf("Failed to get output tensor / 获取输出张量失败\n");
        tflite_wrapper_cleanup(&wrapper);
        return;
    }
    
    // 在这里处理输出数据
    // Process output data here
    printf("Processing output / 处理输出...\n");
    
    printf("Cleaning up / 清理资源...\n");
    tflite_wrapper_cleanup(&wrapper);
    
    printf("Inference completed successfully / 推理成功完成\n");
}

/**
 * @brief 示例：调用Google Gemini API
 * Example: Calling Google Gemini API
 */
void example_gemini_api() {
    printf("\n=== Gemini API Example ===\n");
    printf("=== Gemini API 示例 ===\n\n");
    
    APIConfig config;
    const char* api_key = "your-api-key-here";
    const char* endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent";
    
    printf("Initializing API configuration / 初始化API配置...\n");
    if (api_config_init(&config, api_key, endpoint) != 0) {
        printf("Failed to initialize API config / 初始化API配置失败\n");
        return;
    }
    
    // 验证API密钥
    // Validate API key
    printf("Validating API key / 验证API密钥...\n");
    if (!api_validate_key(api_key)) {
        printf("API key validation failed / API密钥验证失败\n");
        printf("Note: This is a placeholder key / 注意：这是一个占位符密钥\n");
    }
    
    printf("Calling Gemini API / 调用Gemini API...\n");
    APIResponse response;
    if (api_call_gemini(&config, "Hello, Gemini! 你好，Gemini！", &response) != 0) {
        printf("Failed to call Gemini API / 调用Gemini API失败\n");
        return;
    }
    
    printf("Response status: %d / 响应状态: %d\n", response.status_code);
    if (response.response_data) {
        printf("Response data: %s / 响应数据: %s\n", response.response_data);
    }
    
    printf("Freeing response / 释放响应...\n");
    api_response_free(&response);
    
    printf("API call completed / API调用完成\n");
}

/**
 * @brief 示例：模型导出和打包
 * Example: Model export and packaging
 */
void example_model_export() {
    printf("\n=== Model Export Example ===\n");
    printf("=== 模型导出示例 ===\n\n");
    
    const char* model_path = "example_model.tflite";
    const char* zip_path = "model_package.zip";
    
    printf("Validating model / 验证模型...\n");
    if (!model_validate(model_path)) {
        printf("Model validation failed (file may not exist) / 模型验证失败（文件可能不存在）\n");
        printf("This is expected if you don't have a model file / 如果没有模型文件，这是正常的\n");
    }
    
    printf("Packing model to ZIP / 将模型打包为ZIP...\n");
    if (model_pack_zip(model_path, zip_path) != 0) {
        printf("Failed to pack model / 打包模型失败\n");
        return;
    }
    
    printf("Creating deployment package / 创建部署包...\n");
    if (model_create_deployment_package(model_path, "deployment.zip", true) != 0) {
        printf("Failed to create deployment package / 创建部署包失败\n");
        return;
    }
    
    printf("Model export completed / 模型导出完成\n");
}

/**
 * @brief 主函数 / Main function
 */
int main() {
    printf("╔══════════════════════════════════════════════════════╗\n");
    printf("║  TensorFlow Lite C Integration Examples             ║\n");
    printf("║  TensorFlow Lite C 集成示例                          ║\n");
    printf("╚══════════════════════════════════════════════════════╝\n");
    
    example_tflite_inference();
    example_gemini_api();
    example_model_export();
    
    printf("\n╔══════════════════════════════════════════════════════╗\n");
    printf("║  All examples completed                              ║\n");
    printf("║  所有示例完成                                        ║\n");
    printf("╚══════════════════════════════════════════════════════╝\n");
    
    return 0;
}

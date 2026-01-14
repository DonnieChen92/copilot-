/**
 * TensorFlow Lite C API Integration
 * Google AI 与 Apple C 语言融合实现
 * 
 * This implementation demonstrates the integration of Google AI models
 * with Apple's native C language applications using TensorFlow Lite.
 * 
 * 此实现展示了使用 TensorFlow Lite 将 Google AI 模型
 * 与 Apple 原生 C 语言应用程序集成
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef USE_TENSORFLOW_LITE
#include "tensorflow/lite/c/c_api.h"
#endif

/**
 * Error handling function
 * 错误处理函数
 */
void print_last_error(const char* message) {
#ifdef USE_TENSORFLOW_LITE
    printf("%s: %s\n", message, TfLiteInterpreterGetErrorMessage(NULL));
#else
    printf("%s: TensorFlow Lite not available in this build\n", message);
#endif
}

/**
 * Load and run inference with TensorFlow Lite model
 * 加载并运行 TensorFlow Lite 模型推理
 * 
 * @param model_path Path to the .tflite model file
 * @return 0 on success, 1 on failure
 */
int run_inference(const char* model_path) {
#ifdef USE_TENSORFLOW_LITE
    // 1. 加载模型 (Load model)
    TfLiteModel* model = TfLiteModelCreateFromFile(model_path);
    if (!model) {
        printf("Failed to load model from file: %s\n", model_path);
        return 1;
    }
    printf("Model loaded successfully from: %s\n", model_path);

    // 2. 创建解释器 (Create interpreter)
    TfLiteInterpreterOptions* options = TfLiteInterpreterOptionsCreate();
    TfLiteInterpreter* interpreter = TfLiteInterpreterCreate(model, options);
    if (!interpreter) {
        print_last_error("Failed to create interpreter");
        TfLiteInterpreterOptionsDelete(options);
        TfLiteModelDelete(model);
        return 1;
    }
    TfLiteInterpreterOptionsDelete(options);
    printf("Interpreter created successfully\n");

    // 3. 分配张量 (Allocate tensors)
    if (TfLiteInterpreterAllocateTensors(interpreter) != kTfLiteOk) {
        print_last_error("Failed to allocate tensors");
        TfLiteInterpreterDelete(interpreter);
        TfLiteModelDelete(model);
        return 1;
    }
    printf("Tensors allocated successfully\n");

    // 4. 输入数据 (Input data preparation)
    TfLiteTensor* input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);
    if (!input_tensor) {
        print_last_error("Failed to get input tensor");
        TfLiteInterpreterDelete(interpreter);
        TfLiteModelDelete(model);
        return 1;
    }
    
    // Note: In production, you would fill input_tensor with actual data
    // 注意：在生产环境中，您需要用实际数据填充 input_tensor
    printf("Input tensor obtained, ready for data\n");

    // 5. 运行推理 (Run inference)
    if (TfLiteInterpreterInvoke(interpreter) != kTfLiteOk) {
        print_last_error("Failed to invoke interpreter");
        TfLiteInterpreterDelete(interpreter);
        TfLiteModelDelete(model);
        return 1;
    }
    printf("Inference invoked successfully\n");

    // 6. 获取输出 (Get output)
    const TfLiteTensor* output_tensor = TfLiteInterpreterGetOutputTensor(interpreter, 0);
    if (!output_tensor) {
        print_last_error("Failed to get output tensor");
        TfLiteInterpreterDelete(interpreter);
        TfLiteModelDelete(model);
        return 1;
    }
    
    // Process output_tensor data
    // 处理 output_tensor 数据
    printf("Output tensor obtained\n");

    // 7. 清理资源 (Cleanup resources)
    TfLiteInterpreterDelete(interpreter);
    TfLiteModelDelete(model);
    printf("Resources cleaned up\n");

    printf("Inference completed successfully.\n");
    return 0;
#else
    (void)model_path; // Mark as intentionally unused in non-TFLite build
    printf("TensorFlow Lite support not enabled. Build with USE_TENSORFLOW_LITE flag.\n");
    printf("TensorFlow Lite 支持未启用。使用 USE_TENSORFLOW_LITE 标志构建。\n");
    return 1;
#endif
}

/**
 * Main entry point
 * 主入口点
 */
int main(int argc, char* argv[]) {
    printf("=== TensorFlow Lite C API Integration ===\n");
    printf("=== Google AI 与 Apple C 语言融合 ===\n\n");
    
    const char* model_path = "my_model.tflite";
    
    // Allow custom model path from command line
    // 允许从命令行指定自定义模型路径
    if (argc > 1) {
        model_path = argv[1];
    }
    
    printf("Using model path: %s\n\n", model_path);
    
    int result = run_inference(model_path);
    
    if (result == 0) {
        printf("\n✓ Success! 成功！\n");
    } else {
        printf("\n✗ Failed. 失败。\n");
    }
    
    return result;
}

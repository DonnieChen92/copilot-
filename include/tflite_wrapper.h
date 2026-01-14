#ifndef TFLITE_WRAPPER_H
#define TFLITE_WRAPPER_H

#include "tensorflow/lite/c/c_api.h"

/**
 * @brief TFLite模型包装器结构 / TFLite model wrapper structure
 * 
 * 用于封装TensorFlow Lite模型和解释器
 * Used to encapsulate TensorFlow Lite model and interpreter
 */
typedef struct {
    TfLiteModel* model;
    TfLiteInterpreter* interpreter;
    TfLiteInterpreterOptions* options;
} TFLiteWrapper;

/**
 * @brief 初始化TFLite包装器 / Initialize TFLite wrapper
 * @param wrapper 指向TFLiteWrapper结构的指针 / Pointer to TFLiteWrapper structure
 * @param model_path 模型文件路径 / Model file path
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int tflite_wrapper_init(TFLiteWrapper* wrapper, const char* model_path);

/**
 * @brief 运行推理 / Run inference
 * @param wrapper 指向TFLiteWrapper结构的指针 / Pointer to TFLiteWrapper structure
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int tflite_wrapper_invoke(TFLiteWrapper* wrapper);

/**
 * @brief 获取输入张量 / Get input tensor
 * @param wrapper 指向TFLiteWrapper结构的指针 / Pointer to TFLiteWrapper structure
 * @param index 输入张量索引 / Input tensor index
 * @return 指向输入张量的指针 / Pointer to input tensor
 */
TfLiteTensor* tflite_wrapper_get_input_tensor(TFLiteWrapper* wrapper, int index);

/**
 * @brief 获取输出张量 / Get output tensor
 * @param wrapper 指向TFLiteWrapper结构的指针 / Pointer to TFLiteWrapper structure
 * @param index 输出张量索引 / Output tensor index
 * @return 指向输出张量的指针 / Pointer to output tensor
 */
const TfLiteTensor* tflite_wrapper_get_output_tensor(TFLiteWrapper* wrapper, int index);

/**
 * @brief 清理资源 / Clean up resources
 * @param wrapper 指向TFLiteWrapper结构的指针 / Pointer to TFLiteWrapper structure
 */
void tflite_wrapper_cleanup(TFLiteWrapper* wrapper);

/**
 * @brief 打印错误信息 / Print error message
 * @param message 错误消息 / Error message
 */
void tflite_print_error(const char* message);

#endif // TFLITE_WRAPPER_H

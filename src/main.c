#include <stdio.h>
#include "tensorflow/lite/c/c_api.h"

// 错误处理函数 / Error handling function
void print_last_error(const char* message) {
    printf("%s: %s\n", message, TfLiteInterpreterGetErrorMessage(NULL));
}

int main(int argc, char* argv[]) {
    // 1. 加载模型 / Load model
    TfLiteModel* model = TfLiteModelCreateFromFile("my_model.tflite");
    if (!model) {
        printf("Failed to load model from file.\n");
        return 1;
    }

    // 2. 创建解释器 / Create interpreter
    TfLiteInterpreterOptions* options = TfLiteInterpreterOptionsCreate();
    TfLiteInterpreter* interpreter = TfLiteInterpreterCreate(model, options);
    if (!interpreter) {
        print_last_error("Failed to create interpreter");
        TfLiteInterpreterOptionsDelete(options);
        TfLiteModelDelete(model);
        return 1;
    }
    TfLiteInterpreterOptionsDelete(options);

    // 3. 分配张量 / Allocate tensors
    if (TfLiteInterpreterAllocateTensors(interpreter) != kTfLiteOk) {
        print_last_error("Failed to allocate tensors");
        TfLiteInterpreterDelete(interpreter);
        TfLiteModelDelete(model);
        return 1;
    }

    // 4. 输入数据（此处为示例，需根据您的模型输入进行修改）/ Input data (example, modify according to your model)
    TfLiteTensor* input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);
    // ... 填充 input_tensor 数据 / Fill input_tensor data ...

    // 5. 运行推理 / Run inference
    if (TfLiteInterpreterInvoke(interpreter) != kTfLiteOk) {
        print_last_error("Failed to invoke interpreter");
        TfLiteInterpreterDelete(interpreter);
        TfLiteModelDelete(model);
        return 1;
    }

    // 6. 获取输出 / Get output
    const TfLiteTensor* output_tensor = TfLiteInterpreterGetOutputTensor(interpreter, 0);
    // ... 处理 output_tensor 数据 / Process output_tensor data ...

    // 7. 清理资源 / Clean up resources
    TfLiteInterpreterDelete(interpreter);
    TfLiteModelDelete(model);

    printf("Inference completed successfully.\n");
    return 0;
}

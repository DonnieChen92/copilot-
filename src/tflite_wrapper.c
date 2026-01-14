#include "tflite_wrapper.h"
#include <stdio.h>
#include <stdlib.h>

void tflite_print_error(const char* message) {
    printf("%s: %s\n", message, TfLiteInterpreterGetErrorMessage(NULL));
}

int tflite_wrapper_init(TFLiteWrapper* wrapper, const char* model_path) {
    if (!wrapper || !model_path) {
        fprintf(stderr, "Invalid arguments / 参数无效\n");
        return -1;
    }

    // 加载模型 / Load model
    wrapper->model = TfLiteModelCreateFromFile(model_path);
    if (!wrapper->model) {
        fprintf(stderr, "Failed to load model from file: %s / 无法从文件加载模型: %s\n", model_path, model_path);
        return -1;
    }

    // 创建解释器选项 / Create interpreter options
    wrapper->options = TfLiteInterpreterOptionsCreate();
    if (!wrapper->options) {
        fprintf(stderr, "Failed to create interpreter options / 无法创建解释器选项\n");
        TfLiteModelDelete(wrapper->model);
        wrapper->model = NULL;
        return -1;
    }

    // 创建解释器 / Create interpreter
    wrapper->interpreter = TfLiteInterpreterCreate(wrapper->model, wrapper->options);
    if (!wrapper->interpreter) {
        tflite_print_error("Failed to create interpreter / 无法创建解释器");
        TfLiteInterpreterOptionsDelete(wrapper->options);
        TfLiteModelDelete(wrapper->model);
        wrapper->options = NULL;
        wrapper->model = NULL;
        return -1;
    }

    // 分配张量 / Allocate tensors
    if (TfLiteInterpreterAllocateTensors(wrapper->interpreter) != kTfLiteOk) {
        tflite_print_error("Failed to allocate tensors / 无法分配张量");
        TfLiteInterpreterDelete(wrapper->interpreter);
        TfLiteInterpreterOptionsDelete(wrapper->options);
        TfLiteModelDelete(wrapper->model);
        wrapper->interpreter = NULL;
        wrapper->options = NULL;
        wrapper->model = NULL;
        return -1;
    }

    return 0;
}

int tflite_wrapper_invoke(TFLiteWrapper* wrapper) {
    if (!wrapper || !wrapper->interpreter) {
        fprintf(stderr, "Invalid wrapper or interpreter / 包装器或解释器无效\n");
        return -1;
    }

    if (TfLiteInterpreterInvoke(wrapper->interpreter) != kTfLiteOk) {
        tflite_print_error("Failed to invoke interpreter / 无法执行推理");
        return -1;
    }

    return 0;
}

TfLiteTensor* tflite_wrapper_get_input_tensor(TFLiteWrapper* wrapper, int index) {
    if (!wrapper || !wrapper->interpreter) {
        fprintf(stderr, "Invalid wrapper or interpreter / 包装器或解释器无效\n");
        return NULL;
    }

    return TfLiteInterpreterGetInputTensor(wrapper->interpreter, index);
}

const TfLiteTensor* tflite_wrapper_get_output_tensor(TFLiteWrapper* wrapper, int index) {
    if (!wrapper || !wrapper->interpreter) {
        fprintf(stderr, "Invalid wrapper or interpreter / 包装器或解释器无效\n");
        return NULL;
    }

    return TfLiteInterpreterGetOutputTensor(wrapper->interpreter, index);
}

void tflite_wrapper_cleanup(TFLiteWrapper* wrapper) {
    if (!wrapper) {
        return;
    }

    if (wrapper->interpreter) {
        TfLiteInterpreterDelete(wrapper->interpreter);
        wrapper->interpreter = NULL;
    }

    if (wrapper->options) {
        TfLiteInterpreterOptionsDelete(wrapper->options);
        wrapper->options = NULL;
    }

    if (wrapper->model) {
        TfLiteModelDelete(wrapper->model);
        wrapper->model = NULL;
    }
}

# API Documentation / API文档

[English](#english-api-documentation) | [中文](#中文api文档)

---

## English API Documentation

### TensorFlow Lite Wrapper API

#### `tflite_wrapper_init`

Initialize a TensorFlow Lite wrapper with a model file.

**Signature:**
```c
int tflite_wrapper_init(TFLiteWrapper* wrapper, const char* model_path);
```

**Parameters:**
- `wrapper`: Pointer to TFLiteWrapper structure
- `model_path`: Path to the .tflite model file

**Returns:**
- `0` on success
- Non-zero on failure

**Example:**
```c
TFLiteWrapper wrapper;
if (tflite_wrapper_init(&wrapper, "my_model.tflite") != 0) {
    fprintf(stderr, "Failed to initialize wrapper\n");
    return 1;
}
```

---

#### `tflite_wrapper_invoke`

Execute inference on the loaded model.

**Signature:**
```c
int tflite_wrapper_invoke(TFLiteWrapper* wrapper);
```

**Parameters:**
- `wrapper`: Pointer to initialized TFLiteWrapper structure

**Returns:**
- `0` on success
- Non-zero on failure

---

#### `tflite_wrapper_get_input_tensor`

Get input tensor for filling with data.

**Signature:**
```c
TfLiteTensor* tflite_wrapper_get_input_tensor(TFLiteWrapper* wrapper, int index);
```

**Parameters:**
- `wrapper`: Pointer to initialized TFLiteWrapper structure
- `index`: Input tensor index (usually 0 for single input models)

**Returns:**
- Pointer to input tensor on success
- NULL on failure

---

#### `tflite_wrapper_get_output_tensor`

Get output tensor after inference.

**Signature:**
```c
const TfLiteTensor* tflite_wrapper_get_output_tensor(TFLiteWrapper* wrapper, int index);
```

**Parameters:**
- `wrapper`: Pointer to initialized TFLiteWrapper structure
- `index`: Output tensor index (usually 0 for single output models)

**Returns:**
- Pointer to output tensor on success
- NULL on failure

---

#### `tflite_wrapper_cleanup`

Clean up and free all resources associated with the wrapper.

**Signature:**
```c
void tflite_wrapper_cleanup(TFLiteWrapper* wrapper);
```

**Parameters:**
- `wrapper`: Pointer to TFLiteWrapper structure

---

### API Integration

#### `api_config_init`

Initialize API configuration for Google AI services.

**Signature:**
```c
int api_config_init(APIConfig* config, const char* api_key, const char* endpoint);
```

**Parameters:**
- `config`: Pointer to APIConfig structure
- `api_key`: Your Google AI API key
- `endpoint`: API endpoint URL

**Returns:**
- `0` on success
- Non-zero on failure

---

#### `api_call_gemini`

Call Google Gemini API with a prompt.

**Signature:**
```c
int api_call_gemini(const APIConfig* config, const char* prompt, APIResponse* response);
```

**Parameters:**
- `config`: Pointer to initialized APIConfig
- `prompt`: Text prompt for Gemini
- `response`: Pointer to APIResponse structure to receive the response

**Returns:**
- `0` on success
- Non-zero on failure

---

#### `api_response_free`

Free memory allocated for API response.

**Signature:**
```c
void api_response_free(APIResponse* response);
```

**Parameters:**
- `response`: Pointer to APIResponse structure

---

### Model Export Utilities

#### `model_export`

Export model to a specified location.

**Signature:**
```c
int model_export(const ExportConfig* config);
```

**Parameters:**
- `config`: Pointer to ExportConfig structure containing export settings

**Returns:**
- `0` on success
- Non-zero on failure

---

#### `model_pack_zip`

Pack model into a ZIP archive.

**Signature:**
```c
int model_pack_zip(const char* model_path, const char* zip_path);
```

**Parameters:**
- `model_path`: Path to model file
- `zip_path`: Path for output ZIP file

**Returns:**
- `0` on success
- Non-zero on failure

---

#### `model_validate`

Validate a model file.

**Signature:**
```c
bool model_validate(const char* model_path);
```

**Parameters:**
- `model_path`: Path to model file

**Returns:**
- `true` if model is valid
- `false` if model is invalid

---

## 中文API文档

### TensorFlow Lite封装器API

#### `tflite_wrapper_init`

使用模型文件初始化TensorFlow Lite封装器。

**函数签名：**
```c
int tflite_wrapper_init(TFLiteWrapper* wrapper, const char* model_path);
```

**参数：**
- `wrapper`：指向TFLiteWrapper结构的指针
- `model_path`：.tflite模型文件的路径

**返回值：**
- 成功返回`0`
- 失败返回非零值

**示例：**
```c
TFLiteWrapper wrapper;
if (tflite_wrapper_init(&wrapper, "my_model.tflite") != 0) {
    fprintf(stderr, "初始化封装器失败\n");
    return 1;
}
```

---

#### `tflite_wrapper_invoke`

在加载的模型上执行推理。

**函数签名：**
```c
int tflite_wrapper_invoke(TFLiteWrapper* wrapper);
```

**参数：**
- `wrapper`：指向已初始化的TFLiteWrapper结构的指针

**返回值：**
- 成功返回`0`
- 失败返回非零值

---

#### `tflite_wrapper_get_input_tensor`

获取用于填充数据的输入张量。

**函数签名：**
```c
TfLiteTensor* tflite_wrapper_get_input_tensor(TFLiteWrapper* wrapper, int index);
```

**参数：**
- `wrapper`：指向已初始化的TFLiteWrapper结构的指针
- `index`：输入张量索引（单输入模型通常为0）

**返回值：**
- 成功返回指向输入张量的指针
- 失败返回NULL

---

#### `tflite_wrapper_get_output_tensor`

在推理后获取输出张量。

**函数签名：**
```c
const TfLiteTensor* tflite_wrapper_get_output_tensor(TFLiteWrapper* wrapper, int index);
```

**参数：**
- `wrapper`：指向已初始化的TFLiteWrapper结构的指针
- `index`：输出张量索引（单输出模型通常为0）

**返回值：**
- 成功返回指向输出张量的指针
- 失败返回NULL

---

#### `tflite_wrapper_cleanup`

清理并释放与封装器相关的所有资源。

**函数签名：**
```c
void tflite_wrapper_cleanup(TFLiteWrapper* wrapper);
```

**参数：**
- `wrapper`：指向TFLiteWrapper结构的指针

---

### API集成

#### `api_config_init`

初始化Google AI服务的API配置。

**函数签名：**
```c
int api_config_init(APIConfig* config, const char* api_key, const char* endpoint);
```

**参数：**
- `config`：指向APIConfig结构的指针
- `api_key`：您的Google AI API密钥
- `endpoint`：API端点URL

**返回值：**
- 成功返回`0`
- 失败返回非零值

---

#### `api_call_gemini`

使用提示调用Google Gemini API。

**函数签名：**
```c
int api_call_gemini(const APIConfig* config, const char* prompt, APIResponse* response);
```

**参数：**
- `config`：指向已初始化的APIConfig的指针
- `prompt`：Gemini的文本提示
- `response`：指向APIResponse结构的指针以接收响应

**返回值：**
- 成功返回`0`
- 失败返回非零值

---

#### `api_response_free`

释放为API响应分配的内存。

**函数签名：**
```c
void api_response_free(APIResponse* response);
```

**参数：**
- `response`：指向APIResponse结构的指针

---

### 模型导出工具

#### `model_export`

将模型导出到指定位置。

**函数签名：**
```c
int model_export(const ExportConfig* config);
```

**参数：**
- `config`：指向包含导出设置的ExportConfig结构的指针

**返回值：**
- 成功返回`0`
- 失败返回非零值

---

#### `model_pack_zip`

将模型打包到ZIP归档中。

**函数签名：**
```c
int model_pack_zip(const char* model_path, const char* zip_path);
```

**参数：**
- `model_path`：模型文件路径
- `zip_path`：输出ZIP文件的路径

**返回值：**
- 成功返回`0`
- 失败返回非零值

---

#### `model_validate`

验证模型文件。

**函数签名：**
```c
bool model_validate(const char* model_path);
```

**参数：**
- `model_path`：模型文件路径

**返回值：**
- 如果模型有效返回`true`
- 如果模型无效返回`false`

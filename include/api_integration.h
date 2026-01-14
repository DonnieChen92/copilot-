#ifndef API_INTEGRATION_H
#define API_INTEGRATION_H

#include <stddef.h>
#include <stdbool.h>

/**
 * @brief API配置结构 / API configuration structure
 * 
 * 用于配置Google AI和Apple平台的API集成
 * Used to configure API integration for Google AI and Apple platforms
 */
typedef struct {
    const char* api_key;          // API密钥 / API key
    const char* endpoint;         // API端点 / API endpoint
    int timeout_seconds;          // 超时时间（秒） / Timeout in seconds
    bool use_ssl;                 // 是否使用SSL / Whether to use SSL
} APIConfig;

/**
 * @brief API响应结构 / API response structure
 */
typedef struct {
    int status_code;              // HTTP状态码 / HTTP status code
    char* response_data;          // 响应数据 / Response data
    size_t response_size;         // 响应大小 / Response size
    char* error_message;          // 错误信息 / Error message
} APIResponse;

/**
 * @brief 初始化API配置 / Initialize API configuration
 * @param config 指向APIConfig结构的指针 / Pointer to APIConfig structure
 * @param api_key API密钥 / API key
 * @param endpoint API端点 / API endpoint
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int api_config_init(APIConfig* config, const char* api_key, const char* endpoint);

/**
 * @brief 发送推理请求到Google AI / Send inference request to Google AI
 * @param config API配置 / API configuration
 * @param model_data 模型数据 / Model data
 * @param data_size 数据大小 / Data size
 * @param response 响应结构 / Response structure
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int api_send_inference_request(const APIConfig* config, const void* model_data, 
                                size_t data_size, APIResponse* response);

/**
 * @brief 调用Gemini API / Call Gemini API
 * @param config API配置 / API configuration
 * @param prompt 提示文本 / Prompt text
 * @param response 响应结构 / Response structure
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int api_call_gemini(const APIConfig* config, const char* prompt, APIResponse* response);

/**
 * @brief 释放API响应 / Free API response
 * @param response 响应结构 / Response structure
 */
void api_response_free(APIResponse* response);

/**
 * @brief 验证API密钥 / Validate API key
 * @param api_key API密钥 / API key
 * @return true表示有效，false表示无效 / true for valid, false for invalid
 */
bool api_validate_key(const char* api_key);

#endif // API_INTEGRATION_H

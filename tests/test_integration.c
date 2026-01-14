#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "../include/api_integration.h"
#include "../include/model_export.h"

/**
 * @brief 测试API配置初始化 / Test API configuration initialization
 */
void test_api_config_init() {
    printf("Testing api_config_init / 测试api_config_init\n");
    
    APIConfig config;
    int result = api_config_init(&config, "test_api_key", "https://api.test.com");
    
    assert(result == 0);
    assert(config.api_key != NULL);
    assert(strcmp(config.api_key, "test_api_key") == 0);
    assert(config.endpoint != NULL);
    assert(strcmp(config.endpoint, "https://api.test.com") == 0);
    assert(config.timeout_seconds == 30);
    assert(config.use_ssl);
    
    printf("✓ test_api_config_init passed / 通过\n\n");
}

/**
 * @brief 测试API密钥验证 / Test API key validation
 */
void test_api_validate_key() {
    printf("Testing api_validate_key / 测试api_validate_key\n");
    
    // 有效的API密钥 / Valid API key
    assert(api_validate_key("12345678901234567890") == true);
    
    // 太短的API密钥 / Too short API key
    assert(api_validate_key("short") == false);
    
    // NULL API密钥 / NULL API key
    assert(api_validate_key(NULL) == false);
    
    printf("✓ test_api_validate_key passed / 通过\n\n");
}

/**
 * @brief 测试模型验证 / Test model validation
 */
void test_model_validate() {
    printf("Testing model_validate / 测试model_validate\n");
    
    // NULL路径应该失败 / NULL path should fail
    assert(model_validate(NULL) == false);
    
    // 不存在的文件应该失败 / Non-existent file should fail
    assert(model_validate("/nonexistent/model.tflite") == false);
    
    printf("✓ test_model_validate passed / 通过\n\n");
}

/**
 * @brief 测试API响应释放 / Test API response free
 */
void test_api_response_free() {
    printf("Testing api_response_free / 测试api_response_free\n");
    
    APIResponse response;
    response.status_code = 200;
    response.response_data = NULL;
    response.response_size = 0;
    response.error_message = NULL;
    
    // 应该不会崩溃 / Should not crash
    api_response_free(&response);
    
    // NULL响应应该不会崩溃 / NULL response should not crash
    api_response_free(NULL);
    
    printf("✓ test_api_response_free passed / 通过\n\n");
}

/**
 * @brief 主测试函数 / Main test function
 */
int main() {
    printf("=== Running Tests / 运行测试 ===\n\n");
    
    test_api_config_init();
    test_api_validate_key();
    test_model_validate();
    test_api_response_free();
    
    printf("=== All Tests Passed / 所有测试通过 ===\n");
    return 0;
}

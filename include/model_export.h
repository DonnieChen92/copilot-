#ifndef MODEL_EXPORT_H
#define MODEL_EXPORT_H

#include <stddef.h>
#include <stdbool.h>

/**
 * @brief 模型导出配置 / Model export configuration
 */
typedef struct {
    const char* source_path;      // 源模型路径 / Source model path
    const char* dest_path;        // 目标路径 / Destination path
    bool compress;                // 是否压缩 / Whether to compress
    bool include_metadata;        // 是否包含元数据 / Whether to include metadata
} ExportConfig;

/**
 * @brief 导出模型到指定路径 / Export model to specified path
 * @param config 导出配置 / Export configuration
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int model_export(const ExportConfig* config);

/**
 * @brief 将模型打包为ZIP文件 / Pack model as ZIP file
 * @param model_path 模型路径 / Model path
 * @param zip_path ZIP文件路径 / ZIP file path
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int model_pack_zip(const char* model_path, const char* zip_path);

/**
 * @brief 从ZIP文件解包模型 / Unpack model from ZIP file
 * @param zip_path ZIP文件路径 / ZIP file path
 * @param dest_path 目标路径 / Destination path
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int model_unpack_zip(const char* zip_path, const char* dest_path);

/**
 * @brief 验证模型文件 / Validate model file
 * @param model_path 模型路径 / Model path
 * @return true表示有效，false表示无效 / true for valid, false for invalid
 */
bool model_validate(const char* model_path);

/**
 * @brief 创建部署包 / Create deployment package
 * @param model_path 模型路径 / Model path
 * @param output_path 输出路径 / Output path
 * @param include_runtime 是否包含运行时 / Whether to include runtime
 * @return 0表示成功，非0表示失败 / 0 for success, non-zero for failure
 */
int model_create_deployment_package(const char* model_path, const char* output_path, 
                                     bool include_runtime);

#endif // MODEL_EXPORT_H

#!/usr/bin/env python3
"""
Model Conversion Utilities
模型转换工具

This script demonstrates how to convert AI models to various formats
for deployment on different platforms.

此脚本演示如何将 AI 模型转换为各种格式以在不同平台上部署。

Truth and Fact and Accuracy principles
真实、事实、准确性原则
"""

import os
import sys
from pathlib import Path

def print_bilingual(en_text: str, zh_text: str):
    """Print message in both English and Chinese"""
    print(f"{en_text}")
    print(f"{zh_text}")
    print()

def convert_to_tflite(model_path: str, output_path: str = None, 
                      optimize: bool = True) -> bool:
    """
    Convert TensorFlow model to TensorFlow Lite format
    将 TensorFlow 模型转换为 TensorFlow Lite 格式
    
    Args:
        model_path: Path to the TensorFlow model
        output_path: Output path for .tflite file
        optimize: Whether to apply optimizations
        
    Returns:
        True if successful, False otherwise
    """
    print_bilingual(
        "=== Converting to TensorFlow Lite ===",
        "=== 转换为 TensorFlow Lite ==="
    )
    
    try:
        import tensorflow as tf
        
        # Set default output path
        if output_path is None:
            output_path = model_path.replace('.h5', '.tflite')
        
        print(f"Input: {model_path}")
        print(f"输入：{model_path}")
        print(f"Output: {output_path}")
        print(f"输出：{output_path}\n")
        
        # Load the model
        print_bilingual("Loading model...", "加载模型...")
        model = tf.keras.models.load_model(model_path)
        
        # Create converter
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        
        # Apply optimizations if requested
        if optimize:
            print_bilingual(
                "Applying optimizations (quantization)...",
                "应用优化（量化）..."
            )
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_types = [tf.float16]
        
        # Convert
        print_bilingual("Converting model...", "转换模型...")
        tflite_model = converter.convert()
        
        # Save
        print_bilingual("Saving model...", "保存模型...")
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        # Print size comparison
        original_size = os.path.getsize(model_path) / (1024 * 1024)
        converted_size = os.path.getsize(output_path) / (1024 * 1024)
        
        print(f"Original size: {original_size:.2f} MB")
        print(f"原始大小：{original_size:.2f} MB")
        print(f"Converted size: {converted_size:.2f} MB")
        print(f"转换后大小：{converted_size:.2f} MB")
        print(f"Size reduction: {((1 - converted_size/original_size) * 100):.1f}%")
        print(f"大小减少：{((1 - converted_size/original_size) * 100):.1f}%\n")
        
        print_bilingual(
            "✓ Conversion successful!",
            "✓ 转换成功！"
        )
        return True
        
    except ImportError:
        print_bilingual(
            "Error: TensorFlow not installed. Install with: pip install tensorflow",
            "错误：未安装 TensorFlow。使用以下命令安装：pip install tensorflow"
        )
        return False
    except Exception as e:
        print(f"Error: {e}")
        print(f"错误：{e}")
        return False

def convert_to_onnx(model_path: str, output_path: str = None) -> bool:
    """
    Convert TensorFlow model to ONNX format
    将 TensorFlow 模型转换为 ONNX 格式
    
    Args:
        model_path: Path to the TensorFlow model
        output_path: Output path for .onnx file
        
    Returns:
        True if successful, False otherwise
    """
    print_bilingual(
        "=== Converting to ONNX ===",
        "=== 转换为 ONNX ==="
    )
    
    try:
        import tensorflow as tf
        import tf2onnx
        
        # Set default output path
        if output_path is None:
            output_path = model_path.replace('.h5', '.onnx')
        
        print(f"Input: {model_path}")
        print(f"输入：{model_path}")
        print(f"Output: {output_path}")
        print(f"输出：{output_path}\n")
        
        # Load the model
        print_bilingual("Loading model...", "加载模型...")
        model = tf.keras.models.load_model(model_path)
        
        # Define input signature
        # Note: Adjust shape based on your model
        spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)
        
        # Convert
        print_bilingual("Converting model...", "转换模型...")
        model_proto, _ = tf2onnx.convert.from_keras(
            model,
            input_signature=spec,
            opset=13,
            output_path=output_path
        )
        
        print_bilingual(
            "✓ Conversion successful!",
            "✓ 转换成功！"
        )
        return True
        
    except ImportError:
        print_bilingual(
            "Error: Required packages not installed. Install with: pip install tf2onnx onnx",
            "错误：未安装所需包。使用以下命令安装：pip install tf2onnx onnx"
        )
        return False
    except Exception as e:
        print(f"Error: {e}")
        print(f"错误：{e}")
        return False

def convert_to_coreml(model_path: str, output_path: str = None) -> bool:
    """
    Convert TensorFlow model to Core ML format
    将 TensorFlow 模型转换为 Core ML 格式
    
    Args:
        model_path: Path to the TensorFlow model
        output_path: Output path for .mlmodel file
        
    Returns:
        True if successful, False otherwise
    """
    print_bilingual(
        "=== Converting to Core ML ===",
        "=== 转换为 Core ML ==="
    )
    
    try:
        import coremltools as ct
        
        # Set default output path
        if output_path is None:
            output_path = model_path.replace('.h5', '.mlmodel')
        
        print(f"Input: {model_path}")
        print(f"输入：{model_path}")
        print(f"Output: {output_path}")
        print(f"输出：{output_path}\n")
        
        # Convert
        print_bilingual("Converting model...", "转换模型...")
        model = ct.convert(
            model_path,
            source='tensorflow'
        )
        
        # Save
        print_bilingual("Saving model...", "保存模型...")
        model.save(output_path)
        
        print_bilingual(
            "✓ Conversion successful!",
            "✓ 转换成功！"
        )
        return True
        
    except ImportError:
        print_bilingual(
            "Error: coremltools not installed. Install with: pip install coremltools",
            "错误：未安装 coremltools。使用以下命令安装：pip install coremltools"
        )
        return False
    except Exception as e:
        print(f"Error: {e}")
        print(f"错误：{e}")
        return False

def batch_convert(model_path: str, formats: list = None):
    """
    Convert model to multiple formats
    将模型转换为多种格式
    
    Args:
        model_path: Path to the source model
        formats: List of target formats ['tflite', 'onnx', 'coreml']
    """
    if formats is None:
        formats = ['tflite', 'onnx', 'coreml']
    
    print_bilingual(
        f"=== Batch Conversion: {model_path} ===",
        f"=== 批量转换：{model_path} ==="
    )
    
    results = {}
    
    for fmt in formats:
        if fmt == 'tflite':
            results['tflite'] = convert_to_tflite(model_path)
        elif fmt == 'onnx':
            results['onnx'] = convert_to_onnx(model_path)
        elif fmt == 'coreml':
            results['coreml'] = convert_to_coreml(model_path)
        else:
            print(f"Unknown format: {fmt}")
            print(f"未知格式：{fmt}")
    
    # Print summary
    print_bilingual(
        "\n=== Conversion Summary ===",
        "\n=== 转换摘要 ==="
    )
    
    for fmt, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {fmt.upper()}")
    
    print()

def main():
    """Main entry point"""
    print_bilingual(
        "=== Model Conversion Utilities ===",
        "=== 模型转换工具 ==="
    )
    
    if len(sys.argv) < 2:
        print("Usage: python model_conversion.py <model_path> [format]")
        print("使用方法：python model_conversion.py <模型路径> [格式]")
        print()
        print("Formats: tflite, onnx, coreml, all")
        print("格式：tflite、onnx、coreml、all")
        print()
        print("Example: python model_conversion.py my_model.h5 tflite")
        print("示例：python model_conversion.py my_model.h5 tflite")
        return 1
    
    model_path = sys.argv[1]
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found: {model_path}")
        print(f"错误：未找到模型文件：{model_path}")
        return 1
    
    # Determine format
    if len(sys.argv) >= 3:
        fmt = sys.argv[2].lower()
    else:
        fmt = 'tflite'  # Default format
    
    # Convert
    if fmt == 'all':
        batch_convert(model_path)
    elif fmt == 'tflite':
        convert_to_tflite(model_path)
    elif fmt == 'onnx':
        convert_to_onnx(model_path)
    elif fmt == 'coreml':
        convert_to_coreml(model_path)
    else:
        print(f"Unknown format: {fmt}")
        print(f"未知格式：{fmt}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

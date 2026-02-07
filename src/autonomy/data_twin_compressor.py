"""
Data Twin Compressor for AI Memory
資料雙胞胎壓縮器用於 AI 記憶 / 数据双胞胎压缩器用于 AI 记忆
===================================================================
Compresses conversation/driver data for Tesla integration
(e.g., driver profiles, habits, preferences stored as digital twins).

壓縮對話/駕駛者資料以供 Tesla 整合（例如作為數位雙胞胎儲存的駕駛者檔案、習慣、偏好）。
压缩对话/驾驶者数据以供 Tesla 整合（例如作为数字双胞胎储存的驾驶者档案、习惯、偏好）。

Mathematical Foundation / 數學基礎 / 数学基础:
- Shannon entropy: H(X) = -Σ p(xᵢ) × log₂(p(xᵢ))
  夏農熵：衡量資訊含量 / 香农熵：衡量信息含量
- Compression ratio: R = compressed_size / original_size × 100%
  壓縮比 / 压缩比
- zlib uses DEFLATE (LZ77 + Huffman coding)
  zlib 使用 DEFLATE（LZ77 + 霍夫曼編碼）

Integration / 整合:
- LLM conversation memory → compressed storage on edge device
  LLM 對話記憶 → 邊緣裝置上的壓縮儲存
- Driver habit profiles → compact twin representation
  駕駛者習慣檔案 → 緊湊的雙胞胎表示

Author: Donnie Chen (donniechen92@gmail.com)
"""

import json
import math
import zlib
from collections import Counter
from dataclasses import dataclass
from typing import Any


@dataclass
class CompressionResult:
    """Compression analysis result / 壓縮分析結果 / 压缩分析结果"""
    original_bytes: int            # Original size / 原始大小
    compressed_bytes: int          # Compressed size / 壓縮後大小
    ratio_percent: float           # Compression ratio % / 壓縮比 %
    savings_percent: float         # Space savings % / 節省空間 %
    entropy: float                 # Shannon entropy / 夏農熵
    theoretical_min_bytes: float   # Theoretical minimum / 理論最小值


def shannon_entropy(text: str) -> float:
    """
    Calculate Shannon entropy of text.
    計算文本的夏農熵。
    计算文本的香农熵。

    H(X) = -Σ p(xᵢ) × log₂(p(xᵢ))

    Higher entropy = more random = harder to compress.
    較高熵 = 更隨機 = 更難壓縮。
    较高熵 = 更随机 = 更难压缩。

    Args:
        text: Input text / 輸入文本

    Returns:
        Entropy in bits per character / 每字元的熵（位元）
    """
    if not text:
        return 0.0

    freq = Counter(text)
    length = len(text)
    entropy = 0.0

    for count in freq.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy


def compress_text(text: str, level: int = 6) -> CompressionResult:
    """
    Compress text data using zlib (DEFLATE algorithm).
    使用 zlib（DEFLATE 演算法）壓縮文本資料。
    使用 zlib（DEFLATE 算法）压缩文本数据。

    Args:
        text: Text to compress / 要壓縮的文本
        level: Compression level 1-9 (1=fastest, 9=best) / 壓縮等級

    Returns:
        CompressionResult with metrics / 包含指標的壓縮結果
    """
    original = text.encode("utf-8")
    compressed = zlib.compress(original, level)

    original_bytes = len(original)
    compressed_bytes = len(compressed)
    ratio = (compressed_bytes / original_bytes) * 100 if original_bytes > 0 else 0
    savings = 100 - ratio

    entropy = shannon_entropy(text)
    # Theoretical minimum: entropy bits per char × total chars / 8 bits per byte
    theoretical_min = (entropy * len(text)) / 8.0 if entropy > 0 else 0

    return CompressionResult(
        original_bytes=original_bytes,
        compressed_bytes=compressed_bytes,
        ratio_percent=round(ratio, 2),
        savings_percent=round(savings, 2),
        entropy=round(entropy, 4),
        theoretical_min_bytes=round(theoretical_min, 2),
    )


def compress_json(data: Any, level: int = 6) -> CompressionResult:
    """
    Compress JSON-serializable data.
    壓縮可 JSON 序列化的資料。
    压缩可 JSON 序列化的数据。
    """
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return compress_text(text, level)


def compress_driver_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """
    Compress a driver digital twin profile for edge storage.
    壓縮駕駛者數位雙胞胎檔案以供邊緣儲存。
    压缩驾驶者数字双胞胎档案以供边缘储存。

    Args:
        profile: Driver profile dict with habits, preferences, routes
                 駕駛者檔案字典，含習慣、偏好、路線

    Returns:
        Dict with compressed data and metrics / 含壓縮資料和指標的字典
    """
    result = compress_json(profile)
    compressed_data = zlib.compress(
        json.dumps(profile, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    )

    return {
        "compressed_data": compressed_data,
        "metrics": {
            "original_bytes": result.original_bytes,
            "compressed_bytes": result.compressed_bytes,
            "savings_percent": result.savings_percent,
            "entropy": result.entropy,
        },
    }


def decompress_driver_profile(compressed_data: bytes) -> dict[str, Any]:
    """
    Decompress a driver profile from edge storage.
    從邊緣儲存解壓縮駕駛者檔案。
    从边缘储存解压缩驾驶者档案。
    """
    decompressed = zlib.decompress(compressed_data)
    return json.loads(decompressed.decode("utf-8"))


def batch_compress_conversations(
    messages: list[dict[str, str]],
) -> dict[str, Any]:
    """
    Compress a batch of conversation messages for memory storage.
    批次壓縮對話訊息以供記憶儲存。
    批量压缩对话消息以供记忆储存。

    Args:
        messages: List of {"role": str, "content": str}

    Returns:
        Compression stats and compressed data
    """
    full_text = "\n".join(f"[{m['role']}] {m['content']}" for m in messages)
    result = compress_text(full_text)

    return {
        "message_count": len(messages),
        "original_bytes": result.original_bytes,
        "compressed_bytes": result.compressed_bytes,
        "savings_percent": result.savings_percent,
        "entropy": result.entropy,
        "bytes_per_message": round(result.compressed_bytes / len(messages), 2) if messages else 0,
    }


# --- Demo / 示範 / 示范 ---
if __name__ == "__main__":
    # 1. Simple text compression / 簡單文本壓縮
    print("=== Text Compression / 文本壓縮 ===")
    text = "Your AI conversation history here for compression. " * 10
    result = compress_text(text)
    print(f"Original / 原始: {result.original_bytes} bytes")
    print(f"Compressed / 壓縮: {result.compressed_bytes} bytes")
    print(f"Savings / 節省: {result.savings_percent}%")
    print(f"Entropy / 熵: {result.entropy} bits/char")

    # 2. Driver profile compression / 駕駛者檔案壓縮
    print("\n=== Driver Profile / 駕駛者檔案 ===")
    driver_profile = {
        "driver_id": "donnie-001",
        "preferences": {
            "seat_position": {"x": 15, "y": 10, "recline": 22},
            "mirror_angles": {"left": 12.5, "right": 13.0, "rear": 8.0},
            "climate": {"temp_c": 22, "fan_speed": 3},
            "music": {"genre": "jazz", "volume": 45},
        },
        "driving_habits": {
            "avg_speed_kmh": 75,
            "braking_intensity": 0.6,
            "following_distance_s": 2.5,
            "lane_change_frequency": "moderate",
        },
        "frequent_routes": [
            {"name": "Home to Office", "distance_km": 25, "avg_time_min": 35},
            {"name": "Office to Gym", "distance_km": 8, "avg_time_min": 15},
        ],
    }

    compressed = compress_driver_profile(driver_profile)
    print(f"Original / 原始: {compressed['metrics']['original_bytes']} bytes")
    print(f"Compressed / 壓縮: {compressed['metrics']['compressed_bytes']} bytes")
    print(f"Savings / 節省: {compressed['metrics']['savings_percent']}%")

    # Verify decompression / 驗證解壓縮
    restored = decompress_driver_profile(compressed["compressed_data"])
    assert restored == driver_profile
    print("Decompression verified / 解壓縮驗證成功 ✓")

    # 3. Conversation batch compression / 對話批次壓縮
    print("\n=== Conversation Compression / 對話壓縮 ===")
    messages = [
        {"role": "user", "content": "Navigate to downtown."},
        {"role": "assistant", "content": "Setting route to downtown. ETA 25 minutes."},
        {"role": "user", "content": "Avoid the highway."},
        {"role": "assistant", "content": "Rerouting via local roads. New ETA 35 minutes."},
    ]
    batch = batch_compress_conversations(messages)
    print(f"Messages / 訊息數: {batch['message_count']}")
    print(f"Compressed / 壓縮: {batch['compressed_bytes']} bytes")
    print(f"Per message / 每訊息: {batch['bytes_per_message']} bytes")

#!/usr/bin/env python3
"""
Data Twin Compressor for AI Memory

Evaluates zlib compression ratio on text data to estimate storage
savings for AI conversation history and memory layer data.
"""

import zlib


def compress_data(text):
    """Return compression ratio as percentage of original size."""
    original = text.encode("utf-8")
    compressed = zlib.compress(original)
    return len(compressed) / len(original) * 100


if __name__ == "__main__":
    chat_text = "Your AI conversation history here for compression."
    ratio = compress_data(chat_text)
    print(f"Compression ratio: {ratio:.2f}% of original size")

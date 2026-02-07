#!/usr/bin/env python3
"""
Hamming EDAC (Error Detection And Correction)

Demonstrates Hamming(7,4) encoding, single-bit error injection,
syndrome-based error detection, and correction using parity-check matrix.
"""

from sympy import Matrix

# Generator matrix G (4x7)
G = Matrix([
    [1, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 1, 1],
])

data = Matrix([1, 0, 1, 1])

# Encode
codeword = (data.T * G) % 2
print(f"Original data: {data.T}")
print(f"Encoded codeword: {codeword}")

# Inject single-bit error at position 3
codeword[0, 3] = 1 - codeword[0, 3]
print(f"After error injection: {codeword}")

# Parity-check matrix H (transposed for syndrome computation)
H = Matrix([
    [1, 1, 1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 1, 0, 0, 1],
]).T

syndrome = (H * codeword.T) % 2
error_pos = int("".join(map(str, syndrome)), 2)

if error_pos:
    print(f"Syndrome: {syndrome.T} -> error at position {error_pos}")
    codeword[0, error_pos - 1] = 1 - codeword[0, error_pos - 1]

print(f"Corrected codeword: {codeword}")
print(f"Recovered data: {codeword[0, :4]}")

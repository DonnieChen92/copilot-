#!/usr/bin/env python3
"""
TMR Voting (Triple Modular Redundancy)

Simulates single-event upset (SEU) error rates across three redundant
modules with majority voting. Demonstrates how TMR reduces effective
error rate from single-module probability.
"""

import numpy as np

num_trials = 10000
seu_prob = 0.001

module1 = np.random.binomial(1, seu_prob, num_trials)
module2 = np.random.binomial(1, seu_prob, num_trials)
module3 = np.random.binomial(1, seu_prob, num_trials)

votes = module1 + module2 + module3
corrected = (votes < 2).astype(int)

errors = np.sum(votes >= 2) / num_trials

print(f"Single error rate: {seu_prob:.4f}")
print(f"TMR error rate: {errors:.4f}")
if errors > 0:
    print(f"Improvement: {seu_prob / errors:.2f}x")
else:
    print("Improvement: no TMR errors observed")

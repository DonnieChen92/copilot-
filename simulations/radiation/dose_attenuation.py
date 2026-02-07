#!/usr/bin/env python3
"""
Dose Attenuation (Shielding Simulation)

Simulates GCR-like flux through aluminum shielding using exponential
attenuation. Compares unshielded vs shielded dose rates integrated
over 1-1000 MeV energy range.
"""

import numpy as np
from scipy.integrate import quad

energy_range = np.linspace(1, 1000, 1000)  # MeV
flux = 1e4 / energy_range  # GCR-like flux

thickness = 0.5  # cm Al
attenuation_coeff = 0.1  # cm^-1 for protons


def dose_rate(E):
    return flux[np.argmin(np.abs(energy_range - E))] * (1 / E)


unshielded_dose = quad(dose_rate, 1, 1000)[0]


def shielded_dose_rate(E):
    return dose_rate(E) * np.exp(-attenuation_coeff * thickness * 2.7)


shielded_dose = quad(shielded_dose_rate, 1, 1000)[0]

print(f"Unshielded dose: {unshielded_dose:.2f}")
print(f"Shielded dose: {shielded_dose:.2f}")
print(f"Reduction: {unshielded_dose / shielded_dose:.2f}")

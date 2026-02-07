#!/usr/bin/env python3
"""
Radiation Sim for Space-Linked Autonomy

Models radiation environment for space-linked autonomous systems.
Same GCR flux model as dose_attenuation but contextualised for
autonomous system hardening decisions.
"""

import numpy as np
from scipy.integrate import quad

energy_range = np.linspace(1, 1000, 1000)
flux = 1e4 / energy_range

thickness = 0.5
attenuation_coeff = 0.1


def dose_rate(E):
    return flux[np.argmin(np.abs(energy_range - E))] * (1 / E)


unshielded_dose = quad(dose_rate, 1, 1000)[0]


def shielded_dose_rate(E):
    return dose_rate(E) * np.exp(-attenuation_coeff * thickness * 2.7)


shielded_dose = quad(shielded_dose_rate, 1, 1000)[0]

print(f"Unshielded dose: {unshielded_dose:.2f}")
print(f"Shielded dose: {shielded_dose:.2f}")
print(f"Reduction: {unshielded_dose / shielded_dose:.2f}")

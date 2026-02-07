#!/usr/bin/env python3
"""
Trajectory Planner for Tesla FSD (Orbital Context)

Hohmann transfer computation reframed for autonomous trajectory planning.
Same physics as hohmann_transfer.py but oriented toward autonomous
flight-planning decision support.
"""

import numpy as np

mu = 3.986e14  # m^3/s^2
r1 = 6371e3 + 400e3  # LEO
r2 = 6371e3 + 2000e3  # Target

v1 = np.sqrt(mu / r1)
delta_v1 = np.sqrt(mu / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)

a_transfer = (r1 + r2) / 2
time_transfer = np.pi * np.sqrt(a_transfer**3 / mu)

delta_v2 = np.sqrt(mu / r2) - np.sqrt(mu * (2 / r2 - 1 / a_transfer))


def safe_altitude(r):
    alt = (r - 6371e3) / 1e3
    return 400 < alt < 1000 or alt > 6000


safe_r1 = safe_altitude(r1)
safe_r2 = safe_altitude(r2)

print(f"Delta V1: {delta_v1:.2f} m/s")
print(f"Transfer time: {time_transfer / 3600:.2f} hours")
print(f"Delta V2: {delta_v2:.2f} m/s")
print(f"Safe LEO: {safe_r1}, Safe target: {safe_r2}")

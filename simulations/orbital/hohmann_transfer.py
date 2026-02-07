#!/usr/bin/env python3
"""
Safe Rocket Trajectory Automation (Hohmann Transfer)

Computes delta-V requirements and transfer time for a Hohmann transfer
orbit from LEO (400 km) to a 2000 km target orbit. Includes safety
altitude checks for debris avoidance zones.
"""

import numpy as np

mu = 3.986e14  # m^3/s^2 (Earth gravitational parameter)
r1 = 6371e3 + 400e3  # LEO radius (m)
r2 = 6371e3 + 2000e3  # Target orbit radius (m)

# Circular velocity at LEO
v1 = np.sqrt(mu / r1)

# First burn: inject into transfer ellipse
delta_v1 = np.sqrt(mu / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)

# Transfer orbit parameters
a_transfer = (r1 + r2) / 2
v_transfer = np.sqrt(mu * (2 / r1 - 1 / a_transfer))
time_transfer = np.pi * np.sqrt(a_transfer**3 / mu)

# Second burn: circularize at target
delta_v2 = np.sqrt(mu / r2) - np.sqrt(mu * (2 / r2 - 1 / a_transfer))

total_delta_v = abs(delta_v1) + abs(delta_v2)


def safe_altitude(r):
    """Check if altitude avoids known debris concentration zones."""
    alt = (r - 6371e3) / 1e3  # km
    return 400 < alt < 1000 or alt > 6000


safe_r1 = safe_altitude(r1)
safe_r2 = safe_altitude(r2)

print(f"LEO velocity: {v1:.2f} m/s")
print(f"Delta V1 (injection): {delta_v1:.2f} m/s")
print(f"Transfer time: {time_transfer / 3600:.2f} hours")
print(f"Delta V2 (circularize): {delta_v2:.2f} m/s")
print(f"Total delta-V: {total_delta_v:.2f} m/s")
print(f"Safe LEO: {safe_r1}, Safe target: {safe_r2}")

#!/usr/bin/env python3
"""
Orbital Power & Throughput Simulation (Suncatcher-style)

Simulates power generation and inter-satellite link throughput for an
81-satellite constellation at 650 km altitude. Uses solar angle to
compute effective panel power and distance-dependent link loss.

Requires: astropy
"""

import numpy as np

try:
    from astropy.coordinates import get_sun, EarthLocation, AltAz
    from astropy.time import Time
    from astropy import units as u

    HAS_ASTROPY = True
except ImportError:
    HAS_ASTROPY = False

num_sats = 81
solar_flux = 1400  # W/m^2
efficiency = 0.3
panel_area = 10  # m^2

if HAS_ASTROPY:
    altitude = 650 * u.km
    t = Time.now()
    sun = get_sun(t)
    loc = EarthLocation(lat=0 * u.deg, lon=0 * u.deg, height=altitude)
    altaz = sun.transform_to(AltAz(obstime=t, location=loc))
    solar_angle = altaz.alt.deg
else:
    # Fallback: assume 45 degree solar angle
    solar_angle = 45.0
    print("(astropy not available, using fallback solar angle of 45 deg)")

power_per_sat = (
    solar_flux * efficiency * panel_area * np.cos(np.deg2rad(90 - solar_angle))
)
total_power = power_per_sat * num_sats

dist = np.random.uniform(100, 200, num_sats)  # km
loss_db = 0.1 * dist / 1000
throughput = 1.6e12 * 10 ** (-loss_db / 10)

print(f"Solar angle: {solar_angle:.1f} deg")
print(f"Power per sat: {power_per_sat:.2f} W")
print(f"Total power: {total_power:.2f} W")
print(f"Avg throughput: {np.mean(throughput):.2e} bps")

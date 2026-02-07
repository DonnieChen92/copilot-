#!/usr/bin/env python3
"""
GEANT4 Approximation

Monte Carlo approximation of particle transport through aluminum shielding.
Simulates energy deposition using random particle energies and incident angles,
with complementary error function for transmission probability.
"""

import numpy as np
from scipy.special import erfc

num_particles = 100000
energy_mean = 100  # MeV
energy_std = 20
thickness = 0.5  # cm
density_al = 2.7  # g/cm^3
attenuation_length = 10  # cm

energies = np.random.normal(energy_mean, energy_std, num_particles)

dE_dx = 1 / energies

theta = np.random.uniform(0, np.pi / 2, num_particles)
path_lengths = thickness / np.cos(theta)

transmitted = erfc(path_lengths / attenuation_length) / 2

deposited_energy = dE_dx * path_lengths * density_al * (1 - transmitted)

total_dose = np.sum(deposited_energy) / num_particles

print(f"Average deposited dose: {total_dose:.2f} arbitrary units")
print(f"Transmitted fraction: {np.mean(transmitted):.4f}")

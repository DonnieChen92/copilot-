#!/usr/bin/env python3
"""
Safety Checker for Autonomy (Distance-Based)

Validates that a planned path maintains minimum safe distance from
known hazard locations. Used as a post-planning safety gate for
autonomous navigation.
"""

import math


def is_safe_path(path, hazards, min_distance=2.0):
    """Check all path points are at least min_distance from all hazards."""
    for point in path:
        for hazard in hazards:
            dist = math.sqrt(
                (point[0] - hazard[0]) ** 2 + (point[1] - hazard[1]) ** 2
            )
            if dist < min_distance:
                return False
    return True


if __name__ == "__main__":
    path = [(0, 0), (1, 0), (2, 0), (3, 0)]
    hazards = [(1, 1), (2, 2)]
    safe = is_safe_path(path, hazards)
    print("Path safe?", safe)

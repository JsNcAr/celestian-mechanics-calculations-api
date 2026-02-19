"""
Math helper utilities for celestial mechanics calculations.

This module provides common mathematical operations used throughout the
calculation services (unit conversions, angle normalisation, etc.).
"""

import math


def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.radians(degrees)


def rad_to_deg(radians: float) -> float:
    """Convert radians to degrees."""
    return math.degrees(radians)


def normalize_angle_deg(degrees: float) -> float:
    """Normalise an angle in degrees to the range [0, 360)."""
    return degrees % 360.0


def normalize_angle_rad(radians: float) -> float:
    """Normalise an angle in radians to the range [0, 2π)."""
    return radians % (2 * math.pi)

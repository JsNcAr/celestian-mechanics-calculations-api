"""
Orbital mechanics calculation service.

Placeholder module for Keplerian orbit calculations:
- Orbital period (Kepler's third law)
- Orbital velocity (vis-viva equation)
- Orbital energy
- Eccentricity vector
- True anomaly from mean anomaly (Kepler's equation)

All physical constants use SI units unless otherwise noted.
"""

import math

# Gravitational constant [m³ kg⁻¹ s⁻²]
G: float = 6.674_30e-11

# Standard gravitational parameter for the Sun [m³ s⁻²]
GM_SUN: float = 1.327_124_400_41e20


def orbital_period(semi_major_axis: float, gm: float = GM_SUN) -> float:
    """
    Calculate the orbital period using Kepler's third law.

    Parameters
    ----------
    semi_major_axis : float
        Semi-major axis in metres.
    gm : float
        Standard gravitational parameter (μ = GM) in m³ s⁻².

    Returns
    -------
    float
        Orbital period in seconds.
    """
    return 2 * math.pi * math.sqrt(semi_major_axis**3 / gm)


def orbital_velocity(semi_major_axis: float, distance: float, gm: float = GM_SUN) -> float:
    """
    Calculate orbital speed at a given distance using the vis-viva equation.

    Parameters
    ----------
    semi_major_axis : float
        Semi-major axis in metres.
    distance : float
        Current distance from the central body in metres.
    gm : float
        Standard gravitational parameter (μ = GM) in m³ s⁻².

    Returns
    -------
    float
        Orbital speed in m s⁻¹.
    """
    return math.sqrt(gm * (2.0 / distance - 1.0 / semi_major_axis))

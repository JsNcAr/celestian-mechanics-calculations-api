"""
Coordinate Systems and Transformations
This module defines the data models for representing different coordinate systems (Rectangular and Spherical) and their associated metadata (Plane, Origin, PhysicalState).
It also includes the request model for the coordinate transformation endpoint, which specifies the input coordinates, target shape, plane, origin, physical state, and any translation vector for transformations between different origins.
"""

from enum import Enum, IntEnum
from typing import Tuple, Union
from pydantic import BaseModel, ConfigDict, ConfigDict
import numpy as np


class Plane(str, Enum):
    EQUATORIAL = "equatorial"
    ECLIPTIC = "ecliptic"


class Origin(str, Enum):
    HELIOCENTRIC = "heliocentric"
    GEOCENTRIC = "geocentric"


class Shape(str, Enum):
    RECTANGULAR = "rectangular"
    SPHERICAL = "spherical"

class Rectangular(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)
    x: float
    y: float
    z: float
    plane: Plane
    origin: Origin

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])


class Spherical(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)
    lon_or_ra: float  # Longitude or Right Ascension
    lat_or_dec: float  # Latitude or Declination
    distance: float
    plane: Plane
    origin: Origin


class PhysicalState(IntEnum):
    """
    The w-dimension in homogeneous coordinates acts as a physical state flag.
    w = 0: Vector (Immune to translation, represents direction/magnitude like Velocity).
    w = 1: Point (Affected by translation, represents absolute position in space).
    """
    VECTOR = 0
    POINT = 1

# ==========================================
# Request model for coordinate transformation endpoint
# ==========================================

class CoordinateTransformRequest(BaseModel):
    input_coords: Union[Rectangular, Spherical]
    target_shape: Shape
    target_plane: Plane
    target_origin: Origin
    physical_state: PhysicalState = PhysicalState.POINT
    translation_vector: Tuple[float, float, float] = (0.0, 0.0, 0.0)

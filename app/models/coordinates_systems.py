from enum import Enum
from pydantic import BaseModel
import numpy as np


class Plane(str, Enum):
    EQUATORIAL = "equatorial"
    ECLIPTIC = "ecliptic"


class Origin(str, Enum):
    HELIOCENTRIC = "heliocentric"
    GEOCENTRIC = "geocentric"


class Rectangular(BaseModel):
    x: float
    y: float
    z: float
    plane: Plane
    origin: Origin

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])


class Spherical(BaseModel):
    lon_or_ra: float  # Longitude or Right Ascension
    lat_or_dec: float  # Latitude or Declination
    distance: float
    plane: Plane
    origin: Origin

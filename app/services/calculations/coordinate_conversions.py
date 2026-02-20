"""
Coordinate conversion service.

Placeholder module for coordinate-system transformations used in
celestial mechanics:
- Cartesian ↔ Spherical (RA/Dec)
- Equatorial ↔ Ecliptic
- Geocentric ↔ Heliocentric
"""
import math
import numpy as np
from enum import IntEnum
from app.core.constants import EPSILON_RAD
from app.models.coordinates_systems import PhysicalState, Plane, Origin, Shape, Rectangular, Spherical
from typing import Union

# ==========================================
# INTERNAL MATH: NON-LINEAR (TRIGONOMETRY)
# ==========================================
def _spherical_to_rectangular(lon_or_ra: float, lat_or_dec: float, distance: float) -> dict:
    """
    Converts spherical coordinates (longitude/latitude or RA/Dec) to rectangular (x, y, z).
    
    Parameters:
    -----------
    lon_or_ra : float
        Longitude (for Ecliptic) or Right Ascension (for Equatorial) in degrees.
    lat_or_dec : float
        Latitude (for Ecliptic) or Declination (for Equatorial) in degrees.
    distance : float
        The radial distance from the origin to the point.
    """
    # Convert degrees to radians
    lon_rad = math.radians(lon_or_ra)
    lat_rad = math.radians(lat_or_dec)

    # Compute the rectangular coordinates
    x = distance * math.cos(lat_rad) * math.cos(lon_rad)
    y = distance * math.cos(lat_rad) * math.sin(lon_rad)
    z = distance * math.sin(lat_rad)

    return {
        "x": x,
        "y": y,
        "z": z
    }

def _rectangular_to_spherical(x: float, y: float, z: float) -> dict:
    """
    Converts rectangular coordinates (x, y, z) to spherical (longitude/latitude or RA/Dec).
    
    Parameters:
    -----------
    x, y, z : float
        The rectangular coordinates of the point.
        
    Returns:
    --------
    dict
        A dictionary containing 'lon_or_ra', 'lat_or_dec', and 'distance'.
    """
    # Equivalent to distance = sqrt(x^2 + y^2 + z^2), but more numerically stable for large values
    distance = math.hypot(x, y, z)
    
    if distance == 0:
        raise ValueError("Distance cannot be zero for spherical conversion.")
    
    # Calculate the ratio and clamp it to the [-1.0, 1.0] domain to prevent math domain errors
    z_ratio = z / distance
    clamped_z_ratio = max(-1.0, min(1.0, z_ratio))
    
    lat_rad = math.asin(clamped_z_ratio)
    lon_rad = math.atan2(y, x)

    # Convert radians back to degrees
    lon_or_ra = math.degrees(lon_rad)
    lat_or_dec = math.degrees(lat_rad)

    return {
        "lon_or_ra": lon_or_ra,
        "lat_or_dec": lat_or_dec,
        "distance": distance
    }


# ==========================================
# INTERNAL MATH: LINEAR (PROJECTIVE GEOMETRY)
# ==========================================
def _get_equatorial_ecliptic_rotation(to_ecliptic: bool = True) -> np.ndarray:
    """
    Creates the 4x4 homogeneous rotation matrix to tilt the fundamental plane.
    
    Parameters:
    -----------
    to_ecliptic : bool, default True
        If True, rotates from the Equatorial plane TO the Ecliptic plane (+epsilon).
        If False, rotates from the Ecliptic plane TO the Equatorial plane (-epsilon).

    Mathematical Details:
    ---------------------
    The transformation between Equatorial and Ecliptic coordinates is a pure rotation 
    around the X-axis (which points towards the Vernal Equinox and is shared by both frames).
    
    To reverse the rotation (Ecliptic to Equatorial), we use the negative angle (-epsilon).
    Because cos(-x) = cos(x) and sin(-x) = -sin(x), the signs on the sine terms naturally flip 
    when the math evaluates.
    """
    angle = EPSILON_RAD if to_ecliptic else -EPSILON_RAD

    cos_e = np.cos(angle)
    sin_e = np.sin(angle)

    return np.array([
        [1, 0,      0,     0],
        [0, cos_e,  sin_e, 0],
        [0, -sin_e, cos_e, 0],
        [0, 0,      0,     1]  # The w-dimension remains isolated
    ])


def _get_translation_matrix(tx: float, ty: float, tz: float) -> np.ndarray:
    """
    Creates a 4x4 homogeneous translation matrix.
    
    Parameters:
    -----------
    tx, ty, tz : float
        The translation components along the X, Y, and Z axes respectively.
        
    Physical Interpretation:
    ------------------------
    This shifts the observer's absolute origin. For example, to convert a Heliocentric
    position to a Geocentric position, you must move the origin from the Sun to the Earth.
    To do this, you translate by the NEGATIVE of the Earth's heliocentric position vector: 
    tx = -X_earth, ty = -Y_earth, tz = -Z_earth.
    
    Mathematically, this applies a 4D shear that slides Points (w=1) across the 3D plane,
    but completely ignores Vectors (w=0).
    """
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])
    
def _apply_transform(x: float, y: float, z: float,
                    transformation_matrix: np.ndarray,
                    state: PhysicalState = PhysicalState.POINT) -> dict:
    """
    Applies a 4x4 projective transformation matrix to a 3D physical entity.
    
    Parameters:
    -----------
    x, y, z : float
        The 3D rectangular coordinates of the entity.
    transformation_matrix : np.ndarray
        The 4x4 homogeneous matrix (usually a combined rotation dot translation matrix).
    state : PhysicalState, default PhysicalState.POINT
        Defines whether the entity is a POINT (w=1) or a VECTOR (w=0).
        
    Returns:
    --------
    dict
        The newly transformed 3D rectangular coordinates and its physical classification.
    """
    # 1. Project into 4D space by appending the physical state as the w-component
    entity_4d = np.array([x, y, z, state.value])

    # 2. Apply the linear algebra transformation (Rotation and/or Translation)
    transformed_4d = transformation_matrix.dot(entity_4d)

    # 3. Project back down to our 3D universe
    return {
        "x": transformed_4d[0],
        "y": transformed_4d[1],
        "z": transformed_4d[2],
        "type": "Point" if state == PhysicalState.POINT else "Vector"
    }
    
# ==========================================
# PUBLIC FACADE: The Universal Pipeline
# ==========================================


def convert_celestial_coordinate(
    # Input is now strictly typed to your Pydantic models
    input_coords: Union[Rectangular, Spherical],

    # Target State parameters
    target_shape: Shape,
    target_plane: Plane,
    target_origin: Origin,

    # Dynamic Physics Parameters
    physical_state: PhysicalState = PhysicalState.POINT,
    translation_vector: tuple = (0.0, 0.0, 0.0)
) -> Union[Rectangular, Spherical]:
    """
    Universal pipeline to transform any celestial Pydantic coordinate model into any other state.
    """

    # --- STAGE 1: NORMALIZE TO RECTANGULAR ---
    if isinstance(input_coords, Spherical):
        rect_dict = _spherical_to_rectangular(
            input_coords.lon_or_ra,
            input_coords.lat_or_dec,
            input_coords.distance
        )
    else:
        # It is already Rectangular, just extract the dictionary for the matrix math
        rect_dict = {"x": input_coords.x,
                     "y": input_coords.y, "z": input_coords.z}

    # --- STAGE 2: BUILD AND APPLY THE MASTER MATRIX ---
    master_matrix = np.eye(4)

    # The input inherently knows its own plane and origin
    if input_coords.plane != target_plane:
        to_ecliptic = (target_plane == Plane.ECLIPTIC)
        rotation = _get_equatorial_ecliptic_rotation(to_ecliptic)
        master_matrix = master_matrix.dot(rotation)

    if input_coords.origin != target_origin:
        translation = _get_translation_matrix(*translation_vector)
        master_matrix = master_matrix.dot(translation)

    if not np.array_equal(master_matrix, np.eye(4)):
        rect_dict = _apply_transform(
            rect_dict['x'], rect_dict['y'], rect_dict['z'],
            master_matrix, physical_state
        )

    # --- STAGE 3: FORMAT TO TARGET SHAPE ---
    if target_shape == Shape.SPHERICAL:
        spherical_dict = _rectangular_to_spherical(
            rect_dict['x'], rect_dict['y'], rect_dict['z']
        )
        return Spherical(
            lon_or_ra=spherical_dict['lon_or_ra'],
            lat_or_dec=spherical_dict['lat_or_dec'],
            distance=spherical_dict['distance'],
            plane=target_plane,
            origin=target_origin
        )

    return Rectangular(
        x=rect_dict['x'],
        y=rect_dict['y'],
        z=rect_dict['z'],
        plane=target_plane,
        origin=target_origin
    )

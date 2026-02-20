"""
Coordinates API Router
This module defines the `/coordinates/transform` endpoint for transforming celestial coordinates between different shapes, planes, and origins.
It serves as a universal pipeline that ingests an initial coordinate state (either Rectangular or Spherical) and safely converts it to the requested target state using a 4D homogeneous matrix engine to
handle rotations and translations.
"""
from fastapi import APIRouter, status
from typing import Union

from app.models.coordinates_systems import CoordinateTransformRequest, Rectangular, Spherical
from app.services.calculations.coordinate_conversions import convert_celestial_coordinate

router = APIRouter(prefix="/coordinates", tags=["Coordinates"])


@router.post("/transformations",
             response_model=Union[Rectangular, Spherical],
             status_code=status.HTTP_200_OK)
def create_coordinate_transformation(request: CoordinateTransformRequest):
    """
    Transforms a celestial coordinate between different shapes, planes, and origins.
    
    This endpoint acts as a universal pipeline. It ingests an initial coordinate state 
    (either Rectangular or Spherical) and safely converts it to the requested target 
    state using a 4D homogeneous matrix engine to handle rotations and translations.

    Args:
        request (CoordinateTransformRequest): The JSON payload containing:
            - input_coords: The starting coordinates (inherently defines starting shape, plane, and origin).
            - target_shape: The desired output geometry (Rectangular or Spherical).
            - target_plane: The desired output reference plane (e.g., Ecliptic or Equatorial).
            - target_origin: The desired output origin (e.g., Heliocentric or Geocentric).
            - physical_state: (Optional) 1 for Points (absolute position), 0 for Vectors (velocity/force). Defaults to 1.
            - translation_vector: (Optional) The (x,y,z) shift required if changing origins. Defaults to (0,0,0).

    Returns:
        Union[Rectangular, Spherical]: The fully transformed coordinates strictly mapped 
        to the requested target Pydantic model.
    """
    transformed_coords = convert_celestial_coordinate(
        input_coords=request.input_coords,
        target_shape=request.target_shape,
        target_plane=request.target_plane,
        target_origin=request.target_origin,
        physical_state=request.physical_state,
        translation_vector=request.translation_vector
    )
    return transformed_coords

"""
Shared Pydantic response schemas.

These models are used as ``response_model`` annotations on FastAPI route
handlers to ensure consistent, validated JSON serialisation for all API
responses.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for the ``GET /api/v1/health`` endpoint.

    Attributes
    ----------
    status : str
        Current health status of the API.  Always ``"ok"`` when the service
        is running normally.
    version : str
        Semantic version string of the deployed application.
    """

    status: str
    version: str


class RootResponse(BaseModel):
    """Response schema for the ``GET /`` root endpoint.

    Attributes
    ----------
    message : str
        A short welcome message that includes the application name.
    docs : str
        Relative URL path to the interactive Swagger UI documentation.
    version : str
        Semantic version string of the deployed application.
    """

    message: str
    docs: str
    version: str


class ErrorResponse(BaseModel):
    """Generic error response schema.

    Returned by FastAPI exception handlers when a request cannot be
    fulfilled.

    Attributes
    ----------
    detail : str
        Human-readable description of the error.
    """

    detail: str

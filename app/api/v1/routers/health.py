"""Health router (migrated from `endpoints`).

Defines the `/health` endpoint and registers it on an `APIRouter`.
"""

from fastapi import APIRouter

from app.core.config import get_settings
from app.models.responses import HealthResponse

router = APIRouter(tags=["health"])

settings = get_settings()


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health() -> HealthResponse:
    """Return the current health status of the API."""
    return HealthResponse(status="ok", version=settings.app_version)

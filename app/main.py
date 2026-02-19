"""
Application factory for the Celestial Mechanics Calculations API.

This module creates and configures the FastAPI application instance, registers
middleware (CORS), mounts the versioned API routers, and exposes a root
endpoint that returns a welcome message with links to the interactive docs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as v1_router
from app.core.config import get_settings
from app.models.responses import RootResponse

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Backend API providing common celestial mechanics calculations "
        "for use by TypeScript frontends."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=settings.api_v1_prefix)


@app.get("/", response_model=RootResponse, tags=["root"], summary="API root")
async def root() -> RootResponse:
    """Return a welcome message and links to the interactive documentation."""
    return RootResponse(
        message=f"Welcome to the {settings.app_name}",
        docs="/docs",
        version=settings.app_version,
    )

"""Aggregate router for API version 1.

All v1 routers are imported here and included under the ``/api/v1`` prefix
that is applied in ``app.main``.
"""

from fastapi import APIRouter

# Import routers from the `routers` package
from app.api.v1.routers import health

router = APIRouter()

# include per-domain routers here (prefixes/tags are set on each router file)
router.include_router(health.router)

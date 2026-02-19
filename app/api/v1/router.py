"""
Aggregate router for API version 1.

All v1 endpoint routers are imported here and included under the ``/api/v1``
prefix that is applied in ``app.main``.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

router = APIRouter()

router.include_router(health.router)

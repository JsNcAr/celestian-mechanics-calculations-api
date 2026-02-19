"""
Celestial Mechanics Calculations API.

Top-level package for the FastAPI application.  The application instance is
created in :mod:`app.main` and sub-packages are organised as follows:

- :mod:`app.api`      – versioned HTTP route definitions
- :mod:`app.core`     – application configuration and settings
- :mod:`app.models`   – Pydantic request/response schemas
- :mod:`app.services` – domain calculation logic
- :mod:`app.utils`    – shared utility helpers
"""

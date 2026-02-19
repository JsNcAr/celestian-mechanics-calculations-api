"""
Application settings and configuration management.

Settings are loaded from environment variables and/or a ``.env`` file via
*pydantic-settings*.  The :func:`get_settings` factory is cached with
:func:`functools.lru_cache` so that the same :class:`Settings` instance is
reused across the application lifetime.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised application settings.

    All fields can be overridden by environment variables of the same name
    (case-insensitive) or via a ``.env`` file in the project root.

    Attributes
    ----------
    app_name : str
        Human-readable name of the API, used in the OpenAPI title.
    app_version : str
        Semantic version string returned by the ``/api/v1/health`` endpoint.
    debug : bool
        When ``True``, the Uvicorn server starts with ``--reload``.
    host : str
        Bind address for the development server (see ``run.py``).
    port : int
        Bind port for the development server.
    cors_origins : list[str]
        Comma-separated list of origins allowed by the CORS middleware.
    api_v1_prefix : str
        URL prefix for all v1 routes, e.g. ``/api/v1``.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    app_name: str = "Celestial Mechanics Calculations API"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS – comma-separated list of allowed origins
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # API
    api_v1_prefix: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    """Return the cached application :class:`Settings` instance.

    The settings object is constructed once on the first call and then reused
    for every subsequent call thanks to :func:`functools.lru_cache`.

    Returns
    -------
    Settings
        The singleton settings instance populated from environment variables
        and/or the ``.env`` file.
    """
    return Settings()

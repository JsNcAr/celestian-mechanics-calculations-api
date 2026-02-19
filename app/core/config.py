"""
Application settings and configuration management.

Settings are loaded from environment variables and/or a ``.env`` file via
*pydantic-settings*.  The :func:`get_settings` factory is cached with
:func:`functools.lru_cache` so that the same :class:`Settings` instance is
reused across the application lifetime.
"""

from functools import lru_cache
import json

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from a `.env` file in the project root. We call
# this once at module import so every caller (tests, app startup, CLI) sees a
# consistent environment without having to call `load_dotenv()` repeatedly.
# Existing environment variables are not overridden by `load_dotenv()`.
load_dotenv()


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

    # CORS – list of allowed origins. When provided via environment variables
    # the value may be either a JSON array (recommended) or a comma-separated
    # string. A small validator below normalises both to `list[str]`.
    # Allow either `list[str]` or a raw `str` (CSV / JSON) as the env input so
    # environment values won't break pydantic's parsing pipeline. The
    # validator below will normalise the result to `list[str]`.
    cors_origins: list[str] | str = ["http://localhost:3000", "http://localhost:5173"]

    # API
    api_v1_prefix: str = "/api/v1"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v):
        """Normalise environment input into a `list[str]`.

        Accepted inputs:
        - a Python list (returned unchanged)
        - a JSON array string: '["a","b"]'
        - a comma-separated string: 'a, b'
        - an empty string -> []
        """
        # Already a list -> assume correctly typed
        if isinstance(v, list):
            return [str(x) for x in v]

        # Strings: try JSON array first, otherwise split on commas
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            if s.startswith("[") and s.endswith("]"):
                try:
                    parsed = json.loads(s)
                    return parsed if isinstance(parsed, list) else [str(parsed)]
                except Exception:
                    pass
            return [item.strip() for item in s.split(",") if item.strip()]

        # Fallback - let pydantic handle or raise
        return v


@lru_cache
def get_settings() -> Settings:
    """Return the cached application :class:`Settings` instance.

    The `.env` file (if present) is loaded once at module import via
    `python-dotenv.load_dotenv()` so callers do not need to call it
    explicitly. pydantic-settings will still read environment variables and
    the configured `env_file` if present.

    Returns
    -------
    Settings
        The singleton settings instance populated from environment variables
        and/or the ``.env`` file.
    """
    return Settings()

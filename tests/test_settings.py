import os

import pytest

from app.core import config


def teardown_function():
    # Ensure cached settings don't leak between tests
    try:
        config.get_settings.cache_clear()
    except Exception:
        pass


def test_defaults_match_env_example(monkeypatch):
    # Ensure environment doesn't leak into the test (some CI/dev shells set
    # HOST/PORT globally which would make this test flaky).
    for k in ("APP_NAME", "APP_VERSION", "DEBUG", "HOST", "PORT", "CORS_ORIGINS", "API_V1_PREFIX"):
        monkeypatch.delenv(k, raising=False)

    config.get_settings.cache_clear()
    s = config.get_settings()

    assert s.app_name == "Celestial Mechanics Calculations API"
    assert s.app_version == "0.1.0"
    assert s.debug is False
    assert s.host == "0.0.0.0"
    assert s.port == 8000
    assert isinstance(s.cors_origins, list)
    assert s.api_v1_prefix == "/api/v1"


def test_env_overrides_and_cors_json(monkeypatch):
    monkeypatch.setenv("APP_NAME", "foo-app")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", "1234")
    monkeypatch.setenv("CORS_ORIGINS", '["https://a","https://b"]')
    monkeypatch.setenv("API_V1_PREFIX", "/api/v9")

    config.get_settings.cache_clear()
    s = config.get_settings()

    assert s.app_name == "foo-app"
    assert s.app_version == "9.9.9"
    assert s.debug is True
    assert s.host == "127.0.0.1"
    assert s.port == 1234
    assert s.cors_origins == ["https://a", "https://b"]
    assert s.api_v1_prefix == "/api/v9"


def test_env_overrides_and_cors_csv(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://x.example, https://y.example")

    config.get_settings.cache_clear()
    s = config.get_settings()

    assert s.cors_origins == ["https://x.example", "https://y.example"]

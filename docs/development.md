# Development Guide

This guide describes how to contribute to the project, run tests, and add new features.

## Workflow

1.  Create a new branch for your feature or fix.
2.  Implement your changes.
3.  Add tests for new functionality.
4.  Run the test suite to ensure no regressions.

## Testing

The project uses `pytest` for testing.

### Running Tests
To run all tests (recommended via Poetry):
```bash
poetry run pytest
```

To run with coverage report:
```bash
poetry run pytest --cov=app
```

### Writing Tests
-   **Unit Tests**: Place in `tests/` mirroring the app structure.
-   **API Tests**: Use `TestClient` (from `starlette.testclient`) or `httpx` (async) in `tests/api/` to test endpoints. A `client` fixture is likely available in `tests/conftest.py`.

## Adding a New Endpoint

To add a new calculation features (e.g., Orbital Velocity):

1.  **Implement Logic**: Add the calculation function in `app/services/calculations/orbital_mechanics.py`.
    ```python
    def orbital_velocity(...): ...
    ```

2.  **Define Models**: Add Request/Response Pydantic models in `app/models/` if needed.

3.  **Create Router**: Create a new file `app/api/v1/routers/orbital.py`.
    ```python
    from fastapi import APIRouter
    from app.services.calculations import orbital_mechanics

    router = APIRouter()

    @router.get("/velocity")
    def get_velocity(...):
        return orbital_mechanics.orbital_velocity(...)
    ```

4.  **Register Router**: Import and include the new router in `app/api/v1/routes.py`.
    ```python
    from app.api.v1.routers import orbital
    # ...
    router.include_router(orbital.router, prefix="/orbital", tags=["orbital"])
    ```

### Migrating existing `endpoints/` modules

If you have existing endpoint modules under `app/api/v1/endpoints/`:

- Move the module file to `app/api/v1/routers/` (e.g. `health.py`).
- Update imports in `app/api/v1/router.py` to import from `app.api.v1.routers`.
- Optionally keep a small compatibility shim in `app/api/v1/endpoints/__init__.py` that re-exports the router while you update other imports.

This repository already contains that compatibility shim so the migration is backwards-compatible.

## Code Style

-   Follow PEP 8 guidelines.
-   Use type hints for all function arguments and return values.
-   Document functions and classes using docstrings.

## Dependencies

-   **Adding a dependency (Poetry)**: `poetry add <package>`
-   **Adding a dev dependency (Poetry)**: `poetry add --dev <package>`
-   **Export for non-Poetry consumers / CI**: `poetry export -f requirements.txt --output requirements.txt --dev --without-hashes`

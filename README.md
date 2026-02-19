# Celestial Mechanics Calculations API

A modern **FastAPI** backend providing common celestial mechanics calculations,
designed for consumption by TypeScript frontends.

---

## Project structure

```
.
├── app/
│   ├── main.py                        # FastAPI application factory
│   ├── core/
│   │   └── config.py                  # Settings (pydantic-settings / .env)
│   ├── api/
│   │   └── v1/
│   │       ├── routes.py              # Aggregate v1 router
│   │       └── routers/
│   │           └── health.py          # GET /api/v1/health
│   ├── models:
│   │   └── responses.py               # Shared Pydantic response schemas
│   ├── services/
│   │   └── calculations/
│   │       ├── orbital_mechanics.py   # Keplerian orbit helpers
│   │       └── coordinate_conversions.py  # Coordinate transforms (stub)
│   └── utils/
│       └── math_helpers.py            # Angle / unit-conversion utilities
├── tests/
│   ├── conftest.py                    # Shared pytest fixtures (async client)
│   ├── test_math_helpers.py
│   └── api/v1/
│       └── test_health.py
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── run.py                             # Development entry-point
```

## Quick start

```bash
# Recommended: use Poetry (preferred)
# 1. Install Poetry (if not installed)
#    Official installer: https://python-poetry.org/docs/#installation
curl -sSL https://install.python-poetry.org | python3 -

# 2. Install project dependencies and create the virtual environment
poetry install

# 3. (optional) spawn a shell that uses the Poetry venv
poetry shell
# or run commands with `poetry run` without entering a shell

# 4. Copy and edit environment variables
cp .env.example .env

# 5. Run the development server
poetry run python run.py
# or
poetry run uvicorn app.main:app --reload
```

**Fallback (pip + venv)**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

The API will be available at <http://localhost:8000>.  
Interactive docs: <http://localhost:8000/docs>

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root – welcome message & docs link |
| GET | `/api/v1/health` | Health check |

## Running tests

```bash
# using Poetry (recommended)
poetry run pytest
# or without Poetry
pytest
```

## Linting

```bash
ruff check .
```

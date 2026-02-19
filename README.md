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
│   │       ├── router.py              # Aggregate v1 router
│   │       └── endpoints/
│   │           └── health.py          # GET /api/v1/health
│   ├── models/
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
# 1. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt   # dev / test dependencies

# 2. (Optional) copy and edit environment variables
cp .env.example .env

# 3. Run the development server
python run.py
# or
uvicorn app.main:app --reload
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
pytest
```

## Linting

```bash
ruff check .
```

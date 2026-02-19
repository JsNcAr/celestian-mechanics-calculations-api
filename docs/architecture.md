# Architecture Overview

The project follows a modular, layered architecture typical of scalable FastAPI applications. This ensures code is organized, testable, and easy to maintain.

## Folder Structure

```
app/
├── api/                # API Routing Layer
│   └── v1/             # Version 1 Endpoints
│       ├── endpoints/  # Individual route handlers
│       └── router.py   # Aggregates all v1 endpoints
├── core/               # Application Configuration
│   └── config.py       # Pydantic Settings & Environment variables
├── models/             # Data Models
│   └── responses.py    # Pydantic schemas for API responses
├── services/           # Business Logic Layer
│   └── calculations/   # Core domain logic (Orbital mechanics, etc.)
├── utils/              # Shared Utilities
│   └── math_helpers.py # Helper functions (unit conversion, normalization)
└── main.py             # Application Entry Point
```

## Key Components

### 1. API Layer (`app/api`)
Handles HTTP requests and responses. Minimal logic should exist here.
-   **Routers**: Define paths and HTTP methods (`GET`, `POST`).
-   **Dependency Injection**: Uses FastAPI's `Depends` to inject services or settings.
-   **Serialization**: Uses Pydantic models from `app/models` to validate inputs and outputs.

### 2. Business Logic / Services (`app/services`)
Contains the core domain logic, independent of the HTTP framework.
-   **Calculations**: Modules like `orbital_mechanics.py` reside here.
-   **Pure Functions**: Where possible, logic is implemented as pure functions for easier testing.

### 3. Models (`app/models`)
Defines the data structures used throughout the application.
-   **Pydantic Models**: Used for request validation and response schemas.

### 4. Utilities (`app/utils`)
General-purpose helper functions that can be reused across services.

## Data Flow

1.  **Request**: Enters via `app/main.py`.
2.  **Routing**: Dispatched to the appropriate handler in `app/api/v1/endpoints/`.
3.  **Validation**: FastAPI validates request data against Pydantic models.
4.  **Service Call**: The endpoint calls a function in `app/services/`.
5.  **Response**: The result is wrapped in a Pydantic response model and returned as JSON.

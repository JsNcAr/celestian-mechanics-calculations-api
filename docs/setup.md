# Setup and Installation

This guide covers how to set up the development environment, configure the application, and run the server.

## Prerequisites

- **Python 3.11+**: Ensure you have a compatible Python version installed.
- **Poetry (recommended)**: Dependency and virtualenv manager. See https://python-poetry.org/docs/#installation for installation instructions.
- **pip**: Still supported as a fallback if you prefer `venv` + `requirements.txt`.

## Installation Steps

### Using Poetry (recommended)

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd celestian-mechanics-calculations-api
    ```

2.  **Install dependencies & create venv**:
    ```bash
    poetry install --extras dev
    # activate an interactive shell (optional)
    poetry shell
    # run commands without activating a shell
    poetry run <command>
    ```

3.  **Copy environment file**:
    ```bash
    cp .env.example .env
    ```

### Alternative: pip + venv (fallback)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Exporting requirements (for Docker / CI)

If you need a `requirements.txt` for non-Poetry environments or Dockerfiles:

```bash
poetry export -f requirements.txt --output requirements.txt --dev --without-hashes
```

## Configuration

The application uses **pydantic-settings** to manage configuration. Settings can be defined in environment variables or a `.env` file in the project root.

### Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `APP_NAME` | Name of the API (used in docs) | "Celestial Mechanics Calculations API" |
| `APP_VERSION` | Semantic version string | "0.1.0" |
| `DEBUG` | Enable debug mode (auto-reload) | `False` |
| `HOST` | Bind address for the server | "0.0.0.0" |
| `PORT` | Bind port for the server | `8000` |
| `CORS_ORIGINS` | Comma-separated list _or_ JSON array of allowed origins | (Check `app/core/config.py`) |
| `API_V1_PREFIX` | Prefix for V1 API routes | (Check `app/core/config.py`) |

To customize these values locally, create a `.env` file:
```ini
DEBUG=True
PORT=8080
CORS_ORIGINS=["http://localhost:3000"]
```

The application reads environment variables from a `.env` file (using
`python-dotenv`) and `pydantic-settings` will also consult `.env` when
building `Settings`. Place development overrides in a `.env` file — the
project includes `.env.example` as a template that you can copy to
`.env` locally.

## Running the Server

### Development Mode

You can use the provided `run.py` entry point, which configures `uvicorn` with settings from your environment:

```bash
python run.py
```

Or run `uvicorn` directly:

```bash
uvicorn app.main:app --reload
```

The server needs to be running for the interactive documentation to be accessible. By default it runs at `http://localhost:8000`.

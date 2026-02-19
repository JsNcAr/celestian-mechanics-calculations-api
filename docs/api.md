# API Reference

The Celestial Mechanics Calculations API exposes a RESTful interface for performing calculations.

## Interactive Documentation

FastAPI provides automatic interactive documentation. Once the server is running, you can access:

-   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
    Allows you to explore endpoints, see request/response schemas, and test the API directly from the browser.
-   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)  
    An alternative, clean documentation view.

## Base URL

By default, the API is served at `http://localhost:8000`.

## Versioning

All API endpoints are versioned. The current version is **v1**, accessible under the `/api/v1` prefix.

## Endpoints

### Root

-   `GET /`
    -   **Summary**: Welcome message.
    -   **Returns**: `RootResponse` containing the app name, version, and link to docs.

### Health Check

-   `GET /api/v1/health`
    -   **Summary**: Check API status.
    -   **Returns**: `HealthResponse` `{ "status": "ok", "version": "..." }`.
    -   **Use Case**: Load balancers and monitoring tools use this to verify the service is up.

### Future Endpoints

As the project expands, calculations for orbital mechanics and coordinate conversions will be exposed here. Check the Swagger UI for the most up-to-date list of available endpoints.

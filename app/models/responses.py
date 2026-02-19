from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str


class RootResponse(BaseModel):
    message: str
    docs: str
    version: str


class ErrorResponse(BaseModel):
    detail: str

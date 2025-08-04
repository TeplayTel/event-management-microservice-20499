"""
FastAPI custom exception handlers for Event Engagement API.
Handles EventServiceException, EventNotFoundException, InvalidEventPayloadException, and generic errors,
mapping to standardized JSON error schema responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from event_engagement_backend.src.exceptions.errors import (
    EventServiceException,
    EventNotFoundException,
    InvalidEventPayloadException,
)
from pydantic import BaseModel, Field
import logging

# Standard error response model
# PUBLIC_INTERFACE
class ErrorResponse(BaseModel):
    """Standard error response schema."""
    error_code: str = Field(..., description="Short, unique code for error type.")
    message: str = Field(..., description="Human-readable error message.")
    detail: str | None = Field(None, description="Optional internal detail for debugging.")

def add_exception_handlers(app):
    """Register all event-related exception handlers on the FastAPI app."""

    # Event domain error
    @app.exception_handler(EventServiceException)
    async def handle_service_exception(request: Request, exc: EventServiceException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error_code="service_error",
                message=str(exc),
                detail=None
            ).model_dump()
        )

    # Not found
    @app.exception_handler(EventNotFoundException)
    async def handle_not_found(request: Request, exc: EventNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                error_code="not_found",
                message=str(exc),
                detail=None
            ).model_dump()
        )

    # Validation error
    @app.exception_handler(InvalidEventPayloadException)
    async def handle_invalid_payload(request: Request, exc: InvalidEventPayloadException):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error_code="invalid_payload",
                message=str(exc),
                detail=None
            ).model_dump()
        )

    # Generic error/fallback
    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        logging.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error_code="internal_error",
                message="An unexpected error occurred.",
                detail=str(exc)
            ).model_dump()
        )

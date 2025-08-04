"""
Request/response logging middleware for FastAPI.
Logs HTTP method, path, status code, and processing duration.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from event_engagement_backend.src.logging.logger import get_logger

# Use the centralized logging configuration from logger.py
logger = get_logger("event_engagement_backend.api")

# PUBLIC_INTERFACE
class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs request and response events and timing stats."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} time={duration_ms:.1f}ms"
        )
        return response

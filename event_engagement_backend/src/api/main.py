from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from event_engagement_backend.src.api.routes.event_routes import router as event_router
from event_engagement_backend.src.logging.middleware import LoggingMiddleware
from event_engagement_backend.src.exceptions.error_handlers import add_exception_handlers

app = FastAPI(
    title="Fan Engagement Event Management API",
    description="API for event creation, configuration, and event metadata management with standardized error responses and authentication.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# Add all error/exception handlers
add_exception_handlers(app)

# Register API event router
app.include_router(event_router)

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

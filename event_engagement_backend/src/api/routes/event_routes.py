"""
Event-related FastAPI routes and request/response models.

Defines API endpoints and request/response Pydantic schemas for:
- Creating events
- Configuring event data sources
- Querying event details

Models provide strict validation and OpenAPI docstrings for endpoints.
"""

from fastapi import APIRouter, status

from event_engagement_backend.src.validation.models import (
    EventModel, DataSourceModel, TimelineModel
)
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/fan-engagement/events/v1",
    tags=["Events"]
)


# PUBLIC_INTERFACE
class ConfigureEventRequest(BaseModel):
    """
    Request schema for configuring a fan engagement event.
    """
    event: EventModel = Field(..., description="Fan engagement event details.")


# PUBLIC_INTERFACE
class ConfigureEventResponse(BaseModel):
    """
    Response model for an event configuration request.
    """
    success: bool = Field(..., description="Result of configure operation.")
    message: str = Field(..., description="Status/message text.")
    event_id: str = Field(..., description="Configured event ID.")


# PUBLIC_INTERFACE
@router.post(
    "/configure",
    response_model=ConfigureEventResponse,
    summary="Configure a fan engagement event",
    description="Store new or updated configuration for a fan engagement event.",
    status_code=status.HTTP_201_CREATED,
)
def configure_event(payload: ConfigureEventRequest):
    """
    Configure a fan engagement event.

    Accepts event configuration as payload. Persists configuration and emits Kafka update (to be implemented).

    Parameters:
        payload (ConfigureEventRequest): Fan engagement event configuration object.

    Returns:
        ConfigureEventResponse: A response describing success/failure and the event id.
    """
    pass


# PUBLIC_INTERFACE
class CreateEventRequest(BaseModel):
    """
    Request schema for creating a new fan engagement event.
    """
    title: str = Field(..., description="Event title.")
    description: str = Field(..., description="Event description.")
    startTime: str = Field(..., description="Start time (ISO-8601).")
    endTime: str = Field(..., description="End time (ISO-8601).")
    organizers: list[str] = Field(default_factory=list, description="List of organizer IDs.")
    # Optionally, data sources and timelines
    dataSources: list[DataSourceModel] = Field(default_factory=list, description="List of data sources.")
    timelines: list[TimelineModel] = Field(default_factory=list, description="Event timeline segments.")


class CreateEventResponse(BaseModel):
    """
    Response model for event creation endpoint.
    """
    success: bool = Field(..., description="Result of creation operation.")
    message: str = Field(..., description="Status message.")
    eventId: str = Field(..., description="Newly created event ID.")


# PUBLIC_INTERFACE
@router.post(
    "/event",
    response_model=CreateEventResponse,
    summary="Create a new fan engagement event",
    description="Creates a new fan engagement event with metadata, sources, and timeline.",
    status_code=status.HTTP_201_CREATED,
)
def create_event(payload: CreateEventRequest):
    """
    Create a new fan engagement event.

    Parameters:
        payload (CreateEventRequest): Event creation object.

    Returns:
        CreateEventResponse: Describes result and new eventId.
    """
    pass


# PUBLIC_INTERFACE
class GetEventResponse(BaseModel):
    """
    Response model for retrieving a fan engagement event.
    """
    event: EventModel = Field(..., description="Fan engagement event details.")
    found: bool = Field(True, description="True if event found.")


# PUBLIC_INTERFACE
@router.get(
    "/event",
    response_model=GetEventResponse,
    summary="Get fan engagement event details",
    description="Retrieve metadata, sources, and timelines for a single event.",
    status_code=status.HTTP_200_OK,
)
def get_event(event_id: str):
    """
    Get a fan engagement event by unique identifier.

    Parameters:
        event_id (str): The event's unique identifier.

    Returns:
        GetEventResponse: Event object and found status.
    """
    pass

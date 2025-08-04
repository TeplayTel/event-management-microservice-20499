"""
Event-related FastAPI routes and request/response models.

Defines API endpoints and request/response Pydantic schemas for:
- Creating events
- Configuring event data sources
- Querying event details

Models provide strict validation and OpenAPI docstrings for endpoints.
"""

from fastapi import APIRouter, status, Depends
from event_engagement_backend.src.validation.models import (
    EventModel, DataSourceModel, TimelineModel
)
from event_engagement_backend.src.exceptions.error_handlers import ErrorResponse
from event_engagement_backend.src.business.event_service import EventService
from event_engagement_backend.src.auth.dependencies import get_current_user
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
    responses={
        201: {"model": ConfigureEventResponse},
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Configure a fan engagement event",
    description="Store new or updated configuration for a fan engagement event.",
    status_code=status.HTTP_201_CREATED,
)
def configure_event(
    payload: ConfigureEventRequest,
    user: dict = Depends(get_current_user)
):
    """
    Configure a fan engagement event.

    Accepts event configuration as payload. Persists configuration and emits Kafka update (to be implemented).

    Parameters:
        payload (ConfigureEventRequest): Fan engagement event configuration object.
        user (dict): Authenticated user context.

    Returns:
        ConfigureEventResponse: A response describing success/failure and the event id.
    """
    svc = EventService()
    # event field in payload.event should be EventModel but might not match config model in backend exactly, so convert.
    config_data = {"eventId": payload.event.eventId, "config": payload.event.model_dump()}
    result = svc.configure_event(config_data)
    return ConfigureEventResponse(
        success=result["success"],
        message=result["message"],
        event_id=result["event_id"]
    )


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
    responses={
        201: {"model": CreateEventResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Create a new fan engagement event",
    description="Creates a new fan engagement event with metadata, sources, and timeline.",
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    payload: CreateEventRequest,
    user: dict = Depends(get_current_user)
):
    """
    Create a new fan engagement event.

    Parameters:
        payload (CreateEventRequest): Event creation object.
        user (dict): Authenticated user context.

    Returns:
        CreateEventResponse: Describes result and new eventId.
    """
    svc = EventService()
    result = svc.create_event(payload.model_dump())
    return CreateEventResponse(
        success=result["success"],
        message=result["message"],
        eventId=result["eventId"]
    )


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
    responses={
        200: {"model": GetEventResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Get fan engagement event details",
    description="Retrieve metadata, sources, and timelines for a single event.",
    status_code=status.HTTP_200_OK,
)
def get_event(
    event_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Get a fan engagement event by unique identifier.

    Parameters:
        event_id (str): The event's unique identifier.
        user (dict): Authenticated user context.

    Returns:
        GetEventResponse: Event object and found status.
    """
    svc = EventService()
    result = svc.get_event(event_id)
    return GetEventResponse(
        event=EventModel(**result["event"]),
        found=result["found"]
    )

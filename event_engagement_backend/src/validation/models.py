"""
Validation (Pydantic) models for input and output API payloads: Event, DataSource, Timeline.

Field naming: Prefer camelCase for Pydantic (API/validation) models.
MongoDB models (in data_access/models.py) use snake_case.

Strict validation enforced. All public models documented.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

# PUBLIC_INTERFACE
class DataSourceModel(BaseModel):
    """
    Pydantic model for event data source configuration.
    Field names are camelCase for use in API input/output.
    """
    sourceId: str = Field(..., description="Unique identifier for the data source.")
    name: str = Field(..., description="Name of data source (e.g. 'Polling API', 'Live Score').")
    type: str = Field(..., description="Type of data source (API, file, manual, etc.).")
    config: dict = Field(..., description="Configuration details for the data source.")

    model_config = ConfigDict(extra="forbid", populate_by_name=True, use_enum_values=True)


# PUBLIC_INTERFACE
class TimelineModel(BaseModel):
    """
    Pydantic model for event timeline entries.
    Each timeline has an optional id, a list of actions, and time bounds.
    """
    timelineId: Optional[str] = Field(None, description="Timeline unique identifier.")
    actions: List[str] = Field(..., description="List of actions/steps in the timeline.")
    startTime: str = Field(..., description="Timeline start time (ISO-8601 formatted).")
    endTime: str = Field(..., description="Timeline end time (ISO-8601 formatted).")

    model_config = ConfigDict(extra="forbid", populate_by_name=True, use_enum_values=True)


# PUBLIC_INTERFACE
class EventModel(BaseModel):
    """
    Pydantic model representing a fan engagement event.
    Contains event meta, data sources, timelines, and configuration.
    """
    eventId: str = Field(..., description="Unique event identifier.")
    title: str = Field(..., description="Event title.")
    description: Optional[str] = Field(None, description="Event description.")
    organizers: Optional[List[str]] = Field(default_factory=list, description="List of organizer names/emails.")
    status: str = Field(..., description="Event status (e.g. 'scheduled', 'active', 'completed', 'cancelled').")
    startTime: str = Field(..., description="Start time (ISO-8601 format).")
    endTime: str = Field(..., description="End time (ISO-8601 format).")
    dataSources: Optional[List[DataSourceModel]] = Field(default_factory=list, description="Associated data sources.")
    timelines: Optional[List[TimelineModel]] = Field(default_factory=list, description="Associated timeline segments.")

    model_config = ConfigDict(extra="forbid", populate_by_name=True, use_enum_values=True)

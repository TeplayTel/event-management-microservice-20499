"""
Validation logic for event-related payloads.
"""
from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class EventConfigModel(BaseModel):
    """Schema for event configuration payload validation."""
    event_id: str = Field(..., description="Unique event identifier.")
    config: dict = Field(..., description="Configuration metadata dictionary.")

# PUBLIC_INTERFACE
class EventInputModel(BaseModel):
    """Schema for event creation payload validation."""
    title: str = Field(..., description="Event title")
    description: str = Field(..., description="Description of the event")
    start_time: str = Field(..., description="Event start time (ISO)")
    end_time: str = Field(..., description="Event end time (ISO)")

# Additional validators would be added here as necessary.

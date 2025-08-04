"""
MongoDB data (persistence) models for Event, DataSource, Timeline.

Naming: snake_case for field names. Used for persistence layer and Mongo documents.
"""

from typing import List, Optional, Dict, Any

# PUBLIC_INTERFACE
class DataSourceMongoModel:
    """
    MongoDB model for a data source document (event_data_source collection).
    Field names use snake_case for MongoDB.
    """
    def __init__(self, source_id: str, name: str, type: str, config: Dict[str, Any]):
        self.source_id = source_id
        self.name = name
        self.type = type
        self.config = config

# PUBLIC_INTERFACE
class TimelineMongoModel:
    """
    MongoDB model for a timeline document (event_timelines collection).
    """
    def __init__(
        self,
        timeline_id: Optional[str],
        actions: List[str],
        start_time: str,
        end_time: str,
    ):
        self.timeline_id = timeline_id
        self.actions = actions
        self.start_time = start_time
        self.end_time = end_time

# PUBLIC_INTERFACE
class EventMongoModel:
    """
    MongoDB model for an event document (event_metadata collection).
    """
    def __init__(
        self,
        event_id: str,
        title: str,
        description: Optional[str],
        organizers: Optional[List[str]],
        status: str,
        start_time: str,
        end_time: str,
        data_sources: Optional[List[dict]] = None,
        timelines: Optional[List[dict]] = None,
    ):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.organizers = organizers if organizers is not None else []
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.data_sources = data_sources if data_sources is not None else []
        self.timelines = timelines if timelines is not None else []

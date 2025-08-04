"""
Constant values for event domain, Kafka topics, etc.
"""

# PUBLIC_INTERFACE
class EventConstants:
    """Constant values for event and data source management."""

    KAFKA_EVENT_TOPIC = "event_lifecycle"
    KAFKA_DATASOURCE_TOPIC = "event_data_source"
    EVENT_METADATA_COLLECTION = "event_metadata"
    EVENT_DATASOURCE_COLLECTION = "event_data_source"
    EVENT_TIMELINES_COLLECTION = "event_timelines"

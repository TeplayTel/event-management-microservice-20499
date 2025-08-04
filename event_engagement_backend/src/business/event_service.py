"""
Core event business logic (service layer).
"""

from typing import Any, Dict
import traceback

from event_engagement_backend.src.data_access.mongo_repository import MongoRepository
from event_engagement_backend.src.transformation.transformers import EventTransformer
from event_engagement_backend.src.validation.event_validators import EventInputModel, EventConfigModel
from event_engagement_backend.src.exceptions.errors import (
    EventServiceException,
    EventNotFoundException,
    InvalidEventPayloadException,
)
from event_engagement_backend.src.logging.logger import get_logger

logger = get_logger(__name__)


# PUBLIC_INTERFACE
class EventService:
    """
    Implements application business rules for events.

    Methods encapsulate all fan engagement event flows, using repository, input validation,
    transformation between API/business and DB persistence, type hinting, and robust error propagation.
    Kafka integration (produce) is prepared as placeholders for future extension.
    """

    def __init__(self):
        """Initialize repository, validators, and transformers."""
        self.repo = MongoRepository()
        self.transformer = EventTransformer()

    # PUBLIC_INTERFACE
    def create_event(self, event_data: dict) -> Dict[str, Any]:
        """
        Create an event with provided event_data.

        Args:
            event_data (dict): Validated event data (API/business, camelCase keys).

        Returns:
            dict: Event creation result with {success, message, eventId}.
        Raises:
            InvalidEventPayloadException, EventServiceException
        """
        logger.debug("create_event called with data: %s", event_data)
        try:
            # Validate input - expecting camelCase input here
            validated = EventInputModel.parse_obj(event_data)
            mapped = self.transformer.to_persistence(validated.model_dump(by_alias=True))
            logger.debug("Mapped event_data to persistence model: %s", mapped)

            # Mongo expects snake_case for all fields (enforced in mapping/transformer)
            event_id = self.repo.insert_event(mapped)
            # Placeholder: produce to Kafka event lifecycle topic
            self._publish_event_created(event_id, mapped)

            logger.info("Event created successfully: %s", event_id)
            return {
                "success": True,
                "message": "Event created",
                "eventId": event_id,
            }
        except Exception as ex:
            logger.error("Error creating event: %s", ex)
            logger.debug(traceback.format_exc())
            raise InvalidEventPayloadException(f"Failed to create event: {ex}") from ex

    # PUBLIC_INTERFACE
    def configure_event(self, config_data: dict) -> Dict[str, Any]:
        """
        Store/update event configuration.

        Args:
            config_data (dict): Configuration details with 'eventId' and 'config'.

        Returns:
            dict: Status/result of configuration with {success, message, event_id}.
        Raises:
            InvalidEventPayloadException, EventNotFoundException, EventServiceException
        """
        logger.debug("configure_event called: %s", config_data)
        try:
            # Input: config_data must include 'eventId'
            validated = EventConfigModel.parse_obj(config_data)
            # Try to find event
            event = self.repo.find_event(validated.event_id)
            if not event:
                logger.warning(f"Event not found for configure_event: {validated.event_id}")
                raise EventNotFoundException(f"Event not found: {validated.event_id}")

            # Update the event (add/configure fields as needed in persistence)
            update_success = self.repo.update_event(validated.event_id, {"config": validated.config})
            if update_success:
                # Placeholder: produce to Kafka event configuration topic
                self._publish_event_configured(validated.event_id, validated.config)
                logger.info(f"Configured event: {validated.event_id}")
                return {
                    "success": True,
                    "message": "Event configured.",
                    "event_id": validated.event_id,
                }
            else:
                logger.error(f"Event configuration update failed: {validated.event_id}")
                return {
                    "success": False,
                    "message": "Update operation failed (not found or not modified).",
                    "event_id": validated.event_id,
                }
        except EventNotFoundException as enf:
            logger.error(str(enf))
            raise
        except Exception as ex:
            logger.error("Error in configure_event: %s", ex)
            logger.debug(traceback.format_exc())
            raise InvalidEventPayloadException(f"Failed to configure event: {ex}") from ex

    # PUBLIC_INTERFACE
    def get_event(self, event_id: str) -> Dict[str, Any]:
        """
        Retrieve event by ID.

        Args:
            event_id (str): Unique identifier (str).

        Returns:
            dict: Event data as API/business model with camelCase keys, or error.
        Raises:
            EventServiceException if event not found or on error.
        """
        logger.debug(f"get_event called for event_id: {event_id}")
        try:
            db_event = self.repo.find_event(event_id)
            if not db_event:
                logger.warning(f"Event not found (get_event): {event_id}")
                raise EventNotFoundException(f"Event not found for id: {event_id}")

            # Convert persistence dict (snake_case) to business dict (camelCase)
            event_out = self.transformer.from_persistence(db_event)
            logger.info(f"Fetched event: {event_id}")
            return {
                "event": event_out,
                "found": True,
            }
        except EventNotFoundException as enf:
            logger.error(str(enf))
            raise
        except Exception as ex:
            logger.error("Error retrieving event: %s", ex)
            logger.debug(traceback.format_exc())
            raise EventServiceException(f"Failed to fetch event: {ex}") from ex

    # --- Kafka Placeholder Methods ---
    def _publish_event_created(self, event_id: str, data: dict) -> None:
        """
        Placeholder for producing to Kafka when a new event is created.

        Args:
            event_id (str): Event identifier.
            data (dict): The event details as persisted.
        """
        logger.debug("[Kafka placeholder] Publish event CREATED for %s", event_id)
        pass

    def _publish_event_configured(self, event_id: str, config: dict) -> None:
        """
        Placeholder for producing to Kafka when an event is configured.

        Args:
            event_id (str): Event identifier.
            config (dict): The configuration details.
        """
        logger.debug("[Kafka placeholder] Publish event CONFIGURED for %s", event_id)
        pass

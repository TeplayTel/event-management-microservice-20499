"""
MongoDB repository for CRUD operations on event, data source, and timeline collections.

Implements environment-based connection handling, ensures snake_case for DB fields,
and logs all key operations with proper error handling.

Collections:
- event_metadata
- event_data_source
- event_timelines
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional

from event_engagement_backend.src.constants.event_constants import EventConstants
from event_engagement_backend.src.config import Config
from event_engagement_backend.src.logging.logger import get_logger

logger = get_logger(__name__)

# --- Utilities ---

def _to_object_id(oid: str) -> Optional[ObjectId]:
    try:
        return ObjectId(oid)
    except Exception:
        logger.warning(f"Failed to convert to ObjectId: {oid}")
        return None


# PUBLIC_INTERFACE
class MongoRepository:
    """
    Central repository handling MongoDB CRUD for all collections.

    Ensures:
    - snake_case for DB fields
    - Centralized logging
    """
    def __init__(self):
        """
        Initialize Mongo connection using environment config.

        Raises:
            RuntimeError: If DB connection could not be established.
        """
        try:
            self.client = MongoClient(Config.MONGODB_URL)
            self.db = self.client[Config.MONGODB_DB]
        except Exception as ex:
            logger.error(f"MongoDB connection failed: {ex}")
            raise RuntimeError("DB connection error") from ex

        # Collections (snake_case names)
        self.event_col = self.db[EventConstants.EVENT_METADATA_COLLECTION]
        self.datasource_col = self.db[EventConstants.EVENT_DATASOURCE_COLLECTION]
        self.timeline_col = self.db[EventConstants.EVENT_TIMELINES_COLLECTION]

        logger.info("MongoRepository initialized (DB/Collections ready).")

    # --- EVENTS ---

    # PUBLIC_INTERFACE
    def insert_event(self, data: dict) -> str:
        """
        Insert a new event document.

        Args:
            data (dict): Event document.

        Returns:
            str: Inserted event _id.
        """
        try:
            result = self.event_col.insert_one(data)
            logger.info(f"Inserted event: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as ex:
            logger.error(f"Failed to insert event: {ex}")
            raise

    # PUBLIC_INTERFACE
    def update_event(self, event_id: str, data: dict) -> bool:
        """
        Update an event document by its _id.

        Args:
            event_id (str): Document ObjectId as str.
            data (dict): Update values.

        Returns:
            bool: True if modified, False if not found.
        """
        oid = _to_object_id(event_id)
        if not oid:
            logger.warning(f"Invalid ObjectId for update_event: {event_id}")
            return False
        try:
            result = self.event_col.update_one({"_id": oid}, {"$set": data})
            logger.info(f"Updated event {event_id}: matched={result.matched_count} modified={result.modified_count}")
            return result.modified_count > 0
        except Exception as ex:
            logger.error(f"Failed to update event {event_id}: {ex}")
            raise

    # PUBLIC_INTERFACE
    def find_event(self, event_id: str) -> Optional[dict]:
        """
        Find a single event by its _id or event_id.

        Args:
            event_id (str): Either Mongo ObjectId or "event_id" field value.

        Returns:
            dict or None: Event doc if found.
        """
        oid = _to_object_id(event_id)
        try:
            if oid:
                event = self.event_col.find_one({"_id": oid})
                if event:
                    logger.info(f"Found event by _id {event_id}.")
                    return event
            # Fallback: match on semantic event_id field
            event = self.event_col.find_one({"event_id": event_id})
            logger.info(f"Found event by event_id: {event_id}: {bool(event)}")
            return event
        except Exception as ex:
            logger.error(f"Failed to find event {event_id}: {ex}")
            raise

    # PUBLIC_INTERFACE
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event by id.

        Args:
            event_id (str): Event id.

        Returns:
            bool: True if deleted, False otherwise.
        """
        oid = _to_object_id(event_id)
        try:
            if oid:
                result = self.event_col.delete_one({"_id": oid})
            else:
                result = self.event_col.delete_one({"event_id": event_id})
            logger.info(f"Deleted event {event_id}: deleted={result.deleted_count}")
            return result.deleted_count > 0
        except Exception as ex:
            logger.error(f"Failed to delete event {event_id}: {ex}")
            raise

    # --- DATA SOURCES ---

    # PUBLIC_INTERFACE
    def insert_data_source(self, data: dict) -> str:
        """
        Insert a new data source document.

        Args:
            data (dict): Data source document.

        Returns:
            str: Inserted data source _id.
        """
        try:
            result = self.datasource_col.insert_one(data)
            logger.info(f"Inserted data_source: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as ex:
            logger.error(f"Failed to insert data source: {ex}")
            raise

    # PUBLIC_INTERFACE
    def update_data_source(self, source_id: str, data: dict) -> bool:
        """
        Update a data source document by _id or source_id.

        Args:
            source_id (str): Mongo ObjectId or custom source_id.
            data (dict): Update values.

        Returns:
            bool: True if modified.
        """
        oid = _to_object_id(source_id)
        try:
            if oid:
                result = self.datasource_col.update_one({"_id": oid}, {"$set": data})
            else:
                result = self.datasource_col.update_one({"source_id": source_id}, {"$set": data})
            logger.info(f"Updated data_source {source_id}: matched={result.matched_count} modified={result.modified_count}")
            return result.modified_count > 0
        except Exception as ex:
            logger.error(f"Failed to update data source {source_id}: {ex}")
            raise

    # PUBLIC_INTERFACE
    def find_data_source(self, source_id: str) -> Optional[dict]:
        """
        Find a data source by _id or source_id.

        Args:
            source_id (str): MongoDB ObjectId or source_id field.

        Returns:
            dict or None
        """
        oid = _to_object_id(source_id)
        try:
            if oid:
                ds = self.datasource_col.find_one({"_id": oid})
                if ds:
                    logger.info(f"Found data_source by _id {source_id}.")
                    return ds
            ds = self.datasource_col.find_one({"source_id": source_id})
            logger.info(f"Found data_source by source_id {source_id}: {bool(ds)}")
            return ds
        except Exception as ex:
            logger.error(f"Failed to find data source {source_id}: {ex}")
            raise

    # PUBLIC_INTERFACE
    def delete_data_source(self, source_id: str) -> bool:
        """
        Delete a data source document.

        Args:
            source_id (str): Document id.

        Returns:
            bool: True if deleted.
        """
        oid = _to_object_id(source_id)
        try:
            if oid:
                result = self.datasource_col.delete_one({"_id": oid})
            else:
                result = self.datasource_col.delete_one({"source_id": source_id})
            logger.info(f"Deleted data source {source_id}: deleted={result.deleted_count}")
            return result.deleted_count > 0
        except Exception as ex:
            logger.error(f"Failed to delete data source {source_id}: {ex}")
            raise

    # --- TIMELINES ---

    # PUBLIC_INTERFACE
    def insert_timeline(self, data: dict) -> str:
        """
        Insert a new timeline document.

        Args:
            data (dict): Timeline document.

        Returns:
            str: Inserted timeline _id.
        """
        try:
            result = self.timeline_col.insert_one(data)
            logger.info(f"Inserted timeline: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as ex:
            logger.error(f"Failed to insert timeline: {ex}")
            raise

    # PUBLIC_INTERFACE
    def update_timeline(self, timeline_id: str, data: dict) -> bool:
        """
        Update timeline by id.

        Args:
            timeline_id (str): _id or timeline_id

        Returns:
            bool: True if modified.
        """
        oid = _to_object_id(timeline_id)
        try:
            if oid:
                result = self.timeline_col.update_one({"_id": oid}, {"$set": data})
            else:
                result = self.timeline_col.update_one({"timeline_id": timeline_id}, {"$set": data})
            logger.info(f"Updated timeline {timeline_id}: matched={result.matched_count} modified={result.modified_count}")
            return result.modified_count > 0
        except Exception as ex:
            logger.error(f"Failed to update timeline {timeline_id}: {ex}")
            raise

    # PUBLIC_INTERFACE
    def find_timeline(self, timeline_id: str) -> Optional[dict]:
        """
        Find timeline by _id or timeline_id.

        Args:
            timeline_id (str): Doc id.

        Returns:
            dict or None
        """
        oid = _to_object_id(timeline_id)
        try:
            if oid:
                t = self.timeline_col.find_one({"_id": oid})
                if t:
                    logger.info(f"Found timeline by _id {timeline_id}.")
                    return t
            t = self.timeline_col.find_one({"timeline_id": timeline_id})
            logger.info(f"Found timeline by timeline_id {timeline_id}: {bool(t)}")
            return t
        except Exception as ex:
            logger.error(f"Failed to find timeline {timeline_id}: {ex}")
            raise

    # PUBLIC_INTERFACE
    def delete_timeline(self, timeline_id: str) -> bool:
        """
        Delete timeline doc.

        Args:
            timeline_id (str): Doc id.

        Returns:
            bool: True if deleted.
        """
        oid = _to_object_id(timeline_id)
        try:
            if oid:
                result = self.timeline_col.delete_one({"_id": oid})
            else:
                result = self.timeline_col.delete_one({"timeline_id": timeline_id})
            logger.info(f"Deleted timeline {timeline_id}: deleted={result.deleted_count}")
            return result.deleted_count > 0
        except Exception as ex:
            logger.error(f"Failed to delete timeline {timeline_id}: {ex}")
            raise

    # --- GENERIC UTILS ---

    # PUBLIC_INTERFACE
    def ping(self) -> bool:
        """
        Test connection to Mongo server.

        Returns:
            bool: True if server is reachable.
        """
        try:
            self.client.admin.command('ping')
            logger.info("MongoDB ping ok.")
            return True
        except Exception as ex:
            logger.error(f"MongoDB ping failed: {ex}")
            return False

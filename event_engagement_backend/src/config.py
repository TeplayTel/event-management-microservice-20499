"""
Configuration loader for event_engagement_backend service.

Loads all properties from .env using python-dotenv and exposes config variables for use in the application.
All application and logging configs are loaded strictly from environment variables.
"""

import os
from dotenv import load_dotenv

# Load from the .env file at the project root
load_dotenv()

class Config:
    """
    Configuration management for environment properties.

    All configuration, including logging level, destination, and paths, is loaded 
    from environment variables and never hardcoded.

    Environment Variables:
        MONGODB_URL
        MONGODB_DB
        KAFKA_BOOTSTRAP_SERVERS
        DEBUG
        LOG_LEVEL
        LOG_DESTINATION
        LOG_FILE
    """
    # MongoDB connection
    MONGODB_URL: str = os.getenv("MONGODB_URL", "")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "")
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    # LOGGING
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DESTINATION: str = os.getenv("LOG_DESTINATION", "stdout")
    LOG_FILE: str = os.getenv("LOG_FILE", "service.log")

# Example usage:
# from config import Config
# db_url = Config.MONGODB_URL

"""
Configuration loader for event_engagement_backend service.

Loads all properties from .env using python-dotenv and exposes config variables for use in the application.
Expands MongoDB options as required by MongoRepository.
"""

import os
from dotenv import load_dotenv

# Load from the .env file at the project root
load_dotenv()

class Config:
    """Configuration management for environment properties."""
    # MongoDB connection
    MONGODB_URL: str = os.getenv("MONGODB_URL", "")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "")
    # Kafka (example, extend as needed)
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    # App settings (add more as needed)
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    # Any other global settings can be added here

# Example usage:
# from config import Config
# db_url = Config.MONGODB_URL

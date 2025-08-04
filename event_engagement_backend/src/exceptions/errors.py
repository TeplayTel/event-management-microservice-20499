"""
Custom exception classes for the service.
"""

# PUBLIC_INTERFACE
class EventServiceException(Exception):
    """Base exception for business/domain layer."""
    pass

# PUBLIC_INTERFACE
class EventNotFoundException(EventServiceException):
    """Raised when event is not found."""
    pass

# PUBLIC_INTERFACE
class InvalidEventPayloadException(EventServiceException):
    """Raised for invalid event input or configuration."""
    pass

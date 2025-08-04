"""
Authentication stub dependency for FastAPI security.
Replace this logic in production with real JWT/OAuth2 validation.
"""

from fastapi import HTTPException, status, Header
from event_engagement_backend.src.auth.auth_manager import AuthManager

# PUBLIC_INTERFACE
def get_current_user(authorization: str = Header(None)) -> dict:
    """Dependency for extracting and validating auth token, returns a stub user dict or raises 401."""
    manager = AuthManager()
    if authorization is None or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header."
        )
    token = authorization.split(" ", 1)[1]
    if not manager.verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )
    # Optionally return user context. Here just stubbed as an example.
    user = manager.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or user not found."
        )
    return user

import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .config import get_settings


security = HTTPBasic(auto_error=False)


def verify_basic_auth(credentials: HTTPBasicCredentials | None = Depends(security)) -> str:
    settings = get_settings()
    if not settings.api_basic_auth_enabled:
        return "anonymous"

    if credentials is None:
        raise _auth_error()

    username_ok = secrets.compare_digest(credentials.username, settings.api_username)
    password_ok = secrets.compare_digest(credentials.password, settings.api_password)
    if not (username_ok and password_ok):
        raise _auth_error()

    return credentials.username


def _auth_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Basic"},
    )

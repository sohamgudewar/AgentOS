from datetime import datetime, timedelta, UTC
from typing import Any

from jose import jwt, JWTError

from app.core.config import settings


def create_access_token(
    data: dict[str, Any],
) -> str:
    """Create a signed JWT access token."""

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update(
        {
            "exp": expire,
            }
        )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """Decode and verify a signed JWT access token."""

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        raise ValueError("Invalid or expired access token")

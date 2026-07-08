from datetime import datetime, timedelta, timezone

from fastapi import Cookie, HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def check_auth(access_token: str | None = Cookie(default=None)):

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Not authenticated",
            headers={"Location": "/auth/"},
        )

    try:
        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail="Invalid token",
                headers={"Location": "/auth/"},
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Invalid token",
            headers={"Location": "/auth/"},
        )

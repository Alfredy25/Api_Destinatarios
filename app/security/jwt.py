from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt

from app.config.settings import settings


# Creación de JWT
# -----------------------------------------------------------------------------
def create_access_token(subject: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXP_MINUTES)
    payload = {"sub":subject, "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def create_refresh_token(subject: str):
    expire = datetime.utcnow() + timedelta(days=7)
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

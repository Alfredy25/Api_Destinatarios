from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import bcrypt

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

# Hash de contraseñas
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

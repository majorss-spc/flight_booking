
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pydantic_settings import BaseSettings, SettingsConfigDict


# Load configuration from the project's .env file.
class SecuritySettings(BaseSettings):
    database_url: str
    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = SecuritySettings()
SECRET_KEY = settings.jwt_secret_key


# JWT signing algorithm
ALGORITHM = "HS256"

# Token validity: 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Secure password hashing using Argon2
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convert a plain-text password into a secure hash."""
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its stored hash."""
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    """Create a signed JWT access token."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expires_at,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Verify a JWT and return its payload."""
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

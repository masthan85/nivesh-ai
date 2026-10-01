"""Password hashing, access tokens and the current-user dependency."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# bcrypt only uses the first 72 bytes of a password. The registration schema
# rejects longer passwords so nothing is silently truncated.
BCRYPT_MAX_BYTES = 72


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(data: dict) -> str:
    now = datetime.now(timezone.utc)
    payload = {**data, "iat": now, "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def _credentials_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def user_from_token(token: str, db: Session):
    """Resolve an active user from a token, or raise 401. Shared by HTTP and WebSocket routes."""
    from app.models.user import User

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError:
        raise _credentials_error()
    email = payload.get("sub")
    if not email:
        raise _credentials_error()
    user = db.query(User).filter(User.email == email).first()
    # A deactivated account must lose access immediately, not when its token expires.
    if user is None or not user.is_active:
        raise _credentials_error()
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return user_from_token(token, db)

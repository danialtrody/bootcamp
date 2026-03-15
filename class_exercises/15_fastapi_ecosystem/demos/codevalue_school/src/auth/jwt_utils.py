import os
import time
from dataclasses import asdict

from jose import ExpiredSignatureError, JWTError, jwt
from jose.constants import ALGORITHMS

from src.auth.data_classes import UserTokenData
from src.auth.exceptions import AuthSessionExpiredException, BearAuthException
from src.constants import JWT_EXPIRATION_SECONDS


def _get_secret_key() -> str:
    key = os.getenv("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY environment variable is not set")
    return key


def create_access_token(session_id: str) -> str:
    exp = int(time.time()) + JWT_EXPIRATION_SECONDS
    token_data = UserTokenData(session_id=session_id, exp=exp)
    return jwt.encode(asdict(token_data), _get_secret_key(), algorithm=ALGORITHMS.HS256)


def get_token_payload(session_token: str) -> UserTokenData:
    try:
        payload = jwt.decode(session_token, _get_secret_key(), algorithms=[ALGORITHMS.HS256])
        return UserTokenData(**payload)
    except ExpiredSignatureError:
        raise AuthSessionExpiredException("Session expired")
    except JWTError:
        raise BearAuthException("Token could not be validated")

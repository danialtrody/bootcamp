import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Response, status
from fastapi.security import APIKeyCookie

from src.auth.exceptions import AuthSessionExpiredException, BearAuthException
from src.auth.jwt_utils import get_token_payload
from src.constants import UserRole
from src.models.user import User
from src.secrets_accessor import SecretNotFoundException, get_secrets_accessor
from src.services.auth_service import AuthService, get_auth_service

SESSION_COOKIE_NAME = "session_token"
COOKIE = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)

SessionTokenDep = Annotated[str, Depends(COOKIE)]


def is_auth_required() -> bool:
    try:
        value = get_secrets_accessor().get_secret("REQUIRE_AUTH")
        return value.lower() in ("true", "1", "yes")
    except SecretNotFoundException:
        return True


async def get_current_user(
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    session_token: SessionTokenDep,
) -> User:
    logger = logging.getLogger(__name__)

    if not is_auth_required():
        logger.info("Auth disabled — returning dev user")
        return User(
            id=1,
            email="dev@local.test",
            first_name="Dev",
            last_name="User",
            role=UserRole.ADMIN.value,
            disabled=False,
        )

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No session token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        userdata = get_token_payload(session_token)
        auth_session = await auth_service.get_session_with_user(userdata.session_id)
        user = auth_session.user
        await auth_service.validate_session(auth_session)
        auth_service.refresh_token_if_needed(userdata, user, response)
    except (BearAuthException, AuthSessionExpiredException) as exc:
        logger.warning(f"Auth failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )
    return current_user


async def get_current_admin(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    if current_active_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_active_user

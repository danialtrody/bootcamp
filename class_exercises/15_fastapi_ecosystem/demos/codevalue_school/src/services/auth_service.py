import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Optional

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.auth import (
    AuthSessionExpiredException,
    BearAuthException,
    InvalidCredentialsException,
    SESSION_EXPIRY_HOURS,
    SessionFingerprint,
    UserAlreadyExistsException,
    UserTokenData,
    create_access_token,
)
from src.auth import TOKEN_REFRESH_THRESHOLD, get_token_payload, hash_password, verify_password
from src.database import async_session_maker
from src.dto.user_dto import UserCreateDTO, UserResponseDTO
from src.models import AuthSession, User
from src.repositories import AuthSessionRepository, UserRepository

SESSION_COOKIE_NAME = "session_token"


def _user_to_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO.model_validate(user)


class AuthService:

    def __init__(
        self,
        user_repo: Optional[UserRepository] = None,
        session_repo: Optional[AuthSessionRepository] = None,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self._user_repo = user_repo or UserRepository()
        self._session_repo = session_repo or AuthSessionRepository()
        self._session_maker = session_maker or async_session_maker
        self._logger = logging.getLogger(__name__)

    async def create_user(self, data: UserCreateDTO) -> UserResponseDTO:
        self._logger.info(f"Creating user email={data.email}")
        async with self._session_maker() as session:
            async with session.begin():
                existing = await self._user_repo.get_by_email(session, data.email)
                if existing is not None:
                    raise UserAlreadyExistsException(f"User with email {data.email} already exists")
                user = User(
                    email=data.email,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    password_hash=hash_password(data.password),
                    role=data.role,
                    disabled=data.disabled,
                )
                created = await self._user_repo.create(session, user)
        return _user_to_dto(created)

    async def login(
        self, email: str, password: str, request: Request, response: Response
    ) -> UserResponseDTO:
        self._logger.info(f"Login attempt email={email}")
        async with self._session_maker() as session:
            async with session.begin():
                user = await self._user_repo.get_by_email(session, email)
                if user is None or not verify_password(password, user.password_hash):
                    raise InvalidCredentialsException("Invalid email or password")
                auth_session = await self._create_session_in_db(session, user, request)
        token = create_access_token(auth_session.id)
        self.set_session_cookie(response, token)
        self._logger.info(f"Login successful email={email}")
        return _user_to_dto(user)

    async def logout(self, session_token: str, response: Response) -> None:
        try:
            userdata = get_token_payload(session_token)
            async with self._session_maker() as session:
                async with session.begin():
                    await self._session_repo.deactivate(session, userdata.session_id)
        except (BearAuthException, AuthSessionExpiredException) as exc:
            self._logger.warning(f"Logout with invalid token: {exc}")
        finally:
            response.delete_cookie(SESSION_COOKIE_NAME)

    async def get_session_with_user(self, session_id: str) -> AuthSession:
        async with self._session_maker() as session:
            auth_session = await self._session_repo.get_with_user(session, session_id)
        if auth_session is None:
            raise AuthSessionExpiredException(f"Session {session_id} not found")
        return auth_session

    async def validate_session(self, auth_session: AuthSession) -> None:
        if not auth_session.is_active:
            raise AuthSessionExpiredException("Session is not active")
        current_time = datetime.now(UTC).replace(tzinfo=None)
        if current_time > auth_session.expires_at:
            await self._deactivate_session(auth_session.id)
            raise AuthSessionExpiredException("Session has expired")
        await self._update_last_activity(auth_session.id)

    def should_refresh_token(self, userdata: UserTokenData, user: User) -> bool:
        if user.disabled:
            return False
        current_time = int(datetime.now(UTC).timestamp())
        if userdata.exp < current_time:
            return False
        return userdata.exp < (current_time + TOKEN_REFRESH_THRESHOLD)

    def refresh_token_if_needed(
        self, userdata: UserTokenData, user: User, response: Response
    ) -> None:
        if self.should_refresh_token(userdata, user):
            self._logger.info(f"Refreshing JWT for user={user.email}")
            new_token = create_access_token(userdata.session_id)
            self.set_session_cookie(response, new_token)

    def set_session_cookie(self, response: Response, token: str) -> None:
        response.set_cookie(
            SESSION_COOKIE_NAME,
            token,
            httponly=True,
            secure=False,
            samesite="strict",
        )

    async def _create_session_in_db(
        self, session: AsyncSession, user: User, request: Request
    ) -> AuthSession:
        session_id = str(uuid.uuid4())
        expires_at = datetime.now(UTC).replace(tzinfo=None) + timedelta(hours=SESSION_EXPIRY_HOURS)
        fingerprint = SessionFingerprint(
            user_agent=request.headers.get("User-Agent"),
            ip_address=request.client.host if request.client else None,
        )
        auth_session = AuthSession(
            id=session_id,
            user_id=user.id,
            is_active=True,
            expires_at=expires_at,
            fingerprint={
                "user_agent": fingerprint.user_agent,
                "ip_address": fingerprint.ip_address,
            },
        )
        return await self._session_repo.create(session, auth_session)

    async def _deactivate_session(self, session_id: str) -> None:
        async with self._session_maker() as session:
            async with session.begin():
                await self._session_repo.deactivate(session, session_id)

    async def _update_last_activity(self, session_id: str) -> None:
        async with self._session_maker() as session:
            async with session.begin():
                await self._session_repo.update_last_activity(session, session_id)


def get_auth_service() -> AuthService:
    return AuthService()

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from src.auth.auth_dependencies import COOKIE
from src.auth.exceptions import InvalidCredentialsException
from src.dependencies import AuthServiceDep, CurrentActiveUserDep
from src.dto.user_dto import LoginDTO, UserCreateDTO, UserResponseDTO
from src.infrastructure.handle_exceptions_decorator import handle_exceptions

router = APIRouter(prefix="/auth", tags=["Auth"])

SessionTokenDep = Annotated[str, Depends(COOKIE)]


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
@handle_exceptions()
async def register(data: UserCreateDTO, auth_service: AuthServiceDep) -> UserResponseDTO:
    return await auth_service.create_user(data)


@router.post("/login", response_model=UserResponseDTO)
async def login(
    data: LoginDTO,
    request: Request,
    response: Response,
    auth_service: AuthServiceDep,
) -> UserResponseDTO:
    try:
        return await auth_service.login(data.email, data.password, request, response)
    except InvalidCredentialsException as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    auth_service: AuthServiceDep,
    session_token: SessionTokenDep,
) -> dict[str, str]:
    await auth_service.logout(session_token, response)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponseDTO)
async def me(current_user: CurrentActiveUserDep) -> UserResponseDTO:
    return UserResponseDTO.model_validate(current_user)

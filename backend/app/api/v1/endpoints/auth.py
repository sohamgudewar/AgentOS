from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister, UserResponse, UserLogin, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """Endpoint to register a new user."""

    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        user = await service.register_user(user_data)
        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Endpoint to authenticate a user and return a JWT."""

    user_repository = UserRepository(db)
    service = AuthService(user_repository)

    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
        )

    return await service.login_user(user_data)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """Endpoint to get the current authenticated user's information."""

    return current_user

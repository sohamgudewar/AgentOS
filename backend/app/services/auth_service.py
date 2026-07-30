from app.auth.hashing import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.auth.jwt import create_access_token


class AuthService:
    """Business logic layer for authentication-related operations."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: UserRegister) -> User:
        """Register a new user."""
        # Check if the user already exists
        existing_user = await self.user_repository.get_user_by_email(user_data.email)

        if existing_user:
            raise ValueError("User with this email already exists.")

        # Hash the password before storing it
        hashed_password = hash_password(user_data.password)

        # Create a new User instance
        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
        )

        return await self.user_repository.create_user(user)

    async def login_user(self, user_data: UserLogin) -> TokenResponse:
        """Authenticate a user and return a JWT."""

        user = await self.user_repository.get_user_by_email(
            user_data.email
        )

        if not user:
            raise ValueError("Invalid Email or Password")

        if not verify_password(user_data.password, user.password_hash):
            raise ValueError("Invalid Email or Password")

        access_token = create_access_token(
            {"sub": user.email}
        )

        return TokenResponse(
            access_token=access_token,
        )

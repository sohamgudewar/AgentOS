# this file defies the contract between client(frontend) and backend. instead of accepting random json data, FastAPI will validate the data against the schema defined in this file.

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserRegister(BaseModel):
    """Schema for user registration data."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Schema for user login data."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema returned after successful login."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user data returned in responses."""

    id: UUID
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config={
        "from_attributes": True
    }

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, agents

api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["Health"])

api_router.include_router(
    auth.router,
    tags=["Authentication"])

api_router.include_router(
    agents.router,
    tags=["Agents"])

# #  127.0.0.1:59445 - "POST /api/v1/agents HTTP/1.1" 500 Internal Server Error

# ERROR:    Exception in ASGI application

# Traceback (most recent call last):



# Code	Details

# 500

# Undocumented

# Error: Internal Server Error



# Response body

# Download

# Internal Server Error
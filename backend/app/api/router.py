from fastapi import FastAPI
from fastapi import APIRouter
from app.api.v1.api import api_router
from app.core.constants import API_V1_PREFIX


router = APIRouter()

router.include_router(
    api_router,
    prefix=API_V1_PREFIX
)

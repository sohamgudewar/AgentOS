from fastapi import APIRouter
from app.core.constants import HEALTH_OK
from app.core.logger import logger

router = APIRouter()


@router.get("/health")
async def health_check():
    logger.info("Health check request received")
    return {"status": HEALTH_OK}

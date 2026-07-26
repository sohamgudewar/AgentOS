from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import logger
from app.api.router import router


app = FastAPI(
    title="AgentOS",
    description="AgentOS is a framework for building and deploying autonomous agents that can perform complex tasks and interact with various APIs and services.",
    version="0.1.0",
)


app.include_router(router)

logger.info("AgentOS backend app is starting...")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/health")
async def health():
    logger.info("Health check request received")
    return {"status": "AgentOS is healthy"}

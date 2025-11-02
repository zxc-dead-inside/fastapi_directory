from fastapi import FastAPI

from app.api.middleware import ExceptionHandlerMiddleware, LoggingMiddleware
from app.api.v1 import api_router
from app.core.logger import logger

app = FastAPI(title="Organization Directory API", version="1.0")

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(LoggingMiddleware)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")

logger.info("FastAPI app started successfully")


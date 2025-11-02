import time
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = None

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"{request.method} {request.url.path} "
                f"-> {response.status_code} ({process_time:.2f} ms)"
            )
            return response
        except Exception as e:
            logger.exception(f"Ошибка при обработке запроса {request.url.path}: {e}")
            raise
        finally:
            if not response:
                logger.warning(f"{request.method} {request.url.path} завершился без ответа.")


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/api/v1/"):
            api_key = request.headers.get("X-API-Key")

            if not api_key or api_key != settings.api_key:
                logger.warning(f"Неавторизованный доступ: {request.url.path}")
                raise HTTPException(status_code=401, detail="Invalid or missing API key")

        return await call_next(request)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail, "path": request.url.path},
            )
        except Exception as e:
            logger.exception(f"Необработанная ошибка: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "path": request.url.path},
            )

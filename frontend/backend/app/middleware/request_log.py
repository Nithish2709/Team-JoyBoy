import time
from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        # Parse correlation tracking headers
        correlation_id = request.headers.get("X-Correlation-ID", "N/A")
        client_host = request.client.host if request.client else "unknown"

        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"| Client: {client_host} | CorrelationID: {correlation_id}"
        )
        
        try:
            response: Response = await call_next(request)
            latency = (time.time() - start_time) * 1000
            
            logger.info(
                f"Completed request: {request.method} {request.url.path} "
                f"| Status: {response.status_code} | Latency: {latency:.2f}ms "
                f"| CorrelationID: {correlation_id}"
            )
            return response
        except Exception as exc:
            latency = (time.time() - start_time) * 1000
            logger.exception(
                f"Failed request: {request.method} {request.url.path} "
                f"| Error: {str(exc)} | Latency: {latency:.2f}ms "
                f"| CorrelationID: {correlation_id}"
            )
            raise exc

import redis.asyncio as aioredis
from loguru import logger
from app.core.config import settings

class RedisClientManager:
    def __init__(self) -> None:
        self.pool: aioredis.ConnectionPool | None = None
        
    def init_pool(self) -> None:
        logger.info("Initializing Redis connection pool...")
        self.pool = aioredis.ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=50,
            decode_responses=True
        )
        
    async def close_pool(self) -> None:
        if self.pool:
            logger.info("Closing Redis connection pool...")
            await self.pool.disconnect()
            
    def get_client(self) -> aioredis.Redis:
        if not self.pool:
            self.init_pool()
        assert self.pool is not None
        return aioredis.Redis(connection_pool=self.pool)

# Singleton manager instance
redis_manager = RedisClientManager()

async def check_redis_health() -> bool:
    """
    Verifies Redis connection health by executing a ping command.
    """
    client = redis_manager.get_client()
    try:
        # Execute ping query
        response = await client.ping()
        return response is True
    except Exception as exc:
        logger.error(f"Redis health check ping query failed: {str(exc)}")
        return False
    finally:
        # Ensure client connection closes back to the pool
        await client.close()

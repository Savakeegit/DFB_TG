from decouple import config
from redis.asyncio import Redis


async def get_redis() -> Redis:
    return Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=config('REDIS_DB'))
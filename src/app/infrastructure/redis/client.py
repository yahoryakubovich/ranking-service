import redis.asyncio as aioredis

_redis: aioredis.Redis | None = None


def init_redis(url: str, max_connections: int = 20) -> None:
    global _redis
    _redis = aioredis.from_url(
        url,
        decode_responses=True,
        max_connections=max_connections,
    )


def get_redis() -> aioredis.Redis:
    if _redis is None:
        raise RuntimeError('Redis is not initialized')
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None

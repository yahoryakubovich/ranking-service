import functools
import json
from typing import Callable, Awaitable, Any, TypeVar

from app.infrastructure.redis.client import get_redis

F = TypeVar('F', bound=Callable[..., Awaitable[Any]])


def redis_cache(ttl: int = 300):
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis = get_redis()

            module = getattr(func, '__module__', 'default_module')
            name = getattr(func, '__name__', 'default_name')

            key_parts = [module, name, str(args), str(kwargs)]
            key = ':'.join(key_parts)

            cached = await redis.get(key)
            if cached is not None:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            if result is not None:
                await redis.set(key, json.dumps(result, default=str), ex=ttl)

            return result

        return wrapper

    return decorator

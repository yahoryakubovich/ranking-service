from collections import Counter

from async_lru import alru_cache

from app.config import settings
from app.infrastructure.redis.cache import redis_cache
from app.infrastructure.redis.client import get_redis


@alru_cache(maxsize=1024)
@redis_cache(ttl=300)
async def get_ranked_products(uid: int) -> list[int]:
    redis = get_redis()

    top = await redis.zrevrange(
        f'user:{uid}:top_interest',
        0,
        settings.TOP_N * 4,
    )

    if not top:
        top = await redis.zrevrange(
            'products:top_popular',
            0,
            settings.TOP_N * 4,
        )

    if not top:
        return []

    async with redis.pipeline() as pipe:
        await pipe.hmget('products:brand', *top)
        await pipe.smembers(f'user:{uid}:purchased')
        brands_list, purchased_set = await pipe.execute()

    purchased_set = purchased_set or set()

    result: list[int] = []
    brand_count = Counter()

    for pid, brand in zip(top, brands_list):
        if pid in purchased_set:
            continue
        if brand is None:
            continue
        if brand_count[brand] >= settings.MAX_BRAND_COUNT:
            continue

        result.append(int(pid))
        brand_count[brand] += 1

        if len(result) >= settings.TOP_N:
            break

    return result

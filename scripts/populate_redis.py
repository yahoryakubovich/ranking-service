import asyncio
import os
from pathlib import Path

import pandas as pd
import redis.asyncio as aioredis

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'

INTEREST_FILE = DATA_DIR / 'interest_scores.csv'
POPULARITY_FILE = DATA_DIR / 'popularity_scores.csv'

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'


async def populate_redis():
    r = aioredis.from_url(url=REDIS_URL)

    interest_df = pd.read_csv(INTEREST_FILE)
    user_groups = interest_df.groupby('uid')

    for uid, group in user_groups:
        purchased_set = set(group.loc[group['purchase_count'] > 0, 'pid'])
        top_products = group.loc[~group['pid'].isin(purchased_set)].sort_values(
            'interest_score', ascending=False
        )

        top_zset = {str(pid): score for pid, score in zip(top_products['pid'], top_products['interest_score'][:10])}
        if top_zset:
            await r.zadd(f'user:{uid}:top_interest', top_zset)

        if purchased_set:
            await r.sadd(f'user:{uid}:purchased', *map(str, purchased_set))

    pop_df = pd.read_csv(POPULARITY_FILE)
    top_popular = pop_df.sort_values('popularity_score', ascending=False).head(20)
    await r.zadd(
        'products:top_popular',
        {str(pid): score for pid, score in zip(top_popular['pid'], top_popular['popularity_score'])}
    )

    for _, row in pop_df.iterrows():
        await r.hset('products:brand', row['pid'], row['brand'])

    await r.aclose()
    print('Redis population complete.')


if __name__ == '__main__':
    asyncio.run(populate_redis())

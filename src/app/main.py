from contextlib import asynccontextmanager  # <--- 1. Импортируем декоратор
from typing import AsyncIterator

from fastapi import FastAPI, Query, HTTPException, status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from app.application.ranker import get_ranked_products
from app.config import settings
from app.infrastructure.redis.client import init_redis, close_redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_redis(
        url=settings.redis_url,
        max_connections=20,
    )
    yield
    await close_redis()


app = FastAPI(
    title='Ranking Service',
    version='1.0',
    lifespan=lifespan,
    default_response_class=ORJSONResponse
)


class RecommendationResponse(BaseModel):
    uid: int
    products: list[int]


@app.get('/recommendations', response_model=RecommendationResponse)
async def recommend(user_id: int = Query(...)):
    products = await get_ranked_products(user_id)

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No recommendations found for user {user_id}',
        )

    resp = ORJSONResponse(
        content={'uid': user_id, 'products': products},
    )
    resp.headers['Cache-Control'] = 'public, max-age=300'
    return resp

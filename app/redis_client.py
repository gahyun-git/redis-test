from __future__ import annotations

import redis.asyncio as redis

from app.settings import settings

# 재사용 가능한 전역 Redis 클라이언트 생성
# 엔드포인트, Worker, script 등 모두 공유해서 씀
redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)

import json
from typing import Any
from .redis_client import redis_client

async def get_cached_json(key: str) -> Any | None:
    raw = await redis_client.get(key)
    if raw is None:
        return None
    return json.loads(raw)

async def set_cached_json(key: str, value: Any, ttl_seconds: int = 60) -> None:
    raw = json.dumps(value)
    await redis_client.set(key, raw, ex=ttl_seconds)
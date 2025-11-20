from __future__ import annotations

from typing import Final

from .redis_client import redis_client

# 테스트용 채널명. 추후 "jobs:created", "notifications:deployed" 등으로 사용.
CHANNEL_NAME: Final[str] = "events:test"

async def publish_message(message: str) -> int:
    # 문자열을 put/sub 채널로 발행. 반환값은 구독자수
    receivers: int = await redis_client.publish(channel=CHANNEL_NAME, message=message)
    return receivers
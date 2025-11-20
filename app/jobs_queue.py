from __future__ import annotations

from typing import Any, Final
import uuid
from app.redis_client import redis_client
from app.job_store import create_job_record
import json

JOB_QUEUE_KEY: Final[str] = "jobs:queue"

async def enqueue_job(job_type: str, payload: dict[str, Any] | None = None) -> str:
    """
    새 작업 큐에 넣기.
    LPUSH jobs:queue <job_json> 형태로 저장 후 
    생성된 job_id를 반환.
    """
    job_id = str(uuid.uuid4())

    job = {
        "id": job_id,
        "type": job_type,
        "payload": payload or {}
    }
    # dict -> json
    raw = json.dumps(job)

    # job status 생성 (status: "PENDING")
    await create_job_record(job_id, job_type, payload)

    # lpush는 리스트의 왼쪽에 요소 추가. 추후 brpop 와 조합하면 fifo 큐 처럼 사용가능
    await redis_client.lpush(JOB_QUEUE_KEY, raw)
    return job_id

async def dequeue_job_blocking(timeout: int = 0) -> dict[str, Any] | None:
    """
    큐에서 작업을 하나 꺼냄

    BRPOP jobs:queue timeout=... 를 사용하며,
    timeout=0 이면 무한 대기.
    작업이 있으면 job dict를 반환하고,
    타임아웃이면 None을 반환.
    """
    # BRPOP은 (key, value) 튜플을 반환합니다.
    # 예: ("jobs:queue", "<job_json>")
    result = await redis_client.brpop(JOB_QUEUE_KEY, timeout=timeout)

    # timeout이 0보다 크고, 그 시간 안에 아무 작업도 없으면
    # None 이 반환됩니다.
    if result is None:
        return None

    _queue_key, raw = result
    job: dict[str, Any] = json.loads(raw)

    return job
from __future__ import annotations

import json
from datetime import datetime, timezone
from app.redis_client import redis_client
from typing import Final, Any

JOB_KEY_PREFIX: Final[str] = "job:"

def _job_key(job_id: str) -> str:
    # job_id로 redis key 생성
    return f"{JOB_KEY_PREFIX}{job_id}"

def _now_iso() -> str:
    # 현재시간 ISO 8601 문자열 반환
    return datetime.now(timezone.utc).isoformat()

async def create_job_record(job_id: str, job_type: str, payload: dict[str, Any] | None = None) -> None:
    """
    new job 에 대한 기본 정보를 redis에 저장
    상태는 pending으로 시작
    """

    job = {
        "id": job_id,
        "type": job_type,
        "payload": payload or {},
        "status": "PENDING",
        "error": None,
        "create_time": _now_iso(),
        "upadate_time": _now_iso(),
    }

    raw = json.dumps(job)
    await redis_client.set(_job_key(job_id), raw)

async def update_job_status(job_id: str, status: str, error: str | None = None) -> None:
    # 기존 job의 status와 error 업데이트
    key = _job_key(job_id)
    raw = await get_job_record(key)
    if raw is None:
        return

    job: dict[str, Any] = json.loads(raw)
    job["status"] = status
    job["error"] = error
    job["update_date"] = _now_iso()

    await redis_client.set(key, json.dumps(job))

async def get_job_record(job_id: str) -> dict[str, Any] | None :
    # job_id에 해당하는 job을 redis에서 가져옴
    job = await redis_client.get(_job_key(job_id))
    if job is None:
        return
    
    return json.loads(job)


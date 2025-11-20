from fastapi import APIRouter
from pydantic import BaseModel
from app.redis_client import redis_client

from app.jobs_queue import enqueue_job

router = APIRouter(
    prefix= "/jobs",
    tags= ["/jobs"]
)

from typing import Any

class JobRequest(BaseModel):
    """
    클라이언트가 보내는 작업 요청 형태입니다.

    예시:
    {
      "type": "send_email",
      "payload": {
        "to": "user@example.com",
        "subject": "Hello",
        "body": "World"
      }
    }
    """
    type: str
    payload: dict[str, Any] | None = None


class JobResponse(BaseModel):
    """
    작업이 큐에 성공적으로 등록되었을 때의 응답 형태입니다.
    """
    job_id: str
    type: str


@router.post("", response_model=JobResponse)
async def create_job(body: JobRequest) -> JobResponse:
    # 새 작업 레디스 큐에 넣기
    job_id = await enqueue_job(body.type, body.payload)
    
    return JobResponse(
        job_id=job_id,
        type=body.type,
    )

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.redis_client import redis_client

from app.jobs_queue import enqueue_job
from app.job_store import get_job_record


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


class JobStatusResponse(BaseModel):
    """
    job status 조회 응답
    """
    id: str
    type: str
    status: str
    payload: dict[str, Any]
    error: str | None = None
    created_at: str
    updated_at: str

@router.post("", response_model=JobResponse)
async def create_job(body: JobRequest) -> JobResponse:
    # 새 작업 레디스 큐에 넣기
    job_id = await enqueue_job(body.type, body.payload)
    
    return JobResponse(
        job_id=job_id,
        type=body.type,
    )

@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job(job_id: str) -> JobStatusResponse:
    job = await get_job_record(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(
            id= job["id"],
            type= job["type"],
            status= job["status"],
            payload= job.get("payload") or {},
            error= job.get("error"),
            created_at= job.get("created_at", ""),
            updated_at= job.get("updated_at", ""),
    )
from __future__ import annotations

from typing import Any
from app.jobs_queue import dequeue_job_blocking
import asyncio
from time import sleep

async def process_job(job: dict[str, Any]) -> None:
    """
    실제 작업을 처리하는 자리입니다.
    지금은 학습용으로 단순히 출력하고, 2초간 sleep 합니다.
    """
    job_id = job.get("id")
    job_type = job.get("type")
    payload = job.get("payload")

    print(f"🚀 처리 시작 - job_id={job_id}, type={job_type}, payload={payload}")

    # 여기에서 실제로는:
    # - Git 작업
    # - LLM 호출
    # - 이메일 발송
    # - Docker 빌드
    # 등을 수행
    await asyncio.sleep(2.0)

    print(f"✅ 처리 완료 - job_id={job_id}")


async def worker_loop() -> None:
    """
    무한 루프로 Redis 큐에서 작업을 꺼내 처리하는 워커 루프입니다.
    """
    print("👷 Worker 시작: Redis 큐에서 작업을 기다립니다...")
    
    while True:
        job = await dequeue_job_blocking(timeout=0)

        if job is None:
            continue
        
        try:
            await process_job(job)
        except Exception as exc:
            print(f"❌ 작업 처리 중 예외 발생: {exc!r}")

def main() -> None:
    asyncio.run(worker_loop())

if __name__ == "__main__":
    main()
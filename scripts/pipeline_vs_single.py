import asyncio
import time
from app.redis_client import redis_client

TOTAL = 10_000

async def set_without_pipeline() -> None:
    # 파이프라인없이 키 하나씩 SET
    start = time.time()

    for i in range(TOTAL):
        key = f"bench:no_pipeline: {i}"
        value = f"value-{i}"

        await redis_client.set(key, value)
    
    elapsed = time.time() - start
    print(f"NO PIPE LINE {TOTAL}개 SET: {elapsed:.4f}초")


async def set_with_pipteline(batch_size: int = 1000) -> None:
    # 여러세트를 파이프라인으로 묶어서 전송

    start = time.time()

    pipe = redis_client.pipeline()
    count_in_batch = 0

    for i in range(TOTAL):
        key = f"bench:pipeline:{i}"
        value = f"value-{i}"

        # 파이프라인에 명령 쌓아두고 바로보내진 않음
        pipe.set(key, value)
        count_in_batch += 1

        # batch_size씩 모았다가 한번에 실행
        if count_in_batch >= batch_size:
            await pipe.execute()
            count_in_batch = 0

    # 남은거 있으면 ㄱㄱ
    if count_in_batch > 0:
        await pipe.execute()
    
    elapsed = time.time() - start
    print(f"PIPELINE {TOTAL}개 SET (batch={batch_size}): {elapsed:.4f}초")

async def main() -> None:
    print("=====파이프라인 vs 단일 SET 성능비교\n")
    await set_without_pipeline()
    await set_with_pipteline()

if __name__ == "__main__":
    asyncio.run(main())
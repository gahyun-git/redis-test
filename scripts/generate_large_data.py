import asyncio
import json
import time
import redis.asyncio as redis

TOTAL_KEYS = 1_000_000
BATCH_SIZE = 5000

async def main():
    r = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True,
    )

    # 총 몇 개 키를 넣는지 출력
    print(f"Generating {TOTAL_KEYS} keys into Redis...")

    start = time.time()
    pipe = r.pipeline()

    for i in range(TOTAL_KEYS):
        # 키/값을 올바른 문자열로 생성
        key = f"user:{i}"
        value = {
            "id": i,
            "name": f"User-{i}",
            "email": f"user{i}@example.com",
            "score": i % 1000,
        }

        pipe.set(key, json.dumps(value))

        # 배치 단위로 pipeline 실행
        if i % BATCH_SIZE == 0:
            await pipe.execute()

    # 남은 것 마지막으로 flush
    await pipe.execute()

    elapsed = time.time() - start
    print(f"Done. Inserted {TOTAL_KEYS} keys in {elapsed:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
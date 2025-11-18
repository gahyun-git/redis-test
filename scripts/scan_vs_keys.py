import asyncio
import time


from app.redis_client import redis_client

async def run_key_test(pattern: str) -> None:
    # Keys로 패턴에 맞는 모든 키 한번에 조회
    print(f"KEYS 테스트 시작: patter={pattern!r}")
    start = time.time()

    # keys 는 한번에 모든 키 다 뒤짐. 키 많을수록 무거움
    keys = await redis_client.keys(pattern)

    elapsed = time.time() - start
    print(f"KEY 결과: {len(keys)}개, 소요시간: {elapsed:.4f}초\n")

async def run_scan_test(pattern: str, count: int = 1000) -> None:
    # scan_iter로 패턴에 맞는키 나눠서 조회
    print(f"SCAN_ITER테스트 시작: pattern={pattern!r}, count={count}")

    start = time.time()
    found = 0

    async for key in redis_client.scan_iter(match=pattern, count=count):
        found += 1
        # 키사용은 하지않고 카운팅만

    elapsed = time.time() - start
    print(f"SCAN_ITER 결과: {len(key)}개, 소요시간: {elapsed:.4f}초\n")


async def main() -> None:
    pattern = "user:*"

    print("===== 성능 비교 =====\n")
    await run_key_test(pattern)
    await run_scan_test(pattern)


if __name__ == "__main__":
    asyncio.run(main())


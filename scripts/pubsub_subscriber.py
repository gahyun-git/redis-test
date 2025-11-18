# 메세지 받는 역할.
import asyncio

from app.redis_client import redis_client as client

CHANNEL_NAME = "events:test"

async def run_subscriber() -> None:
    # redis pub/sub 구독 & 들어오는 메세지 출력.
    
    # pub/sub 전용 커넥트 객체
    pubsub = client.pubsub()

    # 특정채널 구독. subbscribe() 호출하면 해당 채널로 들어오는 메세지 받을수있음
    await pubsub.subscribe(CHANNEL_NAME)

    print(f"subscribed to channel: {CHANNEL_NAME!r}")
    print("메세지 기다리는중 ... ctrl + c 로 종료\n")

    # pubsub.listen()은 async generator임. 게속해서 새로운 메세지 yield함
    async for message in pubsub.listen():
        # message 는 dict 형태
        # type에 따라 subscribe, message 등 종류 나뉨
        msg_type = message.get("type")

        if msg_type == "subscribe":
            # 처음 subscribe 할때 한 번 들어오는 컨트롤 메세지
            print(f"Subscribed confirmation: {message}")
            continue

        if msg_type == "message":
            channel = message.get("channel")
            data = message.get("data")
            print(f"[채널: {channel}] 받은메세지: {data!r}")

async def main() -> None:
    try:
        await run_subscriber()
    except asyncio.CancelledError:
        # 종료 시 정리용
        pass


if __name__ == "__main__":
    asyncio.run(main())

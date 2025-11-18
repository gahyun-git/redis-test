# 메세지 보내는 역할

import asyncio
from app.redis_client import redis_client as client

CHANNEL_NAME = "events:test"    # sub 과 동일할 채널명 사용

async def publish_message(message: str) -> None:
    # 문자열 메세지를 redis pub/sub 채널로 발행.
    # publish(channel, message)는 해당 채널 구독중인 모든 구독자에게 메세지 브로드캐스팅
    receivers = await client.publish(CHANNEL_NAME, message)
    print(f"보낸메세지: {message!r} (받은 구독자 수:{receivers})")

async def interactive_loop() -> None:
    # 터미널입력받아서 입력한 내용을 채널로 pub
    print(f"Redis Pub/Sub Publisher (channel={CHANNEL_NAME!r})")
    print("메세지를 입력하면 발행됩니다. 'quit'입력시 종료\n")
    
    loop = asyncio.get_running_loop()

    while True:
        # input()은 blocking 이라 그대로 쓰면 이벤트루프 멈춤
        # 그래서 asyncio.to_thread로 별도 스레드에서 input 받게 해야함
        user_input = await asyncio.to_thread(input, "Message> ")

        if user_input.strip().lower() in ("quit", "exit"):
            print("종료")
            break

        if not user_input.strip():
            continue

        await publish_message(user_input)

async def main() -> None:
    await interactive_loop()

if __name__ == "__main__":
    asyncio.run(main())
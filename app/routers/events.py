from fastapi import APIRouter
from pydantic import BaseModel

from app.pubsub import publish_message

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

class PublishRequest(BaseModel):
    """ 
    클라이언트에서 보낼 요청 바디
    {
        "message": "Hello World"
    }
    """
    message: str

@router.post("/publish")
async def publish_event(body: PublishRequest):
    # 요청 바디로 받은 메세지를 redis pub/sub 채널로 발행
    receivers = await publish_message(body.message)

    return {
        "ok": True,
        "channel": "events:test",
        "message": body.message,
        "receivers": receivers,
    }
    
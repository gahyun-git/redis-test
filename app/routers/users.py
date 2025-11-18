from fastapi import APIRouter
from ..cache import get_cached_json, set_cached_json

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 테스트용 가짜DB 함수.
async def fetch_user_from_db(user_id: str) -> dict:
    return {
        "id": user_id,
        "name": f"user-{user_id}",
        "email": f"user{user_id}@example.com"
    }

# 캐시 -> db -> 캐시 저장 흐름
@router.get("/{user_id}")
async def get_user(user_id:str):
    """
    redis 캐시 조회
    없으면 db 조회
    db 결과 redis에 ttl과 함께 저장
    데이터 반환
    """

    cache_key = f"user:{user_id}"

    # 1. 캐시 조회
    cached = await get_cached_json(cache_key)
    if cached is not None:
        return {
            "source": "cache", # 어디서 가져온건지 확인용
            "data": cached
        }        
    
    # 2. 캐시 미스 -> DB 조회
    user = await fetch_user_from_db(user_id)

    # 3. 캐시에 TTL 60초로 저장
    await set_cached_json(cache_key, user, ttl_seconds=60)

    return {
        "source": "db",
        "data": user,
    }
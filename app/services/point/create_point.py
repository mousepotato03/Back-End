from fastapi import HTTPException
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_point_log(user_id: UUID, point: int):
    """
    point_log 테이블에 새로운 로그를 추가합니다.

    params:
        user_id (UUID): 사용자 ID
        point (int): 포인트 값

    Returns:
        dict: 생성 결과 메시지
    """
    try:

        data = {
            "user_id": str(user_id),
            "point": point,
        }

        response = (
            supabase
            .table("point_log")
            .insert(data)
            .execute()
        )
        if response.data:
            return {"message": "포인트 로그가 성공적으로 추가되었습니다.", "log": response.data[0]}
        else:
            raise HTTPException(status_code=500, detail="포인트 로그 추가에 실패했습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

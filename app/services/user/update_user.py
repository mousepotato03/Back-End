from fastapi import HTTPException
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def update_user_info(user_id: UUID, user_data: dict):
    """
    user_id로 유저 정보를 수정하는 함수입니다. profiles 테이블에서 해당 id의 row를 업데이트합니다.
    """
    try:
        response = (
            supabase
            .table("profiles")
            .update(user_data)
            .eq("id", str(user_id))
            .execute()
        )
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=404, detail="해당 user를 찾을 수 없습니다.")
        return {"user": response.data[0] if isinstance(response.data, list) else response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

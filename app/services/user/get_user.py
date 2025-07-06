from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_info(user_id: int):
    """
    user_id로 유저 정보를 조회하는 함수입니다. profiles 테이블에서 해당 id의 row를 가져옵니다.
    """
    try:
        response = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB 조회 중 오류가 발생했습니다.")
        user = response.data
        if not user:
            raise HTTPException(status_code=404, detail="해당 user를 찾을 수 없습니다.")
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

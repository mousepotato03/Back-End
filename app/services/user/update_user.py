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
        update_response = (
            supabase
            .table("profiles")
            .update(user_data)
            .eq("id", str(user_id))
            .execute()
        )
        if not update_response.data or len(update_response.data) == 0:
            raise HTTPException(status_code=500, detail="유저 수정에 실패했습니다.")

        # 생성된 유저의 ID 추출
        updated_user_id = update_response.data[0]["id"]
        
        # 2단계: 별도 SELECT 쿼리로 프로필 정보와 함께 조회
        select_response = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", updated_user_id)
            .execute()
        )
        
        if not select_response.data or len(select_response.data) == 0:
            raise HTTPException(status_code=500, detail="수정된 유저 조회에 실패했습니다.")

        updated_user = select_response.data[0]
        
        # 생성된 user 데이터 반환
        return {"user": updated_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

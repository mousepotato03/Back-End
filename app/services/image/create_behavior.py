from fastapi import HTTPException, Body
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_user_behavior(
    user_id: UUID = Body(..., embed=True),
    content: str = Body(..., embed=True)
):
    """
    suggest_behavior 테이블에 새로운 행동 제안을 생성하는 API입니다.
    """
    try:
        # 행동 제안 데이터 준비
        behavior_data = {
            "user_id": user_id,
            "content": content
        }
            
        response = (
            supabase
            .table("suggest_behavior")
            .insert(behavior_data)
            .execute()
        )
        
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=500, detail="행동 제안 생성에 실패했습니다.")
        return {"behavior": response.data[0] if isinstance(response.data, list) else response.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

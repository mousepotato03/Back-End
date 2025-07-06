from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from app.core.config import get_supabase_config

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post("/suggest_behavior", response_class=JSONResponse)
async def create_suggest_behavior(
    user_id: int = Body(..., embed=True),
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
        
        if response.error:
            raise HTTPException(status_code=500, detail="DB 생성 중 오류가 발생했습니다.")
        
        created_behavior = response.data[0] if response.data else None
        if not created_behavior:
            raise HTTPException(status_code=500, detail="행동 제안 생성에 실패했습니다.")
            
        return {"message": "행동 제안이 성공적으로 생성되었습니다.", "behavior": created_behavior}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

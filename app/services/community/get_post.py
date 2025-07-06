from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from app.core.config import get_supabase_config

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.get("/posts", response_class=JSONResponse)
async def get_posts():
    try:
        # posts 테이블에서 10개의 row를 가져옴
        response = (
            supabase
            .table("posts")
            .select("*")
            .limit(10)
            .order("created_at", desc=True)
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB 조회 중 오류가 발생했습니다.")
        posts = response.data
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

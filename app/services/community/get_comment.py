from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from app.core.config import get_supabase_config

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


#TODO eq 문장에 post_id도 반영하기
@router.get("posts/{post_id}/comments/{post_id}", response_class=JSONResponse)
async def get_comments(post_id: int):
    """
    특정 post_id에 해당하는 comment들을 가져오는 API입니다.
    """
    try:
        response = (
            supabase
            .table("comments")
            .select("*")
            .eq("post_id", post_id)
            .order("created_at", desc=False)
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB 조회 중 오류가 발생했습니다.")
        comments = response.data
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

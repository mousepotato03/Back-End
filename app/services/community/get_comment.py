from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_comments(post_id: int):
    """
    특정 post_id에 해당하는 comment들을 가져오는 API입니다.
    params:
        post_id: int(required)
    """
    try:
        if not post_id:
            raise HTTPException(status_code=400, detail="post_id는 필수입니다.")
        response = (
            supabase
            .table("comments")
            .select("*")
            .eq("post_id", post_id)
            .order("created_at", desc=True)
            .execute()
        )
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=500, detail="DB 조회 중 오류가 발생했습니다.")
        comments = response.data
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

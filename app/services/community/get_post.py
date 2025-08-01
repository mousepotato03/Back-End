from fastapi import HTTPException
from supabase import create_client, Client
from typing import Optional
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_posts(offset: int, user_id: Optional[str] = None):
    """
    posts 테이블에서 10개의 게시글을 가져오는 함수입니다.
    pagination을 위해 range를 사용합니다.
    params:
        offset: int(required)
        user_id: str(optional) - 특정 사용자의 게시글만 가져올 때 사용
    """
    # posts 테이블에서 10개의 row를 가져옴
    if offset is None:
        raise HTTPException(status_code=400, detail="offset는 필수입니다.")
    try:
        limit = offset + 10
        query = (
            supabase
            .table("posts")
            .select("*, profiles!posts_user_id_fkey(user_img, username)")
        )
        
        # user_id가 제공된 경우 해당 사용자의 게시글만 필터링
        if user_id:
            query = query.eq("user_id", user_id)
            
        response = (
            query
            .range(offset, limit-1)  # range는 시작과 끝 인덱스를 포함
            .order("created_at", desc=True)
            .execute()
        )
        
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            return {"posts": []}
        posts = response.data
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

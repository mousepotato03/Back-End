from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config
from typing import List

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_liked_post_ids(user_id: str, post_ids: List[int]):
    """
    user_id가 post_ids 중 어떤 게시글에 좋아요를 눌렀는지 반환
    """
    if not user_id or not post_ids:
        raise HTTPException(status_code=400, detail="user_id, post_ids는 필수입니다.")
    try:
        # in_ 연산자 사용
        response = (
            supabase
            .table("likes")
            .select("post_id")
            .eq("user_id", user_id)
            .in_("post_id", post_ids)
            .execute()
        )
        liked_post_ids = [row["post_id"] for row in response.data] if response.data else []
        return {"liked_post_ids": liked_post_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"좋아요 조회 중 오류: {str(e)}")
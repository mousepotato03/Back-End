from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_like(post_id: int, user_id: str):
    """
    특정 게시글에 좋아요를 추가합니다.
    params:
        post_id: int(required)
        user_id: str(UUID, required)
    """
    if not post_id or not user_id:
        raise HTTPException(status_code=400, detail="post_id, user_id는 필수입니다.")
    try:
        # 이미 좋아요가 있는지 확인
        existing = (
            supabase
            .table("likes")
            .select("id")
            .eq("post_id", post_id)
            .eq("user_id", user_id)
            .execute()
        )
        if existing.data and len(existing.data) > 0:
            raise HTTPException(status_code=400, detail="이미 좋아요를 누른 상태입니다.")

        # 좋아요 추가
        new_like = {
            "post_id": post_id,
            "user_id": user_id
        }
        insert_response = (
            supabase
            .table("likes")
            .insert(new_like)
            .execute()
        )
        if not insert_response.data or len(insert_response.data) == 0:
            raise HTTPException(status_code=500, detail="좋아요 추가에 실패했습니다.")
        return {"like": insert_response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"좋아요 추가 중 오류가 발생했습니다: {str(e)}")

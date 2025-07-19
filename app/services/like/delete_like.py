from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def delete_like(post_id: int, user_id: str):
    """
    특정 게시글에서 사용자의 좋아요를 삭제합니다.
    params:
        post_id: int(required)
        user_id: str(UUID, required)
    """
    if not post_id or not user_id:
        raise HTTPException(status_code=400, detail="post_id, user_id는 필수입니다.")
    try:
        response = (
            supabase
            .table("likes")
            .delete()
            .eq("post_id", post_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="좋아요를 찾을 수 없습니다.")
        return {"message": "좋아요가 성공적으로 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"좋아요 삭제 중 오류가 발생했습니다: {str(e)}")

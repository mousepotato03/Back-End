from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
async def delete_post(post_id: int):
    """
    post_id로 게시글을 삭제하는 API입니다. posts 테이블에서 해당 id의 row를 삭제합니다.

    params:
        post_id: int(required)
    """
    if not post_id:
        raise HTTPException(status_code=400, detail="post_id는 필수입니다.")
    try:
        response = (
            supabase
            .table("posts")
            .delete()
            .eq("id", post_id)
            .execute()
        )
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=404, detail="해당 게시글을 찾을 수 없습니다.")
        return {"message": "게시글이 성공적으로 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


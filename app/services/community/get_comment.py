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
    if not post_id:
        raise HTTPException(status_code=400, detail="post_id는 필수입니다.")
    try:
        # 먼저 post가 존재하는지 확인
        post_response = (
            supabase
            .table("posts")
            .select("id")
            .eq("id", post_id)
            .execute()
        )
        
        if not post_response.data or len(post_response.data) == 0:
            raise HTTPException(status_code=404, detail="해당 게시글을 찾을 수 없습니다.")
        
        # 댓글 조회
        response = (
            supabase
            .table("comments")
            .select("*, profiles!posts_user_id_fkey(user_img, username)")
            .eq("post_id", post_id)
            .order("created_at", desc=True)
            .execute()
        )
        
        comments = response.data if response.data else []
        return {"comments": comments}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

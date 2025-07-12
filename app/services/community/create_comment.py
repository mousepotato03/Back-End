from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_comment(post_id: int, comment_data: dict):
    """ 
    특정 게시글에 새로운 댓글을 생성하는 API입니다.
    params:
        post_id: int(required)
        user_id: str(required)
        content: str(required)
    """
    if not post_id or not comment_data["user_id"] or not comment_data["content"]:
        raise HTTPException(status_code=400, detail="post_id, user_id, content는 필수입니다.")
    try:
        # 댓글 데이터 준비
        new_comment_data = {
            "post_id": post_id,
            "user_id": comment_data["user_id"],
            "content": comment_data["content"],
        }
            
        response = (
            supabase
            .table("comments")
            .insert(new_comment_data)
            .select("*, profiles!posts_user_id_fkey(user_img, username)")
            .execute()
        )
        
        # response 데이터 검증
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="댓글 생성에 실패했습니다.")

        created_comment = response.data[0]
        
        # 생성된 comment 데이터 반환 (get_comment와 동일한 형식)
        return {"comment": created_comment}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"댓글 작성 중 오류가 발생했습니다: {str(e)}") 
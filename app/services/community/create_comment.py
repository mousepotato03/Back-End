from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config
# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
async def create_comment(comment_data: dict):
    """ 
    특정 게시글에 새로운 댓글을 생성하는 API입니다.
    params:
        post_id: int(required)
        user_id: int(required)
        content: str(required)
    """
    try:
        if not comment_data["post_id"] or not comment_data["user_id"] or not comment_data["content"]:
            raise HTTPException(status_code=400, detail="post_id, user_id, content는 필수입니다.")

        # 댓글 데이터 준비
        comment_data = {
            "post_id": comment_data["post_id"],
            "user_id": comment_data["user_id"],
            "content": comment_data["content"],
        }
            
        response = (
            supabase
            .table("comments")
            .insert(comment_data)
            .execute()
        )
        
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=500, detail="댓글 생성에 실패했습니다.")
        
        return {"comment": response.data[0] if isinstance(response.data, list) else response.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
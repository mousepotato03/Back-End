from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config
# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
async def create_comment(
    post_id: int,
    user_id: int,
    content: str
):
    """
    특정 게시글에 새로운 댓글을 생성하는 API입니다.
    params:
        post_id: int(required)
        user_id: int(required)
        content: str(required)
    """
    try:
        if not post_id or not user_id or not content:
            raise HTTPException(status_code=400, detail="post_id, user_id, content는 필수입니다.")

        # 댓글 데이터 준비
        comment_data = {
            "post_id": post_id,
            "user_id": user_id,
            "content": content,
        }
            
        response = (
            supabase
            .table("comments")
            .insert(comment_data)
            .execute()
        )
        
        if response.error:
            raise HTTPException(status_code=500, detail="DB 생성 중 오류가 발생했습니다.")
        
        created_comment = response.data[0] if response.data else None
        if not created_comment:
            raise HTTPException(status_code=500, detail="댓글 생성에 실패했습니다.")
            
        return {"message": "댓글이 성공적으로 생성되었습니다.", "comment": created_comment}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
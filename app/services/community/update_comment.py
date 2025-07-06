from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def update_comment(comment_id: int, content: str):
    """
    comment_id에 해당하는 댓글의 내용을 수정하는 API입니다.
    params:
        comment_id: int(required)
        content: str(required)
    """
    try:
        if not comment_id or not content:
            raise HTTPException(status_code=400, detail="comment_id와 content는 필수입니다.")
        response = (
            supabase
            .table("comments")
            .update({"content": content})
            .eq("id", comment_id)
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB 수정 중 오류가 발생했습니다.")
        if response.count == 0:
            raise HTTPException(status_code=404, detail="해당 댓글을 찾을 수 없습니다.")
        return {"message": "댓글이 성공적으로 수정되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def delete_comment(post_id: int, comment_id: int):
    """
    comment_id로 댓글을 삭제하는 API입니다. comments 테이블에서 해당 id의 row를 삭제합니다.
    params: 
        comment_id: int(required)
    """
    if not comment_id:
        raise HTTPException(status_code=400, detail="comment_id는 필수입니다.")
    try:
        response = (
            supabase
            .table("comments")
            .delete()
            .eq("id", comment_id)
            .execute()
        )
        
        # response 데이터 검증 및 처리
        if not response.data:
            raise HTTPException(status_code=404, detail="해당 댓글을 찾을 수 없습니다.")
        
        # 데이터가 리스트인지 확인
        if isinstance(response.data, list):
            if len(response.data) == 0:
                raise HTTPException(status_code=404, detail="해당 댓글을 찾을 수 없습니다.")
        
        return {"message": "댓글이 성공적으로 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"댓글 삭제 중 오류가 발생했습니다: {str(e)}")

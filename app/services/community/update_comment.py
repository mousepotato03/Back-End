from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def update_comment(post_id: int, comment_id: int, content: str):
    """
    comment_id에 해당하는 댓글의 내용을 수정하는 API입니다.
    params:
        comment_id: int(required)
        content: str(required)
    """
    if not comment_id or not content:
        raise HTTPException(status_code=400, detail="comment_id와 content는 필수입니다.")
    try:
        # 1단계: UPDATE만 실행
        update_response = (
            supabase
            .table("comments")
            .update({"content": content})
            .eq("id", comment_id)
            .execute()
        )
        
        # response 데이터 검증
        if not update_response.data or len(update_response.data) == 0:
            raise HTTPException(status_code=404, detail="해당 댓글을 찾을 수 없습니다.")
        
        # 2단계: 별도 SELECT 쿼리로 프로필 정보와 함께 조회
        select_response = (
            supabase
            .table("comments")
            .select("*, profiles!comment_user_id_fkey(user_img, username)")
            .eq("id", comment_id)
            .execute()
        )
        
        if not select_response.data or len(select_response.data) == 0:
            raise HTTPException(status_code=500, detail="수정된 댓글 조회에 실패했습니다.")
        
        # 수정된 comment 데이터 반환 (get_comment와 동일한 형식)
        updated_comment = select_response.data[0]
        return {"comment": updated_comment}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"댓글 수정 중 오류가 발생했습니다: {str(e)}")

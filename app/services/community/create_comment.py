from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from app.core.config import get_supabase_config
from datetime import datetime, timezone

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post("/posts/{post_id}/comments", response_class=JSONResponse)
async def create_comment(
    post_id: int,
    user_id: int = Body(..., embed=True),
    content: str = Body(..., embed=True)
):
    """
    특정 게시글에 새로운 댓글을 생성하는 API입니다.
    """
    try:
        # 현재 시간을 created_at으로 설정
        current_time = datetime.now(timezone.utc).isoformat()
        
        # 댓글 데이터 준비
        comment_data = {
            "post_id": post_id,
            "user_id": user_id,
            "content": content,
            # "created_at": current_time,
            # "updated_at": current_time
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
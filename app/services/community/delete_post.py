from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from app.core.config import get_supabase_config

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.delete("/posts/{post_id}", response_class=JSONResponse)
async def delete_post(post_id: int):
    """
    post_id로 게시글을 삭제하는 API입니다. posts 테이블에서 해당 id의 row를 삭제합니다.
    """
    try:
        response = (
            supabase
            .table("posts")
            .delete()
            .eq("id", post_id) 
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB 삭제 중 오류가 발생했습니다.")
        if response.count == 0:
            raise HTTPException(status_code=404, detail="해당 게시글을 찾을 수 없습니다.")
        return {"message": "게시글이 성공적으로 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


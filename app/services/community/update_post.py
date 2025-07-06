from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from app.core.config import get_supabase_config

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.put("/posts/{post_id}", response_class=JSONResponse)
async def update_post(
    post_id: int,
    content: str = Body(..., embed=True),
    image_url: str = Body(..., embed=True)
):
    """
    기존 post의 content와 image_url만 수정하는 API입니다.
    """
    try:
        response = (
            supabase
            .table("posts")
            .update({"content": content, "image_url": image_url})
            .eq("id", post_id)
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB 수정 중 오류가 발생했습니다.")
        updated_post = response.data
        if not updated_post:
            raise HTTPException(status_code=404, detail="해당 post를 찾을 수 없습니다.")
        return {"updated_post": updated_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

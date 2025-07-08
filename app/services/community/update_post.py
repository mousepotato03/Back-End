from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def update_post(
    post_id: int,
    post_data: dict
):
    """
    기존 post의 title, content, image_url만 수정하는 API입니다.

    params:
        post_id: int(required)
        post_data: dict(required)
          required: title, content
          optional: image_url
    """
    if "title" not in post_data or "content" not in post_data:
        raise HTTPException(status_code=400, detail="title과 content는 필수입니다.")
    
    try:
        update_data = {
            "title": post_data["title"],
            "content": post_data["content"],
            "image_url": post_data["image_url"]
        }
        response = (
            supabase
            .table("posts")
            .update(update_data)
            .eq("id", post_id)
            .execute()
        )
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=404, detail="해당 post를 찾을 수 없습니다.")
        return {"post": response.data[0] if isinstance(response.data, list) else response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

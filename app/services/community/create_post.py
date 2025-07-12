from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_post(post_data: dict):
    """
    새로운 게시글을 생성하는 함수입니다.
    
    params:
        post_data (dict): 
          required: user_id, title, content
          optional: image_url
    """
     # 필수 필드 검증
    if "user_id" not in post_data or "title" not in post_data or "content" not in post_data:
        raise HTTPException(status_code=400, detail="user_id와 content는 필수입니다.")
    try:
        # 게시글 데이터 준비
        insert_data = {
            "title": post_data["title"],
            "user_id": post_data["user_id"],
            "content": post_data["content"],
        }
        
        # 선택적 필드들 추가
        if "image_url" in post_data:
            insert_data["image_url"] = post_data["image_url"]
            
        response = (
            supabase
            .table("posts")
            .insert(insert_data)
            .select("*, profiles!posts_user_id_fkey(user_img, username)")
            .execute()
        )
        
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=500, detail="게시글 생성에 실패했습니다.")
        
        # 생성된 post 데이터 반환 (get_post와 동일한 형식)
        created_post = response.data[0] if isinstance(response.data, list) else response.data
        return {"post": created_post}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from app.core.config import get_supabase_config
from datetime import datetime, timezone

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post("/posts", response_class=JSONResponse)
async def create_post(
    user_id: int = Body(..., embed=True),
    content: str = Body(..., embed=True),
    image_url: str = Body(None, embed=True),
    title: str = Body(None, embed=True)
):
    """
    새로운 게시글을 생성하는 API입니다.
    """
    try:
        # 현재 시간을 created_at으로 설정
        current_time = datetime.now(timezone.utc).isoformat()
        
        # 게시글 데이터 준비
        post_data = {
            "user_id": user_id,
            "content": content,
            "title": title,
            # "created_at": current_time,
            # "updated_at": current_time
        }
        
        # 선택적 필드들 추가
        if image_url:
            post_data["image_url"] = image_url
            
        response = (
            supabase
            .table("posts")
            .insert(post_data)
            .execute()
        )
        
        if response.error:
            raise HTTPException(status_code=500, detail="DB 생성 중 오류가 발생했습니다.")
        
        created_post = response.data[0] if response.data else None
        if not created_post:
            raise HTTPException(status_code=500, detail="게시글 생성에 실패했습니다.")
            
        return {"message": "게시글이 성공적으로 생성되었습니다.", "post": created_post}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
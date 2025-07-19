from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List
from app.services.like.create_like import create_like
from app.services.like.delete_like import delete_like
from app.services.like.get_like import get_liked_post_ids

router = APIRouter()

@router.post("/like")
async def create_like_endpoint(post_id: int, user_id: UUID):
    """
    특정 게시글에 좋아요를 추가합니다.
    """
    try:
        return await create_like(post_id, str(user_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/like")
async def delete_like_endpoint(post_id: int, user_id: UUID):
    """
    특정 게시글에서 사용자의 좋아요를 삭제합니다.
    """
    try:
        return await delete_like(post_id, str(user_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/like")
async def get_liked_post_ids_endpoint(user_id: UUID, post_ids: List[int]):
    """
    user_id가 post_ids 중 어떤 게시글에 좋아요를 눌렀는지 반환합니다.
    """
    try:
        return await get_liked_post_ids(str(user_id), post_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# update 는 없어도 되므로 추가 안함
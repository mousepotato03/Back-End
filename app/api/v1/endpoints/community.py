from fastapi import APIRouter, HTTPException
from app.services.community.get_post import get_posts
from app.services.community.create_post import create_post
from app.services.community.update_post import update_post
from app.services.community.delete_post import delete_post

from app.services.community.get_comment import get_comments
from app.services.community.create_comment import create_comment
from app.services.community.update_comment import update_comment
from app.services.community.delete_comment import delete_comment

router = APIRouter()

# -------------------------
# --- START: 게시글 API ---
# -------------------------
@router.get("/posts")
async def get_community_posts(offset: int):
    """
    커뮤니티 게시글 목록을 가져옵니다.
    """
    try:
        return await get_posts(offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/posts")
async def create_community_post(post_data: dict):
    """
    새로운 커뮤니티 게시글을 생성합니다.
    """
    try:
        return await create_post(post_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/posts/{post_id}")
async def update_community_post(post_id: int, post_data: dict):
    """
    커뮤니티 게시글을 수정합니다.
    """
    try:
        return await update_post(post_id, post_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/posts/{post_id}")
async def delete_community_post(post_id: int):
    """
    커뮤니티 게시글을 삭제합니다.
    """
    try:
        return await delete_post(post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# -----------------------
# --- END: 게시글 API ---
# -----------------------

# -----------------------
# --- START: 댓글 API ---
# -----------------------
@router.get("/posts/{post_id}/comments")
async def get_post_comments(post_id: int):
    """
    특정 게시글의 댓글 목록을 가져옵니다.
    """
    try:
        return await get_comments(post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/posts/{post_id}/comments")
async def create_post_comment(post_id: int, comment_data: dict):
    """
    특정 게시글에 새로운 댓글을 생성합니다.
    """
    try:
        return await create_comment(post_id, comment_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/posts/{post_id}/comments/{comment_id}")
async def update_post_comment(post_id: int, comment_id: int, comment_data: str):
    """
    댓글을 수정합니다.
    """
    try:
        return await update_comment(post_id, comment_id, comment_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/posts/{post_id}/comments/{comment_id}")
async def delete_post_comment(post_id: int, comment_id: int):
    """
    댓글을 삭제합니다.
    """
    try:
        return await delete_comment(post_id, comment_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------
# --- END: 댓글 API ---
# ---------------------
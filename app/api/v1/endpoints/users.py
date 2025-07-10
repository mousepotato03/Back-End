from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.services.user.get_user import get_user_info
from app.services.user.update_user import update_user_info
from app.services.user.delete_user import delete_user_info
from app.services.user.create_users import create_user

router = APIRouter()

@router.post("/{user_id}")
async def create_user(user_data: dict):
    """
    새로운 사용자를 생성합니다.
    """
    try:
        return await create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: UUID):
    """
    특정 사용자의 정보를 가져옵니다.
    """
    try:
        return await get_user_info(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}")
async def update_user(user_id: UUID, user_data: dict):
    """
    사용자 정보를 수정합니다.
    """
    try:
        return await update_user_info(user_id, user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    """
    사용자를 삭제합니다.
    """
    try:
        return await delete_user_info(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
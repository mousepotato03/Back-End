from fastapi import APIRouter
from app.services.user.get_user import get_user_info
from app.services.user.update_user import update_user_info
from app.services.user.delete_user import delete_user_info

router = APIRouter()

@router.get("/login")
def login(user_id: str):
    return get_user_info(user_id)
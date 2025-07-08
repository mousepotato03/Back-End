from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config


# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def delete_user_info(user_id: UUID):
    """
    user_id로 유저를 삭제하는 API입니다. profiles 테이블에서 해당 id의 row를 삭제합니다.
    """
    try:
        response = (
            supabase
            .table("profiles")
            .delete()
            .eq("id", str(user_id))
            .execute()
        )
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=404, detail="해당 user를 찾을 수 없습니다.")
        return {"message": "유저가 성공적으로 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import os
from supabase import create_client, Client

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.put("/users/{user_id}", response_class=JSONResponse)
async def update_user_info(user_id: int, user_data: dict):
    """
    user_id로 유저 정보를 업데이트하는 API입니다. profiles 테이블에서 해당 id의 row를 수정합니다.
    user_data는 업데이트할 필드와 값을 포함해야 합니다.
    """
    try:
        response = (
            supabase
            .table("profiles")
            .update(user_data)
            .eq("id", user_id)
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB 업데이트 중 오류가 발생했습니다.")
        if response.count == 0:
            raise HTTPException(status_code=404, detail="해당 user를 찾을 수 없습니다.")
        return {"message": "유저 정보가 성공적으로 업데이트되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import HTTPException
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def update_character(user_id: UUID, character_data: dict):
  try:
    response = (
      supabase
      .table("characters")
      .update(character_data)
      .eq("user_id", str(user_id))
      .execute()
    )
    return {"message": "캐릭터 정보가 성공적으로 업데이트되었습니다."}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
 
from fastapi import HTTPException
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_character_info(user_id: UUID):
  try:
    response = (
      supabase
      .table("characters")
      .select("*")
      .eq("user_id", str(user_id))
      .single()
      .execute()
    )
    if not response.data:
      raise HTTPException(status_code=404, detail="해당 캐릭터를 찾을 수 없습니다.")
    character = response.data
    return {"character": character}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e)) 
from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def create_user(user_data: dict):
    """
    Supabase Oauth(구글 로그인)로 발급된 users 테이블의 uuid를 받아
    profiles 테이블에 새로운 유저를 추가하는 API입니다.
    user_data에는 최소한 'id'(uuid) 필드가 포함되어야 하며, 추가로 필요한 프로필 정보도 포함할 수 있습니다.
    """
    try:
        # id 필드가 없으면 에러 반환
        if "id" not in user_data:
            raise HTTPException(status_code=400, detail="user_data에 'id'(uuid) 필드가 필요합니다.")

        # 이미 해당 id로 등록된 프로필이 있는지 확인
        exist_check = (
            supabase
            .table("profiles")
            .select("id")
            .eq("id", user_data["id"])
            .single()
            .execute()
        )
        if exist_check.data:
            raise HTTPException(status_code=409, detail="이미 해당 uuid로 등록된 프로필이 존재합니다.")

        # profiles 테이블에 유저 추가
        response = (
            supabase
            .table("profiles")
            .insert(user_data)
            .execute()
        )
        if response.error:
            raise HTTPException(status_code=500, detail="DB에 유저 추가 중 오류가 발생했습니다.")

        return {"message": "유저가 성공적으로 생성되었습니다.", "user": response.data[0]}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

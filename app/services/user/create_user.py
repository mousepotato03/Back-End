from fastapi import HTTPException
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def create_user_info(user_data: dict):
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
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=500, detail="유저 생성에 실패했습니다.")
        # 생성된 유저의 ID 추출
        created_user_id = response.data[0]["id"]
        
        # 2단계: 별도 SELECT 쿼리로 프로필 정보와 함께 조회
        select_response = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", created_user_id)
            .execute()
        )
        
        if not select_response.data or len(select_response.data) == 0:
            raise HTTPException(status_code=500, detail="생성된 유저 조회에 실패했습니다.")

        created_user = select_response.data[0]
        print("created_user", created_user)
        # 생성된 user 데이터 반환
        return {"user": created_user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

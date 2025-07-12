from fastapi import HTTPException
from supabase import create_client, Client
from app.core.config import get_supabase_config

# Supabase 클라이언트 초기화
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_leaderboard():
    """
    profiles 테이블에서 포인트 기준 상위 50명의 리더보드를 가져오는 함수입니다.
    """
    try:
        # profiles 테이블에서 total_points 기준 내림차순 정렬, 상위 50명만 가져오기
        response = (
            supabase
            .table("profiles")
            .select("id, username, total_points, continuous_days, user_img")
            .order("total_points", desc=True)
            .limit(50)
            .execute()
        )
        if not response.data or (isinstance(response.data, list) and len(response.data) == 0):
            raise HTTPException(status_code=500, detail="DB 조회 중 오류가 발생했습니다.")
        leaderboard = response.data
        return {"leaderboard": leaderboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

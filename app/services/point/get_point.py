from fastapi import HTTPException
from supabase import create_client, Client
from uuid import UUID
from app.core.config import get_supabase_config
from collections import defaultdict
from datetime import datetime

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_point_log(user_id: UUID):
    """
    특정 user_id에 대한 point_log를 날짜별로 누적 합산하여 반환합니다.
    반환 형식: [{"date": YYYY-MM-DD, "score": 해당 날짜 합산 점수}, ...]
    """
    try:
        response = (
            supabase
            .table("point_log")
            .select("point, created_at")
            .eq("user_id", str(user_id))
            .order("created_at", desc=False)
            .execute()
        )
        if not response.data or len(response.data) == 0:
            return []

        # 날짜별로 point 합산
        date_point_map = defaultdict(int)
        for row in response.data:
            # created_at이 None이거나 비어있으면 건너뜀
            if not row.get("created_at"):
                continue
            # created_at이 ISO 포맷 문자열로 온다고 가정
            try:
                date_str = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")).strftime("%Y-%m-%d")
            except Exception:
                # 혹시 created_at 포맷이 다르면 그냥 앞 10글자(YYYY-MM-DD)만 사용
                date_str = row["created_at"][:10]
            date_point_map[date_str] += row.get("point", 0)

        # 날짜 오름차순 정렬
        result = [
            {"date": date, "score": score}
            for date, score in sorted(date_point_map.items())
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

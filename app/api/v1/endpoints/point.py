from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.services.point.create_point import create_point_log
from app.services.point.get_point import get_point_log

router = APIRouter()

@router.post("/{user_id}")
async def create_point(user_id: UUID, point: int):
    """
    포인트 로그를 생성합니다.

    Parameters:
    - user_id (UUID): 사용자 ID
    - point (int): 추가할 포인트 값

    Returns:
    - dict: 생성된 포인트 로그 정보
        - message (str): 성공 메시지
        - log (dict): 생성된 로그 데이터
    """
    try:
        return await create_point_log(user_id, point)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_points(user_id: UUID):
    """
    사용자의 포인트 로그를 날짜별로 조회합니다.

    Parameters:
    - user_id (UUID): 사용자 ID

    Returns:
    - list: 날짜별 포인트 합계 목록
        - date (str): 날짜 (YYYY-MM-DD 형식)
        - score (int): 해당 날짜의 총 포인트
    """
    try:
        return await get_point_log(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
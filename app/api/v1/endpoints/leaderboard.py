from fastapi import APIRouter, HTTPException
from app.services.leaderBoard.get_ranking import get_leaderboard

router = APIRouter()

@router.get("/leaderBoard")
async def get_leaderboard_ranking():
    """
    리더보드 순위를 가져옵니다.
    """
    try:
        return get_leaderboard()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

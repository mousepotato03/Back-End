from fastapi import APIRouter
from app.api.v1.endpoints import character, community, leaderboard, users, verification

router = APIRouter()
router.include_router(character.router, prefix="/character")
router.include_router(community.router, prefix="/community")
router.include_router(leaderBoard.router, prefix="/leaderboard")
router.include_router(users.router, prefix="/users")
router.include_router(verification.router, prefix="/verification")
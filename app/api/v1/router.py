from fastapi import APIRouter
from app.api.v1.endpoints import character, community, leaderboard, users, verification, point, like

router = APIRouter()
router.include_router(character.router, prefix="/character")
router.include_router(community.router, prefix="/community")
router.include_router(leaderboard.router, prefix="/leaderboard")
router.include_router(users.router, prefix="/users")
router.include_router(verification.router, prefix="/verification")
router.include_router(point.router, prefix="/point")
router.include_router(like.router, prefix="/like")
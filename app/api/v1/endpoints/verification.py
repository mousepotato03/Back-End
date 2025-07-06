from fastapi import APIRouter, HTTPException
from app.services.article.verify_article import verify_summary
from app.services.article.get_article import get_article_with_concepts
# from app.services.image.verify_image import verify_image_upload
from app.services.image.create_behavior import create_user_behavior

router = APIRouter()

@router.post("/summary")
async def verify_article_summary(article_id: int, user_summary: str):
    """
    사용자가 제출한 소감문을 검증합니다.
    """
    try:
        # 1. DB에서 article_id에 해당하는 글의 핵심 개념을 가져옵니다.
        article_info = get_article_with_concepts(article_id)
        if not article_info:
            raise HTTPException(status_code=404, detail="Article not found")
        
        key_concepts = article_info.get("key_concepts", [])
        
        # 2. 소감문의 길이가 너무 짧은 경우 예외 처리
        if len(user_summary) < 10:
            raise HTTPException(status_code=400, detail="Summary is too short. Please write more sincerely.")

        # 3. 검증 로직 함수 호출
        is_verified = verify_summary(user_summary, key_concepts)

        if not is_verified:
            raise HTTPException(
                status_code=400,
                detail="Verification failed. Your summary does not seem to be related to the article's content."
            )

        # 4. 인증 성공 시 포인트 지급 및 성공 응답 반환
        points_earned = 50  # 예시 포인트
        
        return {
            "message": "Verification successful!",
            "is_verified": True,
            "points_earned": points_earned
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image")
async def verify_image(image_data: dict):
    """
    이미지 업로드를 검증합니다.
    """
    try:
        result = verify_image_upload(image_data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/behavior")
async def create_behavior(behavior_data: dict):
    """
    사용자 행동을 기록합니다.
    """
    try:
        result = create_user_behavior(behavior_data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
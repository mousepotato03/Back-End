
#TODO 파일 위치 수정, verify_article.py 와 연결 !!
@router.post("/summary")
async def verify_article_summary(
    request: SummaryVerificationRequest,
    # db: Session = Depends(get_db), # 실제 DB 세션 주입
    # current_user: User = Depends(get_current_user) # 사용자 인증 정보 주입
):
    """
    사용자가 제출한 소감문을 검증합니다.
    """
    # 1. DB에서 article_id에 해당하는 글의 핵심 개념(key_concepts)을 가져옵니다.
    #    (아래는 DB 연동을 가정한 가짜 데이터입니다.)
    if request.article_id == 123:
        # 실제로는: db_article = crud.get_article(db, id=request.article_id)
        # key_concepts = db_article.key_concepts
        key_concepts = ["뱀파이어 전력 (대기전력)", "가정 전력 소비의 6~10% 차지", "플러그 뽑기 또는 멀티탭 끄기"]
    else:
        raise HTTPException(status_code=404, detail="Article not found")
        
    # 2. 소감문의 길이가 너무 짧은 경우 예외 처리
    if len(request.user_summary) < 10:
        raise HTTPException(status_code=400, detail="Summary is too short. Please write more sincerely.")

    # 3. 검증 로직 함수 호출
    is_verified = verify_summary(request.user_summary, key_concepts)

    if not is_verified:
        # 인증 실패 시 명확한 메시지 반환
        raise HTTPException(
            status_code=400,
            detail="Verification failed. Your summary does not seem to be related to the article's content."
        )

    # 4. 인증 성공 시 포인트 지급 및 성공 응답 반환
    #    (포인트 지급 로직은 별도의 서비스 함수로 분리하는 것이 좋습니다.)
    points_earned = 50 # 예시 포인트
    # point_service.add_points(db, user=current_user, amount=points_earned)
    
    return {
        "message": "Verification successful!",
        "is_verified": True,
        "points_earned": points_earned
    }
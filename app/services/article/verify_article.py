from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

# --- 의존성 주입을 위한 Pydantic 모델 정의 ---
class SummaryVerificationRequest(BaseModel):
    article_id: int
    user_summary: str

# TODO FastAPI의 startup 이벤트를 사용하거나 클래스로 감싸기.
similarity_model = SentenceTransformer('jhgan/ko-sroberta-multitask')

router = APIRouter()

# --- 검증 로직 함수 ---
async def verify_summary(summary: str, concepts: list[str], threshold: float = 0.5) -> bool:
    """사용자 소감문이 핵심 개념 중 하나 이상과 의미적으로 유사한지 검증합니다."""
    if not summary or not concepts:
        return False

    summary_embedding = similarity_model.encode(summary, convert_to_tensor=True)
    concept_embeddings = similarity_model.encode(concepts, convert_to_tensor=True)
    
    cosine_scores = util.cos_sim(summary_embedding, concept_embeddings)
    max_score = cosine_scores.max().item()
    
    print(f"DEBUG: Max similarity score is {max_score}") 
    
    return max_score > threshold
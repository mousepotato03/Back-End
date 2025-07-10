from fastapi import APIRouter, HTTPException
from app.services.character.anl_txt import anl_env_relation
# from app.services.character.env_relation_response import generate_character_response

router = APIRouter()

@router.post("/generate")
async def environment_relation_check(text: str):
    """
    환경과 관계가 있는지 판단합니다.
    """
    try:
        result = await anl_env_relation(text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/response")
# async def get_character_response(environment: str, relation: str):
#     """
#     환경과 관계를 기반으로 캐릭터 응답을 생성합니다.
#     """
#     try:
#         response = generate_character_response(environment, relation)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

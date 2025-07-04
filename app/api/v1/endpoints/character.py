from fastapi import APIRouter
from ...services.generate.character.anl_txt import anl_env_relation

router = APIRouter()

@router.get("/gen-character")
def gen_character(text: str):
    anl_env_relation(text)
    # return anl_txt(text)

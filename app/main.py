from fastapi import FastAPI
from app.api.v1.router import api_router

# TODO: 나중에 리드미 쓸 때 지울 것
# 서버 실행 방법
# pip install -r requirements.txt <- 필요 패키지 받기 
# fastapi dev src/main.py <- 디버그(개발)
# fastapi run src/main.py <- 배포 

app = FastAPI()

# API 라우터 확장
app.include_router(api_router, prefix="/api/v1")
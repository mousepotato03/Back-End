from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router

# TODO: 나중에 리드미 쓸 때 지울 것
# 서버 실행 방법
# pip install -r requirements.txt <- 필요 패키지 받기 
# fastapi dev src/main.py <- 디버그(개발)
# fastapi run src/main.py <- 배포 

app = FastAPI()

#cors 허용 도메인
origins = ["http://localhost",
           "https://localhost:8000",
           "http://127.0.0.1:8000",
           "http://10.0.2.2:8000"] 

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins, # allow origin info
  allow_credentials=True, # 인증 정보(cookie, verify header ...etc) allow 여부
  allow_methods=["*"], #모든 HTTP method allow
  allow_headers=["*"] #모든 HTTP 헤더 allow
)

@app.get("/")
async def root():
    return {"message": "hello world"}

# API 라우터 확장
app.include_router(router, prefix="/api/v1")
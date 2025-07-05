from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()  # .env 파일 로드

# Gemini API 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def validate_environment_variables() -> bool:
    """.env 에서 Key, URL 가져와서 isset 검증"""
    required_vars = {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        print(f"경고: 다음 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
        return False
    
    return True

# 환경 변수 검증 (개발 환경에서만)
if os.getenv("ENVIRONMENT", "development") == "development":
    validate_environment_variables()
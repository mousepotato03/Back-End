from google import genai
from google.genai import types
from app.core.config import get_gemini_api_key
import json

# O/X 퀴즈 응답을 위한 JSON 스키마 정의
quiz_ox_response_schema = types.Schema(
    type="object",
    properties={
        "question": types.Schema(type="string", description="The O/X quiz statement in Korean."),
        "answer": types.Schema(type="string", description="The correct answer, either 'O' or 'X'."),
        "explanation": types.Schema(type="string", description="A brief explanation in Korean."),
    },
    required=["question", "answer", "explanation"],
)

system_prompt="""
    You are an AI quiz master for "zeroro", an environmental protection app.
    Your primary goal is to create a single, engaging True/False (O/X) style quiz question to educate users.

    Instructions:

    1.  Topic Selection: Autonomously select a surprising or lesser-known environmental fact. You can choose from a wide range of topics like recycling, energy conservation, food waste, biodiversity, fast fashion, or plastics. Your goal is to find an interesting fact that most people might not know.
    2.  Question Format: The "question" must be a declarative statement (a fact) in Korean that can be judged as either true ('O') or false ('X').
    3.  Language: The entire output (question, answer, explanation) MUST be in Korean.
    4.  Clarity & Tone: Keep the question and explanation concise and easy to understand for a general audience. The tone should be educational and engaging, making users feel like they've learned something new.
"""

async def create_OX_quiz():
    """AI가 자율적으로 주제를 선택하여 O/X 퀴즈를 생성합니다."""
    try: 
        # API key 설정
        api_key = get_gemini_api_key()
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-pro", 
            contents="Generate one O/X quiz now.",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=quiz_ox_response_schema,
                system_instruction=system_prompt
            ),
        )
        # 문자열을 JSON으로 파싱하여 반환
        return json.loads(response.text)
    except Exception as e:
        raise Exception(f"퀴즈 생성 중 오류가 발생했습니다: {str(e)}")
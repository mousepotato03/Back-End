import os 
import random
import google.generativeai as genai

API_key = os.getenv('GOOGLE_GEMINI_API_KEY')
genai.configure(api_key=API_key)

generation_config = genai.GenerationConfig(temparature=1, response_mime_type="application/json")
model = genai.GenerativeModel('gemini-2.5-flash', generation_config=generation_config)


#TODO -> O,X 형으로 변경하기. 변경하면 이 API 하나로 answer, explain까지 담당 가능
def create_quiz_prompt():
    # 데이터베이스나 리스트에서 다양한 주제를 랜덤하게 선택
    topics_in_korean = [
        "올바른 분리배출 상식",
        "생활 속 물 절약 방법",
        "대중교통의 탄소 절감 효과",
        "미세 플라스틱의 위험성",
        "제로 웨이스트 실천 팁"
    ]
    selected_topic = random.choice(topics_in_korean)

    prompt = f"""
    You are an expert AI assistant tasked with creating educational content for "zeroro", an environmental protection app. Your goal is to generate a single, engaging multiple-choice quiz question.

    Instructions:
    1.  Language: The entire output (question, options, answer, explanation) MUST be in Korean (한국어).
    2.  Topic: The quiz should be about the following environmental topic: {selected_topic}.
    3.  Conciseness: Keep the question and options short and clear. They need to be easily readable on a small mobile screen.
    4.  Content: The quiz should be practical and informative for a general audience, not overly academic.
    5.  Explanation: The explanation must be brief (1-2 sentences) and provide a useful fact or a practical tip.

    Output Format:
    You must provide your response ONLY in a valid JSON format. Do not add any text before or after the JSON object. The JSON object must contain these exact keys:

    {{
      "question": "A short quiz question in Korean.",
      "options": [
        "Option 1 in Korean",
        "Option 2 in Korean",
        "Option 3 in Korean",
        "Option 4 in Korean"
      ],
      "answer": "The correct answer's text, exactly as it appears in the options array.",
      "explanation": "A brief explanation in Korean about why the answer is correct."
    }}
    """
    return prompt

response = model.generate_content(create_quiz_prompt())
response.text

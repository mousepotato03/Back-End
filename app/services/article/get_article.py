from google import genai
from google.genai import types
import random
from app.core.config import get_gemini_api_key

# 1. response_schema 수정: 'key_concepts' 필드 추가
article_with_concepts_schema = types.Schema(
    type="object",
    properties={
        "title": types.Schema(type="string", description="The catchy title of the article in Korean."),
        "article_text": types.Schema(type="string", description="The full environmental article in Korean."),
        "key_concepts": types.Schema(
            type="array",
            items=types.Schema(type="string"),
            description="A list of 3-4 key concepts or short phrases from the article in Korean, crucial for understanding its core message."
        )
    },
    required=["title", "article_text", "key_concepts"],
)

def get_article_with_concepts():
    ARTICLE_IDEAS = [
        {'topic': 'Single-Use Plastics', 'angle': 'The surprising journey of a plastic bottle after you throw it away, and why choosing a reusable tumbler matters.'},
        {'topic': 'Fast Fashion', 'angle': 'The hidden environmental cost behind a $10 t-shirt and how "slow fashion" can save your wallet and the planet.'},
        {'topic': 'Food Waste', 'angle': 'Why throwing away "ugly" fruits and leftover food is a big problem, and simple tips to reduce food waste in your kitchen.'},
        {'topic': 'Energy Consumption at Home', 'angle': 'The concept of "Vampire Power": Unplugging electronics to save energy and money effortlessly.'},
        {'topic': 'Water Conservation', 'angle': 'How small changes in your daily routine, like shorter showers, can save thousands of liters of water a year.'},
        {'topic': 'Paper Usage', 'angle': 'Going digital with receipts and bills: A simple switch that saves forests and reduces clutter.'},
        {'topic': 'Carbon Footprint', 'angle': 'What is a "Carbon Footprint" and how your daily transportation choices (walking, biking, public transport) can shrink it.'},
        {'topic': 'Local & Seasonal Food', 'angle': 'The benefits of eating local and seasonal food: Fresher taste, better nutrition, and a smaller environmental impact.'},
        {'topic': 'Biodiversity in the City', 'angle': 'Why bees and small urban parks are crucial for our cities, and how we can help them thrive.'},
        {'topic': 'Upcycling', 'angle': 'The creative power of Upcycling: Turning trash into treasure and giving old items a new life.'},
    ]

    idea = random.choice(ARTICLE_IDEAS)
    
    # API key 설정
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents="Generate the content package now.", # 명시적 명령
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=article_with_concepts_schema,
            system_instruction=f"""
              You are an AI content creator for "zeroro", an environmental app. Your task is to generate a package of content based on the provided topic.

              Topic:
              - Main Topic: {idea['topic']}
              - Specific Angle/Focus: {idea['angle']}

              Primary Task: Write an Article
              Generate a short article in Korean following these requirements:
              - Word Count: Approximately 300 words
              - Language: Korean
              - Tone: Positive, educational, and motivational
              - Article Structure: A catchy title, introduction, body (2-3 key points), and a concluding question.
              - What to avoid: Complex jargon, preachy tone.

              Additional Task: Extract Key Concepts
              After writing the article, extract 3 to 4 of the most important concepts or short phrases. These concepts are essential for a reader to prove they have understood the article.

              Return the entire output in the specified JSON schema format.
              """
        ),
    )
    
    # 3. 반환값: 이제 JSON 텍스트를 반환
    return response.text
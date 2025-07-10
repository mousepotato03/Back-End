from google import genai
from google.genai import types
from app.core.config import get_gemini_api_key

env_relation_response_schema = types.Schema(
    type="object",
    properties={
        "related": types.Schema(type="boolean", description="Is the text about an environmental topic?"),
        "word": types.Schema(type="string", description="Word representing the environmental topic.", nullable=True),
    },
    required=["related"],
)


async def verify_image_upload(text: str):
    # API key 설정
    api_key = get_gemini_api_key()
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=env_relation_response_schema,
            system_instruction="""

""",
        ),
    )
    return response.text

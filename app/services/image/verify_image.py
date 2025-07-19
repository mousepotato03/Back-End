from google import genai
from google.genai import types
from app.core.config import get_gemini_api_key

# 카테고리별 검증을 위한 스키마
category_verification_schema = types.Schema(
    type="object",
    properties={
        "is_valid": types.Schema(type="boolean", description="Is the image appropriate for the selected category and subcategory?"),
        "confidence": types.Schema(type="number", description="Confidence level (0-1) of the verification"),
        "reason": types.Schema(type="string", description="Reason for the verification result"),
    },
    required=["is_valid", "confidence", "reason"],
)

# 카테고리 매핑 (백엔드에서 관리하여 유지보수 편의성 확보)
MAIN_CATEGORIES = {
    0: '올바른 분리배출',
    1: '다회용품 사용', 
    2: '자원 절약 및 재활용',
    3: '건의하기'
}

SUB_CATEGORIES = {
    # mainIndex: 0 (올바른 분리배출)
    0: {'name': '페트병 라벨 제거', 'mainIndex': 0},
    1: {'name': '택배 상자 테이프/송장 제거', 'mainIndex': 0},
    2: {'name': '내용물이 비워진 우유갑/주스팩', 'mainIndex': 0},
    3: {'name': '깨끗한 스티로폼 박스', 'mainIndex': 0},
    
    # mainIndex: 1 (다회용품 사용)
    4: {'name': '카페/식당에서의 텀블러 사용', 'mainIndex': 1},
    5: {'name': '다회용기(용기내) 포장', 'mainIndex': 1},
    6: {'name': '장바구니 사용', 'mainIndex': 1},
    
    # mainIndex: 2 (자원 절약 및 재활용)
    7: {'name': '전자영수증 발급 화면', 'mainIndex': 2},
    8: {'name': '사용하지 않는 플러그 뽑기', 'mainIndex': 2},
}

async def verify_image_by_category(image_bytes: bytes, main_category_index: int, sub_category_index: int):
    """
    프론트엔드에서 넘겨준 카테고리 인덱스를 받아서 해당 내용에 맞는 이미지인지 검증하는 API입니다.
    
    params:
        image_description: str - 이미지에 대한 설명
        main_category_index: int - 프론트엔드에서 넘겨준 메인 카테고리 인덱스
        sub_category_index: int - 프론트엔드에서 넘겨준 서브 카테고리 인덱스
    """
    main_category = MAIN_CATEGORIES.get(main_category_index)
    if not main_category:
        # FastAPI에서는 직접 에러를 발생시키는 것보다 HTTPException을 사용하는 것이 좋음
        # raise HTTPException(status_code=400, detail=f"Invalid main category index: {main_category_index}")
        raise ValueError(f"Invalid main category index: {main_category_index}") # 일단은 그대로 유지

    sub_category = SUB_CATEGORIES.get(sub_category_index)
    if not sub_category:
        raise ValueError(f"Invalid sub category index: {sub_category_index}")

    if sub_category['mainIndex'] != main_category_index:
        raise ValueError(f"Sub category {sub_category_index} does not belong to main category {main_category_index}")

    main_category_name = MAIN_CATEGORIES[main_category_index]
    sub_category_name = sub_category['name']

    # 2. system_instruction을 함수 내에서 동적으로 생성
    system_prompt = f"""
    You are an AI image verification specialist for "zeroro", an environmental app. Your task is to analyze a user-submitted image with extreme focus and strictness.

    **Action to Verify:**
    - **Main Category:** "{main_category_name}"
    - **Specific Action:** "{sub_category_name}"

    **Your Primary Objective:**
    Your one and only goal is to determine if the image provides **direct, undeniable proof** that the user performed the **"Specific Action"** listed above. All other observations are secondary. If the proof for the specific action is not present, the verification must fail, regardless of any other positive environmental activities shown in the image.

    **Evaluation Criteria & Thought Process:**
    1.  **Identify Core Evidence:** First, identify the essential objects and their state required to prove the "Specific Action". (e.g., for 'Removing a bottle label', the core evidence is a BOTTLE and a DETACHED LABEL).
    2.  **Scan for Core Evidence:** Does the image contain this core evidence? This is a simple yes/no check. If no, fail immediately.
    3.  **Assess State & Context:** If the evidence is present, is it in the correct state? (e.g., Is the label *fully* detached?).
    4.  **Check Authenticity:** Does this look like a genuine, user-taken photo?

    **Final Judgement:**
    - **Success (is_valid: true):** Only when there is clear and direct evidence of the **"Specific Action"**.
    - **Failure (is_valid: false):** In ALL other cases. For example, if the action is "Removing the label from a PET bottle" and the user uploads a picture of recycling 10 plastic bottles (a good deed, but not the specified action), you MUST return `false`.

    Provide your response ONLY in the specified JSON schema format. The 'reason' must be a concise explanation in **Korean**.
    """

    try:
        # API key 설정
        api_key = get_gemini_api_key()
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                ),
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=category_verification_schema,
                system_instruction=system_prompt
            ),
        )
        return response.text
        
    except Exception as e:
        raise Exception(f"이미지 검증 중 오류가 발생했습니다: {str(e)}")

import os 
import random
import google.generativeai as genai

API_key = os.getenv('GOOGLE_GEMINI_API_KEY')
genai.configure(api_key=API_key)

generation_config = genai.GenerationConfig(temparature=1, response_mime_type="application/json")
model = genai.GenerativeModel('gemini-2.5-flash', generation_config=generation_config)

def create_article_prompt():
  # 데이터베이스나 설정 파일에 저장해 둘 글감 목록
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
  prompt = f"""
    Generate a short article for an environmental app called 'zeroro'.

    - Main Topic: {idea['topic']}
    - Specific Angle/Focus: {idea['angle']}
    - Word Count: Approximately 100 words.
    - Target Audience: General users interested in starting their eco-friendly journey.
    - Tone: Positive, educational, and motivational.

    The article must have the following structure:
    1. A catchy, short title.
    2. An introduction that explains what the topic is and why it's important.
    3. A body that provides 2-3 key facts or points.
    4. A conclusion that summarizes the main message and ends with a thought-provoking question for the reader to reflect on.
    5. when you return then use this scheme Article = {"article" : str}, Return a `list[Article]`
    6. write this article in korean

    What to avoid:
    - Do not use overly complex scientific jargon.
    - Avoid a preachy or guilt-inducing tone.
  """
  return prompt

response = model.generate_content(create_article_prompt())
response.text


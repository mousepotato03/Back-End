from google import genai
from google.genai import types
import random

article_response_schema = types.Schema(
    type="object",
    properties={
        "article": types.Schema(type="string", description="Generated environmental article in Korean"),
    },
    required=["article"],
)

def get_article():
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
  client = genai.Client()
  response = client.models.generate_content(
      model="gemini-2.5-flash-lite",
      config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=article_response_schema,
        system_instruction=f"""
        You are an AI article generator for an environmental app called 'zeroro'. Generate a short article in Korean about the following topic:
        - Main Topic: {idea['topic']}
        - Specific Angle/Focus: {idea['angle']}

        Requirements:
        - Word Count: Approximately 300 words
        - Language: Korean
        - Tone: Positive, educational, and motivational
        - Target Audience: General users interested in starting their eco-friendly journey

        Article Structure:
        1. A catchy, short title
        2. An introduction that explains what the topic is and why it's important
        3. A body that provides 2-3 key facts or points
        4. A conclusion that summarizes the main message and ends with a thought-provoking question

        What to avoid:
        - Do not use overly complex scientific jargon
        - Avoid a preachy or guilt-inducing tone

        Return the article in the specified JSON schema format with the "article" field containing the complete article text.
      """
    ),
  )
  return response.text


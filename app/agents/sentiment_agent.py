# from google import genai
# import feedparser
# import json
# from app.config import GEMINI_API_KEY

# client = genai.Client(api_key=GEMINI_API_KEY)


# def analyze_sentiment(symbol: str):
#     url = f"https://news.google.com/rss/search?q={symbol}"
#     feed = feedparser.parse(url)

#     headlines = [entry.title for entry in feed.entries[:5]]

#     if not headlines:
#         return {
#             "sentiment": "Neutral",
#             "score": 0.0,
#             "reason": "No recent headlines found."
#         }

#     prompt = f"""
#     Analyze the sentiment of the following news headlines for stock {symbol}.

#     Respond STRICTLY in valid JSON format like this:

#     {{
#         "sentiment": "Positive/Negative/Neutral/Mixed",
#         "score": <number between -1 and 1>,
#         "reason": "Short explanation"
#     }}

#     Headlines:
#     {headlines}
#     """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#     )

#     try:
#         # Try parsing model output as JSON
#         sentiment_json = json.loads(response.text)
#         return sentiment_json
#     except Exception:
#         # Fallback if model adds extra text
#         return {
#             "sentiment": "Unknown",
#             "score": 0.0,
#             "reason": response.text
#         }



from google import genai
import feedparser
import json
import re
from app.config import GEMINI_API_KEY

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def extract_json(text: str):
    """
    Extract JSON object from Gemini response.
    Handles:
    - ```json ... ``` blocks
    - Extra explanatory text
    - Partial formatting issues
    """

    try:
        # Remove markdown code fences if present
        text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```", "", text)

        # Find first JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        return None

    return None


def analyze_sentiment(symbol: str):
    url = f"https://news.google.com/rss/search?q={symbol}"
    feed = feedparser.parse(url)

    headlines = [entry.title for entry in feed.entries[:5]]

    if not headlines:
        return {
            "sentiment": "Neutral",
            "score": 0.0,
            "reason": "No recent headlines found."
        }

    prompt = f"""
    Analyze the sentiment of the following news headlines for stock {symbol}.

    Respond STRICTLY in valid JSON format:

    {{
        "sentiment": "Positive/Negative/Neutral/Mixed",
        "score": number between -1 and 1,
        "reason": "Short explanation"
    }}

    Headlines:
    {headlines}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        parsed = extract_json(response.text)

        if parsed:
            # Ensure safe defaults
            return {
                "sentiment": parsed.get("sentiment", "Unknown"),
                "score": float(parsed.get("score", 0.0)),
                "reason": parsed.get("reason", "No reasoning provided.")
            }

        # If parsing fails
        return {
            "sentiment": "Unknown",
            "score": 0.0,
            "reason": "Could not parse LLM response."
        }

    except Exception as e:
        return {
            "sentiment": "Error",
            "score": 0.0,
            "reason": f"Sentiment analysis failed: {str(e)}"
        }

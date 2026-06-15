import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
import httpx

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello as CareAI.",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are CareAI, a professional e-commerce customer support assistant."
            )
        ),
    )
    print(response.text)
except errors.APIError as error:
    if getattr(error, "code", None) == 429:
        raise RuntimeError(
            "Gemini API quota exceeded. Check your Google AI Studio rate limits, "
            "billing, or wait for quota reset before retrying."
        ) from error
    raise
except httpx.HTTPError as error:
    raise RuntimeError(
        "Could not connect to the Gemini API. Check your internet connection, DNS, "
        "proxy/VPN settings, or firewall rules."
    ) from error
finally:
    client.close()

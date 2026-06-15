import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        pass
    val = os.getenv("GEMINI_API_KEY")
    if val:
        return val
    

api_key = get_api_key()
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

# Load system prompt from file
def load_system_prompt():
    with open("data/system-prompt.txt", "r") as f:
        return f.read()

# Send message and get reply
def get_response(chat_history: list, user_message: str) -> str:
    client = genai.Client(api_key=api_key)

    try:
        # Add new user message to history
        contents = chat_history + [
            types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=load_system_prompt()
            )
        )

        return response.text

    except Exception as e:
        return f"I'm sorry, I ran into an issue. Please try again. (Error: {str(e)})"

    finally:
        client.close()


# Helper — call this after every turn to update history
def update_history(chat_history: list, user_message: str, bot_reply: str) -> list:
    chat_history.append(
        types.Content(role="user", parts=[types.Part(text=user_message)])
    )
    chat_history.append(
        types.Content(role="model", parts=[types.Part(text=bot_reply)])
    )
    return chat_history
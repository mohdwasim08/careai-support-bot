import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        pass
    val = os.getenv("GROQ_API_KEY")
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

    client = Groq(api_key=api_key)

    try:

        messages = [
            {
                "role": "system",
                "content": load_system_prompt()
            }
        ]

        # Add previous conversation
        for msg in chat_history:
            messages.append({
                "role": msg.role,
                "content": msg.parts[0].text
            })

        # Current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"
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
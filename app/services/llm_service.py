import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

def generate_response(prompt, tone_feedback=None):
    system_prompt = "You are a helpful assistant."
    if tone_feedback == "too formal":
        system_prompt = "Use a casual and friendly tone."
    elif tone_feedback == "too casual":
        system_prompt = "Use a more professional and formal tone."

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

import openai
from openai import OpenAI
import os
import json
import re

api_key_groq = os.getenv("GROQ_API_KEY")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key_groq
)

def detect_tone_with_groq(user_input: str):
    prompt = """Analyze the following message and return the tone as a JSON object with the following fields:
- formality: casual, professional, formal
- enthusiasm: low, medium, high
- verbosity: concise, balanced, detailed
- empathy_level: low, medium, high
- humor: none, light, moderate, heavy

Message:
\"\"\"%s\"\"\"
""" % user_input

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        if response and response.choices:
            content = response.choices[0].message.content.strip()

            # ✅ Extract JSON inside code block if present
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
            json_str = match.group(1) if match else content

            try:
                tone = json.loads(json_str)
                print("🤖 Returning tone →", tone)
                return tone
            except json.JSONDecodeError as json_err:
                print("⚠️ Failed to parse JSON from extracted content:", json_str)
                return {
                    "formality": "casual",
                    "enthusiasm": "medium",
                    "verbosity": "balanced",
                    "empathy_level": "medium",
                    "humor": "none"
                }
        else:
            print("⚠️ Empty or malformed response from GROQ:", response)
            return {
                "formality": "casual",
                "enthusiasm": "medium",
                "verbosity": "balanced",
                "empathy_level": "medium",
                "humor": "none"
            }

    except Exception as e:
        print("❌ Exception during GROQ tone detection:", str(e))
        return {
            "formality": "casual",
            "enthusiasm": "medium",
            "verbosity": "balanced",
            "empathy_level": "medium",
            "humor": "none"
        }

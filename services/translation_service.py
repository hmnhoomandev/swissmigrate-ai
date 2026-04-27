import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def translate_text(text, target_language):
    if not text:
        return ""

    if target_language == "English":
        return text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translator. Translate clearly and simply. Do not add explanations."
            },
            {
                "role": "user",
                "content": f"Translate the following text into {target_language}:\n\n{text}"
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
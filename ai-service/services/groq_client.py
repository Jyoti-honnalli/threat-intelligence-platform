import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def call_groq(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY not found in .env file")

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ stable model
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content
        return content

    except Exception as e:
        print("GROQ ERROR:", str(e))
        raise e
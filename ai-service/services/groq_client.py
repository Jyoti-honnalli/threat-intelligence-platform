import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def clean_text(text):
    text = text.replace("**", "")
    text = text.replace("\\n", "\n")

    lines = text.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    return cleaned_lines


def generate_response(prompt, retries=3):
    for attempt in range(retries):
        try:
            logging.info(f"[Groq API] Attempt {attempt+1} | Prompt: {prompt[:30]}...")

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )

            # Safe extraction
            if response and response.choices:
                cleaned = clean_text(response.choices[0].message.content)
                return cleaned

            return "Error: Empty response from API"

        except Exception as e:
            logging.error(f"[Groq API] Attempt {attempt+1} failed | Error: {str(e)}")

            # exponential backoff
            time.sleep(2 ** attempt)

    logging.critical("[Groq API] All retry attempts failed")
    return "Error: Failed after multiple retries"
    
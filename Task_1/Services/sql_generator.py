import time
import random
import google.generativeai as genai
from Utils.prompt_helper import format_prompt
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

def generate_sql(nl_query):
    prompt = format_prompt(nl_query)

    max_retries = 3
    retry_delay = 10  # seconds

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            sql = response.text.strip()
            sql = sql.replace("```sql", "").replace("```", "").strip()

            if not sql.lower().startswith(("select", "insert", "update", "delete")):
                return "Hmm, I couldn’t quite turn that into a valid query. Maybe try rephrasing it?"

            return sql

        except Exception as e:
            error_message = str(e).lower()
            if "rate limit" in error_message or "quota" in error_message:
                wait_time = retry_delay + random.uniform(0, 2)  # add a bit of jitter
                print(f"Rate limit hit. Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                retry_delay = min(retry_delay * 2, 60)  # exponential backoff, max 60 sec
            else:
                print(f"Error: {e}")
                break

    return "The system is a bit busy at the moment. Try again in a bit, and I’ll be ready!"

import os
from .celery_app import celery_app

try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
except Exception:  # if openai not installed or other errors
    openai = None

@celery_app.task
def analyze_rfp(file_path: str) -> str:
    """Analyze RFP document using OpenAI GPT. If no API key, return preview."""
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()
    if openai and openai.api_key:
        try:
            resp = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': f'Summarize:\n{content}'}],
            )
            return resp.choices[0].message['content']
        except Exception as exc:
            return f'error: {exc}'
    # fallback if no OpenAI
    return content[:100]

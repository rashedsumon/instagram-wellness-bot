import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_message(prompt: str, max_tokens: int = 150) -> str:
    """
    Generate a short reply — keep this function generic so you can swap providers.
    """
    if not OPENAI_API_KEY:
        # fallback simple template
        return "Hi! Thanks for your interest. What class time works best for you? We have mornings and evenings available."
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # choose appropriate model; placeholder name
        messages=[{"role": "system", "content": "You are an appointment booking assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.2
    )
    return resp["choices"][0]["message"]["content"].strip()

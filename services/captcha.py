import requests
import os

def verify_turnstile(token: str) -> bool:
    secret = os.environ.get('TURNSTILE_SECRET_KEY')
    if not secret:
        return False
    payload = {
        'secret': secret,
        'response': token
    }
    try:
        response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=payload, timeout=5)
        result = response.json()
        return result.get('success', False)
    except Exception:
        return False
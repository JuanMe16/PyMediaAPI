import requests
from django.conf import settings


def get_discord_token(code: str, url: str, session: requests.Session):
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/api/sign-up",
    }
    session.headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    return session.post(url+'/oauth2/token', data=data).json()


def get_discord_user(code: str, url: str):
    session = requests.Session()
    response = get_discord_token(code, url, session)
    session.headers = {
        "Authorization": f"Bearer {response['access_token']}"
    }
    return session.get(url+'/users/@me').json()

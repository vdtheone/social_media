import requests
from fastapi import Request
from starlette.config import Config

config = Config(".env")  # Load environment variables


def getGoogleOAuthToken(request: Request):
    code = request.query_params.get("code")
    base_url = "https://oauth2.googleapis.com/token"
    options = {
        "code": code,
        "client_id": config("GOOGLE_CLIENT_ID"),
        "client_secret": config("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": config("YOUR_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(base_url, data=options, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["access_token"], data["id_token"]


def getGoogleUser(access_token, id_token):
    url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"

    headers = {"Authorization": f"Bearer {id_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as err:
        print(err, "failed to get Google user")
        raise err

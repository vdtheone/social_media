import requests
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.config import Config

from src.services.google_auth import getGoogleOAuthToken, getGoogleUser

auth_router = APIRouter()

config = Config(".env")  # Load environment variables

oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    authorize_prompt=None,
    authorize_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_token_params=None,
    refresh_token_url=None,
    client_kwargs={"scope": "openid profile email"},
)


@auth_router.get("/auth")
async def auth(request: Request):
    try:
        access_token, id_token = getGoogleOAuthToken(request)
        return getGoogleUser(access_token, id_token)

    except OAuthError as error:
        return HTMLResponse(f"<h1>{error.error}</h1>")
    except requests.exceptions.RequestException as err:
        raise err


@auth_router.get("/varify")
def varify_url_code(code):
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


@auth_router.get("/user_info")
def get_user_info(access_token, id_token):
    url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"

    headers = {"Authorization": f"Bearer {id_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as err:
        print(err, "failed to get Google user")
        raise err


# Create a route to initiate Google OAuth login
@auth_router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)

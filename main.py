from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from src.routers.auth import auth_router
from src.routers.comment import comment_router
from src.routers.like import like_router
from src.routers.post import post_router
from src.routers.user import user_router

app = FastAPI()

config = Config(".env")  # Load environment variables
app.add_middleware(SessionMiddleware, secret_key=config("SECRET_KEY"))

app.include_router(auth_router, tags=["Auth"])
app.include_router(user_router, tags=["user"])
app.include_router(post_router, tags=["post"])
app.include_router(comment_router, tags=["comment"])
app.include_router(like_router, tags=["like"])

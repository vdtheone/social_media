from fastapi import FastAPI

from src.routers.comment import comment_router
from src.routers.like import like_router
from src.routers.post import post_router
from src.routers.user import user_router

app = FastAPI()


app.include_router(user_router, tags=["user"])
app.include_router(post_router, tags=["post"])
app.include_router(comment_router, tags=["comment"])
app.include_router(like_router, tags=["like"])

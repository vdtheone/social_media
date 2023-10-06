from fastapi import FastAPI
from routers.user import user_router
from routers.post import post_router

app = FastAPI()


app.include_router(user_router, tags=["user"])
app.include_router(post_router, tags=["post"])

from fastapi import FastAPI  # type: ignore
from .routers import blogs,users

app = FastAPI()

app.include_router(blogs.router)

app.include_router(users.router)
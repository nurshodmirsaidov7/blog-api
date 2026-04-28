from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine
import models
from routers import auth, posts, comments

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)

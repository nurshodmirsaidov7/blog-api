from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine
import models, os
from routers import auth, posts, comments

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)

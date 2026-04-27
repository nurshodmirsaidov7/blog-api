from fastapi import FastAPI
from database import engine
import models
from routers import auth, posts, comments

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)

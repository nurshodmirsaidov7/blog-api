from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import hash_password, verify_password, create_access_token, get_current_user
from typing import List
import uuid
import os

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schemas.PostResponse])
async def get_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
    ):

    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

@router.get('/{post_id}', response_model=schemas.PostResponse)
async def get_single_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Post with this id not found!')
    
    return post

@router.post('/', response_model=schemas.PostResponse)
async def create_post(
    title: str = Form(...),
    content: str = Form(...), 
    user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    image: UploadFile = File(None)
    
):
    image_path = None
    if image:
        ext = image.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_location = f"uploads/{filename}"

        with open(file_location, 'wb') as f:
            f.write(await image.read())
        image_path = file_location

    new_post = models.Post(
        title = title,
        content = content,
        image = image_path,
        author_id = user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put('/{post_id}', response_model=schemas.PostResponse)
async def update_post(
    post_id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if not post:
        raise HTTPException(404, 'Post Not found!')
    if post.author_id != current_user.id:
        raise HTTPException(403, 'Not Allowed!')

    post.title = updated_post.title
    post.content = updated_post.content
    post.image = updated_post.image

    db.commit()
    db.refresh(post)
    return post

@router.delete('/{post_id}')
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, 'Post Not found!')
    if post.author_id != current_user.id:
        raise HTTPException(403, 'Not Allowed!')
    
    db.delete(post)
    db.commit()
    return {'message': 'Post deleted successfully!'}
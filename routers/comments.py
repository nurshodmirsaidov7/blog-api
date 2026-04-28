from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models
from schemas import CommentCreate, CommentResponse
from typing import List

router = APIRouter(prefix='/posts', tags=["Comments"])

@router.post('/{post_id}/comments', response_model=CommentResponse)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(404, 'Post not found')

    new_comment = models.Comment(
        content=comment.content,
        author_id=current_user.id,
        post_id = post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)


    return new_comment

@router.get('/{post_id}/comments', response_model=List[CommentResponse])
async def get_all_comments(
    post_id: int,
    db: Session = Depends(get_db)
    ):

    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments

@router.delete('/{post_id}/comments/{comment_id}')
async def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    current_comment = db.query(models.Comment).filter(
        models.Comment.id==comment_id,
        models.Comment.post_id==post_id
        ).first()

    if not current_comment:
        raise HTTPException(404, 'Comment Not Found!')
        
    if current_comment.author_id != current_user.id:
        raise HTTPException(403, 'Not Allowed!')

    db.delete(current_comment)
    db.commit()

    return {'message': 'Comment is deleted successfully!'}
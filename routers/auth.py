from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=schemas.UserResponse)
async def register(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
    ):

    existing_user = db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email has already registered!')
    
    hashed_password = hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email==user.username).first()
    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail='Email or password is incorrect!')
    
    token = create_access_token({'sub': existing_user.email})
    return {'access_token': token, 'token_type': 'bearer'}
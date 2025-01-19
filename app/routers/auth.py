from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import models, schemas, utils, database, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post('/')
def login(user_Credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_Credentials.username).first() 
    ## using username instead of email as OAuth2PasswordRequestForm return username
    
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not utils.verify(user_Credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    ## Create a token
    ## Return a token
    return{"access_token" : access_token, "token_type" : "bearer"}
    
    
    
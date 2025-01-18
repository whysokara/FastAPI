from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import models, schemas, utils, database
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post('/')
def login(user_Credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_Credentials.email).first()
    
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not utils.verify(user_Credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    
    ## Create a token
    ## Return a token
    return{"token" : "example token"}
    
    
    
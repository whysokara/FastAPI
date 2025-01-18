from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter()

## Creating a user
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    ## hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    # if new_user:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exsist")
    db.commit()
    db.refresh(new_user)
    return new_user

## Fetch user by id
@router.get("/users/{id}", response_model=schemas.UserOut)

def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == int(id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exsist")
    return user
    
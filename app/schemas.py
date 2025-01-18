from pydantic import BaseModel, EmailStr ## For Schema Validation
from datetime import datetime

## Data Validation
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(PostBase):
    pass

## For response

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

## Creating a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
## Response for User
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
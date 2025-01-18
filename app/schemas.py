from pydantic import BaseModel, ConfigDict ## For Schema Validation

## Data Validation
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(PostBase):
    pass

## For response

class Post(BaseModel):
    title: str
    content: str
    published: bool 
    class Config:
        orm_mode = True
    # model_config = ConfigDict(from_attributes=True)

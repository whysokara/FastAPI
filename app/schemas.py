from pydantic import BaseModel ## For Schema Validation

## Data Validation
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(BaseModel):
    pass
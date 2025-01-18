from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from .database import Base

# Post Table
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    
## User Table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
                  
    
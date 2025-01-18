from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

## Variables
database_name = os.getenv('DATABASE_NAME')
database_user = os.getenv('DATABASE_USER')
secret_key = os.getenv('DATABASE_PASSWORD_ALCHEMY')

SQLALCHEMY_DATABASE_URL = f'postgresql://{database_user}:{secret_key}@localhost/{database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

## Dependency while using sqlalchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
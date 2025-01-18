from psycopg2.extras import RealDictCursor ## to import column names from postgres along with values
from dotenv import load_dotenv
from fastapi import FastAPI
import psycopg2
import os   
## While using ORM
from . import models
from .database import engine
## Routing
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

## Creating an instance
app = FastAPI()

# take environment variables from .env
load_dotenv()  

## Variables
database_name = os.getenv('DATABASE_NAME')
database_user = os.getenv('DATABASE_USER')
secret_key = os.getenv('DATABASE_PASSWORD')


## Connecting to db
# while True:
try:
    conn = psycopg2.connect(host='localhost', database=database_name , user=database_user, password=secret_key, cursor_factory = RealDictCursor)
    cursor = conn.cursor()
    print("Connected successfully to db")
        # break
    
except Exception as error:
    print("Connecting to db failed")
    print("Error: ", error)
        # time.sleep(2)

## as part of router restructuring
app.include_router(post.router)  
app.include_router(user.router) 


## get root path
@app.get("/")

def root():
    return {"message" : "Welcome to my API"}



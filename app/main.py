from fastapi import FastAPI, status, HTTPException, Response, Depends
from psycopg2.extras import RealDictCursor ## to import column names from postgres along with values
from typing import Optional, List
from fastapi.params import Body
from dotenv import load_dotenv
from random import randrange
import psycopg2
import time
import os   

## While using ORM
import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

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


## get root path
@app.get("/")

def root():
    return {"message" : "Welcome to my API"}

## Get all posts
@app.get("/posts", response_model=List[schemas.Post])

def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

## Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)

def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title = post.title, content = post.content, published = post.published) long menthod
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

## Get post by id
@app.get("/posts/{id}", response_model=schemas.Post)

def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == int(id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post

## Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int,db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == int(id))
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exsist")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

## Update a post
@app.put("/posts/{id}", response_model=schemas.Post)

def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == int(id))
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exsist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

## Creating a user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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
@app.get("/users/{id}", response_model=schemas.UserOut)

def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == int(id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exsist")
    return user
    
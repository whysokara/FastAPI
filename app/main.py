from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel ## For Schema Validation
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor ## to import column names from postgres along with values
from dotenv import load_dotenv
import os   
import time

## While using ORM
import sqlalchemy
from sqlalchemy.orm import Session
from . import models
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

## Data Validation
class Post(BaseModel):
    title : str
    content : str
    published : bool = True

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

## Temporary Memory
my_posts = [
    {"title" : "title for post 1", "content" : "content for post 1", "id":1},
    {"title" : "Favourite Food", "content" : "My favourite food is pizza", "id":2}
]

## Finding Post
def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
## For deleting post find index of post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

## get root path
@app.get("/")

def root():
    return {"message" : "Welcome to my API"}

## Get all posts
@app.get("/posts")

def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"Status" : posts}

## Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)

def create_posts(post : Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title = post.title, content = post.content, published = post.published) long menthod
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}

## Get post by id
@app.get("/posts/{id}")

def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == int(id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return {"post details":post}

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
@app.put("/posts/{id}")

def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == int(id))
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exsist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data" : post_query.first()}

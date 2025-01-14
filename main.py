from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel ## For Schema Validation
from typing import Optional
from random import randrange

## Creating an instance
app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

## Temporary Memory
my_posts = [
    {"title" : "title for post 1", "content" : "content for post 1", "id":1},
    {"title" : "Favourite Food", "content" : "My favourite food is pizza", "id":2}
]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
def root():
    return {"message" : "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

## A post request

@app.post("/posts")
def create_posts(post : Post):
    post_dict = post.dict() ## converting pydantic model to python dictionary
    post_dict["id"] = randrange(1, 1000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

## Get posy by id

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return {"post details":post}
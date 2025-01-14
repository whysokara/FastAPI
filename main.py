from fastapi import FastAPI, status, HTTPException, Response
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
        if post['id'] == id:
            return post
        
## For deleting post find index of post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message" : "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

## A post request

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.dict() ## converting pydantic model to python dictionary
    post_dict["id"] = randrange(1, 1000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

## Get posy by id

@app.get("/posts/{id}")
def get_post(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND ## Customise status code when id not found
        # return {'message': f"Post with id: {id} not found"}
    return {"post details":post}


## Delete a post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exsist")
    my_posts.pop(index)
    # raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Post with id: {id} is deleted successfully")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
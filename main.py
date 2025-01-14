from fastapi import FastAPI
from fastapi.params import Body

## Creating an instance
app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data" : "This is your post"}

## A post request
@app.post("/createposts")
def create_posts(payload: dict = Body(...) ):
    print(payload)
    return {"New Post" : f"Title {payload['title']} content: {payload['content']}"}
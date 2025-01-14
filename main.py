from fastapi import FastAPI

## Creating an instance
app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Welcome to my API.."}

@app.get("/posts")
def get_posts():
    return {"data" : "This is your post"}
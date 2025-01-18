from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

## Get all posts
@router.get("/", response_model=List[schemas.Post])

def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

## Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)

def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title = post.title, content = post.content, published = post.published) long menthod
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

## Get post by id
@router.get("/{id}", response_model=schemas.Post)

def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == int(id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post

## Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int,db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == int(id))
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exsist")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

## Update a post
@router.put("/{id}", response_model=schemas.Post)

def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == int(id))
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exsist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

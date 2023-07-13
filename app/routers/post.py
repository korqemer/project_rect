from .. import models, schema
from fastapi import Response, status, HTTPException, Depends
from fastapi import APIRouter
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from .. import oauth2
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags=["POSTS"]
)


@router.get("/", response_model=List[schema.PostResponse])
async def get_posts(db: Session = Depends(get_db), limit: int = 5,
                    skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).\
        limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema.PostResponse)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schema.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db),
           current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NO ID")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NOT ALLOWED")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.PostResponse)
def update_post(id: str, new_post: schema.PostCreate,
                db: Session = Depends(get_db),
                current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NO ID")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not allowed to do this action")
    post_query.update(new_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

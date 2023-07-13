from .. import models, schema
from fastapi import status, HTTPException, Depends
from fastapi import APIRouter
from ..utils import generate_password
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users", tags=["USERS"]
    )


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    hashed_password = generate_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NO ID EXISTS")
    return user


@router.get("/", response_model=List[schema.UserResponse])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema, models
from .. import utils, oauth2


router = APIRouter(
    tags=["AUTH"]
)


@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email ==
                                        user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    respond = utils.verify(user_credentials.password, user.password)
    if not respond:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    # create a token

    key = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token":  key,
            "token_type": "bearer"}

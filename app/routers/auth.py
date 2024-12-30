from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=['Authorization'])

@router.post('/login', response_model=schemas.Token)
def login(LoginUser: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).where(models.User.email == LoginUser.username).filter().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(LoginUser.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    jwt_token = oauth2.create_access_token(data={'ID':user.id})
    
    return {'access_token':jwt_token, 'token_type':'Bearer'}

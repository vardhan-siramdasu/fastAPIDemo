from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import schemas, models, utils

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/createUser', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def Create_Users(user : schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/getUser/{id}', response_model=schemas.UserOut)
def Get_User(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).where(models.User.id == id).filter().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user
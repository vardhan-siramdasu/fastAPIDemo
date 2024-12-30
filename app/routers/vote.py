from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database, oauth2

router = APIRouter(prefix='/votes', tags=['Votes'])

@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), user_id: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).where(models.Post.id == vote.postId).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Post with id {vote.postId} not found')
    
    vote_querry = db.query(models.Vote).where(models.Vote.userId == user_id.id and models.Vote.postId == vote.postId)
    found_vote = vote_querry.first()
    if not found_vote:
        new_vote = models.Vote(postId = vote.postId, userId = user_id.id)
        db.add(new_vote)
        db.commit()
        return {'message': f'vote added for post :{vote.postId}'}
    else:
        db.delete(found_vote)
        db.commit()
        return {'message': f'vote removed for post : {vote.postId}'}


from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import engine, get_db
from .. import schemas, models, oauth2

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.post('/CreatePost', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def Create_posts(post : schemas.CreatePost, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(new_post.title, new_post.content, new_post.published))
    #post = cursor.fetchone()
    #con.commit()
    ##new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(userId=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@router.get('/GetAllPosts', response_model=List[schemas.Post])
@router.get('/GetAllPosts', response_model=List[schemas.PostOut])
def Get_all_posts(db: Session=Depends(get_db), userId: int = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ''  ):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #print(userId, limit, skip, search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    all_posts =  db.query(models.Post, func.count(models.Vote.postId).label('votes')).join(models.Vote, models.Vote.postId == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return all_posts

#@router.get('/GetPost/{id}', response_model=schemas.Post)
@router.get('/GetPost/{id}', response_model=schemas.PostOut)
def Get_posts(id, db: Session = Depends(get_db)):#response : Response
    #cursor.execute("""SELECT * FROM posts WHERE title = '{0}' """.format(title))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    all_posts =  db.query(models.Post, func.count(models.Vote.postId).label('votes')).join(models.Vote, models.Vote.postId == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not all_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        #response.status_code = status.http_404_not_found
        #return {data:'post not found'}
    return all_posts

@router.delete('/DeletePost/{id}')#status_code=status.HTTP_204_NO_CONTENT)
def Delete_post(id, db: Session = Depends(get_db), userId: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE title = '{0}' RETURNING *""".format(title))
    #post = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id)
    post = posts.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.userId != int(userId.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not authorized to perform this operation')
    
    posts.delete(synchronize_session=False)
    db.commit()
    return {'message':'deleted successfully'}

@router.put('/UpdatePost/{id}', response_model=schemas.Post)
def Update_post(id, post : schemas.CreatePost, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE title = %s RETURNING *""", (post.title, post.content, post.published, post.title))
    #updated_post = cursor.fetchone()
    #con.commit()
    postQuerry = db.query(models.Post).filter(models.Post.id == id)

    if postQuerry.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    postQuerry.update(post.dict(),synchronize_session=False)
    db.commit()

    return postQuerry.first()

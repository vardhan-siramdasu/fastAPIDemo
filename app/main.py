from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.base.metadata.create_all(bind=engine) : not needed as we using alembic for migrations

app = FastAPI()

origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'message' : 'Route hit!!!'}

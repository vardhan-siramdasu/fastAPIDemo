from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from app.config import settings

URL = 'postgresql://postgres:GSLVmk(3)@localhost/FastAPIDemo'

engine = create_engine(URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# import psycopg2
# from psycopg2.extras import RealDictCursor #to get coloumn names
# import time as t

# while True:
#     try:
#         con = psycopg2.connect(host='localhost', database='FastAPIDemo', user='postgres',
#                                password='GSLVmk(3)', cursor_factory=RealDictCursor)
#         cursor = con.cursor()
#         print('database connection success !')
#         break
#     except Exception as e:
#         print('database connection failed !')
#         print('error', e)
#         t.sleep(2)
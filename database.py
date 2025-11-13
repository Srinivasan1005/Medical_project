from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL="postgresql://postgres:Postsql123@localhost:5432/fastapi"

engine=create_engine(DATABASE_URL)

Sesssionlocal= sessionmaker(bind=engine,autoflush=False)

Base=declarative_base()

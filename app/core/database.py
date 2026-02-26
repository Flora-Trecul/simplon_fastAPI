
from sqlalchemy import create_engine
from app.models.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


engine= create_engine("sqlite:///app/data/simplon.db")

Base.metadata.create_all(engine)

def get_db():
    with Session(engine) as db:
        yield db


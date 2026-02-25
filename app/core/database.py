
from sqlalchemy import create_engine
from app.models.models import Base

engine= create_engine("sqlite:///data/simplon.db")
Base.metadata.create_all(engine)
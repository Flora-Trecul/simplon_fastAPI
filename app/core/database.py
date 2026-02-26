import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base

db_url = "sqlite:///app/data/simplon.db"

engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# On crée la database avec la commande 'python -m app.core.database --create-db' dans le terminal depuis la racine
if __name__ == "__main__":
    if "--create-db" in sys.argv:
        Base.metadata.create_all(engine)

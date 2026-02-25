import sys
from sqlalchemy import create_engine
from app.models.models import Base


# On crée la database avec la commande 'python -m app.core.database --create-db' dans le terminal depuis la racine
if __name__ == "__main__":
    if "--create-db" in sys.argv:

        db_url = "sqlite:///app/data/simplon.db"
        engine = create_engine(db_url)

        Base.metadata.create_all(engine)
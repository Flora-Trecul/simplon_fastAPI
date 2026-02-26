import sys
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.models.models import Base


db_url = "sqlite:///app/data/simplon.db"
engine = create_engine(db_url)


# On crée la database avec la commande 'python -m app.core.database --create-db' dans le terminal depuis la racine
if __name__ == "__main__":
    if "--create-db" in sys.argv:
        Base.metadata.create_all(engine)


@event.listens_for(Session, "do_orm_execute")
def add_deactivated_filter(execute_state):
    if (execute_state.is_select and not execute_state.execution_options.get("include_deleted", False)):
        execute_state.statement = execute_state.statement.filter_by(is_deleted = False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
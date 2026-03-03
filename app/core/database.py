import sys
from sqlalchemy import create_engine, event
from app.models.models import Base
from sqlalchemy.orm import Session


engine = create_engine("sqlite:///app/data/simplon.db")

def get_db():
    with Session(engine) as db:
        yield db


@event.listens_for(Session, "do_orm_execute")
def add_deactivated_filter(execute_state):
    if (execute_state.is_select and not execute_state.execution_options.get("include_deleted", False)):
        for mapper in execute_state.all_mappers:
            if "deleted_at" in mapper.column_attrs:
                execute_state.statement = execute_state.statement.filter_by(deleted_at = None)


# On crée la database avec la commande 'python -m app.core.database --create-db' dans le terminal depuis la racine
if __name__ == "__main__":
    if "--create-db" in sys.argv:
        Base.metadata.create_all(engine)
        



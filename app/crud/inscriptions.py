from sqlalchemy.orm import Session
from app.schemas.inscriptions import InscriptionCreate
from app.models.models import Inscription, LearningSession,  User

def create_inscription(db:Session, inscription: InscriptionCreate):
    
    learning_session= db.query(LearningSession).filter(LearningSession.id == inscription.session_id).first()
    if not learning_session:
        raise ValueError("Cette session n'existe pas.")
    
    is_registered = db.query(Inscription).filter(Inscription.user_id == inscription.user_id,
                                              Inscription.session_id == inscription.session_id).first()
    if is_registered:
        raise ValueError("L'apprenant est déjà inscrit dans cette session.")
    
    capacity = db.query(Inscription).filter(Inscription.session_id == inscription.session_id).count()
    
    if capacity >= learning_session.max_capacity:
        raise ValueError("La session est déjàa complète.")
    
    inscription = Inscription(**inscription.model_dump())
    db.add(inscription)
    db.commit()
    db.refresh(inscription)
    return inscription

def get_all_sessions(db: Session, user_id: int):
    inscriptions = db.query(Inscription).filter(Inscription.user_id == user_id).all()
    sessions = [inscription.learning_sessions for inscription in inscriptions]
    return sessions

def get_all_users(db: Session, session_id: int):
    inscriptions = db.query(Inscription).filter(Inscription.session_id == session_id).all()
    users = [inscription.user for inscription in inscriptions]
    return users

def delete_inscription(db: Session, user_id: int, session_id: int):
    inscription = db.query(Inscription).filter(Inscription.user_id == user_id,
                                              Inscription.session_id == session_id).first()
    if not inscription:
        return None
    db.delete(inscription)
    db.commit()
    return inscription

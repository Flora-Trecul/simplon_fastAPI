# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.models.models import User, LearningSession, Inscription
from app.schemas.users import UserCreate, UserUpdate
from fastapi import HTTPException, status
from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session, name: str | None = None, role: str | None = None):
    query = db.query(User)

    if name:
        query = query.filter(
            or_(
                User.first_name.ilike(f"%{name}%"),
                User.last_name.ilike(f"%{name}%")
            )
        )
    if role:
        query = query.filter(User.role.ilike(f"%{role}%"))

    return query.all()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def soft_delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    if user.learning_sessions:
        user.deleted_at = datetime.now()
        db.add(user)
    else:
        db.delete(user)
    db.commit()
    return True

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    update_data = user_data.dict(exclude_unset=True)

    if update_data:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        db.query(User).filter(User.id == user_id).update(update_data)
        db.commit()
        db.refresh(user)

    return user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_all_sessions(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return user.learning_sessions

def create_inscription(db: Session, user_id: int, session_id: int):
    inscription = Inscription(user_id=user_id, session_id=session_id)
    db.add(inscription)
    db.commit()
    db.refresh(inscription)
    return inscription



def count_apprenant(db: Session, session_id: int) -> int:
    return (db.query(Inscription).join(User)
            .filter(
            Inscription.session_id == session_id,
            User.role == "apprenant"
         ).count())

def get_learning_session(db: Session, session_id: int):
    return db.query(LearningSession).filter(LearningSession.id == session_id).first()

def get_inscription(db: Session, user_id: int, session_id: int):
    return db.get(Inscription, {"user_id": user_id, "session_id": session_id})


def delete_inscription(db: Session, user_id: int, session_id: int):
    inscription = ( db.query(Inscription).filter(Inscription.user_id == user_id,Inscription.session_id == session_id,).first() )
    if not inscription:
        return None
    db.delete(inscription)
    db.commit()
    return inscription

# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.models.models import User, LearningSession, Inscription
from app.schemas.users import UserCreate, UserUpdate
from fastapi import HTTPException, status
from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="utilisateur introuvable")

        db.query(User).filter(User.id == user_id).update(update_data)
        db.commit()
        db.refresh(user)

    return user

def get_user_with_name(db: Session, user_name: str):
    stmt = select(User).where(
        or_(
            User.first_name.like(f"%{user_name}%"),
            User.last_name.like(f"%{user_name}%")
        )
    ).limit(5)
    return db.execute(stmt).scalars().all()

def get_user_role(db: Session, role: str):
    stmt = select(User).where(User.role.like(f"%{role}%"))
    return db.execute(stmt).scalars().all()

def get_all_sessions(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="utilisateur introuvable")
    return user.learning_sessions

def create_inscription(db: Session, user_id: int, session_id: int):
    inscription = Inscription(user_id=user_id, session_id=session_id)
    db.add(inscription)
    db.commit()
    db.refresh(inscription)
    return inscription

def count_inscriptions(db: Session, session_id: int) -> int:
    return db.query(Inscription).filter(Inscription.session_id == session_id).count()

def get_learning_session(db: Session, session_id: int):
    return db.query(LearningSession).filter(LearningSession.id == session_id).first()

def get_inscription(db: Session, user_id: int, session_id: int):
    return db.get(Inscription, {"user_id": user_id, "session_id": session_id})

def delete_session(db: Session, user_id: int, session_id: int):
    inscription = db.get(Inscription, {"user_id": user_id, "session_id": session_id})
    if inscription:
        db.delete(inscription)
        db.commit()
    return inscription


# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.models.models import User, LearningSession, Inscription
from app.schemas.users import UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_learning_session(db: Session, session_id: int):
    return db.query(LearningSession).filter(LearningSession.id == session_id).first()

def get_inscription(db: Session, user_id: int, session_id: int):
    return db.get(Inscription, {"user_id": user_id, "session_id": session_id})

def get_user_with_name(db: Session, user_name: str):
    stmt = select(User).where(
        or_(
            User.first_name.like(f"%{user_name}%"),
            User.last_name.like(f"%{user_name}%")
        )
    ).limit(5)
    return db.execute(stmt).scalars().all()

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

def create_inscription(db: Session, user_id: int, session_id: int):
    inscription = Inscription(user_id=user_id, session_id=session_id)
    db.add(inscription)
    db.commit()
    db.refresh(inscription)
    return inscription
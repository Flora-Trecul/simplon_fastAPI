# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import User
from app.schemas.users import UserCreate, UserRead, UserUpdate


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

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.email = user_data.email
        user.role = user_data.role
        db.commit()
        db.refresh(user)
    return user
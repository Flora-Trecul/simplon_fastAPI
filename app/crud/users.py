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
    update_data = user_data.dict(exclude_unset=True)

    if update_data:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        db.query(User).filter(User.id == user_id).update(update_data)
        db.commit()
        db.refresh(user)

    return user
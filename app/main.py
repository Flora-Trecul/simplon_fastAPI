from fastapi import FastAPI
from typing import List
from app.schemas.users import UserRead, UserCreate, UserUpdate, UserBase
from app.crud.users import get_all_users, get_user, get_user, create_user as crud_create_user, update_user as crud_update_user, delete_user as crud_delete_user
from app.core.database import get_db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import User

app = FastAPI()

@app.get('/')
def welcome():
    return {'message': 'Welcome to my FastAPI application'}

@app.get("/usersAll", response_model=List[UserRead])
def read_users(db: Session = Depends(get_db)):
    users = get_all_users(db=db)
    return users

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.email == user.email).first()
    if exist_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_create_user(db=db, user=user)

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = crud_update_user(db=db, user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_delete_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}



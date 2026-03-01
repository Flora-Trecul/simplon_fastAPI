from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.users import UserResponse, UserCreate, UserUpdate
from app.crud.users import get_session,get_inscription,create_inscription,get_all_users,get_user,get_user_with_name, create_user as crud_create_user, update_user as crud_update_user, delete_user as crud_delete_user
from app.core.database import get_db
from app.models.models import User, LearningSession, Inscription

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/all", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = get_all_users(db=db)
    return users

@router.get("/id/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user

@router.get("/name/{user_name}", response_model=List[UserResponse])
def read_user(user_name: str, db: Session = Depends(get_db)):
    users = get_user_with_name(db=db, user_name=user_name)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return users

@router.post(
        "/", 
        response_model=UserResponse, 
        status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    exist_email = db.query(User).filter(User.email == user.email).first()
    if exist_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email existe déjà")
    return crud_create_user(db=db, user=user)

@router.patch("/id/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = crud_update_user(db=db, user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user

@router.delete("/id/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_delete_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return {"message": "User deleted"}


@router.post("/id/{user_id}/session/{session_id}", status_code=201)
def inscription(user_id: int, session_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    session = get_session(db, session_id)
    if not user or not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur ou session introuvable")

    exist_inscription = get_inscription(db, user_id, session_id)
    if exist_inscription:
        raise HTTPException(status_code=400, detail="Utilisateur déjà inscrit")

    create_inscription(db, user_id, session_id)
    return {"message": "Utilisateur inscrit avec succès"}

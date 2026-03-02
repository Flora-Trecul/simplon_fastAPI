from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.learning_sessions import LSResponse
from app.schemas.users import UserRead, UserCreate, UserUpdate
from app.crud.users import get_all_users, create_user as crud_create_user, get_user, update_user as crud_update_user, soft_delete_user as crud_delete_user, get_all_sessions, get_inscription, get_learning_session, count_inscriptions, create_inscription
from app.core.database import get_db
from app.models.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/All", response_model=List[UserRead])
def read_users(db: Session = Depends(get_db)):
    users = get_all_users(db=db)
    return users

@router.get("/id/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user

@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.email == user.email).first()
    if exist_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_create_user(db=db, user=user)

@router.patch("/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = crud_update_user(db=db, user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud_delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.post("/id/{user_id}/session/{session_id}", status_code=201)
def inscription(user_id: int, session_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    session = get_learning_session(db, session_id)
    if not user or not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur ou session introuvable")

    exist_inscription = get_inscription(db, user_id, session_id)
    if exist_inscription:
        raise HTTPException(status_code=400, detail="Utilisateur déjà inscrit")
    
    current_count = count_inscriptions(db, session_id)
    if current_count >= session.max_capacity:
        raise HTTPException(status_code=400, detail="Capacité maximale atteinte pour cette session")

    create_inscription(db, user_id, session_id)
    return {"message": "Utilisateur inscrit avec succès"}

@router.get("/id/{user_id}/sessions", response_model=List[LSResponse])
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = get_all_sessions(db, user_id)
    if not sessions:
        raise HTTPException(status_code=404, detail="User not found")
    return sessions
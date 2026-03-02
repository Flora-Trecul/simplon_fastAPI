from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.learning_sessions import LSResponse
from app.schemas.users import UserResponse, UserCreate, UserUpdate
from app.crud.users import get_user_role, delete_session as crud_delete_session,get_learning_session,get_all_sessions,count_inscriptions,get_inscription,create_inscription,get_all_users,get_user,get_user_with_name, create_user as crud_create_user, update_user as crud_update_user, delete_user as crud_delete_user
from app.core.database import get_db
from app.models.models import User, LearningSession, Inscription
from app.schemas.learning_sessions import LSFull
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = get_all_users(db=db)
    return users



@router.get("/{user_id}", response_model=UserResponse)
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

@router.get("/role/{role}", response_model=List[UserResponse])
def read_user(role: str, db: Session = Depends(get_db)):
    users = get_user_role(db=db, role=role)
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

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = crud_update_user(db=db, user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_delete_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return {"message": "Utilisateur supprimé"}

@router.delete("/{user_id}/session/{session_id}")
def delete_session(user_id: int, session_id: int, db: Session = Depends(get_db)):
    session = crud_delete_session(db=db, user_id=user_id, session_id=session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session introuvable")
    return {"message": "Inscription supprimée avec succès"}


@router.post("/{user_id}/inscription", status_code=status.HTTP_201_CREATED)
def inscription(user_id: int, data: dict, db: Session = Depends(get_db)):
    session_id = data.get("session_id")
    if not session_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="session_id est requis")

    user = get_user(db, user_id)
    session = get_learning_session(db, session_id)
    if not user or not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur ou session introuvable")

    exist_inscription = get_inscription(db, user_id, session_id)
    if exist_inscription:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Utilisateur déjà inscrit")

    if user.role == "apprenant":
        current_count = count_inscriptions(db, session_id)
        if current_count >= session.max_capacity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Capacité maximale atteinte pour cette session")

    create_inscription(db, user_id, session_id)
    return {"message": "Utilisateur inscrit avec succès"}


@router.get("/{user_id}/sessions", response_model=List[LSFull])
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = get_all_sessions(db, user_id)
    return sessions

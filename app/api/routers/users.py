from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from typing import List
from sqlalchemy.orm import Session
from app.schemas.learning_sessions import LSResponse
from app.schemas.users import UserResponse, UserCreate, UserUpdate
from app.core.database import get_db
from app.models.models import User, LearningSession, Inscription
from app.crud import users as crud


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[UserResponse])
def read_users(
    name: str | None = None,
    role: str | None = None,
    db: Session = Depends(get_db)):
    return crud.get_all_users(db, name=name, role=role)

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user

@router.get("/name/{user_name}", response_model=List[UserResponse])
def read_user(user_name: str, db: Session = Depends(get_db)):
    users = get_user_with_name(db=db, user_name=user_name)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return users

@router.get("/role/{role}", response_model=Page[UserResponse])
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
    exist_email = crud.get_user_by_email(db=db, email=user.email)
    if exist_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email existe déjà")
    return crud.create_user(db=db, user=user)

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db=db, user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.soft_delete_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return {"message": "Utilisateur supprimé"}


@router.delete("/{user_id}/session/{session_id}", status_code=status.HTTP_200_OK)
def delete_inscription(user_id: int, session_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    session = crud.get_learning_session(db, session_id)
    if not user or not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur ou session introuvable")
    inscription = crud.delete_inscription(db=db, user_id=user_id, session_id=session_id)
    if not inscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="inscription introuvable")
    return {"message": "Inscription supprimée avec succès"}


@router.post("/{user_id}/session/{session_id}", status_code=status.HTTP_201_CREATED)
def inscription(user_id: int, session_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    session = crud.get_learning_session(db, session_id)
    if not user or not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur ou session introuvable")

    exist_inscription = crud.get_inscription(db, user_id, session_id)
    if exist_inscription:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Utilisateur déjà inscrit")
    
    if user.role == "administrateur":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Un administrateur ne peut pas s'inscrire à une session")

    if user.role == "apprenant":
        current_count = crud.count_apprenant(db, session_id)
        if current_count >= session.max_capacity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Capacité maximale atteinte pour cette session")

    crud.create_inscription(db, user_id, session_id)
    return {"message": "Utilisateur inscrit avec succès"}


@router.get("/{user_id}/sessions", response_model=List[LSResponse])
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user.learning_sessions

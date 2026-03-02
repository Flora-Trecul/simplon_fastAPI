from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.inscriptions import InscriptionCreate, InscriptionRead
from app.schemas.users import UserResponse
from app.schemas.learning_sessions import LSShort
from app.crud import inscriptions as crud

router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"])

@router.post("/", response_model=InscriptionRead, status_code=201)
def create(data: InscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_inscription(db, data)

@router.get("/users/{user_id}/sessions", response_model=list[UserResponse]) # - after user implementation
def list_all_sessions(user_id:int, db: Session = Depends(get_db)):
    return crud.get_all_sessions(db, user_id)

@router.get("/sessions/{session_id}/users", response_model=list[LSShort]) # response_model=list[SessionRead] - after session being incremented
def list_all_users(session_id:int, db: Session = Depends(get_db)):
    return crud.get_all_users(db, session_id)

@router.delete("/{user_id}/{session_id}", status_code=204)
def delete(session_id: int, user_id:int, db: Session = Depends(get_db)):
    inscription = crud.delete_inscription(db, user_id, session_id)
    if not inscription:
        raise HTTPException(status_code=404, detail="Inscription non trouvé")
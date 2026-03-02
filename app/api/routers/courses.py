from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.courses import CourseCreate, CourseRead, CourseUpdate
from app.schemas.learning_sessions import LSResponse
from app.crud import courses as crud

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseRead, status_code=201)
def create(data: CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, data)

@router.get("/", response_model=list[CourseRead])
def list_all(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)

@router.get("/{course_id}", response_model=CourseRead)
def get_one(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return course

@router.get("/{course_id}/sessions", response_model = list[LSResponse])
def get_learning_sessions(course_id: int, db: Session = Depends(get_db)):
    sessions = crud.get_course_learning_sessions(db, course_id)
    if not sessions:
        raise HTTPException(status_code=404, detail="Ressource introuvable")
    return sessions

@router.patch("/{course_id}", response_model=CourseRead)
def update(course_id: int, data: CourseUpdate, db: Session = Depends(get_db)):
    course = crud.update_course(db, course_id, data)
    if not course:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return course

@router.delete("/{course_id}", status_code=204)
def delete(course_id: int, db: Session = Depends(get_db)):
    success = crud.soft_delete_course(db, course_id)
    if not success:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return None

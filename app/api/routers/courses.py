from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.courses import CourseCreate, CourseRead, CourseUpdate
from app.crud import courses as crud

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseRead, status_code=201)
def create(data: CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, data)

@router.get("/", response_model=list[CourseRead])
def list_all(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)

@router.get("/{id}", response_model=CourseRead)
def get_one(id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course non trouvé")
    return course

@router.patch("/{id}", response_model=CourseRead)
def update(id: int, data: CourseUpdate, db: Session = Depends(get_db)):
    course = crud.update_course(db, id, data)
    if not course:
        raise HTTPException(status_code=404, detail="Course non trouvé")
    return course

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    course = crud.delete_course(db, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course non trouvé")
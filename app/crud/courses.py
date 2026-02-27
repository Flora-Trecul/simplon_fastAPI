from sqlalchemy.orm import Session
from app.schemas.courses import CourseCreate, CourseUpdate
from app.models.models import Course

def create_course(db:Session, course: CourseCreate):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, courses_id: int):
    return db.query(Course).filter(Course.id == courses_id).first()

def get_all_courses(db: Session, skip: int =0, limit: int =100):
    return db.query(Course).offset(skip).limit(limit).all()

def update_course(db: Session, courses_id: int, course: CourseUpdate):
    db_course = get_course(db, courses_id)
    if not db_course:
        return None
    
    for field, value in course.model_dump(exclude_unset=True).items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, courses_id:int):
    db_course = get_course(db, courses_id)
    if not db_course:
        return None
    db.delete(db_course)
    db.commit()
    return db_course
        
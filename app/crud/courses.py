from sqlalchemy.orm import Session
from app.schemas.courses import CourseCreate, CourseUpdate
from app.models.models import Course
from datetime import datetime

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

def get_course_learning_sessions(db: Session, courses_id: int):
    db_course = get_course(db, courses_id)
    if not db_course:
        return None
    
    return db_course.learning_sessions

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

def soft_delete_course(db: Session, courses_id:int):
    db_course = get_course(db, courses_id)
    if not db_course:
        return False
    if db_course.learning_sessions:
        db_course.deleted_at = datetime.now()
        db.add(db_course)
    else:
        db.delete(db_course)
    db.commit()
    return True
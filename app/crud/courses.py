from sqlalchemy.orm import Session
from app.schemas.courses import CourseCreate, CourseUpdate
from app.models.models import Course

def create_course(db:Session, course: CourseCreate):
    course = Course(**course.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def get_course(db: Session, courses_id: int):
    return db.query(Course).filter(Course.id == courses_id).first()

def get_all_courses(db: Session, skip: int =0, limit: int =100):
    return db.query(Course).offset(skip).limit(limit).all()

def update_course(db: Session, courses_id: int, course: CourseUpdate):
    course = get_course(db, courses_id)
    if not course:
        return None
    
    for field, value in course.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course

def delete_course(db: Session, courses_id:int):
    course = get_course(db, courses_id)
    if course:
        db.delete(course)
        db.commit()
    return course
        
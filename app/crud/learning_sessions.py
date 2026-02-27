from sqlalchemy.orm import Session
from app.models.models import LearningSession
from app.schemas.learning_sessions import LSCreate, LSUpdate
from datetime import date, datetime


def get_one_ls(db: Session, ls_id: int) -> LearningSession:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()

	if not db_ls:
		return None
	
	return db_ls


def get_all_ls(db: Session) -> list[LearningSession]:
	db_ls = db.query(LearningSession).all()

	if not db_ls:
		return None
	
	return db_ls


def get_one_ls_by_course_dates(db: Session, course_id: int, start_date: date, end_date: date):
	db_ls = db.query(LearningSession).filter(
		LearningSession.course_id == course_id,
		LearningSession.start_date == start_date,
		LearningSession.end_date == end_date
	).first()

	return db_ls


def create_ls(db: Session, schema: LSCreate):
	ls_data = schema.model_dump()
	ls_valid_data = {key: value for key, value in ls_data.items() if key in LearningSession.__table__.columns}

	db_ls = LearningSession(**ls_valid_data)

	db.add(db_ls)
	db.commit()
	db.refresh(db_ls)
	return db_ls


def update_ls(db: Session, ls_id: int, schema: LSUpdate) -> LearningSession:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()

	if not db_ls:
		return None
	
	updated_data = schema.model_dump(exclude_unset=True)

	for field, value in updated_data.items():
		setattr(db_ls, field, value)
	
	db.add(db_ls)
	db.commit()
	db.refresh(db_ls)
	return db_ls


def delete_ls(db: Session, ls_id:int) -> bool:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()
	
	if not db_ls:
		return False
	
	db.delete(db_ls)
	db.commit()
	return True


def deactivate_ls(db: Session, ls_id:int) -> bool:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()
	
	if not db_ls:
		return False
	
	db_ls.deleted_at = datetime.now()
	db.add(db_ls)
	db.commit()
	return True


def get_all_ls_including_deleted(db: Session) -> list[LearningSession]:
	db_ls = db.query(LearningSession).execution_options(include_deleted = True).all()

	if not db_ls:
		return None
	
	return db_ls
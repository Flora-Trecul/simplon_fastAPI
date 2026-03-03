from sqlalchemy.orm import Session
from app.models.models import LearningSession, User
from app.schemas.learning_sessions import LSCreate, LSUpdate
from datetime import date, datetime


def get_one_ls(db: Session, ls_id: int) -> None | LearningSession:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()

	if not db_ls:
		return None
	
	return db_ls


def get_all_ls(db: Session) -> None | list[LearningSession]:
	db_ls = db.query(LearningSession).all()

	if not db_ls:
		return None
	
	return db_ls


def get_one_ls_by_course_dates(db: Session, course_id: int, start_date: date, end_date: date) -> None | LearningSession:
	db_ls = db.query(LearningSession).filter(
		LearningSession.course_id == course_id,
		LearningSession.start_date == start_date,
		LearningSession.end_date == end_date
	).first()

	if not db_ls:
		return None
	
	return db_ls


def get_ls_users(db: Session, ls_id: int) -> None | list[User]:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()

	if not db_ls:
		return None
	
	return db_ls.users


def create_ls(db: Session, schema: LSCreate) -> LearningSession:
	ls_data = schema.model_dump()
	ls_valid_data = {key: value for key, value in ls_data.items() if key in LearningSession.__table__.columns}

	db_ls = LearningSession(**ls_valid_data)

	db.add(db_ls)
	db.commit()
	db.refresh(db_ls)
	return db_ls


def update_ls(db: Session, ls_id: int, schema: LSUpdate) -> None | LearningSession:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()
	
	updated_data = schema.model_dump(exclude_unset=True)

	if "start_date" in updated_data or "end_date" in updated_data:
		start_date = updated_data.get("start_date", db_ls.start_date)
		end_date = updated_data.get("end_date", db_ls.end_date)

		if start_date >= end_date:
			return None

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


def soft_delete_ls(db: Session, ls_id:int) -> bool:
	db_ls = db.query(LearningSession).filter(LearningSession.id == ls_id).first()
	
	if not db_ls:
		return False
	
	if db_ls.users:
		db_ls.deleted_at = datetime.now()
		db.add(db_ls)
	else:
		db.delete(db_ls)

	db.commit()
	return True


def get_all_ls_including_deleted(db: Session) -> None | list[LearningSession]:
	db_ls = db.query(LearningSession).execution_options(include_deleted = True).all()

	if not db_ls:
		return None
	
	return db_ls
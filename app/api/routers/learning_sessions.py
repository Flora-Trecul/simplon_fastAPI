from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.learning_sessions import LSFull, LSShort, LSCreate, LSUpdate
from app.crud.learning_sessions import get_all_ls, get_one_ls, get_one_ls_by_course_dates, create_ls, delete_ls, update_ls


router = APIRouter(
	prefix="/learning-sessions",
	tags=["Learning Sessions"],
)


@router.get("/", response_model=list[LSShort])
async def read_learning_sessions(ls_id: int, db: Session = Depends(get_db)):
	db_ls = get_all_ls(db, ls_id)

	if not db_ls:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Ressource introuvable")
	
	return db_ls


@router.get("/{ls_id}", response_model=LSFull)
async def read_learning_session(ls_id: int, db: Session = Depends(get_db)):
	db_ls = get_one_ls(db, ls_id)

	if not db_ls:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Ressource introuvable")
	
	return db_ls


@router.patch("/{ls_id}", response_model=LSFull)
async def udpate_learning_sessions(ls_id: int, schema: LSUpdate, db: Session = Depends(get_db)):
	db_ls = update_ls(db = db, ls_id = ls_id, schema = schema)

	if not db_ls:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Ressource introuvable")

	return db_ls


@router.post("/", response_model=LSFull, status_code = status.HTTP_201_CREATED)
async def create_learning_session(schema: LSCreate, db: Session = Depends(get_db)):
	existing_ls = get_one_ls_by_course_dates(
		db,
		course_id = schema.course_id,
		start_date = schema.start_date,
		end_date = schema.end_date
	)

	if existing_ls:
		raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Cette session de formation existe déjà.")

	return create_ls(db = db, schema = schema)


@router.delete("/{ls_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_learning_session(ls_id: int, db: Session = Depends(get_db)):
	success = delete_ls(db = db, ls_id = ls_id)

	if not success:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Ressource introuvable")

	return None
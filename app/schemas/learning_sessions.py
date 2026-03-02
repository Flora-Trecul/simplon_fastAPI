from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date


class LSBase(BaseModel):
	start_date: date
	end_date: date
	max_capacity: int = Field(ge=1, le=50)
	course_id: int = Field(ge=0)

	@model_validator(mode="after")
	def validate_dates(self):
		if self.start_date >= self.end_date:
			raise ValueError("La date de fin doit être supérieure à la date de début.")
		return self


class LSCreate(LSBase):
	pass


class LSUpdate(BaseModel):
	start_date: Optional[date] = None
	end_date: Optional[date] = None
	max_capacity: Optional[int] = Field(None, ge=1, le=50)
	courses_id: Optional[int] = Field(None, ge=0)


class LSResponse(LSBase):
	id: int = Field(ge=0)

	class Config:
		from_attributes = True
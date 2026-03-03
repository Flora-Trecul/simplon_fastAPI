from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum

class EnumLevel(str, Enum):
    begginer = "débutant"
    intermediary = "intermédiaire"
    advanced = "avancé" 

class Coursebase(BaseModel):
    title: str = Field(..., min_length=2)
    duration: int = Field(..., gt=0)
    description: str | None = None
    level: EnumLevel
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls,title):
        if not title.strip():
            raise ValueError("Le titre n'est peut pas être vide.")
        return title.strip()

class CourseCreate(Coursebase):
    pass

class CourseUpdate(BaseModel):
    title: str | None  = Field(None, min_length=2)
    duration: int | None = Field(None, gt=0)
    description: str | None = Field(None)
    level: EnumLevel | None =  None
    
class CourseRead(Coursebase):
    id: int
   
    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import date
from enum import Enum

class RoleEnum(str, Enum):
    administrateur = "administrateur"
    formateur = "formateur"
    apprenant = "apprenant"

class UserBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(max_length=120)
    role: RoleEnum
    inscription_date: Optional[date] = Field(default_factory=date.today)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    inscription_date: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    inscription_date: Optional[datetime] = Field(default_factory=datetime.utcnow)


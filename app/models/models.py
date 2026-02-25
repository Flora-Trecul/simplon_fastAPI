from sqlalchemy import String, DateTime, Integer, Enum, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    role: Mapped[str] = mapped_column(Enum("administrateur", "formateur", "apprenant"))
    inscription_date: Mapped[datetime] = mapped_column(DateTime)
    
    sessions: Mapped[List["Session"]] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r},lastname={self.lastname!r},firstname={self.firstname!r})"

class Session(Base):
    __tablename__= "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    max_capacity: Mapped[int] = mapped_column(Integer)
    courses_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    
    user: Mapped[List["User"]] = relationship(back_populates="sessions")
    course: Mapped["Course"] = relationship(back_populates="sessions")
    
class Course(Base):
    __tablename__= "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]]
    level: Mapped[str] = mapped_column(Enum("débutant", "intermédiaire", "avancé"))

    sessions: Mapped[List["Session"]] = relationship(back_populates="course")
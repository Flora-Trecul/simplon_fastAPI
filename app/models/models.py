from sqlalchemy import String, DateTime, Integer, Enum, ForeignKey, UniqueConstraint
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
    # deleted_at: Mapped[datetime] = mapped_column(DateTime)
    
    learning_sessions: Mapped[List["LearningSession"]] = relationship(secondary="inscriptions", back_populates="users", viewonly=True)
    ls_assoc: Mapped[List["Inscription"]] = relationship(back_populates="user",  cascade='all, delete')
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r},lastname={self.lastname!r},firstname={self.firstname!r})"

class LearningSession(Base):
    __tablename__= "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    max_capacity: Mapped[int] = mapped_column(Integer)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    # deleted_at: Mapped[datetime] = mapped_column(DateTime)
    
    course: Mapped["Course"] = relationship(back_populates="learning_sessions")
    user_assoc : Mapped[List["Inscription"]] = relationship(back_populates="learning_session",  cascade='all, delete')
    users : Mapped[List["User"]] = relationship(secondary= "inscriptions", back_populates="learning_sessions",viewonly=True)
    
    __table_args__ = (
        UniqueConstraint("course_id", "start_date", "end_date", name = "course_dates_uc"),
        )

class Course(Base):
    __tablename__= "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]]
    level: Mapped[str] = mapped_column(Enum("débutant", "intermédiaire", "avancé"))
    # deleted_at: Mapped[datetime] = mapped_column(DateTime)
     
    learning_sessions: Mapped[List["LearningSession"]] = relationship(back_populates="course")
    
class Inscription(Base):
    __tablename__= "inscriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True)
    
    user: Mapped["User"] = relationship(back_populates="ls_assoc")
    learning_session: Mapped["LearningSession"] = relationship(back_populates="user_assoc")

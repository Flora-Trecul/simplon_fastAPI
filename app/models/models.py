from sqlalchemy import String, Date, DateTime, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date, datetime
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
    inscription_date: Mapped[date] = mapped_column(Date)
    
    learning_sessions: Mapped[List["LearningSession"]] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r},lastname={self.lastname!r},firstname={self.firstname!r})"


class LearningSession(Base):
    __tablename__= "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    max_capacity: Mapped[int] = mapped_column(Integer)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    deleted_at: Mapped[datetime] = mapped_column(DateTime)
    
    user: Mapped[List["User"]] = relationship(back_populates="learning_sessions")
    course: Mapped["Course"] = relationship(back_populates="learning_sessions")

    __table_args__ = (
        UniqueConstraint("course_id", "start_date", "end_date", name = "course_dates_uc")
        )


class Course(Base):
    __tablename__= "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]]
    level: Mapped[str] = mapped_column(Enum("débutant", "intermédiaire", "avancé"))

    learning_sessions: Mapped[List["LearningSession"]] = relationship(back_populates="course")
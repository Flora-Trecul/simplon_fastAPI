from __future__ import annotations
from sqlalchemy import String, DateTime, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(Enum("administrateur", "formateur", "apprenant"), nullable=False)
    inscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)    
    
    learning_sessions: Mapped[List[Inscription]] = relationship(back_populates="user")


class LearningSession(Base):
    __tablename__= "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    max_capacity: Mapped[int] = mapped_column(Integer)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    
    course: Mapped[Course] = relationship(back_populates="learning_sessions")
    users : Mapped[List[Inscription]] = relationship(back_populates="learning_session")
    
    __table_args__ = (
        UniqueConstraint("course_id", "start_date", "end_date", name = "course_dates_uc"),
        )
    
class Inscription(Base):
    __tablename__= "inscriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True)
    
    user: Mapped[User] = relationship(back_populates="learning_sessions")
    learning_session: Mapped[LearningSession] = relationship(back_populates="users")

class Course(Base):
    __tablename__= "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]]
    level: Mapped[str] = mapped_column(Enum("débutant", "intermédiaire", "avancé"))

    learning_sessions: Mapped[List[LearningSession]] = relationship(back_populates="course")
    
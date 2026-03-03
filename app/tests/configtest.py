import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models.models import Base, Course, LearningSession, User, Inscription
from datetime import date

# Configuration d'une database SQLite en mémoire (StaticPool conserve les données entre deux connexions)
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Création / destruction de la base de test
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# Simulation d'appels à l'API en utilisant la base de test
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_course(db_session):
    course = Course(
        title = "Dev IA",
        description = "Formation développeur en intelligence artificielle",
        duration = 1600,
        level = "avancé"
    )
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    return course

@pytest.fixture
def sample_session_1(db_session, sample_course):
    session = LearningSession(
        title = "Dev IA 2025-2026", 
        course_id = sample_course.id,
        start_date = date(2025, 11, 17),
        end_date = date(2026, 6, 30)
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session

@pytest.fixture
def sample_session_2(db_session, sample_course):
    session = LearningSession(
        title = "Dev IA 2024-2025", 
        course_id = sample_course.id,
        start_date = date(2024, 9, 15),
        end_date = date(2025, 12, 31)
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session

@pytest.fixture
def sample_user(db_session):
    user = User(
        first_name = 'Charles-Henri',
        last_name = 'Tudor',
        email = 'ch.tudor@example.com',
        role = 'apprenant',
        inscription_date = date.today()
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def sample_inscription(db_session, sample_session_1, sample_user):
    inscription = User(
        user_id = sample_session_1.id,
        session_id = sample_user.id
    )
    db_session.add(inscription)
    db_session.commit()
    db_session.refresh(inscription)
    return inscription


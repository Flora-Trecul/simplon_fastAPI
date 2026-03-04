import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import date

from app.main import app
from app.core.database import get_db
from app.models.models import Base, User, LearningSession, Course, Inscription



db_url_test = "sqlite:///app/data/test.db"

engine_test = create_engine(db_url_test, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Crée le schéma avant tous les tests, le supprime après."""
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)


@pytest.fixture(scope="function")
def db():
    """Session isolée par test — rollback automatique après chaque test."""
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    """TestClient qui utilise la session de test."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def apprenant_data():
    return {
        "first_name": "Alice",
        "last_name": "Dupont",
        "email": "alice@test.com",
        "role": "apprenant",
        "inscription_date": str(date.today()),
    }

@pytest.fixture()
def formateur_data():
    return {
        "first_name": "Bob",
        "last_name": "Martin",
        "email": "bob@test.com",
        "role": "formateur",
        "inscription_date": str(date.today()),
    }

@pytest.fixture()
def administrateur_data():
    return {
        "first_name": "Charlie",
        "last_name": "Admin",
        "email": "charlie@test.com",
        "role": "administrateur",
        "inscription_date": str(date.today()),
    }

@pytest.fixture
def course_data():
    return{
        "title": "Dévelopment IA",
        "description": "Dévelopoment IA et Data",
        "duration": 500,
        "level": "intermédiaire"        
            }


@pytest.fixture()
def created_apprenant(client, apprenant_data):
    response = client.post("/users/", json=apprenant_data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def created_formateur(client, formateur_data):
    response = client.post("/users/", json=formateur_data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def created_administrateur(client, administrateur_data):
    response = client.post("/users/", json=administrateur_data)
    assert response.status_code == 201
    return response.json()



@pytest.fixture()
def created_course(db):
    course = Course(
        title="Python avancé",
        duration=30,
        description="Formation Python",
        level="avancé",
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@pytest.fixture()
def created_session(db, created_course):
    session = LearningSession(
        start_date=date(2025, 6, 1),
        end_date=date(2025, 6, 30),
        max_capacity=2,
        course_id=created_course.id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

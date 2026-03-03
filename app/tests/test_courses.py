import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.main import app
from app.core.database import get_db
from fastapi.testclient import TestClient
from app.models.models import Base

db_url_test = "sqlite:///./test.db"

engine_test = create_engine(db_url_test, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# fixtures initialize test functions. They provide a fixed baseline so that tests execute reliably and produce consistent, repeatable results.
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)
    
@pytest.fixture(scope="function")
def db():
    """
    Create a new database session for each test and roll it back after the test.
    """
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db):
    """
    Provide a TestClient that uses the test database session.
    Override the get_db dependency to use the test session.
    """
    def override_get_db():
            yield db
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

#Tests pour le post
class TestCreateCouse:
    def test_create_course_success(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }

        response = client.post("/courses", json=payload)

        assert response.status_code == 201

        data = response.json()
        assert data["id"] is not None
        assert data["title"] == "Dévelopment IA"
        assert data["duration"] == 500
        assert data["level"] == "intermédiaire"

    def test_create_title_too_short(self, client):
        payload = {
            "title": "D",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        response = client.post("/courses", json=payload)

        assert response.status_code == 422

    def test_create_negative_duration(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": -5,
            "level": "intermédiaire"
        }
        response = client.post("/courses", json=payload)

        assert response.status_code == 422

    def test_create_duration_zero(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 0,
            "level": "intermédiaire"
        }
        response = client.post("/courses", json=payload)

        assert response.status_code == 422

    def test_nonexisting_level(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "advanced"
        }
        response = client.post("/courses", json=payload)

        assert response.status_code == 422

    def test_create_course_missing_tittle(self, client):
        payload = {
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        response = client.post("/courses", json=payload)

        assert response.status_code == 422

    def test_create_course_empty_tittle(self, client):
        payload = {
            "title": "        ",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        response = client.post("/courses", json=payload)

        assert response.status_code == 422

    def test_create_without_description(self, client):
        payload = {
            "title": "Dévelopment IA",
            "duration": 500,
            "level": "intermédiaire"
        }
        response = client.post("/courses", json=payload)
        assert response.status_code == 201
        assert response.json()["description"] == None

# Tests pour le get
class TestGetCourse:
    def test_get_all_courses_empty(self, client):
        response = client.get("/courses")
        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_get_all_courses(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        response = client.get("/courses")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1
    
    def test_get_course_by_id(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        course_id = create_formation.json()["id"]
        response = client.get(f"/courses/{course_id}")
        assert response.status_code == 200
        assert response.json()["id"] == course_id
    
    def test_get_course_not_found(self, client):
        
        response = client.get(f"/courses/777")
        assert response.status_code == 404
        assert response.json()["detail"] == "Formation non trouvée"
        
class TestCourseSession:
    def test_get_sessions_course_not_found(self, client):
        response = client.get("/courses/999/sessions")
        assert response.status_code == 404
        assert response.json()["detail"] == "Ressource introuvable"
    
    def test_get_course_without_sessions(self, client):
        payload = {
            "title": "Python",
            "description": "Cours Python",
            "duration": 40,
            "level": "intermédiaire"
        }

        create_course = client.post("/courses", json=payload)
        course_id = create_course.json()["id"]

        response = client.get(f"/courses/{course_id}/sessions")

        assert response.status_code == 404
    def test_get_courses_with_one_session(self, client):
        course_payload = {
            "title": "Python",
            "description": "Cours Python",
            "duration": 40,
            "level": "intermédiaire"
        }

        create_course = client.post("/courses", json=course_payload)
        course_id = create_course.json()["id"]

        session_payload = {
            "course_id": course_id,
            "start_date": "2025-06-01",
            "end_date": "2025-06-30",
            "max_capacity": 20
        }
        # client.post("/sessions", json=session_payload)
        create_session = client.post("/learning-sessions", json=session_payload)
        print(create_session.status_code)
        print(create_session.json())
        response = client.get(f"/courses/{course_id}/sessions")

        assert response.status_code == 200
        assert len(response.json()) == 1
    
    def test_get_courses_with_multiple_sessions(self, client):
        course_payload = {
            "title": "Data",
            "description": "Data Science",
            "duration": 60,
            "level": "avancé"
        }

        create_course = client.post("/courses", json=course_payload)
        course_id = create_course.json()["id"]

        for i in range(3):
            session_payload = {
                "course_id": course_id,
                "start_date": f"2025-07-0{i+1}",
                "end_date": f"2025-07-1{i+1}",
                "max_capacity": 15
            }
            client.post("/learning-sessions", json=session_payload)

        response = client.get(f"/courses/{course_id}/sessions")

        assert response.status_code == 200
        assert len(response.json()) == 3
        
# Tests pour le patch   
class TestUpdateCourse:
    def test_update_course_title(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        course_id = create_formation.json()["id"]
        response = client.patch(f"/courses/{course_id}", json={
            "title": "Apple Foundation Program"
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Apple Foundation Program"

    def test_update_course_duration(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        course_id = create_formation.json()["id"]
        response = client.patch(f"/courses/{course_id}", json={
            "duration": 80
        })
        assert response.status_code == 200
        assert response.json()["duration"] == 80

    def test_update_course_not_found(self, client):
        response = client.patch("/courses/999", json={"title": "Nouveau"})
        assert response.status_code == 404

    def test_update_course_invalid_duration(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        course_id = create_formation.json()["id"]
        response = client.patch(f"/courses/{course_id}", json={
            "duration": -5
        })
        assert response.status_code == 422

    def test_update_course_partial(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        course_id = create_formation.json()["id"]
        original_duration = create_formation.json()["duration"]
        response = client.patch(f"/courses/{course_id}", json={
            "title": "Nouveau titre"
        })
        assert response.status_code == 200
        assert response.json()["duration"] == original_duration

#Tests deleteclass TestDeleteCourse:
class TestDeleteCourse:
    def test_delete_course_success(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        course_id = create_formation.json()["id"]
        response = client.delete(f"/courses/{course_id}")
        assert response.status_code == 204

    def test_delete_course_not_found(self, client):
        response = client.delete("/courses/999")
        assert response.status_code == 404

# à voir avec la chose de deactivation
    def test_delete_course_really_deleted(self, client):
        payload = {
            "title": "Dévelopment IA",
            "description": "Dévelopoment IA et Data",
            "duration": 500,
            "level": "intermédiaire"
        }
        create_formation = client.post("/courses", json=payload)
        course_id = create_formation.json()["id"]
        client.delete(f"/courses/{course_id}")
        response = client.get(f"/courses/{course_id}")
        assert response.status_code == 404
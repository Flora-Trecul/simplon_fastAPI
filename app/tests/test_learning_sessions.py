import pytest
from pydantic import ValidationError
from app.schemas import learning_sessions as schema
from datetime import date, datetime
from app.models.models import Course, LearningSession, User, Inscription
from app.crud import learning_sessions as crud
from sqlalchemy.orm import Query


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
        course_id = sample_course.id,
        start_date = date(2025, 11, 17),
        end_date = date(2026, 6, 30),
        max_capacity = 13
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session

@pytest.fixture
def sample_session_2(db_session, sample_course):
    session = LearningSession(
        course_id = sample_course.id,
        start_date = date(2024, 9, 15),
        end_date = date(2025, 12, 31),
        max_capacity = 15
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
    inscription = Inscription(
        user_id = sample_user.id,
        session_id = sample_session_1.id
    )
    db_session.add(inscription)
    db_session.commit()
    db_session.refresh(inscription)
    return inscription


class TestSchemasLSCreate:

    def test_create_ls_with_valid_data_raises_no_error(self):
        data = {
            "course_id": 0,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 15
        }
        
        session = schema.LSCreate(**data)

        assert session.course_id == 0
        assert session.start_date == date.today()
        assert session.end_date == date(2027, 9, 30)
        assert session.start_date < session.end_date
        assert session.max_capacity == 15


    def test_create_ls_with_missing_field_raises_error(self):
        data = {
            "course_id": 0,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        errors = exc_info.value.errors()

        assert any(err["loc"] == ("max_capacity",) for err in errors)
        assert errors[0]["type"] == "missing"


    # --- Tests sur max_capacity ---

    def test_create_ls_max_capacity_too_low_raises_error(self):
        data = {
            "course_id": 10,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 0
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        assert any("max_capacity" in err["loc"] for err in exc_info.value.errors())


    def test_create_ls_max_capacity_too_high_raises_error(self):
        data = {
            "course_id": 0,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 51
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        assert any("max_capacity" in err["loc"] for err in exc_info.value.errors())


    def test_create_ls_max_capacity_float_raises_error(self):
        data = {
            "course_id": 0,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 15.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        assert any("max_capacity" in err["loc"] for err in exc_info.value.errors())


    def test_create_ls_max_capacity_str_raises_error(self):
        data = {
            "course_id": 0,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": "quinze"
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        assert any("max_capacity" in err["loc"] for err in exc_info.value.errors())


    # --- Tests sur course_id ---

    def test_create_ls_course_id_negative_raises_error(self):
        data = {
            "course_id": -1,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 15
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        assert any("course_id" in err["loc"] for err in exc_info.value.errors())


    def test_create_ls_course_id_float_raises_error(self):
        data = {
            "course_id": 2.5,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 15
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        assert any("course_id" in err["loc"] for err in exc_info.value.errors())


    def test_create_ls_course_id_str_raises_error(self):
        data = {
            "course_id": "deux",
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 15
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        assert any("course_id" in err["loc"] for err in exc_info.value.errors())


    # --- Tests sur les dates ---

    def test_create_ls_with_str_dates_is_valid(self):
        data = {
            "course_id": 0,
            "start_date": "2026-03-03",
            "end_date": "2027-09-30",
            "max_capacity": 15
        }

        session = schema.LSCreate(**data)

        assert session.start_date == date(2026, 3, 3)
        assert session.end_date == date(2027, 9, 30)


    def test_create_ls_with_same_day_dates_raises_error(self):
        data = {
            "course_id": 0,
            "start_date": date.today(),
            "end_date": date.today(),
            "max_capacity": 15
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        
        assert "La date de fin doit être supérieure à la date de début." in str(exc_info.value)


    def test_create_ls_with_incoherent_dates_raises_error(self):
        data = {
            "course_id": 0,
            "start_date": date.today(),
            "end_date": date(2025, 2, 2),
            "max_capacity": 15
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.LSCreate(**data)
        
        assert "La date de fin doit être supérieure à la date de début." in str(exc_info.value)


class TestSchemaLSUpdate:

    def test_update_ls_with_full_valid_data_raises_no_error(self):
        data = {
            "course_id": 1,
            "start_date": date.today(),
            "end_date": date(2027, 9, 30),
            "max_capacity": 15
        }
        
        session = schema.LSUpdate(**data)

        assert session.course_id == 1
        assert session.start_date == date.today()
        assert session.end_date == date(2027, 9, 30)
        assert session.start_date < session.end_date
        assert session.max_capacity == 15


    # --- Tests sur max_capacity ---

    def test_update_ls_max_capacity_updates_only_this_field(self):
        data = {"max_capacity": 15}

        update_schema = schema.LSUpdate(**data)
        dump = update_schema.model_dump(exclude_unset=True)

        assert dump == {"max_capacity": 15}
        assert "course_id" not in dump
        assert "start_date" not in dump
        assert "end_date" not in dump


    def test_update_ls_max_capacity_too_low_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(max_capacity=0)
        
        errors = exc_info.value.errors()
        assert "max_capacity" in errors[0]["loc"]
        assert "greater_than" in errors[0]["type"]


    def test_update_ls_max_capacity_too_high_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(max_capacity=51)
        
        errors = exc_info.value.errors()
        assert "max_capacity" in errors[0]["loc"]
        assert "less_than" in errors[0]["type"]


    def test_update_ls_max_capacity_float_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(max_capacity=15.5)
        
        errors = exc_info.value.errors()
        assert "max_capacity" in errors[0]["loc"]
        assert "int_from_float" in errors[0]["type"]


    def test_update_ls_max_capacity_str_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(max_capacity="quinze")
        
        errors = exc_info.value.errors()
        assert "max_capacity" in errors[0]["loc"]
        assert "int_parsing" in errors[0]["type"]


    # --- Tests sur course_id ---

    def test_update_course_id_updates_only_this_field(self):
        data = {"course_id": 1}

        update_schema = schema.LSUpdate(**data)
        dump = update_schema.model_dump(exclude_unset=True)

        assert dump == {"course_id": 1}
        assert "max_capacity" not in dump
        assert "start_date" not in dump
        assert "end_date" not in dump


    def test_update_ls_course_id_negative_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(course_id=-1)
        
        errors = exc_info.value.errors()
        assert "course_id" in errors[0]["loc"]
        assert "greater_than" in errors[0]["type"]


    def test_update_ls_course_id_float_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(course_id=10.5)
        
        errors = exc_info.value.errors()
        assert "course_id" in errors[0]["loc"]
        assert "int_from_float" in errors[0]["type"]


    def test_update_ls_course_id_str_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(course_id="deux")
        
        errors = exc_info.value.errors()
        assert "course_id" in errors[0]["loc"]
        assert "int_parsing" in errors[0]["type"]


    # --- Tests sur dates ---

    def test_update_dates_updates_only_these_fields(self):
        data = {"start_date": date.today(), "end_date": date(2027, 9, 30)}

        update_schema = schema.LSUpdate(**data)
        dump = update_schema.model_dump(exclude_unset=True)

        assert dump == {"start_date": date.today(), "end_date": date(2027, 9, 30)}
        assert "max_capacity" not in dump
        assert "course_id" not in dump


    def test_update_ls_dates_str_is_valid(self):
        update_data = schema.LSUpdate(start_date="2026-03-03", end_date="2027-09-30")

        assert isinstance(update_data.start_date, date)
        assert update_data.start_date == date(2026, 3, 3)
        assert isinstance(update_data.end_date, date)
        assert update_data.end_date == date(2027, 9, 30)


    def test_update_ls_same_day_dates_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(start_date="2026-03-03", end_date="2026-03-03")

        assert "La date de fin doit être supérieure à la date de début." in str(exc_info.value)


    def test_update_ls_incoherent_dates_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            schema.LSUpdate(start_date="2026-03-03", end_date="2025-09-30")

        assert "La date de fin doit être supérieure à la date de début." in str(exc_info.value)


class TestCrudLS:

    # --- Tests get_all_ls (+ including_deleted) ---

    def test_get_all_ls_returns_query(self, db_session, sample_session_1):
        query = crud.get_all_ls(db=db_session)
        
        assert isinstance(query, Query)
        assert query.count() == 1
        assert query.first().id == sample_session_1.id


    def test_get_all_ls_returns_empty_query_when_empty_database(self, db_session):
        query = crud.get_all_ls(db=db_session)
        
        assert isinstance(query, Query)
        assert query.count() == 0


    def test_get_all_ls_including_deleted_returns_query(self, db_session, sample_session_1):
        sample_session_1.deleted_at = datetime.now()
        db_session.commit()

        query = crud.get_all_ls_including_deleted(db=db_session)
        
        assert isinstance(query, Query)
        assert query.count() == 1

        results = query.all()
        assert any(s.deleted_at is not None for s in results)


    def test_get_all_ls_including_deleted_returns_none_when_empty_database(self, db_session):
        query = crud.get_all_ls_including_deleted(db=db_session)
        
        assert isinstance(query, Query)
        assert query.count() == 0


    # --- Tests get_one_ls (+ by course_dates) ---

    def test_get_one_ls_returns_valid_ls(self, db_session, sample_session_1):
        learning_session = crud.get_one_ls(db=db_session, ls_id=sample_session_1.id)
        assert learning_session.id == sample_session_1.id


    def test_get_one_ls_not_found_returns_none(self, db_session):
        learning_session = crud.get_one_ls(db=db_session, ls_id=999)
        assert learning_session is None


    def test_get_one_ls_by_course_dates_returns_valid_ls(self, db_session, sample_session_1):
        learning_session = crud.get_one_ls_by_course_dates(
            db = db_session, 
            course_id = sample_session_1.course_id,
            start_date = sample_session_1.start_date,
            end_date = sample_session_1.end_date
        )

        assert learning_session.id == sample_session_1.id


    def test_get_one_ls_by_course_dates_not_found_returns_none(self, db_session):
        learning_session = crud.get_one_ls_by_course_dates(
            db = db_session, 
            course_id = 0,
            start_date = date(2025, 2, 3),
            end_date = date(2026, 2, 3)
        )
        
        assert learning_session is None


    # --- Tests get_ls_users ---

    def test_get_ls_users_returns_users_registered(self, db_session, sample_session_1, sample_inscription):
        ls_users = crud.get_ls_users(db=db_session, ls_id=sample_session_1.id)

        assert isinstance(ls_users, list)
        assert len(ls_users) == 1
        assert ls_users[0].id == sample_inscription.user_id


    def test_get_ls_users_returns_none_if_ls_not_found(self, db_session):
        ls_users = crud.get_ls_users(db=db_session, ls_id=9999)

        assert ls_users is None


    def test_get_ls_users_returns_empty_list_if_no_users_registered(self, db_session, sample_session_1):
        ls_users = crud.get_ls_users(db=db_session, ls_id=sample_session_1.id)

        assert ls_users == []


    # --- Tests create_ls ---

    def test_create_ls_returns_valid_data(self, db_session, sample_course):
        schema_ls = schema.LSCreate(
            course_id = sample_course.id,
            start_date = date.today(),
            end_date = date(2027, 9, 30),
            max_capacity = 15
        )

        new_ls = crud.create_ls(db=db_session, schema=schema_ls)

        assert isinstance(new_ls.id, int)
        assert new_ls.course_id == sample_course.id
        assert new_ls.start_date == date.today()
        assert new_ls.end_date == date(2027, 9, 30)
        assert new_ls.max_capacity == 15


    def test_create_ls_returns_none_if_invalid_course_id(self, db_session):
        schema_ls = schema.LSCreate(
            course_id = 299,
            start_date = date.today(),
            end_date = date(2027, 9, 30),
            max_capacity = 15
        )

        new_ls = crud.create_ls(db=db_session, schema=schema_ls)
        assert new_ls is None


    # --- Tests update_ls ---


    def test_update_ls_basic_fields_returns_valid_data(self, db_session, sample_session_1, sample_course):
        updated_data = schema.LSUpdate(
            max_capacity = 45,
            course_id = sample_course.id
        )
        updated_ls = crud.update_ls(db=db_session, ls_id=sample_session_1.id, schema=updated_data)

        assert updated_ls.max_capacity == 45
        assert updated_ls.course_id == sample_course.id
        assert updated_ls.start_date == sample_session_1.start_date


    def test_update_ls_dates_returns_valid_data(self, db_session, sample_session_1):
        updated_data = schema.LSUpdate(
            start_date = date(2026, 4, 1),
            end_date = date(2027, 11, 1)
        )

        updated_ls = crud.update_ls(db=db_session, ls_id=sample_session_1.id, schema=updated_data)

        assert updated_ls.start_date == date(2026, 4, 1)
        assert updated_ls.end_date == date(2027, 11, 1)
        assert updated_ls.max_capacity == sample_session_1.max_capacity
        assert updated_ls.course_id == sample_session_1.course_id


    def test_update_ls_incoherent_start_date_returns_none(self, db_session, sample_session_1):
        updated_data = schema.LSUpdate(
            start_date = date(2028, 3, 3)
        )

        updated_ls = crud.update_ls(db=db_session, ls_id=sample_session_1.id, schema=updated_data)

        assert updated_data.start_date >= sample_session_1.end_date
        assert updated_ls is None


    def test_update_ls_incoherent_end_date_returns_none(self, db_session, sample_session_1):
        updated_data = schema.LSUpdate(
            end_date = date(2020, 3, 3)
        )

        updated_ls = crud.update_ls(db=db_session, ls_id=sample_session_1.id, schema=updated_data)

        assert sample_session_1.start_date >= updated_data.end_date
        assert updated_ls is None


    # --- Tests delete_ls + soft_delete_ls ---

    def test_delete_ls_returns_true(self, db_session, sample_session_1):
        result = crud.delete_ls(db=db_session, ls_id=sample_session_1.id)

        assert result is True
        assert db_session.get(LearningSession, sample_session_1.id) is None


    def test_delete_ls_not_found_returns_false(self, db_session):
        result = crud.delete_ls(db=db_session, ls_id=999)
        assert result is False
    

    def test_soft_delete_ls_not_found_returns_false(self, db_session):
        result = crud.soft_delete_ls(db=db_session, ls_id=999)
        assert result is False


    def test_soft_delete_ls_without_users_actually_deletes(self, db_session, sample_session_1):
        result = crud.soft_delete_ls(db=db_session, ls_id=sample_session_1.id)

        assert result is True
        assert db_session.get(LearningSession, sample_session_1.id) is None


    def test_soft_delete_ls_with_users_updates_timestamp(self, db_session, sample_session_1, sample_inscription):
        ls_id = sample_session_1.id
        ls_users = crud.get_ls_users(db=db_session, ls_id=ls_id)
        assert ls_users[0].id == sample_inscription.user_id

        result = crud.soft_delete_ls(db=db_session, ls_id=ls_id)
        assert result is True

        assert db_session.get(LearningSession, ls_id) is None
        
        all_ls = crud.get_all_ls_including_deleted(db=db_session)
        updated_ls = all_ls.filter(LearningSession.id == ls_id).first()
        
        assert updated_ls is not None
        assert updated_ls.deleted_at is not None
        assert isinstance(updated_ls.deleted_at, datetime)


class TestRouterLS:

    # --- Tests GET ---

    def test_router_get_all_ls_returns_list_ls(self, client, sample_session_1):

        response = client.get("/learning-sessions/")
        data = response.json()

        assert response.status_code == 200
        assert "items" in data
        assert len(data["items"]) == 1
        assert "id" in data["items"][0]
        assert "course_id" in data["items"][0]


    def test_router_get_all_returns_404_if_no_ls(self, client):
        response = client.get("/learning-sessions/")

        assert response.status_code == 404
        assert response.json()["detail"] == "Aucune session de formation trouvée."


    def test_router_get_all_ls_pagination_is_valid(self, client, sample_session_1):
        response = client.get("/learning-sessions/?page=1&size=1")
        data = response.json()

        assert response.status_code == 200
        assert data["size"] == 1
        assert len(data["items"]) == 1


    def test_router_get_one_ls_returns_valid_ls(self, client, sample_session_1):
        response = client.get(f"/learning-sessions/{sample_session_1.id}")
        data = response.json()

        if response.status_code == 422:
            print(response.json())

        assert response.status_code == 200
        assert data["id"] == sample_session_1.id
        assert data["course_id"] == sample_session_1.course_id


    def test_router_get_one_ls_returns_404_if_ls_not_found(self, client):
        response = client.get("/learning-sessions/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Cette session de formation est introuvable."


    def test_router_get_ls_users_returns_valid_users_list(self, client, sample_session_1, sample_inscription):
        response = client.get(f"/learning-sessions/{sample_session_1.id}/users")
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 1
        assert "last_name" in data[0]
        assert "email" in data[0]


    def test_router_get_ls_users_returns_404_if_ls_not_found(self, client):
        response = client.get("/learning-sessions/9999/users")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Cette session de formation est introuvable."


    def test_router_get_ls_users_returns_empty_list_if_no_registered_users(self, client, sample_session_1):
        response = client.get(f"/learning-sessions/{sample_session_1.id}/users")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Aucun utilisateur inscrit à cette session de formation."


    # --- Tests PATCH ---

    def test_router_patch_ls_returns_valid_ls(self, client, sample_session_1):
        update_data = {"max_capacity": 20}
        response = client.patch(f"/learning-sessions/{sample_session_1.id}", json=update_data)
        
        assert response.status_code == 201
        assert response.json()["max_capacity"] == 20


    def test_router_patch_ls_returns_404_if_ls_not_found(self, client):
        response = client.patch("/learning-sessions/9999", json={"max_capacity": 20})
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Cette session de formation est introuvable."


    def test_router_patch_ls_returns_404_if_course_not_found(self, client, sample_session_1):
        response = client.patch(f"/learning-sessions/{sample_session_1.id}", json={"course_id": 999})
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Cette formation est introuvable."


    def test_router_patch_ls_returns_422_if_invalid_dates(self, client, sample_session_1):
        invalid_start_date = {"start_date": "2027-08-25"}
        response = client.patch(f"/learning-sessions/{sample_session_1.id}", json=invalid_start_date)
        
        assert response.status_code == 422
        assert response.json()["detail"] == "La date de fin doit être supérieure à la date de début."


    # --- TESTS POST (Create) ---

    def test_router_post_ls_returns_valid_ls(self, client, sample_course):
        """Vérifie la création d'une session (201)"""
        new_ls = {
            "course_id": sample_course.id,
            "start_date": "2026-03-04",
            "end_date": "2028-02-02",
            "max_capacity": 25
        }
        response = client.post("/learning-sessions/", json=new_ls)
        
        assert response.status_code == 201
        assert response.json()["max_capacity"] == 25


    def test_router_post_ls_returns_400_if_ls_already_exists(self, client, sample_session_1):
        duplicate_data = {
            "course_id": sample_session_1.course_id,
            "start_date": sample_session_1.start_date.isoformat(),
            "end_date": sample_session_1.end_date.isoformat(),
            "max_capacity": sample_session_1.max_capacity
        }
        response = client.post("/learning-sessions/", json=duplicate_data)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Cette session de formation existe déjà."


    def test_router_post_ls_returns_404_if_course_not_found(self, client):
        new_ls = {
            "course_id": 9999,
            "start_date": "2026-03-04",
            "end_date": "2028-02-02",
            "max_capacity": 25
        }
        response = client.post("/learning-sessions/", json=new_ls)
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Cette formation n'existe pas."


    # --- Tests DELETE ---

    def test_router_delete_ls_returns_204_if_success(self, client, sample_session_1):
        response = client.delete(f"/learning-sessions/{sample_session_1.id}")
        
        assert response.status_code == 204
        if response.content:
            assert response.json()["message"] == "Session de formation supprimée."


    def test_router_delete_ls_returns_404_if_ls_not_found(self, client):
        response = client.delete("/learning-sessions/9999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Cette session de formation est introuvable."

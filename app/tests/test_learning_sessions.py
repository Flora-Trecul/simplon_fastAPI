import pytest
from pydantic import ValidationError
from app.schemas import learning_sessions as schema
from datetime import date
from app.models.models import Course, LearningSession, User, Inscription


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
        user_id = sample_session_1.id,
        session_id = sample_user.id
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


"""


"""

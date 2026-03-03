import pytest
from pydantic import ValidationError
from app.schemas import learning_sessions as schema
from datetime import date

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



"""
- LSUpdate valide complet
- LSUpdate avec max_capacity valide
- LSUpdate avec max_capacity < 1
- LSUpdate avec max_capacity > 50
- LSUpdate avec max_capacity float
- LSUpdate avec max_capacity str
- LSUpdate avec course_id négatif
- LSUpdate avec course_id float
- LSUpdate avec course_id str
- LSUpdate avec dates str
- LSUpdate avec deux dates incohérentes
- LSUpdate avec une seule date valide
- LSUpdate avec une seule date incohérente (à voir car cette validation se fait ailleurs)

- Faut-il tester LSResponse ?
"""

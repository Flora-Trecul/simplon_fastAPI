import pytest

# POST /users/

def test_create_apprenant_success(client, apprenant_data):
    response = client.post("/users/", json=apprenant_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == apprenant_data["email"]
    assert data["first_name"] == apprenant_data["first_name"]
    assert data["role"] == "apprenant"
    assert "id" in data

def test_create_user_duplicate_email(client, apprenant_data):
    client.post("/users/", json=apprenant_data)
    response = client.post("/users/", json=apprenant_data)
    assert response.status_code == 400
    assert "Email" in response.json()["detail"]

def test_create_user_invalid_role(client, apprenant_data):
    apprenant_data["role"] = "inconnu"
    response = client.post("/users/", json=apprenant_data)
    assert response.status_code == 422

def test_create_user_missing_field(client):
    response = client.post("/users/", json={"first_name": "Alice"})
    assert response.status_code == 422


# GET /users/
def test_get_all_users(client, created_apprenant):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    assert data["total"] >= 1

def test_get_users_filter_by_name(client, created_apprenant):
    response = client.get("/users/?name=Alice")
    assert response.status_code == 200
    data = response.json()
    assert any(u["first_name"] == "Alice" for u in data["items"])

def test_get_users_filter_by_name_partial(client, created_apprenant):
    response = client.get("/users/?name=ali")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1

def test_get_users_filter_by_role(client, created_apprenant, created_formateur):
    response = client.get("/users/?role=apprenant")
    assert response.status_code == 200
    data = response.json()
    assert all(u["role"] == "apprenant" for u in data["items"])

# GET /users/{user_id}

def test_get_user_by_id_success(client, created_apprenant):
    response = client.get(f"/users/{created_apprenant['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_apprenant["id"]

def test_get_user_by_id_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404

# PATCH /users/{user_id}

def test_update_user_success(client, created_apprenant):
    response = client.patch(f"/users/{created_apprenant['id']}", json={"first_name": "Alicia"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Alicia"

def test_update_user_role(client, created_apprenant):
    response = client.patch(f"/users/{created_apprenant['id']}", json={"role": "formateur"})
    assert response.status_code == 200
    assert response.json()["role"] == "formateur"

def test_update_user_not_found(client):
    response = client.patch("/users/9999", json={"first_name": "Bob"})
    assert response.status_code == 404

def test_update_user_invalid_role(client, created_apprenant):
    response = client.patch(f"/users/{created_apprenant['id']}", json={"role": "inconnu"})
    assert response.status_code == 422


# DELETE /users/{user_id}

def test_delete_user_success(client, created_apprenant):
    response = client.delete(f"/users/{created_apprenant['id']}")
    assert response.status_code == 200

def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404

def test_delete_user_soft_deleted_hidden(client, created_apprenant):
    client.delete(f"/users/{created_apprenant['id']}")
    response = client.get(f"/users/{created_apprenant['id']}")
    assert response.status_code == 404

def test_delete_user_with_session_is_soft_deleted(client, created_apprenant, created_session):
    user_id = created_apprenant["id"]
    session_id = created_session.id
    client.post(f"/users/{user_id}/session/{session_id}")
    client.delete(f"/users/{user_id}")
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


# POST /users/{user_id}/session/{session_id}

def test_inscription_apprenant_success(client, created_apprenant, created_session):
    response = client.post(f"/users/{created_apprenant['id']}/session/{created_session.id}")
    assert response.status_code == 201
    assert response.json()["message"] == "Utilisateur inscrit avec succès"

def test_inscription_formateur_success(client, created_formateur, created_session):
    response = client.post(f"/users/{created_formateur['id']}/session/{created_session.id}")
    assert response.status_code == 201

def test_inscription_administrateur_forbidden(client, created_administrateur, created_session):
    response = client.post(f"/users/{created_administrateur['id']}/session/{created_session.id}")
    assert response.status_code == 403

def test_inscription_already_registered(client, created_apprenant, created_session):
    user_id = created_apprenant["id"]
    session_id = created_session.id
    client.post(f"/users/{user_id}/session/{session_id}")
    response = client.post(f"/users/{user_id}/session/{session_id}")
    assert response.status_code == 400
    assert "déjà inscrit" in response.json()["detail"]

def test_inscription_max_capacity_reached(client, created_session):
    """max_capacity = 2, le 3ème apprenant est refusé."""
    apprenants = [
        {"first_name": f"User{i}", "last_name": "Test", "email": f"user{i}@test.com", "role": "apprenant"}
        for i in range(3)
    ]
    ids = [client.post("/users/", json=a).json()["id"] for a in apprenants]

    client.post(f"/users/{ids[0]}/session/{created_session.id}")
    client.post(f"/users/{ids[1]}/session/{created_session.id}")
    response = client.post(f"/users/{ids[2]}/session/{created_session.id}")
    assert response.status_code == 400
    assert "Capacité" in response.json()["detail"]

def test_inscription_user_not_found(client, created_session):
    response = client.post(f"/users/9999/session/{created_session.id}")
    assert response.status_code == 404

def test_inscription_session_not_found(client, created_apprenant):
    response = client.post(f"/users/{created_apprenant['id']}/session/9999")
    assert response.status_code == 404


# DELETE /users/{user_id}/session/{session_id}

def test_delete_inscription_success(client, created_apprenant, created_session):
    user_id = created_apprenant["id"]
    session_id = created_session.id
    client.post(f"/users/{user_id}/session/{session_id}")
    response = client.delete(f"/users/{user_id}/session/{session_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Inscription supprimée avec succès"

def test_delete_inscription_not_found(client, created_apprenant, created_session):
    response = client.delete(f"/users/{created_apprenant['id']}/session/{created_session.id}")
    assert response.status_code == 404

def test_delete_inscription_user_not_found(client, created_session):
    response = client.delete(f"/users/9999/session/{created_session.id}")
    assert response.status_code == 404

# GET /users/{user_id}/sessions

def test_get_user_sessions_success(client, created_apprenant, created_session):
    user_id = created_apprenant["id"]
    client.post(f"/users/{user_id}/session/{created_session.id}")
    response = client.get(f"/users/{user_id}/sessions")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_user_sessions_empty(client, created_apprenant):
    response = client.get(f"/users/{created_apprenant['id']}/sessions")
    assert response.status_code == 200
    assert response.json() == []

def test_get_user_sessions_not_found(client):
    response = client.get("/users/9999/sessions")
    assert response.status_code == 404
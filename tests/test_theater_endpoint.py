from django.contrib.auth.models import User


def test_get_all_movie_theaters(api_client):
    response = api_client.get("/api/movie-theaters/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert len(response.json()) == 1


def test_get_one_movie_theater(api_client):
    response = api_client.get("/api/movie-theaters/1/")
    assert response.status_code == 200
    assert response.data["name"] == "Cine 1"
    assert response.json()["name"] == "Cine 1"


def test_unauthorized_post(api_client):
    response = api_client.post("/api/movie-theaters/", {"name": "Cine 2"})
    assert response.status_code == 401


def test_authorized_post(api_client):
    user = User.objects.get(id=1)
    api_client.force_authenticate(user)
    response = api_client.post("/api/movie-theaters/", {"name": "Cine 2"})
    assert response.status_code == 201
    assert response.data["name"] == "Cine 2"
    assert response.json()["name"] == "Cine 2"

    response = api_client.get("/api/movie-theaters/")
    assert response.status_code == 200
    assert len(response.data) == 2
    assert len(response.json()) == 2


def test_unauthorized_put(api_client):
    response = api_client.put("/api/movie-theaters/1/", {"name": "Cine 3"})
    assert response.status_code == 401


def test_authorized_put(api_client):
    user = User.objects.get(id=1)
    api_client.force_authenticate(user)
    response = api_client.put("/api/movie-theaters/1/", {"name": "Cine 3"})
    assert response.status_code == 200
    assert response.data["name"] == "Cine 3"
    assert response.json()["name"] == "Cine 3"

    response = api_client.get("/api/movie-theaters/1/")
    assert response.status_code == 200
    assert response.data["name"] == "Cine 3"
    assert response.json()["name"] == "Cine 3"


def test_unauthorized_delete(api_client):
    response = api_client.delete("/api/movie-theaters/1/")
    assert response.status_code == 401


def test_authorized_delete(api_client):
    user = User.objects.get(id=1)
    api_client.force_authenticate(user)
    response = api_client.delete("/api/movie-theaters/1/")
    assert response.status_code == 204

    response = api_client.get("/api/movie-theaters/")
    assert response.status_code == 200
    assert len(response.data) == 0
    assert len(response.json()) == 0

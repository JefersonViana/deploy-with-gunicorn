def test_get_authentication_token_using_wrong_credentials(client):
    response = client.post("/api/generate-token",
                           {"username": "admin", "password": "wrong"})
    assert response.status_code == 400
    assert "non_field_errors" in response.json()

    # FORMA 1 DE FAZER
    # assert str(response.data['non_field_errors'][0]) == (
    #     "Impossível fazer login com as credenciais fornecidas."
    # )

    # FORMA 2 DE FAZER
    # assert (
    # "Impossível fazer login com as credenciais fornecidas."
    # ) in response.json()["non_field_errors"]

    # FORMA 3 DE FAZER
    assert (
        "Impossível fazer login com as credenciais fornecidas."
    ) == response.json()["non_field_errors"][0]


def test_get_authentication_token_using_correct_credentials(client):
    response = client.post("/api/generate-token",
                           {"username": "testuser", "password": "12345"})
    assert response.status_code == 200
    assert "token" in response.json()


def test_post_new_theater_without_token(client):
    response = client.post("/api/movie-theaters/", {"name": "Cine 2"})
    assert response.status_code == 401


def test_post_new_theater_using_generated_token(api_client):
    user = {"username": "testuser", "password": "12345"}
    response = api_client.post("/api/generate-token", user)
    assert response.status_code == 200

    # OUTRA FORMA DE FAZER
    # token = response.json()["token"]
    # response = api_client.post(
    #     "/api/movie-theaters/",
    #     {"name": "Cine 2"},
    #     headers={"Authorization": f"Token {token}"}
    #   )
    # assert response.status_code == 201
    # assert response.json()["name"] == "Cine 2"

    token = response.json()["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = api_client.post("/api/movie-theaters/", {"name": "Cine 2"})
    assert response.status_code == 201
    assert response.json()["name"] == "Cine 2"

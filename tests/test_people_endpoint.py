from django.contrib.auth.models import User


def test_get_all_peoplies(api_client):
    response = api_client.get('/api/people/')
    assert response.status_code == 200
    assert len(response.data) == 3
    assert len(response.json()) == 3


def test_get_one_people(api_client):
    response = api_client.get('/api/people/1/')
    assert response.status_code == 200
    assert response.data['name'] == 'Antoine Fuqua'
    assert response.json()['name'] == 'Antoine Fuqua'


def test_unauthorized_post(api_client):
    response = api_client.post('/api/people/', {'name': 'Nome Fake_1'})
    assert response.status_code == 401


def test_authorized_post(api_client):
    user = User.objects.get(id=1)
    api_client.force_authenticate(user)
    response = api_client.post('/api/people/', {'name': 'Nome Fake_1'})
    assert response.status_code == 201
    assert response.data['name'] == 'Nome Fake_1'
    assert response.json()['name'] == 'Nome Fake_1'

    response = api_client.get('/api/people/')
    assert response.status_code == 200
    assert len(response.data) == 4
    assert len(response.json()) == 4


def test_unauthorized_put(api_client):
    response = api_client.put('/api/people/1/', {'name': 'Nome Fake_2'})
    assert response.status_code == 401


def test_authorized_put(api_client):
    user = User.objects.get(id=1)
    api_client.force_authenticate(user)
    response = api_client.put('/api/people/1/', {'name': 'Nome Fake_2'})
    assert response.status_code == 200
    assert response.data['name'] == 'Nome Fake_2'
    assert response.json()['name'] == 'Nome Fake_2'

    response = api_client.get('/api/people/1/')
    assert response.status_code == 200
    assert response.data['name'] == 'Nome Fake_2'
    assert response.json()['name'] == 'Nome Fake_2'


def test_unauthorized_delete(api_client):
    response = api_client.delete('/api/people/1/')
    assert response.status_code == 401


def test_authorized_delete(api_client):
    user = User.objects.get(id=1)
    api_client.force_authenticate(user)
    response = api_client.delete('/api/people/1/')
    assert response.status_code == 204

    response = api_client.get('/api/people/')
    assert response.status_code == 200
    assert len(response.data) == 2
    assert len(response.json()) == 2

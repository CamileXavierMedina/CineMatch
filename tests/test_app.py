import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_tmdb_api_success(client, requests_mock):
    tmdb_url = "https://api.themoviedb.org/3/search/movie?query=Matrix"
    mock_response = {"results": [{"id": 603, "title": "The Matrix"}]}
    requests_mock.get(tmdb_url, json=mock_response, status_code=200)

    response = client.get('/api/buscar?query=Matrix')
    assert response.status_code == 200
    assert b"The Matrix" in response.data
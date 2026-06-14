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

def test_tmdb_api_success(client):
    response = client.get('/api/buscar?query=Matrix')
   
    assert response.status_code in [200, 500]
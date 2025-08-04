import pytest
from app.main import app
from app.models import url_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

def test_shorten_url(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

def test_redirect(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = response.get_json()['short_code']

    redirect_response = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_response.status_code == 302

def test_stats(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = response.get_json()['short_code']

    client.get(f'/{short_code}')  # simulate a click
    stats = client.get(f'/api/stats/{short_code}')
    data = stats.get_json()

    assert data['clicks'] == 1
    assert data['url'] == 'https://example.com'
    assert 'created_at' in data

def test_invalid_url(client):
    response = client.post('/api/shorten', json={'url': 'invalid'})
    assert response.status_code == 400

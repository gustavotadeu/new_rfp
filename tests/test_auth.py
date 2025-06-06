import os
import sys

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from backend.app import main, database, models

# reinitialize database
models.Base.metadata.create_all(bind=database.engine)
client = TestClient(main.app)

def test_register_and_login():
    response = client.post('/register', json={
        'username': 'tester',
        'email': 'tester@example.com',
        'password': 'secret'
    })
    assert response.status_code == 200, response.text

    response = client.post('/login', json={
        'email': 'tester@example.com',
        'password': 'secret'
    })
    assert response.status_code == 200
    token = response.json()['access_token']

    response = client.get('/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

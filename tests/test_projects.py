import os
import sys
temp_dir = os.path.abspath(os.path.dirname(__file__))

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["CELERY_TASK_ALWAYS_EAGER"] = "true"
os.environ["CELERY_BROKER_URL"] = "memory://"
os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.app import main, database, models

models.Base.metadata.create_all(bind=database.engine)
client = TestClient(main.app)


def create_user_and_token():
    client.post(
        "/register",
        json={"username": "projuser", "email": "proj@example.com", "password": "pw"},
    )
    resp = client.post("/login", json={"email": "proj@example.com", "password": "pw"})
    return resp.json()["access_token"]


def test_project_and_rfp_upload(tmp_path):
    token = create_user_and_token()
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/projects", json={"name": "My Project"}, headers=headers)
    assert resp.status_code == 200
    project_id = resp.json()["id"]

    file_path = tmp_path / "rfp.txt"
    file_path.write_text("hello rfp")
    with open(file_path, "rb") as f:
        resp = client.post(
            f"/projects/{project_id}/rfps", files={"file": ("rfp.txt", f, "text/plain")}, headers=headers
        )
    assert resp.status_code == 200
    rfp_id = resp.json()["id"]

    resp = client.post(f"/projects/{project_id}/rfps/{rfp_id}/analyze", headers=headers)
    assert resp.status_code == 200
    assert "task_id" in resp.json()

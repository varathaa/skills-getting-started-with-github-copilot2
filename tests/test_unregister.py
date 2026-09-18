import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app


def test_signup_adds_participant_and_rejects_duplicates():
    client = TestClient(app)
    activity_name = "Science Club"
    email = f"signup-{uuid4().hex[:8]}@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

    duplicate_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = f"delete-{uuid4().hex[:8]}@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]

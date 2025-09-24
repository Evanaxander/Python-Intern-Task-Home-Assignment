from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_student():
    resp = client.post("/students/", json={"name": "Charlie"})
    assert resp.status_code == 200
    data = resp.json()
    sid = data["id"]

    get_resp = client.get(f"/students/{sid}")
    assert get_resp.status_code == 200


def test_course_capacity_and_enrollment():
    # Create course with capacity 1
    course = client.post("/courses/", json={"title": "Physics", "capacity": 1}).json()
    # Create two students
    s1 = client.post("/students/", json={"name": "S1"}).json()
    s2 = client.post("/students/", json={"name": "S2"}).json()

    ok = client.post(f"/students/{s1['id']}/enroll", json={"course_id": course['id']})
    assert ok.status_code == 200

    full = client.post(f"/students/{s2['id']}/enroll", json={"course_id": course['id']})
    assert full.status_code == 400
    assert "capacity" in full.json()["detail"].lower()

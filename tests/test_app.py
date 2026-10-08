import pytest
from app import app, init_db

@pytest.fixture
def client(tmp_path, monkeypatch):
    db = tmp_path / "test.db"
    monkeypatch.setattr("app.DB_PATH", db)
    init_db()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_dashboard(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CareTrack" in response.data
    assert b"Today's appointments" in response.data

def test_appointments(client):
    response = client.get("/appointments")
    assert response.status_code == 200
    assert b"Appointments" in response.data

def test_add_appointment(client):
    response = client.post("/appointments/add", data={
        "patient": "Test Patient",
        "doctor": "Dr. Meera Shah",
        "department": "Cardiology",
        "time": "14:00"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Patient" in response.data

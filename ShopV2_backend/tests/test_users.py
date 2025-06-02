from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", data={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code in [303, 409]  # 303 – успішно, 409 – користувач вже існує

def test_list_users_requires_admin():
    response = client.get("/users")
    assert response.status_code == 401 or response.status_code == 403  # Неавторизований або неадмін

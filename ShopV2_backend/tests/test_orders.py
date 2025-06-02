from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order_unauthenticated():
    response = client.post("/orders/create", data={
        "product_id": "1",
        "quantity": "2"
    })
    assert response.status_code == 401  # Без токена доступ заборонено

def test_list_orders_requires_auth():
    response = client.get("/orders")
    assert response.status_code == 401  # Очікується авторизація

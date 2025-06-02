from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_products_empty():
    response = client.get("/products")
    assert response.status_code == 200
    assert "products" in response.text or response.json()

def test_create_product_as_admin():
    token = "Bearer your_valid_jwt_token_here"
    response = client.post(
        "/products/create",
        data={"name": "Test", "description": "Test product", "price": 99.99},
        headers={"Authorization": token}
    )
    assert response.status_code in [200, 303]

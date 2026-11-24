import mongomock
import pytest
from app import create_app
@pytest.fixture()
def client():
    mongo = mongomock.MongoClient()
    app = create_app({"TESTING": True, "MONGO_CLIENT": mongo, "MONGO_DB": mongo.shopsphere_test, "JWT_SECRET_KEY": "test"})
    return app.test_client()
@pytest.fixture()
def auth(client):
    response = client.post("/api/auth/register", json={"name":"Ada", "email":"ada@example.com", "password":"password123"})
    return {"Authorization": f"Bearer {response.json['token']}"}

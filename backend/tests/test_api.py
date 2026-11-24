def test_registration_and_product_cart_flow(client, auth):
    assert client.get("/api/health").status_code == 200
    client.application.db.users.update_one({"email":"ada@example.com"}, {"$set":{"role":"admin"}})
    login = client.post("/api/auth/login", json={"email":"ada@example.com", "password":"password123"})
    admin_headers = {"Authorization": f"Bearer {login.json['token']}"}
    created = client.post("/api/products", json={"name":"Headphones","description":"x","price":99,"category":"Audio","stock":3}, headers=admin_headers)
    assert created.status_code == 201
    product_id = created.json["product"]["_id"]
    assert client.post("/api/cart/items", json={"productId":product_id,"quantity":2}, headers=admin_headers).status_code == 201
